from web3.auto import Web3
import json
import matplotlib.pylab as plt


# This file try to call the creator contract to create a new Token
f = open('address_test.json')
address = json.load(f)
f.close()
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
f = open('contract_interface/BankContract.json')
BankContractInterface = json.load(f)
f.close()
f = open('contract_interface/MetaCoin.json')
Erc20ContractInterface = json.load(f)
f.close()

bankcontractaddress = ''
erc20address = ""
n = 100000
id = 0
tokenAmount = 1000
blockn = 0
gas = {}


def deployCreatorContract():
    w3.eth.default_account = address["bank_address"]
    w3.eth.account.privateKeyToAccount(address["bank_private_key"])
    bankcontract = w3.eth.contract(
        abi=BankContractInterface['abi'], bytecode=BankContractInterface["bytecode"])
    tx_hash = bankcontract.constructor(address["bank_address"]).transact({
        "from": address["bank_address"]})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt.contractAddress)
    gas["deployCreatorContract"] = tx_receipt.gasUsed
    return tx_receipt.contractAddress

def initNewPayment():
    w3.eth.account.privateKeyToAccount(address["bank_private_key"])
    print(bankcontractaddress)
    bankcontract = w3.eth.contract(
        address=bankcontractaddress, abi=BankContractInterface['abi'])
    tx_hash = bankcontract.functions.initPaymentChannel(
        address["client_pub"], address["service_provider_pub"], 1000000, 1, blockn, id).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt.gasUsed)
    gas["initNewPayment"] = tx_receipt.gasUsed


def getERC20Address():
    bankcontract = w3.eth.contract(
        address=bankcontractaddress, abi=BankContractInterface['abi'])

    result = bankcontract.functions.getPayment(0).call()
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return(result[2])


def transfer():
    w3.eth.account.privateKeyToAccount(address["bank_private_key"])
    erc20 = w3.eth.contract(
        address=erc20address, abi=Erc20ContractInterface['abi'])
    print(erc20.functions.balanceOf(address["bank_address"]).call())
    tx = erc20.functions.transfer(address["client_pub"], n).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx)
    gas["transfer"] = tx_receipt.gasUsed


def clientAllocateBank():
    w3.eth.default_account = address["client_pub"]
    w3.eth.account.privateKeyToAccount(address["client_pk"])

    erc20 = w3.eth.contract(
        address=erc20address, abi=Erc20ContractInterface['abi'])
    tx = erc20.functions.approve(
        bankcontractaddress, tokenAmount).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx)
    gas["approve"] = tx_receipt.gasUsed


def requestservice():
    w3.eth.account.privateKeyToAccount(address["client_pk"])

    bankcontract = w3.eth.contract(
    address=bankcontractaddress, abi=BankContractInterface['abi'])

    tx_hash = bankcontract.functions.requestServiceAndEscrowTokens(id, tokenAmount).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    gas["request"] = tx_receipt.gasUsed
    print(tx_receipt)

def serviceDone():
    w3.eth.default_account = address["service_provider_pub"]

    w3.eth.account.privateKeyToAccount(address["service_provider_pk"])
    bankcontract = w3.eth.contract(
    address=bankcontractaddress, abi=BankContractInterface['abi'])
    tx_hash = bankcontract.functions.serviceDone(id).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    gas["done"] = tx_receipt.gasUsed

def pay():
    w3.eth.account.privateKeyToAccount(address["service_provider_pk"])
    bankcontract = w3.eth.contract(
    address=bankcontractaddress, abi=BankContractInterface['abi'])
    tx_hash = bankcontract.functions.pay(id).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    gas["pay"] = tx_receipt.gasUsed

def balanceofeveryone():
    w3.eth.account.privateKeyToAccount(address["bank_private_key"])
    erc20 = w3.eth.contract(
        address=erc20address, abi=Erc20ContractInterface['abi'])
    print(erc20.functions.balanceOf(address["bank_address"]).call())
    print(erc20.functions.balanceOf(address["service_provider_pub"]).call())
    print(erc20.functions.balanceOf(address["client_pub"]).call())

def closePaymentChannel():
    w3.eth.account.privateKeyToAccount(address["bank_private_key"])
    w3.eth.default_account = address["bank_address"]

    bankcontract = w3.eth.contract(
        address=bankcontractaddress, abi=BankContractInterface['abi'])
    tx_hash = bankcontract.functions.closePaymentChannel(id).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    gas["closeChannel"] = tx_receipt.gasUsed
    print("Payment Channel closed")


    



bankcontractaddress = deployCreatorContract()

for k in range(10):
    initNewPayment()
# erc20address = getERC20Address()
# transfer()
# clientAllocateBank()
# requestservice()
# serviceDone()
# balanceofeveryone()
# pay()
# balanceofeveryone()
# closePaymentChannel()
# lists = sorted(gas.items())
# x,y = zip(*lists)
# plt.plot(x,y)
# plt.show()
print(gas)
