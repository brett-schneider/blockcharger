#!/usr/local/opt/python@3.8/bin/python3

from raiden_api import rnode
from flask import Flask
import json
import random
import argparse

DEFAULT_PROVIDER_NODE_PORT = 5006
DEFAULT_PRICE_FOR_KWH = 300000000000000000  # 0.3 EBC

def parse_args():
    parser = argparse.ArgumentParser(description="Run provider simulation")
    parser.add_argument(
        "--node-port",
        action="store",
        default=DEFAULT_PROVIDER_NODE_PORT,
        help="set the port of the Raiden node to connect to (default: {})".format(
            DEFAULT_PROVIDER_NODE_PORT
        ),
    )
    parser.add_argument(
        "--price-per-kwh",
        action="store",
        default=DEFAULT_PRICE_FOR_KWH,
        help="set the default price for kWh (default: {})".format(
            DEFAULT_PRICE_FOR_KWH
        ),
    )
    return parser.parse_args()


# Parse commmand-line arguments.
args = parse_args()

node = rnode(args.node_port)

conf = { 'priceperkwh': 300000000000000000,
        'maxkw': 25, 
        'address' : node.address
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
