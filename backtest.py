"""
CSP Mean Reversion Backtest
----------------------------
Backtests a cash secured put strategy on large-cap stocks.
Signal: single-day price drop within a defined threshold.
Exit: 50% profit target or 14-day time stop.

Author: [Your Name]
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os

# ── Configuration ────────────────────────────────────────────────────────────

TICKERS = ['TSLA', 'NVDA']
HOLD_DAYS = 14
PROFIT_TARGET = 0.50  # Close at 50% of estimated max profit

THRESHOLDS = [
    (-0.01, -0.02),
    (-0.02, -0.03),
    (-0.03, -0.05),
    (-0.05, -0.08),
]
THRESHOLD_LABELS = ['1-2%', '2-3%', '3-5%', '5-8%']

START_DATE = "2019-01-01"
OUTPUT_DIR = "results"

# ── Core Backtest ─────────────────────────────────────────────────────────────

def run_backtest(ticker: str, df: pd.DataFrame) -> list:
    """
    Run the CSP backtest for a single ticker across all drop thresholds.
    Returns a list of result dicts.
    """
    results = []
    df = df.copy()
    df['daily_return'] = df['Close'].pct_change()

    for (lower, upper), label in zip(THRESHOLDS, THRESHOLD_LABELS):

        # Signal: drop falls within this threshold band
        df['signal'] = (
            (df['daily_return'] <= lower) &
            (df['daily_return'] > upper)
        )

        trades = []
        entry_dates = df[df['signal']].index

        for entry in entry_dates:
            try:
                entry_price = float(df.loc[entry, 'Close'].iloc[0])
                drop_pct = float(df.loc[entry, 'daily_return'].iloc[0])

                # Get the next HOLD_DAYS rows after entry
                future = df.loc[entry:].iloc[1:HOLD_DAYS + 1]
                if len(future) < 3:
                    continue

                exit_day = None
                exit_reason = None
                estimated_pnl_pct = None

                # Walk forward — check each day for profit target
                for i, (date, row) in enumerate(future.iterrows()):
                    current_price = float(row['Close'].iloc[0])
                    price_recovery = (current_price - entry_price) / entry_price
                    estimated_pnl_pct = price_recovery / abs(drop_pct)

                    if estimated_pnl_pct >= PROFIT_TARGET:
                        exit_day = i + 1
                        exit_reason = f'Target hit day {i + 1}'
                        break

                # Time stop — exit at end of hold window
                if exit_day is None:
                    exit_day = len(future)
                    current_price = float(future['Close'].iloc[-1].iloc[0])
                    price_recovery = (current_price - entry_price) / entry_price
                    estimated_pnl_pct = price_recovery / abs(drop_pct)
                    exit_reason = 'Time exit'

                trades.append({
                    'entry_date': entry.date(),
                    'drop_pct': round(drop_pct * 100, 2),
                    'exit_day': exit_day,
                    'exit_reason': exit_reason,
                    'pnl': round(estimated_pnl_pct * 100, 2),
                    'win': estimated_pnl_pct > 0,
                })

            except Exception:
                continue

        if not trades:
            continue

        df_trades = pd.DataFrame(trades)

        results.append({
            'Ticker': ticker,
            'Drop Range': label,
            'Trades': len(df_trades),
            'Win Rate %': round(df_trades['win'].mean() * 100, 1),
            'Avg Days Held': round(df_trades['exit_day'].mean(), 1),
            'Target Hit %': round(
                df_trades['exit_reason'].str.contains('Target').mean() * 100, 1
            ),
            'Avg PnL %': round(df_trades['pnl'].mean(), 2),
            'Best Trade %': df_trades['pnl'].max(),
            'Worst Trade %': df_trades['pnl'].min(),
        })

        # Save per-ticker per-threshold trade log
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        safe_label = label.replace('-', '_')
        df_trades.to_csv(
            f"{OUTPUT_DIR}/{ticker}_{safe_label}_trades.csv", index=False
        )

    return results


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    all_results = []

    for ticker in TICKERS:
        print(f"Downloading data for {ticker}...")
        df = yf.download(
            ticker,
            start=START_DATE,
            progress=False,
            auto_adjust=True
        )
        df = df[['Open', 'Close', 'High', 'Low']].copy()

        ticker_results = run_backtest(ticker, df)
        all_results.extend(ticker_results)

    summary = pd.DataFrame(all_results)

    print("\n── Backtest Results ──────────────────────────────────────────")
    print(summary.to_string(index=False))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    summary.to_csv(f"{OUTPUT_DIR}/summary.csv", index=False)
    print(f"\nResults saved to /{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
```

---

# 📄 requirements.txt
```
yfinance>=0.2.0
pandas>=1.5.0
numpy>=1.23.0
