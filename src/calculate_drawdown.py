# bierzemy maksimum lokalne i liczymy do minimum lokalnego i liczymy spadek w procentach, potem bierzemy maksimum z tych spadków

import pandas as pd
from pathlib import Path

prices = pd.read_csv("data/prices.csv", index_col="Date", parse_dates=True)


def calculate_drawdown(asset_prices):
    asset_prices = asset_prices.dropna().sort_index()
    running_max = asset_prices.cummax()
    drawdown = asset_prices / running_max - 1
    max_drawdown = drawdown.min()
    trough_date = drawdown.idxmin()
    peak_date = asset_prices.loc[:trough_date].idxmax()
    peak_price = asset_prices.loc[peak_date]
    trough_price = asset_prices.loc[trough_date]
    recovery_prices = asset_prices.loc[trough_date:]
    recovery_prices = recovery_prices[recovery_prices >= peak_price]
    if not recovery_prices.empty:
        recovery_date = recovery_prices.index[0]
    else:
        recovery_date = pd.NaT
    summary = {
        "Max Drawdown": max_drawdown,
        "Peak Date": peak_date,
        "Trough Date": trough_date,
        "Recovery Date": recovery_date,
        "Peak Price": peak_price,
        "Trough Price": trough_price,
    }
    return drawdown, summary


drawdowns = {}
summary_results = []

for asset in prices.columns:
    drawdown, summary = calculate_drawdown(prices[asset])
    drawdowns[asset] = drawdown
    summary_results.append({"Asset": asset, **summary})

drawdown_series = pd.DataFrame(drawdowns)
max_drawdown_summary = pd.DataFrame(summary_results).set_index("Asset")

annual_drawdowns = {}

for asset in prices.columns:
    asset_prices = prices[asset].dropna()
    yearly_results = {}
    for year, yearly_prcies in asset_prices.groupby(asset_prices.index.year):
        runing_max = yearly_prcies.cummax()
        yearly_drawdown = yearly_prcies / runing_max - 1
        yearly_results[year] = yearly_drawdown.min()
    annual_drawdowns[asset] = pd.Series(yearly_results)
max_drawdown_by_year = pd.DataFrame(annual_drawdowns)
max_drawdown_by_year.index.name = "Year"

Path("data").mkdir(exist_ok=True)

drawdown_series.to_csv("data/drawdown_series.csv")

max_drawdown_summary.to_csv("data/max_drawdown_summary.csv")

max_drawdown_by_year.to_csv("data/max_drawdown_by_year.csv")


print("\Max DRAWDOWN - FULL PERIOD")
print("=" * 50)

summary_display = max_drawdown_summary.copy()

summary_display["Max Drawdown"] = (summary_display["Max Drawdown"] * 100).map(
    lambda x: f"{x:.2f}%"
)

print(summary_display)


print("\Max DRAWDOWN BY YEAR")
print("=" * 50)

print((max_drawdown_by_year * 100).round(2).astype(str) + "%")


print("\nRESULTS SAVED:")
print("- data/drawdown_series.csv")
print("- data/max_drawdown_summary.csv")
print("- data/max_drawdown_by_year.csv")
