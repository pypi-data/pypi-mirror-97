from typing import Optional, Tuple, List, Dict, Union, Literal

from redis import Redis

import rfq.redis

import rfq.version
import rfq.publish
import rfq.info
import rfq.listq
import rfq.purge
import rfq.topics
import rfq.harvest
import rfq.consume


class Task:
    r: Optional[Redis]
    topic: str
    msgid: str
    msg: Dict[str, str]

    def __init__(self, topic: str, msgid: str, msg: Dict[str, str], redis: Optional[Redis] = None) -> None:
        self.r = rfq.redis.default() if redis is None else redis

        self.topic = topic
        self.msgid = msgid
        self.msg = msg

    def result(self) -> Dict[str, str]:
        return self.msg

    def cancel(self) -> str:
        return self.msgid

    def done(self) -> str:
        return rfq.consume.commit(topic=self.topic, msgid=self.msgid, redis=self.r)


class Queue:
    r: Redis

    def __init__(self, redis: Optional[Redis] = None) -> None:
        self.r = rfq.redis.default() if redis is None else redis

    def version(self) -> Tuple[str, str]:
        return rfq.version.version(redis=self.r)

    def publish(self, topic: str, message: Dict[str, str], front: bool = False) -> str:
        return rfq.publish.publish(topic=topic, message=message, front=front, redis=self.r)

    def info(self, topic: str) -> Tuple[int, int]:
        return rfq.info.info(topic=topic, redis=self.r)

    def listq(self, topic: str, queue: Union[Literal["backlog"], Literal["nextlog"]]) -> List[str]:
        return rfq.listq.listq(topic=topic, queue=queue, redis=self.r)

    def purge(self, topic: str, queue: Union[Literal["backlog"], Literal["nextlog"]]) -> List[str]:
        return rfq.purge.purge(topic=topic, queue=queue, redis=self.r)

    def topics(self) -> List[str]:
        return rfq.topics.topics(redis=self.r)

    def harvest(self, topic: str) -> List[str]:
        return rfq.harvest.harvest(topic=topic, redis=self.r)

    def consume(self, topic: str) -> Task:
        msgid, msg = rfq.consume.consume(topic=topic, redis=self.r)
        return Task(topic=topic, msgid=msgid, msg=msg, redis=self.r)
