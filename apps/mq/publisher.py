from contextlib import contextmanager

from kombu import Connection
from kombu.pools import connections, producers
from kombu.exceptions import ChannelError 

from .mqtt_queues import iot_upload_data_exchange
from .constants import (PERSISTENT,
                        DEFAULT_RETRY_POLICY,DEFAULT_TRANSPORT_OPTIONS)

class UndeliverableMessage(Exception):
    """ Raised when publisher confirms are enabled and a message could not
    be routed or persisted """
    pass



@contextmanager
def get_producer(amqp_uri, confirms=True, ssl=None, transport_options=None):
    if transport_options is None:
        transport_options = DEFAULT_TRANSPORT_OPTIONS.copy()
    transport_options['confirm_publish'] = confirms
    conn = Connection(amqp_uri, transport_options=transport_options, ssl=ssl)

    with producers[conn].acquire(block=True) as producer:
        yield producer

def publish(payload, exchange, routing_key, amqp_uri, serializer="json",retry=True, retry_policy=None):
    if retry_policy is None:
        retry_policy = DEFAULT_RETRY_POLICY
    #TODO: 
    with get_producer(amqp_uri) as publisher:
        publisher.publish(payload,
                        exchange=exchange,
                        routing_key=routing_key,
                        serializer=serializer,
                        retry=retry,
                        retry_policy=retry_policy
                        )

