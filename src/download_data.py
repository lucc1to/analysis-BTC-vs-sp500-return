import yfinance as yf
import pandas as pd
from pathlib import Path

TICKERS = ["^GSPC", "BTC-USD"]
raw_data = yf.download(
    tickers=TICKERS,
    period="10y",
    interval="1d",
    group_by="ticker",
    auto_adjust=False,
    ignore_tz=True,
    progress=False,
)
prices = pd.DataFrame(
    {"SP500": raw_data["^GSPC"]["Close"], "BTC": raw_data["BTC-USD"]["Close"]}
)
prices.index = pd.to_datetime(prices.index)
prices.index.name = "Date"
prices = prices.sort_index()

print("\nClosing prices:")
print(prices.head(10))

print("\nMissing values:")
print(prices.isna().sum())

from pathlib import Path

Path("data").mkdir(exist_ok=True)
prices.to_csv("data/prices.csv")
print("\nData saved to data/prices.csv")
