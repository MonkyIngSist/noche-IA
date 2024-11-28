import requests
from database import save_to_mongo
import config

def fetch_stock_data(symbol):
    url = f"{config.ALPHA_VANTAGE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={config.ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            return data
    return None

def collect_data(symbol):
    stock_data = fetch_stock_data(symbol)
    if stock_data:
        save_to_mongo(stock_data, symbol)
        print(f"Data for {symbol} saved to MongoDB.")
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    collect_data("AMZN")


