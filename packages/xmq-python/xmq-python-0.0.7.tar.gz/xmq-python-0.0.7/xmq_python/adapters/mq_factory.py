class ProducerFactory(object):
    def __init__(self, mq_type: str, **mq_options):
        pass

    def Publish(self, topic_group: str, topic: str, message, **route):
        raise NotImplementedError

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        raise NotImplementedError

    def Start(self):
        raise NotImplementedError

    def Stop(self):
        raise NotImplementedError


class ComsumerFactory(object):
    def __init__(self, mq_type: str, **mq_options):
        pass

    def Register(self, topic_group: str, topic: str, callback, **route):
        raise NotImplementedError

    def Start(self):
        raise NotImplementedError

    def Stop(self):
        raise NotImplementedError
