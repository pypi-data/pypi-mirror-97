from typing import Optional, Dict
import uuid

from redis import Redis

import rfq.redis


def publish(topic: str, message: Dict[str, str], front: bool, redis: Optional[Redis] = None) -> str:
    r = rfq.redis.default() if redis is None else redis

    msgid = uuid.uuid1().hex

    with r.pipeline() as tx:
        tx.hset("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid), mapping=message)

        if front:
            tx.rpush("rfq:{topic}:backlog".format(topic=topic), msgid)
        else:
            tx.lpush("rfq:{topic}:backlog".format(topic=topic), msgid)

        tx.execute()

    return msgid
