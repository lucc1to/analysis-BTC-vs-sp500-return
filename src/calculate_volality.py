# Volality - zienność to takie coś w finansach że określa jak bardzo nasze aktywo ma zmienną wartość
# (porównuje aktywo które rośnie codziennie o 0.5% z aktywem któ©e rośnie raz 8% a potem spada 6%).
# Zmiennosc roczna sigma_(aannual) = sigma_(daily) * sqrt(N), N - liczba dni na giełdzie(S&P500 - 252, BTC - 365)
import numpy as np
import pandas as pd
from pathlib import Path

returns = pd.read_csv("data/log_returns.csv", index_col="Date", parse_dates=True)
periods_per_year = pd.Series({"SP500": 252, "BTC": 365})
annualization_factors = np.sqrt(periods_per_year)

daily_volatility_by_year = returns.groupby(
    returns.index.year
).std()  # grupowanie danych wedlug lat i obliczanie odchylenia standardowego dla kazdego roku (czyli zmiennosci dziennej)

annualized_volatility_by_year = daily_volatility_by_year.mul(
    annualization_factors, axis="columns"
)  # zmiennosc roczna

annualized_volatility_by_year.index.name = "Year"

daily_volatility_full_period = returns.std()

annualized_volatility_full_period = daily_volatility_full_period * annualization_factors

volatility_summary = pd.DataFrame(
    {
        "Daily Volatility": daily_volatility_full_period,
        "Annualized Volatility": annualized_volatility_full_period,
    }
)

Path("data").mkdir(exist_ok=True)
annualized_volatility_by_year.to_csv("data/volatility_by_year.csv")
volatility_summary.to_csv("data/volatility_summary.csv")

print("\nANNUALIZED VOLATILITY BY YEAR")
print("=" * 50)

print((annualized_volatility_by_year * 100).round(2).astype(str) + "%")


print("\nFULL PERIOD VOLATILITY (10 YEARS)")
print("=" * 50)

print((volatility_summary * 100).round(2).astype(str) + "%")


print("\nNUMBER OF OBSERVATIONS PER YEAR")
print("=" * 50)

print(returns.groupby(returns.index.year).count())


print("\nResults saved:")
print("- data/volatility_by_year.csv")
print("- data/volatility_summary.csv")
