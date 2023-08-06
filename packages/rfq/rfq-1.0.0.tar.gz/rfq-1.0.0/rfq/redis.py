import os

import redis


def default():
    host = os.getenv("RFQ_REDIS_HOST", "localhost")
    port = os.getenv("RFQ_REDIS_PORT", 6379)

    return redis.Redis(host=host, port=port, decode_responses=True)
