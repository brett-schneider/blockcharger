#!/usr/local/opt/python@3.8/bin/python3

from flask import Flask

# communication 
app = Flask(__name__)
@app.route('/', methods=['PUT'])
def home_put():
    pass

@app.route('/', methods=['DELETE'])
def home_delete():
    pass
