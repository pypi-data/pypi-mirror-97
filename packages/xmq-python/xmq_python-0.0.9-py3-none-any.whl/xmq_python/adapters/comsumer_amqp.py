from .mq_factory import ComsumerFactory
from ..encode import CJsonEncoder
from multiprocessing import Process
from pika.exchange_type import ExchangeType
from ..utils import AliyunCredentialsProvider3 as credentials
import pika
import json
import logging

# def callback(channel, method, properties, body):
#     print(body)
#     channel.basic_ack(delivery_tag=method.delivery_tag)


# def on_open(connection):
#     connection.channel(on_open_callback = on_channel_open)


# def on_channel_open(channel):
#     channel.basic_consume('boh.doc.plan.update.doc.status', callback)

def amqp_handler_wrapper(f):
    def message_handler(chan, method_frame, header_frame, body, userdata=None):
        data = body
        try:
            data = json.loads(body)
        except:
            pass
        res = f(data)
        if res == True:
            chan.basic_ack(delivery_tag=method_frame.delivery_tag)
    return message_handler


def on_channel_open_wrapper(callbacks, topic_group, comsumer_group_name):
    def on_channel_open(channel):
        channel.exchange_declare(
            exchange=topic_group,
            exchange_type=ExchangeType.direct,
            passive=False,
            durable=True,
            auto_delete=False)
        
        channel.basic_qos(prefetch_count=2)
        for topic, cb in callbacks.items():
            queue_name = "{}_{}".format(topic,comsumer_group_name)
            channel.queue_declare(
                        queue_name,
                        passive=False,
                        durable=True,
                        exclusive=False,
                        auto_delete=False,
                        arguments=None
                    )
            channel.queue_bind(
                    queue_name,
                    topic_group,
                    routing_key=topic,
                    arguments=None
                )
            channel.basic_consume(queue_name, amqp_handler_wrapper(cb))
    return on_channel_open


def on_open_wrapper(callbacks, topic_group, comsumer_group_name):
    def on_open(connection):
        connection.channel(
            on_open_callback=on_channel_open_wrapper(callbacks, topic_group, comsumer_group_name))
    return on_open


class ComsumerAMQP(ComsumerFactory):
    def __init__(self, comsumer_group_name='', host='', port=0, access_key='', access_secret='', thread_num=None, batch_size=None, username=None, password=None, virtual_host=None, instance_id=None, **mq_options):
        # self.__parameters = []
        self.__credentials = None
        self.__callbacks = dict()
        self.__topic_group = None
        if (not access_key or not access_secret) and (not username or not password):
            raise Exception("access_key/access_secret or username/password should be provided for acccessing amqp")
        if not host or not port:
            raise Exception("host/port should be provided for acccessing amqp")
        if not virtual_host:
            raise Exception("virtual_host should be provided for acccessing amqp")
        if not instance_id:
            raise Exception("instance_id should be provided for acccessing amqp")
        if not comsumer_group_name:
            raise Exception("comsumer_group_name should be provided for acccessing amqp")
        self.__comsumer_group_name = comsumer_group_name
        if access_key and access_secret:
            cred = credentials.AliyunCredentialsProvider(
                access_key=access_key, access_secret=access_secret, instanceId=instance_id)
            username = cred.get_username()
            password = cred.get_password()
        self.__url_parameters = pika.URLParameters(
            'amqp://{}:{}@{}:{}/{}'.format(username, password, host, port, virtual_host))


    def Register(self, topic_group: str, topic: str, callback, **route):
        if not self.__topic_group:
            self.__topic_group = topic_group
        elif self.__topic_group != topic_group:
            raise Exception("only on topic group allowed in one comsumer")
        self.__callbacks[topic] = callback

    def Start(self):
        self.__connection = pika.SelectConnection(
            self.__url_parameters, on_open_callback=on_open_wrapper(self.__callbacks, self.__topic_group, self.__comsumer_group_name))
        print("build Comsumer SelectConnection was built!")
        try:
            self.__connection.ioloop.start()
            print("Comsumer worker started!")
        except KeyboardInterrupt:
            self.__connection.close()
        except Exception as e:
            if self.__connection.is_open:
                self.__connection.close()
            print('Fail to start AMQP Comsumer!')
            raise e

    def Stop(self):
        self.__connection.close()
