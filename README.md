# Top Gainers Bot
A Telegram and Discord bot that fetches the top 15 cryptocurrencies by 24h percentage change from CoinMarketCap, generates bar charts (high/low/current price) and line charts (24h price trends using CoinGecko), and posts to specified channels.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `config/config.json` or `.env` with API keys and tokens.
3. Run: `python src/main.py`

## Deployment
- Local: Run `python src/main.py`.
- Heroku: Push to Heroku, set environment variables, and scale the worker.

## Notes
- Fetches all available coins from CoinMarketCap (up to 5000) and selects top 15 gainers.
- Uses CoinGecko for 24h price trend graphs.
- Expand `coingecko_id_map` in `helpers.py` if trend graphs are missing for some coins.
