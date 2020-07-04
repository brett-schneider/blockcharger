#!/usr/local/opt/python@3.8/bin/python3

import json
import time
import random
from raiden_api import rnode
import argparse
import requests
from math import ceil

DEFAULT_PROVIDER_ADDRESS = "http://localhost:5000"  
DEFAULT_CONSUMER_NODE_PORT = 5001
DEFAULT_METER_ADDRESS = "http://localhost:5200" 
DEFAULT_PAYMENT_PORT = 5900

def getmaxcharge():  # dummy for maximum chargeability
    return 20

def getmaxspeed():  # dummy for max charge speed
    return 15

def getunitpay(speed, price, paypersec = None):
    if paypersec is None:
        # default: 5 payments per second
        paypersec = 0.5
    # actual unit of payment
    iup = int(speed*price/paypersec/3600)
    # may result in inaccurate decimal representation
    mu = iup/price
    # take two most significant digits of measuring unit
    mux = 0
    for i in range(100):
        if ceil(mu*10**i) >= 10:
            mux = i
            break
    # return those times price so no rounding errors
    return price*(ceil(mu*10**mux))/10**mux

def parse_args():
    parser = argparse.ArgumentParser(description="Run consumer simulation")
    parser.add_argument(
        "--node-port",
        action="store",
        default=DEFAULT_CONSUMER_NODE_PORT,
        help="set the port of the Raiden node to connect to (default: {}).format(DEFAULT_CONSUMER_NODE_PORT)",
    )
    parser.add_argument(
        "--provider-address",
        action="store",
        default=DEFAULT_PROVIDER_ADDRESS,
        help="set provider api address (default: {})".format(
            DEFAULT_PROVIDER_ADDRESS
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
    parser.add_argument(
        "--payment-port",
        action="store",
        default=DEFAULT_PAYMENT_PORT,
        help="set payment server port (default: {})".format(
            DEFAULT_PAYMENT_PORT
        ),
    )
    return parser.parse_args()

# Parse commmand-line arguments.
args = parse_args()
# Connect to the Raiden node.
node = rnode(args.node_port)

from werkzeug.serving import make_server
import threading
from flask import Flask
from flask import request
from logging import Logger
log = Logger(__name__)

startmeter = 0.0
provider = None
priceperkwh = None
chargemaxkw = None
chargespeed = None
unitpay = None
meterunit = None
payid = None
class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', args.payment_port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        log.info('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def stop_server():
    global server
    server.shutdown()

def start_server():
    global server
    app = Flask('myapp')
    @app.route('/', methods=['POST'])
    def home_post():
        d = json.loads(request.json)
        # for k,v in d.items():
        #     print ('{}: {}'.format(k,v))
        meter = d['meter']
        #Vprint('payid: {}'.format(payid))
        node.pay(provider, unitpay, node.token, id=payid)
        balance = node.getbalance(payid)
        # r = requests.get(args.meter_address)
        # meter = json.loads(r.text)['meter']
        print ('meter: {} :: startmeter: {} :: priceperkwh: {}'.format(meter, startmeter, priceperkwh))
        balancemeter = (meter - startmeter) * priceperkwh
        print ('balance: {}, meter: {:.5f}, startmeter: {:.5f}, balance-by-meter: {}'.format(balance,meter,startmeter,int(balancemeter)))
        if abs(balance - balancemeter) > unitpay * 2:
            print('abort: balances differ by {}, max {}'.format(abs(balance - balancemeter),unitpay*2))
            requests.delete(args.meter_address)
        return "<h1>meter ping received</h1>"
    # @app.route('/', methods=['DELETE'])
    # def home_delete():
    #     print('stop charge received')
    #     requests.delete(args.meter_address)
    #     # stop_server()
    #     return "<h1>finished charging</h1>"
    server = ServerThread(app)
    server.start()
    log.info('server started')

from time import sleep
start_server()
print('server started')

# PAUSE: consumer is set up, ready to connect
# connect to charger and query price etc
def connectcharger():
    r = requests.get('{}/client'.format(args.provider_address))
    if r.status_code != 200:
        exit (r.status_code)
    jr = json.loads(r.text)
    # provider = jr['address']
    # priceperkwh = jr['priceperkwh']
    # chargemaxkw = jr['maxkw']
    return jr

# PAUSE: consumer decides to charge
def begincharge(meterunit,chargespeed):
    global payid, startmeter
    r = requests.put('{}/client'.format(args.provider_address))
    if r.status_code != 200:
        print (r._content)
        print ('error: {}'.format(r.status_code))
        exit (r.status_code)
    jr = json.loads(r.text)
    payid = jr['identifier']
    chargedict = {}
    chargedict['meterunit'] = meterunit
    chargedict['chargespeed'] = chargespeed
    chargedict['consumerurl'] = "http://localhost:{}/".format(args.payment_port)
    chargedict['payid'] = payid
    chargedict['providerurl'] = args.provider_address
    chargedict['unitpay'] = unitpay
    data = json.dumps(chargedict)
    r = requests.get(args.meter_address)
    startmeter = json.loads(r.text)['meter']
    print('requesting charge, payid: {}'.format(payid))
    requests.put(args.meter_address,data=json.dumps(data),headers = {"Content-Type": "application/json"})
    print ('charge request ended')
    return (payid,startmeter)

while True:
    try:
        print ('1: connect charger')
        print ('2: disconnect charger')
        print ('3: begin charge')
        key = input()
        if key == '1':
            x = connectcharger()
            provider = x['address']
            priceperkwh = x['priceperkwh']
            chargemaxkw = x['maxkw']
            chargespeed = min(chargemaxkw, getmaxspeed())
            unitpay = getunitpay(chargespeed, priceperkwh)
            meterunit = unitpay/priceperkwh
            print ('chargespeed: {}'.format(chargespeed))
            print ('unitpay: {}'.format(unitpay))
            print ('meterunit: {} kWh'.format(meterunit))
        elif key == '2':
            if provider is None:
                print ('not connected')
            else:
                provider = None
                priceperkwh = None
                chargemaxkw = None
        elif key == '3':
            if provider is None:
                print ('not connected')
            else:
                (payid,startmeter) = begincharge(meterunit,chargespeed)
                # print ('recieved payid from charger: {}'.format(payid))
    except KeyboardInterrupt:
        break
stop_server()
exit(0)

#dbg:
print ('last payments on targets (charger busy?)')
for key,val in node.lastpay().items():
    print ('{}: {}'.format(key,val))

# commence charge

print('monitor charge')
(m,n) = (0.0,0.0)
print('server started')
wait = meterunit * 3600 / chargespeed

# try:
#     while m+(meterunit*5) > n:
#         r = requests.get(args.meter_address)
#         n = m
#         m = json.loads(r.text)['meter']
#         print ('m: {}, n: {}'.format(m,n))
#         print (wait)
#         sleep(wait+2)
#         print('loop')
# except KeyboardInterrupt:
#     stop_server()

stop_server()
exit(0)

start = time.time()
node.pay(provider, 1, node.token, 100)
end = time.time()
print(end - start)

# some reactive stuff i'm working on
from rx3 import create
from time import sleep


def runmeter(observer, scheduler):
    try:
        while True:
            observer.on_next("1")
            sleep(0.05)
    except KeyboardInterrupt:
        observer.on_completed()


exit(0)

source = create(runmeter)

source.subscribe(
    on_next=lambda i: print("Received {0}".format(i)),
    on_error=lambda e: print("Error Occurred: {0}".format(e)),
    on_completed=lambda: print("Done!"),
)
