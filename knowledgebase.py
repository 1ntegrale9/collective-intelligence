import os
import redis
from pymongo import MongoClient
from typing import List
from typing import Optional
from functools import reduce
from operator import and_
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class DataBase():
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URL'))
        self.database = self.client.gkb

    def _compose_document(self, tag1: str, tag2: str, domain: str, domain_id: str, user_id: str):
        return {
            'tag1': tag1,
            'tag2': tag2,
            'domain': domain,
            'domain_id': domain_id,
            'user_id': user_id,
            'created_at': datetime.now(),
        }
    
    def compose_documents(self, tag1: str, tag2: str, domain: str, domain_id: str, user_id: str):
        document1 = self._compose_document(tag1, tag2, domain, domain_id, user_id)
        document2 = self._compose_document(tag2, tag1, domain, domain_id, user_id)
        return [document1, document2]

    def set_tags_relationship(self, documents: List[dict], domain: Optional[str]):
        self.database[domain or 'global'].insert_many(documents)

    def get_related_tags(self, tag: str, domain: str = '', domain_id: str = '', user_id: str = ''):
        filter = {'tag1': tag}
        if domain_id != '':
            filter['domain_id'] = domain_id
        if user_id != '':
            filter['user_id'] = user_id
        related_tags = self.database[domain or 'global'].find(
            filter=filter,
            projection={'_id': False, 'tag2': True},
        ).distinct('tag2')
        return sorted(related_tags)

    def get_all_tags(self):
        tags = self.database['global'].find(
            filter={},
            projection={'_id': False, 'tag1': True},
        ).distinct('tag1')
        return sorted(tags)

class Cache():
    def __init__(self):
        self.pool = redis.ConnectionPool.from_url(
            url=os.getenv('REDIS_URL'),
            decode_responses=True
        )
        self.conn = redis.Redis(connection_pool=self.poolol)

    def set_tags_relationship(self, tag1, tag2) -> List[int]:
        return self.conn.pipeline().sadd(tag1, tag2).sadd(tag2, tag1).execute()

    def get_related_tags(self, tag):
        return sorted(self.conn.smembers.get(tag, []))

    def get_intersection(self, tags):
        if not all(self.conn.exists(tag) for tag in tags):
            return []
        return reduce(and_, (self.conn.smembers(t) for tag in tags for t in self.conn.keys(tag)))

    def get_all_tags(self):
        return sorted(self.conn.keys())

def test():
    db = DataBase()
    result = db.get_related_tags('discord.py', 'discord')
    print(result)
