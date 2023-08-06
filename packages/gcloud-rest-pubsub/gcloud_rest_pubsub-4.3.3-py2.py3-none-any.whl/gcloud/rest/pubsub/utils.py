from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
from typing import Any
from typing import Dict
from typing import Union

from gcloud.rest.auth import encode  # pylint: disable=no-name-in-module


# https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
class PubsubMessage(object):
    def __init__(self, data                   , ordering_key      = '',
                 **kwargs                )        :
        self.data = data
        self.attributes = kwargs
        self.ordering_key = ordering_key

    def __repr__(self)       :
        return str(self.to_repr())

    def to_repr(self)                  :
        msg = {
            'data': encode(self.data).decode('utf-8'),
            'attributes': self.attributes,
        }
        if self.ordering_key:
            msg['orderingKey'] = self.ordering_key
        return msg
