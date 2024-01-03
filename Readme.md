# Telegram Reward Distribution Bot
## Overview
This project contains the development of a Telegram bot designed to monitor our reward distribution process and send daily statistics to our designated Telegram group.

## Installation and Configuration
Follow these steps to set up and configure the bot locally:

- Clone the Repository
```
git clone https://github.com/ausaafnabi/RewardDistribution.git
cd RewardDistribution
```

- Set Up Your Environment Variables

Create a .env file in the root directory and add the following variables:
```
BOT_TOKEN=<bot_token>
POSTGRES_USERNAME=<postgres_username>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_HOST=<postgres_host>
POSTGRES_PORT=<postgres_port>
POSTGRES_DB_NAME=<postgres_db_name>
CONTRACT_ADDRESS=<contract_address>
DISTRIBUTOR_ACCOUNT=<distributor_account>
ETHSCAN_API_TOKEN=<etherscan_api_token>
TOPIC=<topic_hash>

```
Get your Telegram Bot Token from BotFather and replace YOUR_TELEGRAM_BOT_TOKEN. 

- Create a Virtual Environment and Activate It
```
python3 -m venv env
source env/bin/activate  # On Windows, run `.\env\Scripts\activate`
```

- Install Required Packages
```
pip install -r requirements.txt
```


- Run the Application
```
python3 main.py
```
Usage
After completing the installation and setup, start receiving daily updates about reward distribution statistics in your chat. 

Tests
No tests have been included yet. Feel free to contribute test cases and improve overall code coverage. Make sure to write clear and comprehensive unit tests while adhering to best practices. Use tools like pytest and unittest to structure and execute them efficiently.