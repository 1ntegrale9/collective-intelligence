import os
import redis
from functools import reduce
from operator import and_
from dotenv import load_dotenv

load_dotenv()

pool = redis.ConnectionPool.from_url(
    url=os.getenv('REDIS_URL'),
    decode_responses=True
)
conn = redis.Redis(connection_pool=pool)


def set_tags_relationship(tag1, tag2):
    return conn.pipeline().sadd(tag1, tag2).sadd(tag2, tag1).execute()


def get_related_tags(tag):
    return sorted(conn.smembers(tag)) if conn.exists(tag) else []


def get_intersection(tags):
    if not all(conn.exists(tag) for tag in tags):
        return []
    return reduce(and_, (conn.smembers(t) for tag in tags for t in conn.keys(tag)))


def get_all_tags():
    return sorted(conn.keys())
