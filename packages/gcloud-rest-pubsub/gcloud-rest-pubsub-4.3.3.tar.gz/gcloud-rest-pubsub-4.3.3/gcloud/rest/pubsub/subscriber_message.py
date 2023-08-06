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
import base64
import datetime
from typing import Any
from typing import Dict
from typing import Optional


def parse_publish_time(publish_time     )                     :
    try:
        return datetime.datetime.strptime(
            publish_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return datetime.datetime.strptime(
            publish_time, '%Y-%m-%dT%H:%M:%SZ')


class SubscriberMessage(object):
    def __init__(self, ack_id     , message_id     ,
                 publish_time                     ,
                 data                 ,
                 attributes                          ,
                 delivery_attempt                = None):
        self.ack_id = ack_id
        self.message_id = message_id
        self.publish_time = publish_time
        self.data = data
        self.attributes = attributes
        self.delivery_attempt = delivery_attempt

    @staticmethod
    def from_repr(received_message                
                  )                       :
        ack_id = received_message['ackId']
        message_id = received_message['message']['messageId']
        raw_data = received_message['message'].get('data')
        data = base64.b64decode(raw_data) if raw_data is not None else None
        attributes = received_message['message'].get('attributes')
        publish_time                    = parse_publish_time(
            received_message['message']['publishTime'])
        delivery_attempt = received_message.get('deliveryAttempt')
        return SubscriberMessage(ack_id=ack_id, message_id=message_id,
                                 publish_time=publish_time, data=data,
                                 attributes=attributes,
                                 delivery_attempt=delivery_attempt)

    def to_repr(self)                  :
        r                 = {
            'ackId': self.ack_id,
            'message': {
                'messageId': self.message_id,
                'publishTime': self.publish_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        }
        if self.attributes is not None:
            r['message']['attributes'] = self.attributes
        if self.data is not None:
            r['message']['data'] = base64.b64encode(self.data)
        if self.delivery_attempt is not None:
            r['deliveryAttempt'] = self.delivery_attempt
        return r
