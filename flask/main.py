from flask import Flask, request
from pprint import pprint
from flask import make_response
from flask import redirect

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Python Bot</h1>"


@app.route('/make_response')
def index2():
    response = make_response('<h1>This document carries a cookie.</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/', methods=['POST'])
def result():

    return request.args.get('test-key')  # raw data
    # json, if content-type of application/json is sent with the request
    # pprint(request.json)
    # json, if content-type of application/json is not sent
    # pprint(request.get_json(force=True))


@app.route('/user/<name>')
def user(name):
    return f"<h1>Hello, {name}</h1>"


@app.route('/query-example')
def query_example():
    # If key doesn't exits, returns None
    language = request.args.get('language')
    test = request.args['test']

    return f"<h1>The language value is: {language} {test}</h1>"


@app.route('/redirect/<redirect_address>')
def rdirect(redirect_address):
    return redirect(f'https://{redirect_address}')


@app.route('/tradingview', methods=['POST'])
def drsi_with_filters():
    pprint(request.content_type)
    pprint(request.json)
    response = make_response()
    response.status_code = 200
    return response


# app.run(debug=True, host='0.0.0.0', port=81)
