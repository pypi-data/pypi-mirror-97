from .mq_factory import ProducerFactory
from ..encode import CJsonEncoder
from rocketmq.client import Producer, Message
import json


class ProducerRocketMQ(ProducerFactory):
    def __init__(self, producer_group_id='', lookup_address='', node_address='', access_key='', access_secret='',timeout=None, max_message_size=None):
        self.producer = Producer(producer_group_id)
        self.producer.set_name_server_address(lookup_address)
        if access_key:
            self.producer.set_session_credentials(
                access_key=access_key, access_secret=access_secret)
        # 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 分别对应下面的延迟时间
        # messageDelayLevel=1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h
        self.__message_delay_levels = [0, 1, 5, 10, 30, 1*60, 2*60, 3*60, 4*60,
                                       5*60, 6*60, 7*60, 8*60, 9*60, 10*60, 20*60, 30*60, 1*60*60, 2*60*60]

    def start(self):
        self.producer.start()

    def stop(self):
        self.producer.shutdown()

    # topic_group: 对应rocketmq的topic
    # topic: 对应rocketmq的message tag
    def Publish(self, topic_group: str, topic: str, message, **route):
        try:
            msg = Message(topic_group)
            msg.set_tags(topic)
            msg_body = json.dumps(message, cls=CJsonEncoder) if isinstance(
                message, dict) else message
            msg.set_body(msg_body)
            ret = self.producer.send_sync(msg)
            print(ret.status, ret.msg_id, ret.offset)
            return True, None
        except Exception as ex:
            return False, ex

    def __get_message_delay_level(self, delay):
        if not isinstance(delay, int):
            raise Exception("'delay must be int by seconds'")
        if delay <= 0:
            return 0
        last_level = 0
        last_level_time = 0
        for level_index, t in enumerate(self.__message_delay_levels):
            if delay <= t:
                if last_level == 0:
                    return level_index
                else:
                    return (level_index if abs(t-delay) < abs(last_level_time-delay)else last_level)
            else:
                if level_index >= (len(self.__message_delay_levels) - 1):
                    return level_index
                else:
                    last_level = level_index
                    last_level_time = t
        return last_level

    # topic_group: 对应rocketmq的topic
    # topic: 对应rocketmq的message tag
    # delay: 秒，在方法内会转换为rocketmq的延迟等级，但不会和延迟等级的时间一一对应，找最接近的延迟时间

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        try:
            message_delay_level = 0
            msg = Message(topic_group)
            msg.set_tags(topic)
            msg.set_delay_time_level(self.__get_message_delay_level(delay))
            msg_body = json.dumps(message, cls=CJsonEncoder) if isinstance(
                message, dict) else message
            msg.set_body(msg_body)
            ret = self.producer.send_sync(msg)
            print(ret.status, ret.msg_id, ret.offset)
            return True, None
        except Exception as ex:
            return False, ex
