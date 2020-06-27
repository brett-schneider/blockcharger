#!/usr/local/opt/python@3.8/bin/python3

# geth --http --goerli --http.corsdomain="*" 

import requests
import json
import time

# this could go in a config file
port = 5001
endpoint = 'http://localhost:{}/api/v1/'.format(port)
r = requests.get('{}/address'.format(endpoint))
d = json.loads(r.text)
myaddress = d['our_address']
print (myaddress)

def getmaxcharge(): #dummy for maximum chargeability
    return 20

token = "0xce4b48DF1E88DFd74da1963416a53bBA9cf3B2aE"
#charger = "0x961D954009Db8D9ab527632D7537411f3b3b8473" # node 3
charger = "0xE76Ba8dA05B3fdA938Cd76fC4A9D044d0ab45Cd9" # node 6
priceperkwh = 300000000000000000 # 0.3 EBC
factor = 1000000000000000000

def pget(url):
    print ('{}/{}'.format(endpoint,url))
    r = requests.get('{}/{}'.format(endpoint,url))
    print (r.status_code)
    d = json.loads(r.text)
    for p in d:
        print (p)

def pay(token, target, amount):
    r = requests.post('{}/payments/{}/{}'.format(endpoint,token,target), 
        headers={ 'Content-Type': 'application/json', }, 
        json={ 'amount': '{}'.format(amount), 'identifier': '1', })
    print (r.status_code)
    print (r.text)
    if r.status_code == 409:   # 409 conflict: If the address or the amount is invalid or if there is no path to the target, or if the identifier is already in use for a different payment.
        r = requests.put('{}/channels', 
            headers={ 'Content-Type': 'application/json', }, 
            json={ 'partner_address': target
                , 'reveal_timeout': '50'
                , 'settle_timeout': '500'
                , 'token_address': token
                , 'total_deposit': getmaxcharge()*priceperkwh, })
        print (r.status_code)
        print (r.text)
    
    # 200 OK
    # 404 Not Found: The given token and / or target addresses are not valid eip55-encoded Ethereum addresses
    # 402 Payment Required: If the payment can’t start due to insufficient balance
    # 400 Bad Request: malformed json

#pget ('channels')
pget ('channels/{}'.format(token))
exit (0)

start = time.time()
pay (token, charger, 1)
end = time.time()
print (end - start)

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

exit (0)    

source = create(runmeter)

source.subscribe(
    on_next = lambda i: print("Received {0}".format(i)),
    on_error = lambda e: print("Error Occurred: {0}".format(e)),
    on_completed = lambda: print("Done!"),
)