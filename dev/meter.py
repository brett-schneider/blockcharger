#!/usr/local/opt/python@3.8/bin/python3

from flask import Flask

# communication 
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home_get():
    # TODO: read meter current thing
    pass

@app.route('/', methods=['PUT'])
def home_put():
    # todo: speed => ticks
    pass

@app.route('/', methods=['DELETE'])
def home_delete():
    pass

@app.route('/reset', methods=['PUT'])
def reset_put():
    # TODO: reset meter?
    pass
