import requests
import logging
from time import sleep

# Configure logging
logging.basicConfig(filename='logs/bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CoinMarketCapAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency"

    def get_top_gainers(self, limit=5000):  # Large limit to fetch all available coins
        """Fetch all coins and return top 15 by 24h percentage change."""
        url = f"{self.base_url}/listings/latest"
        headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": self.api_key}
        params = {
            "start": "1",
            "limit": str(limit),  # Fetch up to 5000 coins (free tier max)
            "convert": "USD",
            "sort": "percent_change_24h",
            "sort_dir": "desc"
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("status", {}).get("error_code") != 0:
                logging.error(f"API error: {data.get('status', {}).get('error_message')}")
                return []
            return data["data"][:15]  # Return top 15 gainers
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching CoinMarketCap data: {e}")
            sleep(60)  # Wait before retrying
            return []
