import numpy as np
import pandas as pd

prices = pd.read_csv("data/prices.csv", index_col="Date", parse_dates=True)

sp500_prices = prices["SP500"].dropna()
btc_prices = prices["BTC"].dropna()

log_returns = pd.DataFrame(
    {
        "SP500": np.log(sp500_prices / sp500_prices.shift(1)),
        "BTC": np.log(btc_prices / btc_prices.shift(1)),
    }
)

log_returns.index.name = "Date"
log_returns.to_csv("data/log_returns.csv")

# 6. Display results
print("\nLOGARITHMIC RETURNS")
print("=" * 40)

print("\nFirst 10 observations:")
print(log_returns.head(10))

print("\nNumber of observations:")
print(log_returns.count())

print("\nMissing values:")
print(log_returns.isna().sum())

print("\nData saved to data/log_returns.csv")
