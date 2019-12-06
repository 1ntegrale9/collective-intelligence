import uvicorn
from fastapi import FastAPI
from gkb import get_keys

app = FastAPI()


@app.get('/tags')
def read_tags():
    return {'tags': get_keys()}


if __name__ == '__main__':
    uvicorn.run(app)
