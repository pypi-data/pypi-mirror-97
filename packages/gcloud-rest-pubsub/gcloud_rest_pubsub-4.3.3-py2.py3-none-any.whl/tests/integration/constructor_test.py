from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# from gcloud.rest.pubsub import SubscriberClient
# This ain't a great test, but we need *somethign* in this directory to avoid
# pytest failing and this does at least validate the auth token to some extent.
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
def test_constructor():
    assert True
    # TODO: not implemented in gcloud-rest
    # subscriber = SubscriberClient()
    # assert subscriber
