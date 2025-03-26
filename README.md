# 🚀 Cryptocurrency Telegram Bot

Advanced cryptocurrency tracking and portfolio management Telegram bot.

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Cryptocurrencies](#supported-cryptocurrencies)
- [Contributing](#contributing)
- [Contact](#contact)

## ✨ Features

### 💹 Price Queries
- View real-time prices with `/price [crypto_code]`
  ```
  Example: /price btc
  ```
- Multiple cryptocurrency queries
  ```
  Example: /price btc eth sol
  ```
- List top 10 cryptocurrencies with `/top` command
- View popular cryptocurrencies with `/list` command

### ⭐ Favorites Management
- Add to favorites with `/add [crypto_code]`
- View favorite list with `/favorites`
- Remove from favorites with `/remove [crypto_code]`

### 📊 Portfolio Tracking
- View portfolio with `/portfolio`
- Add transactions with `/add_transaction`
  ```
  Format: /add_transaction [crypto_code] [buy/sell] [amount] [price] [date] [fee]
  Example: /add_transaction btc buy 0.05 35000 2023-11-20 10
  ```
- Profit/loss analysis with `/performance`
- Transaction history with `/list_transactions`
- Delete transactions with `/delete_transaction`

## 🛠️ Requirements

- Python 3.7+
- python-telegram-bot
- pycoingecko
- python-dotenv
- requests

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/username/telegrambot.git
cd telegrambot
```

2. Create virtual environment:
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

5. Run the bot:
```bash
python bot.py
```

## 📱 Usage

### 🔰 Basic Commands
| Command | Description |
|---------|-------------|
| `/start` | Starts the bot and shows usage information |
| `/help` | Shows detailed description of all commands |

### 💰 Price Commands
| Command | Description |
|---------|-------------|
| `/price btc` | Shows Bitcoin price |
| `/price btc eth` | Shows prices for specified cryptocurrencies |
| `/top` | Lists top 10 cryptocurrencies |
| `/list` | Lists popular cryptocurrencies |

### ⭐ Favorite Commands
| Command | Description |
|---------|-------------|
| `/add sol` | Adds Solana to favorites |
| `/favorites` | Lists favorite cryptocurrencies |
| `/remove sol` | Removes Solana from favorites |

### 📈 Portfolio Commands
| Command | Description |
|---------|-------------|
| `/portfolio` | Shows portfolio status |
| `/add_transaction` | Adds new transaction |
| `/performance` | Shows portfolio performance |
| `/list_transactions` | Lists all transactions |
| `/delete_transaction` | Deletes transaction |

## 🪙 Supported Cryptocurrencies

| Symbol | Cryptocurrency |
|--------|---------------|
| BTC | Bitcoin |
| ETH | Ethereum |
| SOL | Solana |
| DOGE | Dogecoin |
| XRP | Ripple |
| ADA | Cardano |
| DOT | Polkadot |
| LTC | Litecoin |
| BNB | Binance Coin |
| USDT | Tether |
| USDC | USD Coin |
| MATIC | Polygon |
| LINK | Chainlink |
| UNI | Uniswap |
| AVAX | Avalanche |


## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---
⭐ Don't forget to star this project if you found it useful!
