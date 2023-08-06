import rfq.redis


def info(topic, redis=None):
    r = rfq.redis.default() if redis is None else redis

    p = r.pipeline()

    p.llen("rfq:{topic}:backlog".format(topic=topic))
    p.llen("rfq:{topic}:nextlog".format(topic=topic))

    n, m = p.execute()

    return n, m
