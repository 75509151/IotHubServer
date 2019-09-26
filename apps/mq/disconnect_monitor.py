import bson

from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu.utils.functional import reprcall

from .mqtt_queues import disconnect_queue
from .tasks import app

logger = get_logger(__name__)



class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=disconnect_queue,
                         on_message = self.handle_message)]

    def handle_message(self, msg):
        app.do(msg, "disconnect")
        msg.ack()

def monitor():
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])

    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')

if __name__ == '__main__':
    monitor()

