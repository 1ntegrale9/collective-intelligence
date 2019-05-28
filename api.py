from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from gkb import get_keys
from gkb import get_values
from gkb import set_values

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/api/get_keys', methods=['GET'])
def api_get_keys():
    json = jsonify({'keys': get_keys()})
    return make_response(json, 200)


@app.route('/api/get_values/<path:key>', methods=['GET'])
def api_get_values(key):
    json = jsonify({key: get_values(key)})
    return make_response(json, 200)


@app.route('/api/set_values', methods=['POST'])
def api_set_values():
    posted = request.get_json()
    keys = list(posted.keys())
    if len(keys) != 1:
        json = jsonify({'Error': 'Specify only one key'})
        return make_response(json, 400)
    key = keys[0]
    values = posted[key]
    if type(values) != list or any(type(value) != str for value in values):
        json = jsonify({'Error': 'Value must be an array of strings'})
        return make_response(json, 400)
    set_values(key, values)
    values = get_values(key)
    json = jsonify({key: values})
    return make_response(json, 201)


if __name__ == '__main__':
    app.run()
