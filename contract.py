import os
import json
import requests


from web3 import Web3
#from etherscan import EtherscanProvider

provider = ''
w3 = Web3(Web3.HTTPProvider())
#w3 = Web3(provider=provider)
contract_address = w3.to_checksum_address('0xaBe235136562a5C2B02557E1caE7E8c85F2a5DA0')
CONTRACT_ADDR = os.getenv("CONTRACT_ADDRESS")
API_KEY = os.getenv("ETHSCAN_API_TOKEN")

def get_contract_abi(): 
    #url = f"https://api.etherscan.io/api"
    #response = requests.get(url, params={'module':'contract','action':'getabi','address':CONTRACT_ADDR,'apikey':API_KEY}).json()
    url = f'https://api.etherscan.io/api?module=contract&action=getabi&address=0xaBe235136562a5C2B02557E1caE7E8c85F2a5DA0'
    response = requests.get(url).json()
    #print(response)
    abi = response.get('result') or []
    return abi

abi=get_contract_abi()

contract = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)

def get_contract_events(startblock, endblock): 
    #First get txIDs for last 24 hours

    #then for every ID request and get last element 
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x0dfd460ff10de202be107c804137c0c0d36ada2b5dc687ff001885a2330c33c6"
    response = requests.get(url).json()
    logs = response.get('result') or []
    #Accumulate the logs for the transactions
    return logs

def parse_total_distribution_logs(logs):
    total_dict = {
        'processed': {'value': 0},
        'distributed': {'value': 0},
        'bought': {'value': 0},
        'distributed_eth': {'value': 0}
    }

    #parsing logic

    return total_dict

def get_events():
    start_block = ... # start block time
    end_block = int(time.time() / 15) * 15 + 60*15 - 24*60*60
    event_filter = get_all_entries() #some function to get IDs
    logs = get_contract_events(event_filter)
    return logs

print(w3, contract_address)
print(contract.events.TotalDistribution())
if __name__ == '_main__':
    #logs=getevents() 
    #print(logs)
    print(w3, contract_address)