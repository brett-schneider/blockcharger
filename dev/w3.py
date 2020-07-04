import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3.eth.getBlock('latest')

abi = json.loads('[ { "inputs": [ { "internalType": "uint256", "name": "_p", "type": "uint256" } ], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": true, "inputs": [], "name": "get", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "_n", "type": "uint256" } ], "name": "setNP", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "_n", "type": "uint256" } ], "name": "setP", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" } ]')
checksum_address = Web3.toChecksumAddress('0xc0cf5d6b317d00ab65a33ca780b503232c2feda3')
our_address ='0x8ccAE3CC7b16Ce2c7AbC4fA098eE1a185287C7a4'
nonce = w3.eth.getTransactionCount(our_address)

smartcontract = w3.eth.contract(
    address=checksum_address,
    abi=abi
)

print("nonce: ", nonce)
print("get():")
print(smartcontract.functions.get().call())

txn = smartcontract.functions.setP(1).buildTransaction({
     'from': our_address,
     'chainId': 5,
     'gas': 900000,
     'gasPrice': w3.toWei('1', 'gwei'),
     'nonce': nonce,
})
private_key = 'D5228D9892AB6DEAE3696CA941AA2B6018D9929136B14AFAE8F9F12C6956F326'

signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
print()
print(signed_txn.hash)
print(w3.eth.sendRawTransaction(signed_txn.rawTransaction))
print(w3.toHex(w3.keccak(signed_txn.rawTransaction)))

