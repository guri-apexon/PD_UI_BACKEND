import json
import getpass
import socket
import logging
from kombu import Exchange, Queue
from kombu.mixins import ConsumerMixin
from etmfa_finalization.messaging.models.finalization_request import Document_Processing_Error
from etmfa_finalization import Constants
from iqv_finalization_error import FinalizationException
from iqv_finalization_error import ErrorCodes
from etmfa_finalization import Globals
from etmfa_finalization.messaging.messagepublisher import MessagePublisher

logger = logging.getLogger(Constants.MICROSERVICE_NAME)


class MessageListener(ConsumerMixin):
    def __init__(self, connection, connection_str, exchange_name=None, queue_callback_dict={}, logger=None):
        self.connection = connection
        self.connection_str = connection_str
        self.exchange_name = exchange_name
        self.queue_callback_dict = queue_callback_dict
        self.logger = logger

        if logger == None:
            print("WARNING: No logger used in message listener.")

        self.exchange = Exchange(exchange_name, type='direct', durable=True)

    def get_queues(self):
        return [Queue(q, exchange=self.exchange, routing_key=q, durable=True) for q in self.queue_callback_dict.keys()]

    def _create_consumer(self, Consumer, queues):
        consumer = Consumer(queues=[queues], callbacks=[self._on_message], prefetch_count=5)
        consumer.tag_prefix = f'{socket.gethostname()} - {getpass.getuser()} | Finalizer-{Globals.VERSION} etmfa-core-{Globals.CORE_VERSION} | '

        return consumer

    def get_consumers(self, Consumer, channel):
        return [self._create_consumer(Consumer, q) for q in self.get_queues()]

    def add_listener(self, queue_name, callback):
        """
        Add a queue listener with the mapped callback to be invoked whenever a message is received. Listeners cannot be added after calling 'run()'

        queue_name: string
        callback: Function with the signature (dictionary_object, message publisher), where the dictionary_object corresponds to the received message.

        Note: Only one top-level callback can be registered per queue.
        """
        if not queue_name:
            raise ValueError("Queue name parameter must be non-empty or whitespace: {}".format(queue_name))

        if queue_name in self.queue_callback_dict:
            raise ValueError("Only one callback can be registered for a single queue. If multiple callbacks are required, compose functions.")

        self.queue_callback_dict[queue_name] = callback


    def _on_message(self, body, message):
        """Callback function executed when a message is consumed from the queue."""
        queue_name = message.delivery_info['routing_key']
        try:
            message_body = json.loads(body)
            Globals.THREAD_LOCAL.aidocid = message_body.get('id')
            logger.debug("Received message on queue: {},\
                         body: {}".format(queue_name, message_body))
        except Exception as ex:
            logger.error("could not parse message on queue: {}\
                         body: {}, exception: {} ".format(queue_name, body, str(ex)))

        try:
            self.queue_callback_dict[queue_name](
                json.loads(body),
                MessagePublisher(self.connection_str, self.exchange_name)
            )
        except FinalizationException as ex:
            logger.error("{}".format(str(ex)))
            id = "" # message_body.get('id')
            message_publisher = MessagePublisher(self.connection_str, self.exchange_name)
            msg = Document_Processing_Error(id, ex.error_code, ex.error_message, ex.error_message_details)
            message_publisher.send_obj(msg)

        except Exception as ex:
            id = "" # message_body.get('id')
            logger.error("Fatal error while processing queue: {} {} {}".format(queue_name, id, str(ex)))
            message_publisher = MessagePublisher(self.connection_str, self.exchange_name)
            msg = Document_Processing_Error(id, ErrorCodes.UNKNOWN_ERROR, str(ex))
            message_publisher.send_obj(msg)

        finally:
            message.ack()
