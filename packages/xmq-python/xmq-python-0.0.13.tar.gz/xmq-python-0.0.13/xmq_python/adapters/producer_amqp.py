from .mq_factory import ProducerFactory
from ..encode import CJsonEncoder
from ..utils import AliyunCredentialsProvider3 as credentials
import pika
import json


class ProducerAMQP(ProducerFactory):
    def __init__(self, host='', port=0, access_key='', access_secret='', timeout=None, max_message_size=None, username=None, password=None, virtual_host=None, instance_id=None, **mq_options):
        self.__parameters = []
        self.__credentials = None
        if (not access_key or not access_secret) and (not username or not password):
            raise Exception("access_key/access_secret or username/password should be provided for acccessing amqp")
        if not host or not port:
            raise Exception("host/port should be provided for acccessing amqp")
        if not virtual_host:
            raise Exception("virtual_host should be provided for acccessing amqp")
        if not instance_id:
            raise Exception("instance_id should be provided for acccessing amqp")
        if access_key and access_secret:
            cred = credentials.AliyunCredentialsProvider(
                access_key=access_key, access_secret=access_secret, instanceId=instance_id)
            username = cred.get_username()
            password = cred.get_password()
        if username and password:
            self.__credentials = pika.PlainCredentials(username, password)
        self.__parameters.append(pika.ConnectionParameters(
            host=host, port=port, virtual_host=virtual_host, credentials=self.__credentials))

    def Start(self):
        self.__connection = pika.BlockingConnection(self.__parameters)
        self.__producer = self.__connection.channel()

    def Stop(self):
        self.__connection.close()

    # topic_group: amqp的exchange
    # topic: 对应amqp的routing_key
    def Publish(self, topic_group: str, topic: str, message, **route):
        try:
            msg_body = json.dumps(message, cls=CJsonEncoder) if isinstance(
                message, dict) else message
            ret = self.__producer.basic_publish(
                exchange=topic_group, routing_key=topic, body=msg_body,
                properties=pika.BasicProperties(content_type='text/plain', delivery_mode=1))
            return True, None
        except Exception as ex:
            return False, ex

    # topic_group: amqp的exchange
    # topic: 对应amqp的routing_key
    # delay: 秒，TODO：此版本不支持延迟消息

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        try:
            msg_body = json.dumps(message, cls=CJsonEncoder) if isinstance(
                message, dict) else message
            self.__producer.basic_publish(
                exchange=topic_group, routing_key=topic, body=msg_body,
                properties=pika.BasicProperties(content_type='text/plain', delivery_mode=1))
            return True, None
        except Exception as ex:
            return False, ex
