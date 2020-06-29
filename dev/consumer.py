#!/usr/local/opt/python@3.8/bin/python3

# geth --http --goerli --http.corsdomain="*"

import json
import time
from datetime import datetime
import random
from raiden_api import rnode
import argparse

token = "0xce4b48DF1E88DFd74da1963416a53bBA9cf3B2aE"
charger = "0x961D954009Db8D9ab527632D7537411f3b3b8473"  # node 3
# charger = "0xE76Ba8dA05B3fdA938Cd76fC4A9D044d0ab45Cd9" # node 6
priceperkwh = 300000000000000000  # 0.3 EBC
factor = 1000000000000000000


def getmaxcharge():  # dummy for maximum chargeability
    return 20

def parse_args():
    parser = argparse.ArgumentParser(description="Run consumer simulation")
    parser.add_argument(
        "--node-port",
        action="store",
        default=5001,
        help="set the port of the Raiden node to connect to (default: 5001)",
    )
    return parser.parse_args()

args = parse_args()
node = rnode(args.node_port)
q = node.histpay()
payhist = json.loads(q.text)
# print (type(payhist))

for f in payhist:
    if "identifier" not in f:
        f["identifier"] = "0"
    if "amount" not in f:
        f["amount"] = "0"
    # print (f)
    print(
        "{}: {} at {} :: {}".format(
            f["identifier"], f["amount"], f["log_time"], f["event"]
        )
    )
    # print (datetime.strptime(f['log_time'],'%Y-%m-%dT%H:%M:%S.%f'))


payid = random.randrange(1, 1000000000)
while True:
    try:
        start = time.time()
        # s = node.pay(charger,1,node.token,counter)
        s = node.pay(charger, 1, node.token, payid)
        end = time.time()
        print(end - start)
        # 409 conflict: If the address or the amount is invalid or if there is no path to the target, or if the identifier is already in use for a different payment.
        if s.status_code == 409:
            print("409 encountered, opening channel")
            o = node.openchan(charger, getmaxcharge * priceperkwh)
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
node.pay(charger, 1, node.token, 100)
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
