import numpy as np
import pandas as pd
from pathlib import Path

prices = pd.read_csv("data/prices.csv", index_col="Date", parse_dates=True)
common_prices = prices.dropna(subset=["SP500", "BTC"]).dropna().sort_index()

if len(common_prices) < 2:
    raise RuntimeError(
        "Not enough common dates between SP500 and BTC for correlation calculation."
    )

log_returns = np.log(common_prices / common_prices.shift(1)).dropna()

if len(log_returns) < 2:
    raise RuntimeError(
        "Not enough data points after calculating log returns for correlation calculation."
    )

correlation_matrix = log_returns.corr(method="pearson")
full_period_correlation = correlation_matrix.loc["SP500", "BTC"]

yearly_results = []
for year, yearly_returns in log_returns.groupby(log_returns.index.year):
    correlation = yearly_returns["SP500"].corr(yearly_returns["BTC"], method="pearson")
    observations = len(yearly_returns)
    yearly_results.append(
        {
            "Year": year,
            "Pearson Correlation": correlation,
            "Observations": observations,
        }
    )

correlation_by_year = pd.DataFrame(yearly_results).set_index("Year")

rolling_correlation = log_returns["SP500"].rolling(window=90).corr(log_returns["BTC"])

rolling_correlation.name = "Rolling Correlation (90 observations)"


correlation_summary = pd.DataFrame(
    {
        "Pearson Correlation": [full_period_correlation],
        "Observations": [len(log_returns)],
        "Start Date": [log_returns.index.min()],
        "End Date": [log_returns.index.max()],
    },
    index=["Full Period"],
)

Path("data").mkdir(exist_ok=True)

log_returns.to_csv("data/correlation_returns.csv")

correlation_matrix.to_csv("data/correlation_matrix.csv")

correlation_by_year.to_csv("data/correlation_by_year.csv")

rolling_correlation.to_csv("data/rolling_correlation_90d.csv")

correlation_summary.to_csv("data/correlation_summary.csv")

print("\nFULL PERIOD CORRELATION MATRIX")
print("=" * 50)
print(correlation_matrix.round(4))


print("\nFULL PERIOD PEARSON CORRELATION")
print("=" * 50)
print(round(full_period_correlation, 4))


print("\nYEARLY PEARSON CORRELATION")
print("=" * 50)
print(correlation_by_year.round(4))


print("\nROLLING CORRELATION - LAST 10 OBSERVATIONS")
print("=" * 50)
print(rolling_correlation.tail(10).round(4))


print("\nRESULTS SAVED:")
print("- data/correlation_returns.csv")
print("- data/correlation_matrix.csv")
print("- data/correlation_by_year.csv")
print("- data/rolling_correlation_90d.csv")
print("- data/correlation_summary.csv")
