#!/usr/local/opt/python@3.8/bin/python3

# geth --http --goerli --http.corsdomain="*"

import requests
import json
import time
import random


class rnode:
    DEFAULT_TOKEN = "0xce4b48DF1E88DFd74da1963416a53bBA9cf3B2aE"

    def dbg(self, **kwargs):
        if self.dbglevel > 0:
            print(**kwargs)

    def __init__(self, port, endpoint=None, token=DEFAULT_TOKEN):
        address_key = "our_address"

        self.port = port
        if endpoint is not None:
            self.endpoint = endpoint
        else:
            self.endpoint = endpoint = "http://localhost:{}/api/v1".format(port)
        self.token = token

        r = requests.get("{}/address".format(endpoint))
        d = json.loads(r.text)
        try:
            self.address = d["our_address"]
        except KeyError as e:
            print("Response from Raiden node does not contain {}: {}".format(address_key, d))
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
        print("{}/payments/{}/{}".format(self.endpoint, ptoken, target))
        # print ({ 'amount': '{}'.format(amount), 'identifier': '{}'.format(id), })
        print(
            {"amount": amount, "identifier": id,}
        )
        r = requests.post(
            "{}/payments/{}/{}".format(self.endpoint, ptoken, target),
            headers={"Content-Type": "application/json",},
            json={"amount": amount, "identifier": id,},
        )
        print(r.status_code)
        print(r.text)
        return r

    def openchan(self, target, deposit, token=None):
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        c = requests.put(
            "{}/channels".format(self.endpoint, ptoken, target),
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
        return r

    def registertoken(self, token=None):
        r = requests.put("{}/tokens/{}".format(self.endpoint, token))
        return r

    def listchan(self, token=None, target=None):
        # no defaulting, because none -> all channels for all tokens
        return pget(self, "/channels/{}/{}".format(token, target))
