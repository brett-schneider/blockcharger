#!/usr/local/opt/python@3.8/bin/python3

from raiden_api import rnode

node = rnode(5006)

q = node.histpay()
print(q.text)
