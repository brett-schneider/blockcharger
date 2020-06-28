#!/usr/local/opt/python@3.8/bin/python3

# geth --http --goerli --http.corsdomain="*" 

import requests
import json
import time
import random

class rnode:
    def __init__(self,port,endpoint,token = None):
        self.port = port
        self.endpoint = endpoint
        r = requests.get('{}/address'.format(endpoint))
        d = json.loads(r.text)
        myaddress = d['our_address']
        self.token = token
        if token is None:
            self.token = "0xce4b48DF1E88DFd74da1963416a53bBA9cf3B2aE"
        return myaddress

    def pget(self,url):
        print ('{}/{}'.format(self.endpoint,url))
        r = requests.get('{}/{}'.format(self.endpoint,url))
        print (r.status_code)
        d = json.loads(r.text)
        for p in d:
            print (p)

    def pay(self,target,amount,token = None,id = 1):
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        print ('{}/payments/{}/{}'.format(self.endpoint,ptoken,target))
        #print ({ 'amount': '{}'.format(amount), 'identifier': '{}'.format(id), })
        print ({ 'amount': amount, 'identifier': id, })
        r = requests.post('{}/payments/{}/{}'.format(self.endpoint,ptoken,target), 
            headers={ 'Content-Type': 'application/json', }, 
            json={ 'amount': amount, 'identifier': id, })
        print (r.status_code)
        print (r.text)
        return r

    def openchan(self,target,deposit,token = None):
        ptoken = token
        if ptoken is None:
            ptoken = self.token
        c = requests.put('{}/channels'.format(self.endpoint,ptoken,target), 
            headers={ 'Content-Type': 'application/json', }, 
            json={ 'partner_address': target
                , 'reveal_timeout': '50'
                , 'settle_timeout': '500'
                , 'token_address': ptoken
                , 'total_deposit': deposit, })
        print (c.status_code)
        print (c.text)
        return c
