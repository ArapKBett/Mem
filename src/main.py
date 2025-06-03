import schedule
import time
import logging
from src.api.coinmarketcap import CoinMarketCapAPI
from src.api.coingecko import CoinGeckoAPI
from src.bot.telegram_bot import TelegramBot
from src.bot.discord_bot import DiscordBot
from src.utils.helpers import load_config, format_coin_message, get_coingecko_id
from src.utils.graph import create_price_graph, create_trend_graph
import asyncio
import os

# Configure logging
logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def update_gainers():
    """Fetch top gainers, generate graphs, and post to Telegram and Discord."""
    config = load_config()
    cmc_api = CoinMarketCapAPI(config["coinmarketcap_api_key"])
    cg_api = CoinGeckoAPI()
    telegram_bot = TelegramBot(config["telegram_bot_token"], config["telegram_channel_id"])
    discord_bot = DiscordBot(config["discord_bot_token"], config["discord_channel_id"])

    # Fetch top gainers
    gainers = cmc_api.get_top_gainers(limit=5000)  # Fetch all available coins
    if not gainers:
        logging.error("No gainers fetched, skipping update")
        return

    # Post each gainer
    for coin in gainers:
        message = format_coin_message(coin)
        symbol = coin["symbol"]
        # Generate bar chart (high/low/current price)
        create_price_graph(coin["quote"]["USD"], coin["name"], symbol)
        # Fetch and generate 24h trend line graph
        coin_id = get_coingecko_id(symbol)
        historical_data = cg_api.get_historical_data(coin_id, days=1)
        has_trend = create_trend_graph(historical_data, coin["name"], symbol)
        
        # Post to Telegram
        telegram_bot.send_message(message, f"logs/{symbol}_price.png")
        if has_trend:
            telegram_bot.send_message("", f"logs/{symbol}_trend.png")
        
        # Post to Discord
        await discord_bot.send_message(message, f"logs/{symbol}_price.png")
        if has_trend:
            await discord_bot.send_message("", f"logs/{symbol}_trend.png")
        
        time.sleep(2)  # Avoid rate limits

def main():
    """Main function to run the bot and schedule updates."""
    config = load_config()
    telegram_bot = TelegramBot(config["telegram_bot_token"], config["telegram_channel_id"])
    discord_bot = DiscordBot(config["discord_bot_token"], config["discord_channel_id"])

    # Start Telegram bot in a separate thread
    telegram_bot.start()

    # Schedule updates every 30 minutes
    schedule.every(0.5).hours.do(lambda: asyncio.run(update_gainers()))

    # Run Discord bot and scheduler
    loop = asyncio.get_event_loop()
    loop.create_task(discord_bot.bot.start(config["discord_bot_token"]))
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
