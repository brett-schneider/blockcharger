import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3.eth.getBlock('latest')

abi = json.loads('[ { "inputs": [ { "internalType": "uint256", "name": "_p", "type": "uint256" } ], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": true, "inputs": [], "name": "get", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "_n", "type": "uint256" } ], "name": "setNP", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "_n", "type": "uint256" } ], "name": "setP", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function" } ]')
checksum_address = Web3.toChecksumAddress('0xc0cf5d6b317d00ab65a33ca780b503232c2feda3')

smartcontract = w3.eth.contract(
    address=checksum_address,
    abi=abi
)

print("get():")
print(smartcontract.functions.get().call())

txn = smartcontract.functions.setP(1).buildTransaction({'gasPrice': gas_price})
print(txn)

smartcontract.eth.sendTransaction(txn)


# nonce = w3.eth.getTransactionCount('0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E')
# 
# # Build a transaction that invokes this contract's function, called transfer
# unicorn_txn = unicorns.functions.transfer(
#         checksum_address
#     1,
# ).buildTransaction({
#     'chainId': 1,
#     'gas': 70000,
#     'gasPrice': w3.toWei('1', 'gwei'),
#     'nonce': nonce,
# })
# 
# private_key = b"\xb2\\}\xb3\x1f\xee\xd9\x12''\xbf\t9\xdcv\x9a\x96VK-\xe4\xc4rm\x03[6\xec\xf1\xe5\xb3d"
# 
# signed_txn = w3.eth.account.sign_transaction(unicorn_txn, private_key=private_key)
# 
# signed_txn.hash
# 
# HexBytes('0xf8a980843b9aca008301117094fb6916095ca1df60bb79ce92ce3ea74c37c5d35980b844a9059cbb000000000000000000000000fb6916095ca1df60bb79ce92ce3ea74c37c5d359000000000000000000000000000000000000000000000000000000000000000125a00fb532eea06b8f17d858d82ad61986efd0647124406be65d359e96cac3e004f0a02e5d7ffcfb7a6073a723be38e6733f353cf9367743ae94e2ccd6f1eba37116f4')
# >>> signed_txn.r
# 7104843568152743554992057394334744036860247658813231830421570918634460546288
# >>> signed_txn.s
# 20971591154030974221209741174186570949918731455961098911091818811306894497524
# >>> signed_txn.v
# 37
# 
# >>> w3.eth.sendRawTransaction(signed_txn.rawTransaction)  
# 
# # When you run sendRawTransaction, you get the same result as the hash of the transaction:
# >>> w3.toHex(w3.keccak(signed_txn.rawTransaction))
# '0x4795adc6a719fa64fa21822630c0218c04996e2689ded114b6553cef1ae36618'
