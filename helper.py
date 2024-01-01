from datetime import datetime
from web3 import Web3

def get_results(data: list)->dict:

    first_tx=datetime.fromtimestamp(int(data[0]['timeStamp'],16))
    last_tx=datetime.fromtimestamp(int(data[-1]['timeStamp'],16))
    diff1 = datetime.now()-first_tx
    diff2 = datetime.now()-last_tx
    print(str(diff2))
    res=[]
    for i in data:
        aix_eth_distibution=i['data'].split('x')[1]
        n = len(aix_eth_distibution)//4 # chunk length
        chunks = [int(aix_eth_distibution[j:j+n],16) for j in range(0, len(aix_eth_distibution), n)]
        report = {  'transactionHash' : i['transactionHash'],
                    'inputAixAmount' : round(float(Web3.from_wei(chunks[0], 'ether')),18),
                    'distributedAixAmount' : round(float(Web3.from_wei(chunks[1], 'ether')),18),
                    'swappedEthAmount' : round(float(Web3.from_wei(chunks[2], 'ether')),18),
                    'distributedEthAmount' : round(float(Web3.from_wei(chunks[3], 'ether')),18),
                    'blockNumber': int(i['blockNumber'],16),
                    'timeStamp':datetime.fromtimestamp(int(i['timeStamp'],16)),
                    'logIndex': int(i['logIndex'],16)
                }
        res.append(report)

    return {'results':res,                    
            'first_tx': diff1,
            'last_tx': diff2
        }

def build_report(stats):
    
    report = f"📊 Daily $AIX Stats:\n\n" \
             f"- First TX: {str(stats['first_tx'])} Ago\n" \
             f"- Last TX: {str(stats['last_tx'])} Ago\n\n" \
             f"- AIX processed: {stats['results'][-1]['inputAixAmount']:,.2f}\n" \
             f"- AIX distributed: {stats['results'][-1]['distributedAixAmount']:,.2f}\n" \
             f"- ETH bought: {stats['results'][-1]['swappedEthAmount'] :,.4f}\n" \
             f"- ETH distributed: {stats['results'][-1]['distributedEthAmount'] :,.4f}\n\n" \
             f"👛 Distributor wallet: {stats['distributors_account']}\n" \
             f"💠 Distributor balance: {stats['distributors_balance']} ETH\n\n"
    return report