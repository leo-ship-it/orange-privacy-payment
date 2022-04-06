from web3.auto import Web3
import json


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
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
print(tx_hash)
last = creator_contract.functions.getLastContract().call()
print(last)