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
    return { "meter": meter }

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
    providerurl = d['providerurl']
    startmeter = meter
    while active == 1:
        # print(r.text)
        meter += meterunit
        print ('meter: {}'.format(meter))
        jparm = {}
        jparm['meter'] = meter
        jparm['startmeter'] = startmeter
        jparm['unitpay'] = d['unitpay']
        print('active: {}'.format(active))
        data = json.dumps(jparm)
        requests.post(consumerurl,data=json.dumps(data),headers = {"Content-Type": "application/json"})
        requests.post('{}/meter'.format(providerurl),data=json.dumps(data),headers = {"Content-Type": "application/json"})
        sleep (wait)
    print('done charging. active: {}'.format(active))
    requests.delete(consumerurl)
    return "<h1>charge initiated</h1>"

@app.route('/', methods=['DELETE'])
def home_delete():
    global active, consumerurl
    active = 0
    # print('stopping ' + consumerurl)
    # requests.delete(consumerurl)
    return "<h1>charge stopped</h1>"

@app.route('/reset', methods=['PUT'])
def reset_put():
    global meter
    meter = 0.0
    return "<h1>meter reset</h1>"

app.run(port=5200)