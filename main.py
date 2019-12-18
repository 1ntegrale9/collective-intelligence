from fastapi import FastAPI
from pydantic import BaseModel
from r import get_all_tags, get_related_tags, set_tags_relationship

app = FastAPI(
    title='collective-intelligence',
    description='文字列タグ指向無向グラフ型ナレッジベース',
    docs_url='/'
)


class Tags(BaseModel):
    tag1: str
    tag2: str


@app.get('/api')
def read_all_tags():
    return get_all_tags()


@app.post('/api/push')
def create_tags_relationship(tags: Tags):
    set_tags_relationship(tags.tag1, tags.tag2)
    return {tag: get_related_tags(tag) for _, tag in tags}


@app.post('/api/pull')
def read_related_tags(tag: str):
    return get_related_tags(tag)
