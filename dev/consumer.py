#!/usr/local/opt/python@3.8/bin/python3

import json
import time
from datetime import datetime
import random
from raiden_api import rnode
import argparse
import requests

DEFAULT_PROVIDER_ADDRESS = "localhost:5000"  # node 3
DEFAULT_CONSUMER_NODE_PORT = 5001

def getmaxcharge():  # dummy for maximum chargeability
    return 20

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
        help="set the ETH address of the provider (default: {})".format(
            DEFAULT_PROVIDER_ADDRESS
        ),
    )
    return parser.parse_args()

# Parse commmand-line arguments.
args = parse_args()
# Connect to the Raiden node.
node = rnode(args.node_port)

# PAUSE: consumer is set up, ready to connect
# connect to charger and query price etc
r = requests.get(args.provider_address)
jr = json.loads(r.text)
provider = jr['address']
priceperkwh = jr['priceperkwh']
chargemaxkwh = jr['maxkw']

# PAUSE: consumer decides to charge
r = requests.put(args.provider_address)
jr = json.loads(r.text)
payid = jr['identifier']

#dbg:
print (r.text)
print ('payid: '.format(payid))
exit (0)

while True:  #
    try:
        start = time.time()
        s = node.pay(provider, 1, node.token, payid)
        end = time.time()
        print(end - start)
        # 409 conflict: If the address or the amount is invalid or if there is no path to the target, or if the identifier is already in use for a different payment.
        if s.status_code == 409:
            print("409 encountered, opening channel")
            o = node.openchan(provider, getmaxcharge() * priceperkwh)
            if o.status_code != 201:
                break
    except KeyboardInterrupt:
        break

    # 200 OK
    # 404 Not Found: The given token and / or target addresses are not valid eip55-encoded Ethereum addresses
    # 402 Payment Required: If the payment can’t start due to insufficient balance
    # 400 Bad Request: malformed json

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
