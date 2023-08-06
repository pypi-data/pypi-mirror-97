from .adapters.producer_amqp import ProducerAMQP
from .adapters.producer_rocketmq import ProducerRocketMQ
from .mq_type import *


class Producer(object):
    def __init__(self, mq_type='AMQO', **mq_options):
        if mq_type == MQ_TYPE_AMQP:
            self.__agent = ProducerAMQP(**mq_options)
        elif mq_type == MQ_TYPE_ROCKETMQ:
            self.__agent = ProducerRocketMQ(**mq_options)
        else:
            self.__agent = ProducerAMQP(**mq_options)

    def Start(self):
        self.__agent.Start()

    def Stop(self):
        self.__agent.Stop()

    def Publish(self, topic_group: str, topic: str, message, **route):
        return self.__agent.Publish(topic_group, topic, message, **route)

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        return self.__agent.DelayPublish(topic_group, topic, delay, message, **route)
