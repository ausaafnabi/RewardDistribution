import os
import psycopg2
import json
import logging
from collections import OrderedDict
from datetime import datetime, timedelta
import datetime
from dotenv import load_dotenv

load_dotenv()

DBNAME = os.getenv('POSTGRES_DB_NAME')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')

def post_to_db(query,row):
    try:
        conn = psycopg2.connect(dbname=DBNAME, 
                            #    user=POSTGRES_USERNAME, 
                            #    password=POSTGRES_PASSWORD, 
                               host=POSTGRES_HOST)
        cursor = conn.cursor()
        cursor.execute(query, row)
        print('Single Post Query Procesed!')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

def post_multi_to_db(query,rows):
    try:
        conn = psycopg2.connect(dbname=DBNAME, 
                            #    user=POSTGRES_USERNAME, 
                            #    password=POSTGRES_PASSWORD, 
                               host=POSTGRES_HOST)
        cursor = conn.cursor()
        for row in rows:
            cursor.execute(query, row)
        print('Multi Post Query Procesed!')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
    

def get_from_db(query):
    try:
        conn = psycopg2.connect(dbname=DBNAME, 
                            #    user=POSTGRES_USERNAME, 
                            #    password=POSTGRES_PASSWORD, 
                               host=POSTGRES_HOST)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        print('Query Procesed!')
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

def insert_logs_into_db(data): 
    logs = []
    query = """INSERT INTO rewards (transaction_hash, log_index, block_number, timestamp, aix_processed, aix_distributed, eth_bought, eth_distributed_eth) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    for log in data['results']:
        logs.append(tuple([log[field] for field in ["transactionHash", "logIndex", "blockNumber", "timeStamp", "inputAixAmount", "distributedAixAmount", "swappedEthAmount", "distributedEthAmount"]]))
    post_multi_to_db(query,logs)


def get_data_daily_report_aggregated():
    query = '''SELECT MAX(timestamp), MIN(timestamp), SUM(aix_processed), SUM(aix_distributed), SUM(eth_bought), SUM(eth_distributed_eth) FROM rewards WHERE timestamp >= NOW()::DATE - INTERVAL '1 day';'''
    result = get_from_db(query) or []
    return result


