import time
import pika

from libra_core.log import *
from libra_core.utils import sleep


class RabbitmqClient(object):

    def __init__(self,
                 exchange_name: str,
                 exchange_type: str,
                 routing_key: str = '',
                 queue: str = '',
                 durable: bool = True,
                 host=None,
                 port=None,
                 user=None,
                 passwd=None,
                 vhost=None):

        self._host = host
        self._port = port
        self._passwd = passwd
        self._user = user
        self._vhost = vhost
        self._queue = queue
        self._durable = durable
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._routing_key = routing_key
        self._connected = False

    def _connect(self):
        if not self._connected:
            try:
                credentials = pika.credentials.PlainCredentials(username=self._user, password=self._passwd)
                self._rabbit_conn = pika.BlockingConnection(pika.ConnectionParameters(host=self._host,
                                                                                      port=self._port,
                                                                                      credentials=credentials,
                                                                                      virtual_host=self._vhost))
                self._channel = self._rabbit_conn.channel()
                self._channel.exchange_declare(exchange=self._exchange_name,
                                               exchange_type=self._exchange_type,
                                               durable=self._durable)
                if self._queue:
                    q = self._channel.queue_declare(queue=self._queue,
                                                    durable=self._durable,
                                                    exclusive=False)
                    self._channel.queue_bind(queue=self._queue,
                                             exchange=self._exchange_name,
                                             routing_key=self._routing_key)
                    self._channel.basic_qos(prefetch_count=1)
                self._connected = True
                log_info('Succeed to connect {}:{} rabbit mq'.format(self._host, self._port))
            except Exception as e:
                log_error('Fail to connect {}:{} rabbit mq.error msg({})'.format(self._host,
                                                                                 self._port, str(e)))
        return self._connected

    def publish_msg(self, msg_str, retry=5, expiration=0):
        need_loop = False
        if retry <= 0:
            need_loop = True
        while retry > 0 or need_loop:
            while not self._connect():
                log_error('waiting to connect to rabbitmq: {}:{} {} ...'.format(self._host,
                                                                                self._port, self._user))
                time.sleep(0.5)
            try:
                if expiration > 0:
                    self._channel.basic_publish(exchange=self._exchange_name,
                                                routing_key=self._routing_key,
                                                properties=pika.BasicProperties(
                                                    expiration=str(expiration),
                                                ),
                                                body=msg_str)
                else:
                    self._channel.basic_publish(exchange=self._exchange_name,
                                                routing_key=self._routing_key,
                                                body=msg_str)
                return True
            except Exception as e:
                log_error('publish msg error({})'.format(e))
                self._connected = False
                time.sleep(0.5)
                retry -= 1
        return False

    def close_conn(self):
        self._rabbit_conn.close()

    def consume_msg(self, callback):
        while True:
            while not self._connect():
                sleep(0.1)
            if not self._queue:
                q = self._channel.queue_declare(exclusive=True)
                self._channel.queue_bind(queue=q.method.queue,
                                         exchange=self._exchange_name,
                                         routing_key=self._routing_key)
                self._queue = q.method.queue

            self._channel.basic_qos(prefetch_count=1)
            try:
                self._channel.basic_consume(callback, queue=self._queue)
                self._channel.start_consuming()
            except Exception as e:
                log_error('consume {} msg error({})'.format(self._queue, e))
                self._connected = False
                sleep(0.1)

    def consume_one(self, callback):
        while True:
            while not self._connect():
                sleep(0.1)
            if not self._queue:
                q = self._channel.queue_declare(exclusive=True)
                self._channel.queue_bind(queue=q.method.queue,
                                         exchange=self._exchange_name,
                                         routing_key=self._routing_key)
                self._queue = q.method.queue

            try:
                method, properties, body = self._channel.basic_get(queue=self._queue)
                callback(self._channel, method, properties, body)
                self._channel.start_consuming()
            except Exception as e:
                log_error('consume {} msg error({})'.format(self._queue, e))
                self._connected = False
                sleep(0.1)

    def queue_message_count(self, queue_name, retry=5):
        while retry > 0:
            while not self._connect():
                sleep(0.1)
            try:
                declear_queue_result = self._channel.queue_declare(queue=queue_name, durable=True)
                queue_message_count = declear_queue_result.method.message_count
                return queue_message_count
            except Exception as e:
                log_error('publish msg error({})'.format(e))
                self._connected = False
                time.sleep(0.5)
                retry -= 1
        return False

    def queue_bind_consumer_count(self, queue_name, retry=5):
        while retry > 0:
            while not self._connect():
                sleep(0.1)
            try:
                declear_queue_result = self._channel.queue_declare(queue=queue_name, passive=True, durable=True)
                queue_message_count = declear_queue_result.method.consumer_count
                return queue_message_count
            except Exception as e:
                log_error('publish msg error({})'.format(e))
                self._connected = False
                time.sleep(0.5)
                retry -= 1
        return False
