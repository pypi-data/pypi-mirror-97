"""REST client for the Waylay Storage Service."""

from waylay.service import WaylayService

from .bucket import BucketResource
from .object import ObjectResource, FolderResource
from .content import ContentTool
from .about import AboutResource
from .subscription import SubscriptionResource


class StorageService(WaylayService):
    """REST client for the Waylay Storage Service."""

    config_key = 'storage'
    service_key = 'storage'
    default_root_url = 'https://storage.waylay.io'
    resource_definitions = {
        'bucket': BucketResource,
        'object': ObjectResource,
        'folder': FolderResource,
        'subscription': SubscriptionResource,
        'about': AboutResource
    }

    bucket: BucketResource
    object: ObjectResource
    folder: FolderResource
    subscription: SubscriptionResource
    about: AboutResource

    @property
    def content(self) -> ContentTool:
        """Get the tool to access the content of storage objects."""
        return ContentTool(self.object)
