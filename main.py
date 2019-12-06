from fastapi import FastAPI
from pydantic import BaseModel
from gkb import get_all_tags, get_related_tags, set_tags

app = FastAPI(docs_url='/')


class Tags(BaseModel):
    tag1: str
    tag2: str


@app.get('/api')
def read_all_tags():
    return get_all_tags()


@app.get('/api/{tag:path}')
def read_related_tags(tag: str):
    return get_related_tags(tag)


@app.post('/api')
def create_tags_relationship(tags: Tags):
    set_tags(tags.tag1, tags.tag2)
    return {
        tag1: get_related_tags(tag1),
        tag2: get_related_tags(tag2)
    }
