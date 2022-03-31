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
    creatorAddress = "0x30C9c0a3653c801773E21EA573d1C13bCA77e85F"
    creator_contract = w3.eth.contract(address=creatorAddress,abi=interface['abi'])
    # tx_hash = creator_contract.functions.deploy().transact()
    raw_txn = creator_contract.functions.deploy().buildTransaction(
        {
     'chainId': 1337,
     'gas': 70000,
     'maxFeePerGas': w3.toWei('2', 'gwei'),
     'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
     'nonce': 0x00,
 }
    )
    pk = '4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efc'
    signed_txn = w3.eth.account.sign_transaction(raw_txn, private_key=pk)
    print(signed_txn.hash)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
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


# Endpoint for the client to explicit that the service is done. Transfers token to service Provider.
# In this example we don't check the Origin of the caller but this can be done by adding a rule to the transfer function of the smart contract
# https://web3py.readthedocs.io/en/stable/web3.eth.account.html
@app.route('/service_done')
def service_done():
    with open('transaction_data.json') as json_file:
        data = json.load(json_file)
    # amount = Web3.utils.toBN(data["amount"])
    to = data["to"]
    erc20add = data["contract"]
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=erc20add,abi=interface['abi'])
    tx_hash = erc20_contract.functions.transfer(to, 1990).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    bal = erc20_contract.functions.balanceOf(to).call()

    return str(bal)

@app.route('/token_settlement')
def token_settlement():
    with open('transaction_data.json') as json_file:
        data = json.load(json_file)
    to = data["to"]
    erc20add = data["contract"]
    fro = data["from"]
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=erc20add,abi=interface['abi'])
    client_amount = erc20_contract.functions.balanceOf(fro).call()
    provider_amount = erc20_contract.functions.balanceOf(to).call()
    return f"Token settelement done. Payed Client : {client_amount} and Service Provider {provider_amount}"