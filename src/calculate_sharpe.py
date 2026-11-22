# sharpe ratio -- odpowiada co jest lepsze
# zwrot roczny 15% z roczną zmiennością 10%    czy    zwrot roczny 30% z roczną zmiennością 40%
# Sharpe = Rp-Rf / sigma_p
# gdzie Rp - zwrot portfela, Rf - stopa wolna od ryzyka, sigma_p - zmienność portfela
# My musimy zrobić Sharpe_annual = Rd-Rf,d / sigma_d * sqrt(N), gdzie Rd - zwrot dzienny, Rf,d - stopa wolna od ryzyka dzienna, sigma_d - zmienność dzienna, N - liczba dni w roku
# Rf - damy 3miesieczne obligacje Treasury bills.

import numpy as np
import pandas as pd
from pathlib import Path

prices = pd.read_csv("data/prices.csv", index_col="Date", parse_dates=True)

start_date = (prices.index.min() - pd.Timedelta(days=10)).strftime(
    "%Y-%m-%d"
)  # to jest potrzebne bo w przypadku BTC mamy 2020-01-01, a w przypadku SP500 mamy 2020-01-10, a chcemy żeby były te same daty dla obu aktywów
end_date = prices.index.max().strftime(
    "%Y-%m-%d"
)  # to jest potrzebne bo w przypadku BTC mamy 2024-01-01, a w przypadku SP500 mamy 2024-06-30, a chcemy żeby były te same daty dla obu aktywów

fred_url = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv"
    f"?id=DGS3MO&cosd={start_date}&coed={end_date}"
)

fred_data = pd.read_csv(fred_url)
fred_data["observation_date"] = pd.to_datetime(fred_data["observation_date"])

risk_free_annual = (
    pd.Series(
        pd.to_numeric(fred_data["DGS3MO"], errors="coerce").values,
        index=fred_data["observation_date"],
    )
    .dropna()
    .sort_index()
    / 100
)

if risk_free_annual.empty:
    raise RuntimeError(
        "Could not fetch risk-free rate data from FRED. Please check the URL or your internet connection."
    )


def calculate_excess_returns(asset_prices, risk_free_rates):
    asset_prices = asset_prices.dropna().sort_index()
    asset_returns = asset_prices.pct_change(
        fill_method=None
    ).dropna()  # oblcizanie stopy zwrotu
    previous_dates = asset_prices.index[:-1]
    return_dates = asset_prices.index[1:]
    elapsed_days = pd.Series((return_dates - previous_dates).days, index=return_dates)
    period_risk_free = risk_free_annual.reindex(
        previous_dates, method="ffill"
    )  # jak jakis dzien nie ma publikowane stopy to przesuwamy z ostatniej mozliwej daty czyli z piaatku na niedizele
    period_risk_free.index = return_dates
    if period_risk_free.isna().any():
        raise RuntimeError("Missing risk-free rate observations.")
    risk_free_returns = (1 + period_risk_free) ** (elapsed_days / 365) - 1
    excess_returns = asset_returns - risk_free_returns
    return asset_returns, risk_free_returns, excess_returns


assets = {
    "SP500": prices["SP500"],
    "BTC": prices["BTC"],
}

simple_returns = {}
risk_free_returns = {}
excess_returns = {}

for asset, asset_prices in assets.items():
    returns, rf_returns, excess = calculate_excess_returns(
        asset_prices, risk_free_annual
    )
    simple_returns[asset] = returns
    risk_free_returns[asset] = rf_returns
    excess_returns[asset] = excess
simple_returns = pd.DataFrame(simple_returns)
risk_free_returns = pd.DataFrame(risk_free_returns)
excess_returns = pd.DataFrame(excess_returns)

periods_per_year = pd.Series({"SP500": 252, "BTC": 365})

mean_excess_by_year = excess_returns.groupby(excess_returns.index.year).mean()

std_excess_by_year = excess_returns.groupby(excess_returns.index.year).std()

sharpe_by_year = mean_excess_by_year.div(
    std_excess_by_year
).mul(
    np.sqrt(periods_per_year), axis="columns"
)  # dzielimy srednia nadwyzke stopy zwrotu przez odchylenie standardowe nadwyzkowych zwrotow a potem to mnozymy razy sqrt(N)

sharpe_by_year.index.name = "Year"
mean_excess_full = excess_returns.mean()
std_excess_full = excess_returns.std()

sharpe_full = (mean_excess_full / std_excess_full) * np.sqrt(periods_per_year)

sharpe_summary = pd.DataFrame(
    {
        "Mean Daily Excess Return": mean_excess_full,
        "Daily Excess Volatility": std_excess_full,
        "Annualized Sharpe Ratio": sharpe_full,
    }
)

Path("data").mkdir(exist_ok=True)

simple_returns.to_csv("data/simple_returns.csv")
risk_free_returns.to_csv("data/risk_free_returns.csv")
excess_returns.to_csv("data/excess_returns.csv")

sharpe_by_year.to_csv("data/sharpe_by_year.csv")
sharpe_summary.to_csv("data/sharpe_summary.csv")


# 10. Display results
print("\nANNUALIZED SHARPE RATIO BY YEAR")
print("=" * 50)
print(sharpe_by_year.round(3))


print("\nFULL PERIOD SHARPE RATIO")
print("=" * 50)
print(sharpe_summary.round(4))


print("\nNUMBER OF OBSERVATIONS PER YEAR")
print("=" * 50)
print(excess_returns.groupby(excess_returns.index.year).count())


print("\nRESULTS SAVED:")
print("- data/simple_returns.csv")
print("- data/risk_free_returns.csv")
print("- data/excess_returns.csv")
print("- data/sharpe_by_year.csv")
print("- data/sharpe_summary.csv")
