from flask import Flask
from flask import request
import random
from web3 import Web3, EthereumTesterProvider
import json

app = Flask(__name__)
fee = 5
decimals = 100
    
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Bank's wallet
w3.eth.defaultAccount = "0x62B9a2F427Ae8649b2467e08095C65551140926d"
 
# Bank address : 0x62B9a2F427Ae8649b2467e08095C65551140926d
# Bank private Key : 0x4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efct

# Endpoint to init new Transaction : draw token value, deploy new erc20, store client and service provider infos
@app.route('/init_transaction')
def init_transaction():
    address_from = request.args.get('from')
    address_to = request.args.get('to')
    amount = request.args.get('amount')
    f = open('contract_interface/Creator.json')
    interface = json.load(f)
    creatorAddress = "0x6C4754E5D7362eDb8947877EE07b6b60b4d9F4B3"
    creator_contract = w3.eth.contract(address=creatorAddress,abi=interface['abi'])
    tx_hash = creator_contract.functions.deploy().transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    last = creator_contract.functions.getLastContract().call()
    print(last)
    f.close()
    rate = random.random()
    data_to_store = {
        "from" : address_from,
        "to" : address_to,
        "amount" : amount,
        "fee" : fee,
        "contract" : last,
        "rate" : rate
    }
    with open('transaction_data.json', 'w') as outfile:
        json.dump(data_to_store, outfile)
    return("New contract created at" + last)

# EndPoint where the client pays the bank and the bank transfer the right amount of tokens to the client
@app.route('/pay')
def pay():
    with open('transaction_data.json') as json_file:
        data = json.load(json_file)
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    erc20_contract = w3.eth.contract(address=data["contract"],abi=interface['abi'])
    to_send = (int(data["amount"]) ) / float(data["rate"]) * decimals
    print(to_send)
    tx_hash = erc20_contract.functions.transfer(data["from"], int(to_send)).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_hash

