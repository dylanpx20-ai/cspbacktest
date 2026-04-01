# CSP Mean Reversion Backtest

A Python backtest for a **Cash Secured Put (CSP)** options strategy on high-volatility large-cap stocks.

The core thesis: when a stock drops sharply in a single session, implied volatility spikes,
inflating put premiums. Selling puts into that fear premium — and closing early once the 
position recovers — captures the IV crush and mean reversion in combination.

---

## Strategy Logic

- **Signal:** Stock drops X% in a single trading day
- **Entry:** Sell a cash secured put at end of day (power hour)
- **Strike:** Estimated $3–5 below close price (buffer zone)
- **Exit:** Close position when estimated P&L hits 50% of max profit, or after 14 days
- **Tickers tested:** TSLA, NVDA

---

## Drop Thresholds Tested

| Range  | Description              |
|--------|--------------------------|
| 1–2%   | Minor pullback           |
| 2–3%   | Moderate dip             |
| 3–5%   | Significant single-day drop |
| 5–8%   | High-volatility event    |

---

## How P&L Is Estimated

Since this backtest uses price data (not live options chains), P&L is estimated as:
```
price_recovery = (exit_price - entry_price) / entry_price
estimated_pnl  = price_recovery / abs(drop_pct)
```

This approximates how much of the drop was recovered relative to the size of the drop —
a proxy for how much of the sold put premium would have decayed.

---

## Requirements
```
yfinance
pandas
numpy
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Usage
```bash
python backtest.py
```

Results print to console and save to `/results/` as CSV files.

---

## Output Columns

| Column        | Meaning                                      |
|---------------|----------------------------------------------|
| Ticker        | Stock symbol                                 |
| Drop Range    | Signal threshold that triggered entry        |
| Trades        | Total trades in sample                       |
| Win Rate %    | % of trades that were profitable             |
| Avg Days Held | Average days to exit                         |
| Target Hit %  | % of trades that hit 50% profit target early |
| Avg PnL %     | Average estimated P&L per trade              |

---

## Disclaimer

This is a backtesting framework for educational and research purposes only.
It does not constitute financial advice. Past backtest results do not guarantee
future performance. Options trading involves substantial risk of loss.

---

## Dylan Parkinson

Built and designed by [Your Name]  
Strategy research, signal design, and AI-assisted quantitative analysis.
