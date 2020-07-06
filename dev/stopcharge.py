#!/usr/local/opt/python@3.8/bin/python3

import requests
DEFAULT_METER_ADDRESS = "http://localhost:5200" 
r = requests.delete(DEFAULT_METER_ADDRESS)