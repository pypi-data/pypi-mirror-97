from .adapters.comsumer_rocketmq import ComsumerRocketMQ
from .mq_type import *


class Comsumer(object):
    def __init__(self, mq_type='ROCKETMQ', comsumer_group_id='', lookup_address='', node_address='', access_key='', access_secret='', thread_num=None, batch_size=None):
        if mq_type == MQ_TYPE_ROCKETMQ:
            self.__agent = ComsumerRocketMQ(comsumer_group_id=comsumer_group_id, lookup_address=lookup_address,
                                            node_address=node_address, access_key=access_key, access_secret=access_secret, thread_num=thread_num, batch_size=batch_size)
        else:
            self.__agent = ComsumerRocketMQ(comsumer_group_id=comsumer_group_id, lookup_address=lookup_address,
                                            node_address=node_address, access_key=access_key, access_secret=access_secret, thread_num=thread_num, batch_size=batch_size)

    def Register(self, topic_group: str, topic: str, callback, **route):
        self.__agent.Register(topic_group, topic, callback, **route)

    def start(self):
        self.__agent.start()

    def stop(self):
        self.__agent.stop()
