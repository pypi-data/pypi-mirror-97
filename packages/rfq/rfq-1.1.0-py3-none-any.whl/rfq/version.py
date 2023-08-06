from typing import Optional, Tuple
import importlib.metadata

from redis import Redis

import rfq.redis


def version(redis: Optional[Redis] = None) -> Tuple[str, str]:
    r = rfq.redis.default() if redis is None else redis

    n = importlib.metadata.version("rfq")
    m = r.info("server").get("redis_version", "unknown")

    return n, m
