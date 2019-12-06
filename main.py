from fastapi import FastAPI
from gkb import get_keys

app = FastAPI()


@app.get('/')
def read_tags():
    return {'tags': get_keys()}
