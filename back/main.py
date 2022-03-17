from lib2to3.pgen2.token import AMPER
from flask import Flask
from flask import request
import random

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
