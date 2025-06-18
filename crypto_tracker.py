# crypto_tracker.py

import requests
import pandas as pd
from datetime import datetime
import os


def fetch_price(crypto_id='bitcoin', currency='usd'):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}"
    response = requests.get(url)
    data = response.json()
    price = data[crypto_id][currency]
    return price, datetime.now()


def log_price_to_csv(price, timestamp, filename='prices.csv'):
    new_data = pd.DataFrame([[timestamp, price]], columns=['Timestamp', 'Price'])

    if os.path.exists(filename):
        new_data.to_csv(filename, mode='a', header=False, index=False)
    else:
        new_data.to_csv(filename, index=False)


# Run and log
if __name__ == "__main__":
    price, time = fetch_price()
    log_price_to_csv(price, time)
    print(f"Logged Bitcoin Price: ${price} at {time}")
