import os
import json
import requests
import time
from dotenv import load_dotenv
import logging

from web3 import Web3
from etherscan import Etherscan

load_dotenv()

CONTRACT_ADDR = os.getenv("CONTRACT_ADDRESS")
API_KEY = os.getenv("ETHSCAN_API_TOKEN")
TOPIC = os.getenv("TOPIC")

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

w3 = Web3(Web3.HTTPProvider(f'https://api.zmok.io/mainnet/{os.getenv("API_KEY_ZMOK")}'))
contract_address = w3.to_checksum_address(CONTRACT_ADDR)
eth = Etherscan(API_KEY)

def get_balance(request: list):

    balance = eth.get_eth_balance(contract_addresses))

def get_transaction_24h():
    # Set up the parameters for the call to getTransactionCount
    period = 86400  # 24 hours in seconds
    timestamp = int(time.time())-period
    try:
        from_block = eth.get_block_number_by_timestamp(timestamp=timestamp,closest='after')
        url=f'https://api.etherscan.io/api?module=logs&action=getLogs&address={contract_address}&topic0={TOPIC}&fromBlock={from_block}&page=1&apikey={API_KEY}'
        response = requests.get(url)
        #print(response)
        resp = response.json().get('result') or []
        return resp
    except:
        logger.error('Unable to process the query from the API.')
        return []


transactions = get_transaction_24h()
for txn in transactions:
    print(f"{txn['hash']} ({txn['timeStamp']})")

def get_event_logs(txs):
    event=[]
    return event