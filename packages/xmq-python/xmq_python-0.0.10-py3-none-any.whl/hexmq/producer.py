from .adapters.producer_rocketmq import ProducerRocketMQ
from .mq_type import *


class Producer(object):
    def __init__(self, mq_type='ROCKETMQ', producer_group_id='', lookup_address='', node_address='', access_key='', access_secret=''):
        if mq_type == MQ_TYPE_ROCKETMQ:
            self.__agent = ProducerRocketMQ(producer_group_id=producer_group_id, lookup_address=lookup_address,
                                            node_address=node_address, access_key=access_key, access_secret=access_secret)
        else:
            self.__agent = ProducerRocketMQ(producer_group_id=producer_group_id, lookup_address=lookup_address,
                                            node_address=node_address, access_key=access_key, access_secret=access_secret)

    def start(self):
        self.__agent.start()

    def stop(self):
        self.__agent.stop()

    def Publish(self, topic_group: str, topic: str, message, **route):
        return self.__agent.Publish(topic_group, topic, message, **route)

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        return self.__agent.DelayPublish(topic_group, topic, delay, message, **route)
