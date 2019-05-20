import os
from flask import Flask
from gkb import get_keys
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/keys')
def keys():
    results = '\n'.join(get_keys())
    return results

if __name__ == '__main__':
    app.run()
