from typing import Optional, Tuple

from redis import Redis

import rfq.redis


def info(topic: str, redis: Optional[Redis] = None) -> Tuple[int, int]:
    r = rfq.redis.default() if redis is None else redis

    p = r.pipeline()

    p.llen("rfq:{topic}:backlog".format(topic=topic))
    p.llen("rfq:{topic}:nextlog".format(topic=topic))

    n, m = p.execute()

    return n, m
