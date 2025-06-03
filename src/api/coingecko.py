import requests
import pandas as pd
import logging

class CoinGeckoAPI:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_historical_data(self, coin_id, days=1):
        """Fetch historical price data for a coin over the specified days."""
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": str(days), "interval": "hourly"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            prices = data.get("prices", [])
            if not prices:
                logging.warning(f"No historical data for {coin_id}")
                return None
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching CoinGecko data for {coin_id}: {e}")
            return None
