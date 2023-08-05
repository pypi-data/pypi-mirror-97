import datetime
import json
import six

from girder import logger
from girder.constants import AccessType
from girder.exceptions import RestException
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.setting import Setting
from girder.models.user import User
from girder_large_image_annotation.models.annotation import Annotation

from .constants import PluginSettings


def _itemFromEvent(event, identifierEnding, itemAccessLevel=AccessType.READ):
    """
    If an event has a reference and an associated identifier that ends with a
    specific string, return the associated item, user, and image file.

    :param event: the data.process event.
    :param identifierEnding: the required end of the identifier.
    :returns: a dictionary with item, user, and file if there was a match.
    """
    info = event.info
    identifier = None
    reference = info.get('reference', None)
    if reference is not None:
        try:
            reference = json.loads(reference)
            if (isinstance(reference, dict) and
                    isinstance(reference.get('identifier'), six.string_types)):
                identifier = reference['identifier']
        except (ValueError, TypeError):
            logger.debug('Failed to parse data.process reference: %r', reference)
    if identifier is not None and identifier.endswith(identifierEnding):
        if 'userId' not in reference or 'itemId' not in reference or 'fileId' not in reference:
            logger.error('Reference does not contain required information.')
            return

        userId = reference['userId']
        imageId = reference['fileId']

        # load models from the database
        user = User().load(userId, force=True)
        image = File().load(imageId, level=AccessType.READ, user=user)
        item = Item().load(image['itemId'], level=itemAccessLevel, user=user)
        return {'item': item, 'user': user, 'file': image}


def process_annotations(event):
    """Add annotations to an image on a ``data.process`` event"""
    results = _itemFromEvent(event, 'AnnotationFile')
    if not results:
        return
    item = results['item']
    user = results['user']

    file = File().load(
        event.info.get('file', {}).get('_id'),
        level=AccessType.READ, user=user
    )

    if not file:
        logger.error('Could not load models from the database')
        return
    try:
        data = json.loads(b''.join(File().download(file)()).decode('utf8'))
    except Exception:
        logger.error('Could not parse annotation file')
        raise

    if not isinstance(data, list):
        data = [data]
    for annotation in data:
        try:
            Annotation().createAnnotation(item, user, annotation)
        except Exception:
            logger.error('Could not create annotation object from data')
            raise


def quarantine_item(item, user, makePlaceholder=True):
    """
    Quarantine an item, marking which user did it.  Note that this raises
    RestExceptions for failures.

    :param user: the user doing the quarantining.
    :param item: an item to quarantine.
    :returns: the modified item.
    """
    folder = Setting().get(PluginSettings.HUI_QUARANTINE_FOLDER)
    if not folder:
        raise RestException('The quarantine folder is not configured.')
    folder = Folder().load(folder, force=True, exc=True)
    if not folder:
        raise RestException('The quarantine folder does not exist.')
    if str(folder['_id']) == str(item['folderId']):
        raise RestException('The item is already in the quarantine folder.')
    originalFolder = Folder().load(item['folderId'], force=True)
    quarantineInfo = {
        'originalFolderId': item['folderId'],
        'originalBaseParentType': item['baseParentType'],
        'originalBaseParentId': item['baseParentId'],
        'originalUpdated': item['updated'],
        'quarantineUserId': user['_id'],
        'quarantineTime': datetime.datetime.utcnow()
    }
    item = Item().move(item, folder)
    if makePlaceholder:
        placeholder = Item().createItem(
            item['name'] + ' [Removed - Quarantined]',
            {'_id': item['creatorId']}, originalFolder,
            description=item['description'])
        quarantineInfo['placeholderItemId'] = placeholder['_id']
    item.setdefault('meta', {})['quarantine'] = quarantineInfo
    item = Item().updateItem(item)
    if makePlaceholder:
        placeholderInfo = {
            'quarantined': True,
            'quarantineTime': quarantineInfo['quarantineTime']
        }
        placeholder.setdefault('meta', {})['quarantine'] = placeholderInfo
        placeholder = Item().updateItem(placeholder)
    return item


def restore_quarantine_item(item, user):
    """
    Unquarantine an item, returning it to its original location.  Note that
    this raises RestExceptions for failures.

    :param item: an item to unquarantine.
    :returns: the modified item.
    """
    if not item.get('meta', {}).get('quarantine'):
        raise RestException('The item has no quarantine record.')
    folder = Folder().load(item['meta']['quarantine']['originalFolderId'], force=True)
    if not folder:
        raise RestException('The original folder is not accessible.')
    if 'placeholderItemId' in item['meta']['quarantine']:
        placeholder = Item().load(item['meta']['quarantine']['placeholderItemId'], force=True)
    else:
        placeholder = None
    item = Item().move(item, folder)
    item['updated'] = item['meta']['quarantine']['originalUpdated']
    del item['meta']['quarantine']
    item = Item().updateItem(item)
    if placeholder is not None:
        Item().remove(placeholder)
    return item


def process_metadata(event):
    """Add metadata to an item on a ``data.process`` event"""
    results = _itemFromEvent(event, 'ItemMetadata', AccessType.WRITE)
    if not results:
        return
    file = File().load(
        event.info.get('file', {}).get('_id'),
        level=AccessType.READ, user=results['user']
    )

    if not file:
        logger.error('Could not load models from the database')
        return
    try:
        data = json.loads(b''.join(File().download(file)()).decode('utf8'))
    except Exception:
        logger.error('Could not parse metadata file')
        raise

    item = results['item']
    Item().setMetadata(item, data, allowNull=False)
