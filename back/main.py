from flask import Flask
from flask import request
import random
from web3 import Web3, EthereumTesterProvider
import json


app = Flask(__name__)


fee = 5

@app.route('/')
def new_transaction():
    address_from = request.args.get('address_from')
    address_to = request.args.get('address_to')
    amount = request.args.get('amount')
    rate = random.random()
    amount_to = (amount - fee) / rate
    # call sc to create a token and send it to the address to 

    contract_address = ""
    data_to_store = {
        "from" : address_from,
        "to" : address_to,
        "amount" : amount,
        "fee" : fee,
        "contract" : contract_address,
        "rate" : rate,
    }



    return "Created contract at address " + contract_address

@app.route('/call_contract')
def call_contract():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    f = open('contract_interface/Creator.json')
    interface = json.load(f)
    creatorAddress = "0x6C4754E5D7362eDb8947877EE07b6b60b4d9F4B3"
    creator_contract = w3.eth.contract(address=creatorAddress,abi=interface['abi'])
    r = creator_contract.functions.deploy().call()
    r1 = creator_contract.functions.getAllContract().call()
    print(r, r1)
    f.close()
    return("New contract created at", str(r))