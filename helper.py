from datetime import datetime
from web3 import Web3
import datetime as dt

def parse_hexa_amounts(hex_string):
    n = len(hex_string) // 4  # Chunk length with 4 objects encoded
    chunks = [int(hex_string[j:j + n], 16) for j in range(0, len(hex_string), n)]
    return chunks

def convert(hex_distribution):
    return round(float(Web3.from_wei(hex_distribution, 'ether')),18)

def get_results(data: list) -> dict:
    now = datetime.now
    first_tx = now() - dt.timedelta(seconds=int(data[0]['timeStamp'], 16))
    last_tx = now() - dt.timedelta(seconds=int(data[-1]['timeStamp'], 16))
    print(f'Last transaction time difference: {last_tx}')
    results = []
    for entry in data:
        hexa_distribution = entry['data'].split('x')[1]
        distribution_values = parse_hexa_amounts(hexa_distribution)
        result = {
            'transactionHash': entry['transactionHash'],
            'inputAixAmount': convert(distribution_values[0]),
            'distributedAixAmount': convert(distribution_values[1]),
            'swappedEthAmount': convert(distribution_values[2]),
            'distributedEthAmount': convert(distribution_values[3]),
            'blockNumber': int(entry['blockNumber'],16),
            'timeStamp':datetime.fromtimestamp(int(entry['timeStamp'],16)),
            'logIndex': int(entry['logIndex'],16)
        }
        results.append(result)

    return {
        'results': results,
        'first_tx': first_tx,
        'last_tx': last_tx,
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