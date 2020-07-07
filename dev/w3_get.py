import json
import pprint

from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3.eth.getBlock("latest")
abi = json.loads( '[ { "inputs": [ { "internalType": "address", "name": "_address", "type": "address" }, { "internalType": "string", "name": "_location", "type": "string" } ], "name": "registerProvider", "outputs": [ { "internalType": "uint256", "name": "providerID", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "energy_providers", "outputs": [ { "internalType": "uint256", "name": "id", "type": "uint256" }, { "internalType": "address", "name": "provider_address", "type": "address" }, { "internalType": "string", "name": "location", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "getAllProviders", "outputs": [ { "internalType": "address[]", "name": "", "type": "address[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "providerID", "type": "uint256" } ], "name": "getProviderLocation", "outputs": [ { "internalType": "string", "name": "location", "type": "string" } ], "stateMutability": "view", "type": "function" } ]')

checksum_address = Web3.toChecksumAddress("0x4ef9b41395C94188827d3660cCbf9534425e701A")
#"0xb14f3486bb315d7cad8abacc745e3da6151ecb08"
our_address = "0x37275F6314cAA14dE6A2D5332709f97d89ef162F"
nonce = w3.eth.getTransactionCount(our_address)

smartcontract = w3.eth.contract(address=checksum_address, abi=abi)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(smartcontract.functions)

print("nonce: ", nonce)

providers = smartcontract.functions.getAllProviders().call()

locations = []
for i in range(len(providers)):
    locations.append(smartcontract.functions.getProviderLocation(i).call())
    
print(providers[:-2])
print(locations[:-2])
