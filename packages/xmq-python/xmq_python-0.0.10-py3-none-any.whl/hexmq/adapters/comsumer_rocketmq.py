from .mq_factory import ComsumerFactory
from ..encode import CJsonEncoder
from rocketmq.client import PushConsumer, ConsumeStatus

import json


def rocketmq_handler_wrapper(f):
    def message_handler(message):
        ret = f(message)
        if ret:
            return ConsumeStatus.CONSUME_SUCCESS
        else:
            return ConsumeStatus.RECONSUME_LATER
    return message_handler


class ComsumerRocketMQ(ComsumerFactory):
    def __init__(self, comsumer_group_id='', lookup_address='', node_address='', access_key='', access_secret='', thread_num=None, batch_size=None):
        self.consumer = PushConsumer(comsumer_group_id)
        self.consumer.set_name_server_address(lookup_address)
        if thread_num and thread_num > 0:
            self.consumer.set_thread_count()
        if batch_size and batch_size > 0:
            self.consumer.set_message_batch_max_size(batch_size)
        if access_key:
            self.consumer.set_session_credentials(
                access_key=access_key, access_secret=access_secret)

    def Register(self, topic_group: str, topic: str, callback, **route):
        self.consumer.subscribe(
            topic_group, rocketmq_handler_wrapper(callback), expression=topic)

    def start(self):
        self.consumer.start()

    def stop(self):
        self.consumer.shutdown()
