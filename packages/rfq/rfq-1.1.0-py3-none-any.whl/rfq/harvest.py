from typing import Optional, List

from redis import Redis

import rfq.redis


def harvest(topic: str, redis: Optional[Redis] = None) -> List[str]:
    r = rfq.redis.default() if redis is None else redis

    msgids = set()

    while True:
        msgid = r.rpoplpush("rfq:{topic}:nextlog".format(topic=topic),
                            "rfq:{topic}:backlog".format(topic=topic))

        if msgid is None or msgid in msgids:
            break

        msgids.add(msgid)

    return list(msgids)
