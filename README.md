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
## Limitations

This backtest uses **price data only** — it does not simulate actual options contracts.

A few things it does not account for:

- **Expiry type** — weekly vs 1DTE contracts behave differently, especially around theta decay
- **Strike selection** — real CSP performance depends heavily on how far OTM the strike is
- **Implied volatility** — IV levels at entry significantly affect premium collected
- **Bid/ask spread** — real fills are rarely at mid price, especially in fast-moving markets
- **Assignment risk** — a sharp continued drop could result in assignment, not just a loss
- **Liquidity** — not all strikes or expiries have sufficient volume for clean execution

### What it does validate

The backtest confirms that the **underlying mean reversion edge exists** in the price action —
meaning stocks in this universe tend to recover after single-day drops of the tested magnitude.
This is the core requirement for a CSP strategy to work. Whether that edge translates 
directly to options P&L depends on the IV environment at entry and strike selection,
which requires historical options chain data to model precisely.

### On historical options data

Accurate options backtesting requires historical chain data (strikes, IV, bid/ask by expiry).
This data is available from vendors such as CBOE DataShop, OptionsDX, and Nasdaq Data Link,
but is not free. This project uses Yahoo Finance price data as a freely available alternative
to demonstrate the directional edge.
## Dylan Parkinson

Built and designed by Dylan Parkinson  
Strategy research, signal design, and AI-assisted quantitative analysis.
