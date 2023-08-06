import importlib.metadata

import rfq.redis


def version(redis=None):
    r = rfq.redis.default() if redis is None else redis

    n = importlib.metadata.version("rfq")
    m = r.info("server").get("redis_version", "unknown")

    return n, m
