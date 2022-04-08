from web3.auto import Web3
import json

# This file try to call the creator contract to create a new Token
f = open('default_data.json')
default = json.load(f)
f.close()


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.defaultAccount = default["bank_address"]
pk = default["bank_private_key"]
w3.eth.account.privateKeyToAccount(pk)
print(str(w3.eth.account))
f = open('contract_interface/Creator.json')
interface = json.load(f)
f.close()
creatorAddress = default["creator_contract_address"]
creator_contract = w3.eth.contract(address=creatorAddress,abi=interface['abi'])
tx_hash = creator_contract.functions.deploy().transact()
print(tx_hash)
last = creator_contract.functions.getLastContract().call()
print(last)