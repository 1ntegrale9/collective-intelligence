import os
import uvicorn
import knowledgebase
from typing import List
from fastapi import FastAPI
from model import PushTags
from model import PullTag

app = FastAPI(
    title='collective-intelligence',
    description='文字列タグ指向無向グラフ型ナレッジベース',
    docs_url='/'
)
db = knowledgebase.DataBase()
# cache = knowledgebase.Cache()


@app.get('/api')
def read_all_tags():
    return db.get_all_tags()


@app.post('/api/push')
def create_tags_relationship(push: PushTags) -> List[List[str]]:
    documents = db.compose_documents(push.tag1, push.tag2, push.domain, push.domain_id, push.user_id)
    db.set_tags_relationship(documents)
    return [
        db.get_related_tags(push.tag1, push.domain, push.domain_id),
        db.get_related_tags(push.tag2, push.domain, push.domain_id),
    ]


@app.post('/api/pull')
def read_related_tags(pull: PullTag) -> List[str]:
    return db.get_related_tags(pull.tag, pull.domain, pull.domain_id, pull.user_id)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=os.getenv('PORT', default=5000), log_level='info')
