import json
import logging
from dotenv import load_dotenv
import os

def load_config():
    """Load configuration from config.json or environment variables."""
    load_dotenv()
    try:
        with open("config/config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "coinmarketcap_api_key": os.getenv("COINMARKETCAP_API_KEY"),
            "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
            "discord_bot_token": os.getenv("DISCORD_BOT_TOKEN"),
            "telegram_channel_id": os.getenv("TELEGRAM_CHANNEL_ID"),
            "discord_channel_id": os.getenv("DISCORD_CHANNEL_ID")
        }
    if not all(config.values()):
        logging.error("Missing configuration values")
        raise ValueError("Configuration incomplete")
    return config

def format_coin_message(coin):
    """Format coin data into a message."""
    usd = coin["quote"]["USD"]
    return (
        f"**{coin['name']} ({coin['symbol']})**\n"
        f"Price: ${usd['price']:.4f}\n"
        f"24h Change: {usd['percent_change_24h']:.2f}%\n"
        f"24h High: ${usd['high_24h']:.4f}\n"
        f"24h Low: ${usd['low_24h']:.4f}\n"
        f"24h Volume: ${usd['volume_24h']:,.2f}\n"
        f"Market Cap: ${usd['market_cap']:,.2f}\n"
        f"Warning: Cryptocurrencies are volatile. Do your own research!\n"
    )

def get_coingecko_id(symbol):
    """Map CoinMarketCap symbol to CoinGecko ID."""
    coingecko_id_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "XRP": "ripple",
        "ADA": "cardano",
        "SOL": "solana",
        "DOGE": "dogecoin",
        "SHIB": "shiba-inu",
        "PEPE": "pepe",
        "USDT": "tether",
        "USDC": "usd-coin",
        "BUSD": "binance-usd",
        "DAI": "dai",
        "MATIC": "polygon",
        "DOT": "polkadot"
    }
    return coingecko_id_map.get(symbol, symbol.lower())  # Fallback to lowercase symbol
