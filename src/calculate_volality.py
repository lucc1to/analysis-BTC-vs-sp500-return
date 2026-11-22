# Volality - zienność to takie coś w finansach że określa jak bardzo nasze aktywo ma zmienną wartość
# (porównuje aktywo które rośnie codziennie o 0.5% z aktywem któ©e rośnie raz 8% a potem spada 6%).
# Zmiennosc roczna sigma_(aannual) = sigma_(daily) * sqrt(N), N - liczba dni na giełdzie(S&P500 - 252, BTC - 365)
import numpy as np
import pandas as pd

returns = pd.read_csv("data/log_returns.csv", index_col="Date", parse_dates=True)
daily_volatility = returns.std()
trading_days = {"SP500": 252, "BTC": 365}

results = {}

for asset, days in trading_days.items():
    results[asset] = daily_volatility[asset] * np.sqrt(days)

annualized_volatility = pd.Series(results)

print("\nANNUALIZED VOLATILITY")
print("=" * 40)

print("\nDaily volatility:")
print(daily_volatility)

print("\nAnnualized volatility:")
print(annualized_volatility.apply(lambda x: f"{x:.2%}"))

volatility_results = pd.DataFrame(
    {
        "Daily Volatility": daily_volatility,
        "Annualized Volatility": annualized_volatility,
    }
)

volatility_results.to_csv("data/volatility.csv")

print("\nResults saved to data/volatility.csv")
