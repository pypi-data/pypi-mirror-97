import os

import redis


def default() -> redis.Redis:
    host = os.getenv("RFQ_REDIS_HOST", "localhost")
    port = os.getenv("RFQ_REDIS_PORT", 6379)

    return redis.Redis(host=host, port=int(port), decode_responses=True)
