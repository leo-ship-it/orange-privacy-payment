from web3.auto import Web3
import json


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# Bank's wallet
w3.eth.defaultAccount = "0x62B9a2F427Ae8649b2467e08095C65551140926d"
pk = '4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efc'
w3.eth.account.privateKeyToAccount(pk)
print(str(w3.eth.account))
f = open('contract_interface/Creator.json')
interface = json.load(f)
f.close()
creatorAddress = "0x30C9c0a3653c801773E21EA573d1C13bCA77e85F"
creator_contract = w3.eth.contract(address=creatorAddress,abi=interface['abi'])
tx_hash = creator_contract.functions.deploy().transact()
# raw_txn = creator_contract.functions.deploy().buildTransaction(
#     {
#     'chainId': 1337,
#     'gasLimit': 6721975,
#     'maxFeePerGas': w3.toWei('2', 'gwei'),
#     'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
#     'nonce': 0x00,
# }
# )
# signed_txn = w3.eth.account.sign_transaction(raw_txn, private_key=pk)
# print(signed_txn.hash)
# tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(tx_hash)
# w3.eth.waitForTransactionReceipt(tx_hash)
last = creator_contract.functions.getLastContract().call()
print(last)