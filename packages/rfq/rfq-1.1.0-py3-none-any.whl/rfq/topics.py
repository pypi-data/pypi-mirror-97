from typing import Optional, List

from redis import Redis

import rfq.redis


def topics(redis: Optional[Redis] = None) -> List[str]:
    r = rfq.redis.default() if redis is None else redis

    p = r.pipeline()

    p.keys("rfq:*:backlog")
    p.keys("rfq:*:nextlog")

    bkeys, nkeys = p.execute()

    keys = []

    keys += [k[len("rfq:"): - len(":backlog")] for k in bkeys]
    keys += [k[len("rfq:"): - len(":nextlog")] for k in nkeys]

    keys = list(set(keys))

    return keys
