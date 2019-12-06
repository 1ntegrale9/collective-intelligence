import os
import redis
from functools import reduce
from operator import and_

connection_pool = redis.ConnectionPool.from_url(
    url=os.environ['REDIS_URL'],
    db=0,
    decode_responses=True
)
r = redis.Redis(connection_pool=connection_pool)


def sadd_dual(t1, t2):
    return r.pipeline().sadd(t1, t2).sadd(t2, t1).execute()


def get_all_tags():
    return sorted(r.keys())


def get_related_tags(tag):
    if r.exists(tag):
        return sorted(r.smembers(tag))
    return []


def get_intersection(tags):
    if not all(r.exists(tag) for tag in tags):
        return []
    return reduce(and_, (r.smembers(tag) for tag in tags for tag in r.keys(tag)))


def set_tags(tag1, tag2):
    sadd_dual(tag1, tag2)
    return get_related_tags(tag1)
