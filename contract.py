import os
import json
import requests
import time
from dotenv import load_dotenv
import logging

import web3
from web3 import Web3
from etherscan import Etherscan

from helper import get_results, build_report

load_dotenv()

CONTRACT_ADDR = os.getenv("CONTRACT_ADDRESS")
API_KEY = os.getenv("ETHSCAN_API_TOKEN")
TOPIC = os.getenv("TOPIC")
DISTRIBUTOR_ACCOUNT= os.getenv("DISTRIBUTOR_ACCOUNT")

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

w3 = Web3(Web3.HTTPProvider(f'https://api.zmok.io/mainnet/{os.getenv("API_KEY_ZMOK")}'))
contract_address = w3.to_checksum_address(CONTRACT_ADDR)
eth = Etherscan(API_KEY)

def get_balance(request: list):
    account_list = set()
    data=[]
    for i in request:
        txHash = i['transactionHash']
        receipt = eth.get_proxy_transaction_receipt(txHash)
        account_list.add(receipt['from'])
        data.append(receipt)
        time.sleep(0.2)
    results=data
    if len(account_list)==1:
        balance = eth.get_eth_balance(account_list.pop())
        balances = Web3.from_wei(int(balance), 'ether') 
    else:
        balances = eth.get_eth_balance_multiple(list(account_list))
        #To implement in case of multiple users (confirmation needed.)

    return balances

def get_balance_distributor():
    distributor_account = DISTRIBUTOR_ACCOUNT
    balance = eth.get_eth_balance(distributor_account)
    balances = Web3.from_wei(int(balance), 'ether') 
    return balances

def get_transactions(contract_address):
    txs = []
    start_block = eth.get_block_number_by_timestamp(timestamp="1578638524", closest="before")
    return txs

def get_transaction_24h():
    # Set up the parameters for the call to getTransactionCount
    period = 86400  # 24 hours in seconds
    timestamp = int(time.time())-period
    
    from_block = eth.get_block_number_by_timestamp(timestamp=timestamp,closest='after')
    try:
        url=f'https://api.etherscan.io/api?module=logs&action=getLogs&address={contract_address}&topic0={TOPIC}&fromBlock={from_block}&page=1&apikey={API_KEY}'
        response = requests.get(url)
        #print(response)
        resp = response.json().get('result') or []
        return resp
    except:
        logger.error('Unable to process the query from the API.')
        return []

def generate_report():
    data= get_transaction_24h()
    processed_data=get_results(data)
    #distributors_balance = get_balance(processed_data['results'])
    distributors_balance = get_balance_distributor()
    processed_data['distributors_balance'] = distributors_balance
    processed_data['distributors_account'] = DISTRIBUTOR_ACCOUNT
    return build_report(processed_data)

#transactions = get_transaction_24h()
print(generate_report())