Cryptocurrency Telegram Bot
This bot is a Python application that allows users to query cryptocurrency prices and track their portfolios via Telegram.

Features
Price Query
Show the current price of a specified cryptocurrency using the /price [crypto_code] command (e.g., /price btc)

Query multiple cryptocurrencies at once (e.g., /price btc eth)

List the top 10 cryptocurrencies using the /top command

Show a list of popular cryptocurrencies using the /list command

Managing Favorite Cryptocurrencies
Add cryptocurrencies to favorites using the /add [crypto_code] command (e.g., /add sol)

View your favorite cryptocurrencies with the /favorites command

Remove a cryptocurrency from favorites using the /remove [crypto_code] command (e.g., /remove sol)

Portfolio Tracking
View your portfolio using the /portfolio command

Add a transaction to your portfolio using the /add_transaction [crypto_code] [transaction_type] [amount] [price] [date] [fee] command

View portfolio performance and profit/loss with the /performance command

List all transactions using the /list_transactions command

Delete a specific transaction with the /delete_transaction [crypto_code] [transaction_id] command

Technical Requirements
Python 3.7+

python-telegram-bot library

CoinGecko API for cryptocurrency data

Planning
Project Structure Setup

Create necessary directories and files

Set up requirements.txt

Bot Core Setup

Connect to Telegram API

Define command handlers

CoinGecko API Integration

Fetch cryptocurrency data

Process and present the data

Implement Commands

Implement /price command

Implement /top command

Implement /add, /remove, and /favorites commands

Implement portfolio tracking commands

Error handling

Testing and Debugging

Test different scenarios

Debug and fix issues

Installation
Clone the repository:

bash
Kopyala
Düzenle
git clone https://github.com/username/telegrambot.git
cd telegrambot
Create a virtual environment and install dependencies:

bash
Kopyala
Düzenle
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Create a .env file and add your Telegram Bot Token:

ini
Kopyala
Düzenle
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
Run the bot:

nginx
Kopyala
Düzenle
python bot.py
How to Use the Bot
Basic Commands
/start - Starts the bot and provides usage information

/help - Displays help information about commands

Price Commands
/price btc - Shows the current price of Bitcoin

/price btc eth - Shows prices for the specified cryptocurrencies

/top - Lists the top 10 cryptocurrencies

/list - Displays a list of popular cryptocurrencies

Favorite Commands
/add sol - Adds Solana to favorites

/favorites - Lists your favorite cryptocurrencies

/remove sol - Removes Solana from favorites

Portfolio Commands
/portfolio - Displays your portfolio

/add_transaction btc buy 0.05 35000 2023-11-20 10 - Adds a Bitcoin purchase transaction

Format: /add_transaction [crypto_code] [buy/sell] [amount] [price] [date] [fee]

Date and fee are optional

/performance - Shows portfolio performance and profit/loss

/list_transactions - Lists all transactions

/delete_transaction btc 1 - Deletes transaction #1 for Bitcoin

Supported Cryptocurrencies
The bot recognizes the following common cryptocurrency abbreviations:

btc - Bitcoin

eth - Ethereum

sol - Solana

doge - Dogecoin

xrp - Ripple

ada - Cardano

dot - Polkadot

ltc - Litecoin

Contact
If you have any questions or suggestions, please open an issue on GitHub.
