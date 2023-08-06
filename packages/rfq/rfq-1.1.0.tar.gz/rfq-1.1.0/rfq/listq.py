from typing import Optional, List, Union, Literal

from redis import Redis

import rfq.redis


def listq(topic: str, queue: Union[Literal["backlog"], Literal["nextlog"]], redis: Optional[Redis] = None) -> List[str]:
    r = rfq.redis.default() if redis is None else redis

    msgids = r.lrange("rfq:{topic}:{queue}".format(topic=topic, queue=queue), 0, -1)

    return msgids
