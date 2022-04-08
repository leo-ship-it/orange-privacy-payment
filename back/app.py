from flask import Flask
from flask import request
import random
from web3 import Web3, EthereumTesterProvider
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
f = open('default_data.json')
default = json.load(f)
f.close()
fee = default["bank_fee"]
decimals = default["erc_20_decimals"]
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Bank's wallet
bankAddress = default["bank_address"]
w3.eth.defaultAccount = bankAddress
# Loading account from private key.
pk = default["bank_private_key"]
w3.eth.account.privateKeyToAccount(pk)

creatorAddress = default["creator_contract_address"]
f = open('contract_interface/Creator.json')
interface = json.load(f)
creator_contract = w3.eth.contract(
    address=creatorAddress, abi=interface['abi'])
f.close()

# Endpoint to init new Transaction : draw token value, deploy new erc20, store client and service provider infos
# Parameters: 
# from : wallet address of the client
# to : wallet address of the service proviedr
# amount : amount of money implied in the transfer
@app.route('/init_transaction')
def init_transaction():
    address_from = request.args.get('from')
    address_to = request.args.get('to')
    amount = request.args.get('amount')
    rate = random.random()
    tx_hash = creator_contract.functions.deploy().transact()
    print(tx_hash)
    last = creator_contract.functions.getLastContract().call()
    print(last)
    data_to_store = {
        "from": address_from,
        "to": address_to,
        "amount": amount,
        "fee": fee,
        "contract": last,
        "rate": rate
    }
    with open(default["json_file_name"], 'w') as outfile:
        json.dump(data_to_store, outfile)
    return("New contract created at" + last)

# EndPoint where the client pays the bank and the bank transfer the right amount of tokens to the client
@app.route('/pay')
def pay():
    with open(default["json_file_name"]) as json_file:
        data = json.load(json_file)
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    erc20_contract = w3.eth.contract(
        address=data["contract"], abi=interface['abi'])
    to_send = (int(data["amount"])) / float(data["rate"]) * decimals
    print(to_send)
    tx_hash = erc20_contract.functions.transfer(data["from"], int(to_send)).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_hash


# Endpoint for the client to explicit that the service is done. Transfers token to service Provider.
# In this example we don't check the Origin of the caller but this can be done by adding a rule to the transfer function of the smart contract
# https://web3py.readthedocs.io/en/stable/web3.eth.account.html
@app.route('/service_done')
def service_done():
    with open(default["json_file_name"]) as json_file:
        data = json.load(json_file)
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=data["contract"], abi=interface['abi'])
    txn_transferFrom = erc20_contract.functions.transferFrom(data["from"], bankAddress, int(data["amount"])).transact({'from':bankAddress})
    w3.eth.waitForTransactionReceipt(txn_transferFrom)
    return str(erc20_contract.functions.balanceOf(data["to"]).call())

# API called by the provider when the service as been fullfilled, the bank transfer tokens to the provider's wallet
@app.route('/service_fullfilled')
def service_fullfilled():
    with open(default["json_file_name"]) as json_file:
        data = json.load(json_file)
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=data["contract"],abi=interface['abi'])
    client_amount = erc20_contract.functions.balanceOf(data["from"]).call()
    tx_transfer = erc20_contract.functions.transfer(data["from"], int(client_amount)).transact()
    print(tx_transfer)
    return f"Service Fullfilled"

# When the client and the provider disagree on the service provided the tokens are dirstributed according a ratio
# Parameters:
# ratio : number between 0 and 1 that specifieces how much should be given to the services provider, the rest will be given back to the client
@app.route('/service_claim')
def service_claim():
    ratio = float(request.args.get('ratio'))
    assert(ratio >= 0 and ratio <= 1)
    with open(default["json_file_name"]) as json_file:
        data = json.load(json_file)
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address= data["contract"],abi=interface['abi'])
    tx_hash = erc20_contract.functions.transfer(data["to"], int(ratio * int(data["amount"]))).transact()
    tx_hash2 = erc20_contract.functions.transfer(data["from"], int((1-ratio)*int(data["amount"]))).transact()
    print(tx_hash, tx_hash2)
    return f"Claim Occured"

# Finalize the transaction, deletes the token contract and pays the client and the provider
@app.route('/token_settlement')
def token_settlement():
    with open(default["json_file_name"]) as json_file:
        data = json.load(json_file)
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=data["contract"],abi=interface['abi'])
    client_amount = erc20_contract.functions.balanceOf(data["from"]).call()
    provider_amount = erc20_contract.functions.balanceOf(data["to"]).call()
    txn_transferFrom = erc20_contract.functions.finalize().transact()
    print(txn_transferFrom)
    return f"Token settelement done. Smart Contract Destroyed. Payed {client_amount} to client and {provider_amount} to provider"