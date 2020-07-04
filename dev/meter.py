#!/usr/local/opt/python@3.8/bin/python3

from flask import Flask
from flask import request
import json
from time import sleep
import requests

meter = 0.0
meterunit = 0.0
active = 0
consumerurl = ''


# communication 
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home_get():
    global meter
    return { "meter": meter}

@app.route('/', methods=['PUT'])
def home_put():
    global active, consumerurl, meterunit, meter
    print (request.json)
    d = json.loads(request.json)
    for key,val in d.items():
        print ('{}: {}'.format(key,val))
    wait = d['meterunit'] * 3600 / d['chargespeed']
    print (wait)
    active = 1
    consumerurl = d['consumerurl']
    meterunit = d['meterunit']
    while active == 1:
        r = requests.get(consumerurl)
        # print(r.text)
        meter += meterunit
        print ('meter: {}'.format(meter))
        sleep (wait)
    requests.delete(consumerurl)
    return "<h1>charge initiated</h1>"

@app.route('/', methods=['DELETE'])
def home_delete():
    global active, consumerurl
    active = 0
    print(consumerurl)
    requests.delete(consumerurl)
    return "<h1>charge stopped</h1>"

@app.route('/reset', methods=['PUT'])
def reset_put():
    global meter
    meter = 0.0
    return "<h1>meter reset</h1>"

app.run(port=5200)