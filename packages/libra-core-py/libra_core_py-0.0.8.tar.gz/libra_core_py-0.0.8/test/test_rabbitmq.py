import sys
sys.path.append('')
from libra_core.config import *
from libra_core.log import *
from libra_core.rabbitmq import RabbitmqClient

def test_config():
    init_config()
    print(config("log_path"))
    print(config("log", "logging.level.com.apus"))
    print(config("channel_country_config"))

def test_rabbitmq():
    init_config()
    rabbitmq_client = RabbitmqClient(exchange_name = config("rabbitmq.spider.exchange"),
                                     exchange_type = config("rabbitmq.spider.exchange_type"),
                                     routing_key = config("rabbitmq.routing_key"),
                                     queue = config("rabbitmq.queue"),
                                     durable = config("rabbitmq.durable"),
                                     host=config("rabbitmq.host"),
                                     port=config("rabbitmq.port"),
                                     user=config("rabbitmq.user"),
                                     passwd=config("rabbitmq.password"),
                                     vhost=config("rabbitmq.vhost"))
    print(config("rabbitmq.spider.exchange"),
          config("rabbitmq.spider.exchange_type"),
          config("rabbitmq.routing_key"),
          config("rabbitmq.queue"),
          config("rabbitmq.durable"),
          config("rabbitmq.host"),
          config("rabbitmq.port"),
          config("rabbitmq.user"),
          config("rabbitmq.password"),
          config("rabbitmq.vhost"))
    resp = rabbitmq_client.publish_msg("hello")
    def callback(ch, method, properties, body):
        print(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    rabbitmq_client.consume_one(callback)

def test_queue_count():
    init_local_config()
    rabbitmq = RabbitmqClient(exchange_name=config('rabbitmq.spider.exchange'),
                              exchange_type = config("rabbitmq.spider.exchange_type"),
                              routing_key = config("rabbitmq.routing_key"),
                              host=config("rabbitmq.host"),
                              port=config("rabbitmq.port"),
                              user=config("rabbitmq.user"),
                              passwd=config("rabbitmq.password"),
                              vhost=config("rabbitmq.vhost"))
    queue_list = [
        config('rabbitmq.spider.list_task.queue'),
        config('rabbitmq.spider.detail_task.queue'),
        config('rabbitmq.spider.image_task.queue')
    ]

    for queue in queue_list:
        print(queue)
        print(type(rabbitmq._exchange_type))
        print(rabbitmq.queue_message_count(queue))
        print(rabbitmq.queue_bind_consumer_count(queue))
