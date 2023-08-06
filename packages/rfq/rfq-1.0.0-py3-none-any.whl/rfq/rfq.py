import rfq.redis

import rfq.version
import rfq.publish
import rfq.info
import rfq.listq
import rfq.purge
import rfq.topics
import rfq.harvest
import rfq.consume


class Queue:
    def __init__(self, redis=None):
        self.r = rfq.redis.default() if redis is None else redis

    def version(self):
        return rfq.version.version(redis=self.r)

    def publish(self, topic, message, front=False):
        return rfq.publish.publish(topic=topic, message=message, front=front, redis=self.r)

    def info(self, topic):
        return rfq.info.info(topic=topic, redis=self.r)

    def listq(self, topic, queue):
        return rfq.listq.listq(topic=topic, queue=queue, redis=self.r)

    def purge(self, topic, queue):
        return rfq.purge.purge(topic=topic, queue=queue, redis=self.r)

    def topics(self):
        return rfq.topics.topics(redis=self.r)

    def harvest(self, topic):
        return rfq.harvest.harvest(topic=topic, redis=self.r)

    def consume(self, topic):
        msgid, msg = rfq.consume.consume(topic=topic, redis=self.r)
        return Task(topic=topic, msgid=msgid, msg=msg, redis=self.r)


class Task:
    def __init__(self, topic, msgid, msg, redis=None):
        self.r = rfq.redis.default() if redis is None else redis

        self.topic = topic
        self.msgid = msgid
        self.msg = msg

    def result(self):
        return self.msg

    def cancel(self):
        return self.msgid

    def done(self):
        return rfq.consume.commit(topic=self.topic, msgid=self.msgid, redis=self.r)
