#!/usr/local/opt/python@3.8/bin/python3

from raiden_api import rnode
from flask import Flask
from flask import request
import json
import random
import argparse
import requests

DEFAULT_PROVIDER_NODE_PORT = 5006
DEFAULT_PRICE_FOR_KWH = 300000000000000000  # 0.3 EBC
DEFAULT_METER_ADDRESS = 'localhost:5200'

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
    parser.add_argument(
        "--meter-address",
        action="store",
        default=DEFAULT_METER_ADDRESS,
        help="set meter address (default: {})".format(
            DEFAULT_METER_ADDRESS
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

# globals to do the metering
payid = 0
meter = None

# communication 
app = Flask(__name__)
@app.route('/client', methods=['GET'])
def client_get():
    return json.dumps (conf)

# initiate charge
@app.route('/client', methods=['PUT'])
def client_put():
    global payid
    # find unused payid
    payid = random.randrange(1,1000000000)
    q = node.histpay(id = payid)
    while q != []:
        payid += 1
        q = node.histpay(id = payid)
    # return payid to consumer
    # meter = startmeter()
    return json.dumps ({ 'identifier': payid, })

# receive meter stuff TODO
@app.route('/meter', methods=['POST'])
def meter_post():
    d = json.loads(request.json)
    # for key,val in d.items():
    #     print ('{}: {}'.format(key,val))
    meter = d['meter']
    startmeter = d['startmeter']
    unitpay = d['unitpay']
    balancemeter = (meter - startmeter) * args.price_per_kwh
    balance = node.getbalance(payid)
    print ('balance: {}, meter: {:.5f}, startmeter: {:.5f}, balance-by-meter: {}'.format(balance,meter,startmeter,int(balancemeter)))
    if abs(balance - balancemeter) > unitpay * 2:
        print('abort: balances differ by {}, max {}'.format(abs(balance - balancemeter),unitpay*2))
        requests.delete(args.meter_address)

    
    # balance/ pending payments
    # stopmeter if whoopie
    # what abt restarts when more payment arrives
    return json.dumps ({ 'status': 'OK', })

app.run()

