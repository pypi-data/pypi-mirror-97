from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
class MetricsAgent(object):
    """
    Any metric client should implement this interface
    to be compatible with subscriber.subscribe
    """
    def histogram(self,
                  metric     ,
                  value       )        :
        pass

    def increment(self,
                  metric     ,
                  value        = 1)        :
        pass
