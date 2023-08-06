from .mq_factory import ConsumerFactory
from ..encode import CJsonEncoder
from rocketmq.client import PushConsumer, ConsumeStatus

import json


def rocketmq_handler_wrapper(handlers):
    def message_handler(message):
        f = handlers.get(message.tags.decode('utf-8'))
        ret = False
        data = message
        if f !=None:
            try:
                data = json.loads(message.body.decode('utf-8'))
            except Exception as ex:
                print("Error to load message to json: ", ex)
            ret = f(data)
        if ret:
            return ConsumeStatus.CONSUME_SUCCESS
        else:
            return ConsumeStatus.RECONSUME_LATER
    return message_handler


class ConsumerRocketMQ(ConsumerFactory):
    def __init__(self, consumer_group_name='', channel='', lookup_address='', node_address='', access_key='', access_secret='', thread_num=None, batch_size=None, **mq_options):
        self.consumer = PushConsumer(consumer_group_name)
        self.consumer.set_name_server_address(lookup_address)
        if thread_num and thread_num > 0:
            self.consumer.set_thread_count(thread_num)
        if batch_size and batch_size > 0:
            self.consumer.set_message_batch_max_size(batch_size)
        if access_key:
            self.consumer.set_session_credentials(
                access_key=access_key, access_secret=access_secret, channel=channel)
        self.__handlers=dict()
        self.__topic_group=dict()

    def Register(self, topic_group: str, topic: str, callback, **route):
        self.__handlers[topic]=callback
        if topic_group not in self.__topic_group:
            self.__topic_group[topic_group]=[]
        self.__topic_group[topic_group].append(topic)
        

    def Start(self):
        for topic_group, topics in self.__topic_group.items():
            self.consumer.subscribe(
            topic_group, rocketmq_handler_wrapper(self.__handlers), expression="||".join(topics))
        self.consumer.start()

    def Stop(self):
        self.consumer.shutdown()
