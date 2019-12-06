from fastapi import FastAPI
from pydantic import BaseModel
from gkb import get_all_tags, get_related_tags, set_tags

app = FastAPI()


class Tags(BaseModel):
    tag1: str
    tag2: str


@app.get('/')
def read_all_tags():
    return {'tags': get_all_tags()}


@app.get('/{tag:path}')
def read_related_tags(tag: str):
    return {tag: get_related_tags(tag)}


@app.post('/')
def create_relation(tags: Tags):
    return {tags.tag1: set_tags(tags.tag1, tags.tag2)}
