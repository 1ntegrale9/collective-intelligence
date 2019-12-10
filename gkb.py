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


def get_all_tags():
    return sorted(r.keys())


def get_related_tags(tag):
    if not r.exists(tag):
        return []
    return sorted(r.smembers(tag))
    

def get_intersection(tags):
    if not all(r.exists(tag) for tag in tags):
        return []
    return reduce(and_, (r.smembers(tag) for tag in tags for tag in r.keys(tag)))


def set_tags(tag1, tag2):
    return r.pipeline().sadd(tag1, tag2).sadd(tag2, tag1).execute()
