#!/usr/local/opt/python@3.8/bin/python3

# geth --http --goerli --http.corsdomain="*"

import requests
import json
import time
import random
from datetime import datetime


class rnode:
    DEFAULT_TOKEN = "0xce4b48DF1E88DFd74da1963416a53bBA9cf3B2aE"
    DEFAULT_DECIMALS = 18

    def __init__(self, port, endpoint=None, token=DEFAULT_TOKEN):
        self.port = port
        if endpoint is not None:
            self.endpoint = endpoint
        else:
            self.endpoint = endpoint = "http://localhost:{}/api/v1".format(port)
        self.token = token

        r = requests.get("{}/address".format(self.endpoint))
        d = json.loads(r.text)
        try:
            self.address = d["our_address"]
        except KeyError as e:
            print("Response from Raiden node does not contain {}: {}".format("our_address", e))
            raise

    def pget(self, url):
        print("{}/{}".format(self.endpoint, url))
        r = requests.get("{}/{}".format(self.endpoint, url))
        print(r.status_code)
        d = json.loads(r.text)
        for p in d:
            print(p)

    def pay(self, target, amount, token=None, id=1):
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        # print("{}/payments/{}/{}".format(self.endpoint, ptoken, target))
        # print ({ 'amount': '{}'.format(amount), 'identifier': '{}'.format(id), })
        # print({"amount": amount, "identifier": id,})
        r = requests.post(
            "{}/payments/{}/{}".format(self.endpoint, ptoken, target),
            headers={"Content-Type": "application/json",},
            json={"amount": amount, "identifier": id,},
        )
        if r.status_code == 409:
            print("409 encountered, opening channel")
            o = self.openchan(provider, getmaxcharge() * priceperkwh)
            # if o.status_code != 201:
        # print(r.status_code)
        # print(r.text)
        # 200 OK
        # 404 Not Found: The given token and / or target addresses are not valid eip55-encoded Ethereum addresses
        # 402 Payment Required: If the payment can’t start due to insufficient balance
        # 400 Bad Request: malformed json
        return r

    def openchan(self, target, deposit, token=None):
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        c = requests.put(
            "{}/channels".format(self.endpoint),
            headers={"Content-Type": "application/json",},
            json={
                "partner_address": target,
                "reveal_timeout": "50",
                "settle_timeout": "500",
                "token_address": ptoken,
                "total_deposit": deposit,
            },
        )
        print(c.status_code)
        print(c.text)
        return c

    def histpay(self, token=None, target=None, id=None):
        # Query the payment history. This includes successful (EventPaymentSentSuccess) and
        # failed (EventPaymentSentFailed) sent payments as well as received payments (EventPaymentReceivedSuccess).
        # token_address and target_address are optional and will filter the list of events accordingly.
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        print("target: {}".format(target))
        ptarget = "/{}".format(target)
        if target is None:
            ptarget = ""
        print("{}/payments/{}{}".format(self.endpoint, ptoken, ptarget))
        r = requests.get("{}/payments/{}{}".format(self.endpoint, ptoken, ptarget))
        # print (r.status_code)
        # print (r.text)
        # self.dbg (r.status_code)
        # self.dbg (r.text)
        jr = json.loads(r.text)
        if id is not None:
            jr = [ x for x in jr if 'identifier' in x ]
            jr = [ x for x in jr if x['identifier'] == '{}'.format(id) ]
        return jr

    def getbalance(self,id):
        a = self.histpay(id=id)
        balance = 0
        for p in a:
            if 'amount' in p:
                balance += int(p['amount'])
            else:
                print(p)
        return balance

    def lastpay(self, token=None, target=None):
        # Query the payment history. This includes successful (EventPaymentSentSuccess) and
        # failed (EventPaymentSentFailed) sent payments as well as received payments (EventPaymentReceivedSuccess).
        # token_address and target_address are optional and will filter the list of events accordingly.
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        print("target: {}".format(target))
        ptarget = "/{}".format(target)
        if target is None:
            ptarget = ""
        print("{}/payments/{}{}".format(self.endpoint, ptoken, ptarget))
        r = requests.get("{}/payments/{}{}".format(self.endpoint, ptoken, ptarget))
        # print (r.status_code)
        # print (r.text)
        # self.dbg (r.status_code)
        # self.dbg (r.text)
        jr = json.loads(r.text)
        jr = [ x for x in jr if 'target' in x ]
        m = {}
        for x in jr:
            if len(x['log_time']) == 19:
                d = datetime.strptime(x['log_time'],'%Y-%m-%dT%H:%M:%S')    
            else:
                d = datetime.strptime(x['log_time'],'%Y-%m-%dT%H:%M:%S.%f')
            t = x['target']
            if t in m:
                if m[t] < d:
                    m[t]=d
            else:
                m[t]=d
        return m

    def registertoken(self, token=None):
        r = requests.put("{}/tokens/{}".format(self.endpoint, token))
        return r

    def listchan(self, token=None, target=None):
        # no defaulting, because none -> all channels for all tokens
        return self.pget("/channels/{}/{}".format(token, target))
