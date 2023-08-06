from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from pkg_resources import get_distribution
__version__ = get_distribution('gcloud-rest-pubsub').version

from gcloud.rest.auth import BUILD_GCLOUD_REST
from gcloud.rest.pubsub.publisher_client import PublisherClient
from gcloud.rest.pubsub.subscriber_client import SubscriberClient
from gcloud.rest.pubsub.utils import PubsubMessage
from gcloud.rest.pubsub.subscriber_message import SubscriberMessage

__all__ = ['__version__', 'PublisherClient', 'PubsubMessage',
           'SubscriberClient', 'SubscriberMessage']

if not BUILD_GCLOUD_REST:
    from gcloud.rest.pubsub.subscriber import subscribe
    __all__.append('subscribe')
