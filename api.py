from flask import Flask
from flask import request
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
    response = jsonify({'keys': get_keys()})
    response.status_code = 200
    return response


@app.route('/api/get_values/<path:key>', methods=['GET'])
def api_get_values(key):
    response = jsonify({key: get_values(key)})
    response.status_code = 200
    return response


@app.route('/api/set_values', methods=['POST'])
def api_set_values():
    posted = request.get_json()
    keys = list(posted.keys())
    if len(keys) != 1:
        response = jsonify({'Error': 'Specify only one key'})
        response.status_code = 400
        return response
    key = keys[0]
    values = posted[key]
    if type(values) != list or any(type(value) != str for value in values):
        response = jsonify({'Error': 'Value must be an array of strings'})
        response.status_code = 400
        return response
    set_values(key, values)
    values = get_values(key)
    response = jsonify({key: values})
    response.status_code = 201
    return response


if __name__ == '__main__':
    app.run()
