import json
import pprint

from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3.eth.getBlock("latest")
abi = json.loads('[ { "inputs": [ { "internalType": "address", "name": "_address", "type": "address" }, { "internalType": "string", "name": "_location", "type": "string" } ], "name": "registerProvider", "outputs": [ { "internalType": "uint256", "name": "providerID", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "energy_providers", "outputs": [ { "internalType": "uint256", "name": "id", "type": "uint256" }, { "internalType": "address", "name": "provider_address", "type": "address" }, { "internalType": "string", "name": "location", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "getAllProviders", "outputs": [ { "internalType": "address[]", "name": "", "type": "address[]" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "providerID", "type": "uint256" } ], "name": "getProviderLocation", "outputs": [ { "internalType": "string", "name": "location", "type": "string" } ], "stateMutability": "view", "type": "function" } ]')

checksum_address = Web3.toChecksumAddress("0x4ef9b41395C94188827d3660cCbf9534425e701A")
our_address = "0xE76Ba8dA05B3fdA938Cd76fC4A9D044d0ab45Cd9"
nonce = w3.eth.getTransactionCount(our_address)

location = "52.515875,13.378057"

smartcontract = w3.eth.contract(address=checksum_address, abi=abi)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(smartcontract.functions)

print("nonce: ", nonce)
temp = smartcontract.functions.registerProvider(our_address, location)

txn = temp.buildTransaction(
    {
        "from": our_address,
        "chainId": 5,
        "gas": 900000,
        "gasPrice": w3.toWei("1", "gwei"),
        "nonce": nonce,
    }
)

private_key = "344E44476EF44B6573F95FF2FBF345B4E494C3FA08E8F203D0E251C7D2AB1EBE"

signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
print()
print(signed_txn.hash)
print()
print(w3.eth.sendRawTransaction(signed_txn.rawTransaction))
print()
print(w3.toHex(w3.keccak(signed_txn.rawTransaction)))
