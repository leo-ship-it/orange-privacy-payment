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
pk = '4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efc'
# Loading account from private key.
w3.eth.account.privateKeyToAccount(pk)

creatorAddress = "0x3E8B23e576ad350F3f0464a482cb976E6D105231"
bankAddress = "0x62B9a2F427Ae8649b2467e08095C65551140926d"
f = open('contract_interface/Creator.json')
interface = json.load(f)
creator_contract = w3.eth.contract(
    address=creatorAddress, abi=interface['abi'])
f.close()


# Bank address : 0x62B9a2F427Ae8649b2467e08095C65551140926d
# Bank private Key : 0x4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efct

# Endpoint to init new Transaction : draw token value, deploy new erc20, store client and service provider infos
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
    with open('transaction_data.json') as json_file:
        data = json.load(json_file)
    # amount = Web3.utils.toBN(data["amount"])
    to = data["to"]
    erc20add = data["contract"]
    fro = data["fro"]
    amount = int(data["amount"])
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=erc20add, abi=interface['abi'])
    txn_transferFrom = erc20_contract.functions.transferFrom(fro, bankAddress,amount).transact({'from':bankAddress})
    w3.eth.waitForTransactionReceipt(txn_transferFrom)
    bal = erc20_contract.functions.balanceOf(to).call()
    return str(bal)

@app.route('/service_fullfilled')
def service_fullfilled():
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
    txn_transferFrom = erc20_contract.functions.transferFrom(fro, bankAddress,int(client_amount)).transact({'from':bankAddress})
    return f"Service Fullfilled"

@app.route('/service_claim')
def service_claim():
    ratio = int(request.args.get('ratio'))
    assert(ratio >= 0 and ratio <= 1)
    with open('transaction_data.json') as json_file:
        data = json.load(json_file)
    to = data["to"]
    erc20add = data["contract"]
    fro = data["from"]
    amount = data["amount"]
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=erc20add,abi=interface['abi'])
    tx_hash = erc20_contract.functions.transfer(to, int(ratio * amount)).transact()
    tx_hash2 = erc20_contract.functions.transfer(fro, int((1-ratio)*amount)).transact()
    return f"Claim Occured"


@app.route('/token_settlement')
def token_settlement():
    with open('transaction_data.json') as json_file:
        data = json.load(json_file)
    to = data["to"]
    erc20add = data["contract"]
    fro = data["from"]
    to = data["to"]
    f = open('contract_interface/MetaCoin.json')
    interface = json.load(f)
    f.close()
    erc20_contract = w3.eth.contract(address=erc20add,abi=interface['abi'])
    client_amount = erc20_contract.functions.balanceOf(fro).call()
    provider_amount = erc20_contract.functions.balanceOf(to).call()

    txn_transferFrom = erc20_contract.functions.finalize().transact()
    return f"Token settelement done. Smart Contract Destroyed. Payed {client_amount} to client and {provider_amount} to provider"