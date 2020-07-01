#!/usr/local/opt/python@3.8/bin/python3

from raiden_api import rnode
from flask import Flask
import json
import random

node = rnode(5006)
#payhist = node.histpay()

conf = { 'priceperkwh': 300000000000000000,
        'maxkw': 25, 
         }

payid = 0

# communication 
app = Flask(__name__)
@app.route('/client', methods=['GET'])
def client_get():
    return json.dumps (conf)

# initiate charge
@app.route('/client', methods=['PUT'])
def client_put():
    # find unused payid
    payid = random.randrange(1,1000000000)
    q = node.histpay(id = payid)
    while q != []:
        q += 1
        q = node.histpay(id = payid)
    # return payid to consumer
    return json.dumps ({ 'identifier': payid, })

@app.route('/client', methods=['DELETE'])
def client_delete():
    # get payment history
    q = node.histpay(id = payid)
    # TODO: final balance
    return json.dumps ({ 'identifier': payid, 'status': 'terminated', })

# receive meter stuff TODO
@app.route('/meter', methods=['PUT'])
def meter_put():
    return json.dumps ({ 'status': 'OK', })


app.run()