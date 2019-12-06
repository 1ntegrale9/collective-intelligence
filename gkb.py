import os
import redis
from functools import reduce
from operator import and_

pool = redis.ConnectionPool.from_url(os.environ['REDIS_URL'], db=0, decode_responses=True)
rc = redis.StrictRedis(connection_pool=pool)


def sadd_dual(a, b):
    rc.sadd(a, b)
    rc.sadd(b, a)


def set_values(key, values):
    for value in values:
        sadd_dual(key, value)


def get_values(key):
    if rc.exists(key):
        return sorted(rc.smembers(key))
    return 'KeyError'


def get_intersection(args):
    if all(rc.exists(arg) for arg in args):
        return reduce(and_, (rc.smembers(key) for arg in args for key in rc.keys(arg)))


def get_keys():
    return sorted(rc.keys())
