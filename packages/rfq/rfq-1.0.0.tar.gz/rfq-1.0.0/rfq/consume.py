from redis import WatchError

import rfq.redis


def consume(topic, redis=None):
    r = rfq.redis.default() if redis is None else redis

    with r.pipeline() as p:
        while True:
            try:
                p.watch("rfq::{topic}:backlog".format(topic=topic),
                        "rfq::{topic}:nextlog".format(topic=topic))

                msgid = p.brpoplpush("rfq:{topic}:backlog".format(topic=topic),
                                     "rfq:{topic}:nextlog".format(topic=topic))

                p.multi()

                p.hgetall("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

                msg = p.execute()[0]

                break

            except WatchError:
                continue

    return msgid, msg


def commit(topic, msgid, redis=None):
    r = rfq.redis.default() if redis is None else redis

    with r.pipeline() as tx:
        tx.lrem("rfq:{topic}:nextlog".format(topic=topic), 1, msgid)
        tx.lrem("rfq:{topic}:backlog".format(topic=topic), 1, msgid)
        tx.delete("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid))

        tx.execute()

    return msgid
