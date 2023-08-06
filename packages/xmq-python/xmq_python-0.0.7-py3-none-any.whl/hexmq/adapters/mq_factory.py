class ProducerFactory(object):
    def __init__(self):
        pass

    def Publish(self, topic_group: str, topic: str, message, **route):
        raise NotImplementedError

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class ComsumerFactory(object):
    def __init__(self):
        pass

    def Register(self, topic_group: str, topic: str, callback, **route):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
