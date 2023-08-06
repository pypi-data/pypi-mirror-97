import rfq.redis


def listq(topic, queue, redis=None):
    r = rfq.redis.default() if redis is None else redis

    msgids = r.lrange("rfq:{topic}:{queue}".format(topic=topic, queue=queue), 0, -1)

    return msgids
