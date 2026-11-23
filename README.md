# S&P 500 vs Bitcoin

Krótka analiza historyczna **S&P 500 (`^GSPC`)** i **Bitcoina (`BTC-USD`)** na podstawie dziennych danych w USD.

## Co analizujemy?

- logarytmiczne stopy zwrotu i roczną zmienność,
- Sharpe Ratio z rentownością 3-miesięcznych bonów USA (FRED `DGS3MO`) jako przybliżeniem stopy wolnej od ryzyka,
- Maximum Drawdown,
- korelację Pearsona i korelację kroczącą,
- porównanie wartości początkowych 100 USD.

## Uruchomienie

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/download_data.py
python src/calculate_returns.py
python src/calculate_volatility.py
python src/calculate_sharpe.py
python src/calculate_drawdown.py
python src/calculate_correlation.py
```

Następnie otwórz `notebooks/analysis.ipynb` w VS Code lub Jupyterze i wybierz kernel `.venv`. Notebook tworzy wykresy PNG w katalogu `charts/`.

## Struktura

```text
├── data/               # dane i wyniki CSV
├── src/                # pobieranie danych i obliczenia
├── notebooks/
│   └── analysis.ipynb  # wykresy i interpretacja
├── charts/             # wykresy PNG
├── requirements.txt
└── README.md
```

**Uwaga:** `^GSPC` nie uwzględnia dywidend. `DGS3MO` jest przybliżeniem stopy wolnej od ryzyka. To projekt edukacyjny, nie rekomendacja inwestycyjna.
