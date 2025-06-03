import matplotlib.pyplot as plt
import pandas as pd
import logging

def create_price_graph(coin_data, coin_name, coin_symbol):
    """Create a bar chart for 24h high/low/current price."""
    try:
        data = {
            "Metric": ["24h High", "24h Low", "Current Price"],
            "Value": [coin_data["high_24h"], coin_data["low_24h"], coin_data["price"]]
        }
        df = pd.DataFrame(data)
        plt.figure(figsize=(8, 5))
        plt.bar(df["Metric"], df["Value"], color=["green", "red", "blue"])
        plt.title(f"{coin_name} ({coin_symbol}) - 24h Price Metrics")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        plt.savefig(f"logs/{coin_symbol}_price.png")
        plt.close()
    except Exception as e:
        logging.error(f"Error creating price graph for {coin_symbol}: {e}")

def create_trend_graph(historical_data, coin_name, coin_symbol):
    """Create a line chart for 24h price trend."""
    if historical_data is None:
        logging.warning(f"No historical data for {coin_symbol}")
        return False
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(historical_data["timestamp"], historical_data["price"], label=f"{coin_name} Price", color="blue")
        plt.title(f"{coin_name} ({coin_symbol}) - 24h Price Trend")
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"logs/{coin_symbol}_trend.png")
        plt.close()
        return True
    except Exception as e:
        logging.error(f"Error creating trend graph for {coin_symbol}: {e}")
        return False
