# Backtest Results

Full output from `backtest.py` — run on TSLA and NVDA from 2019 to present.

Exit rule: 50% profit target or 14-day time stop.

---

## Summary Table

| Ticker | Drop Range | Trades | Win Rate % | Avg Days Held | Target Hit % | Avg PnL % |
|--------|------------|--------|------------|---------------|--------------|-----------|
| TSLA   | 1-2%       | 182    | 81.9%      | 4.9           | 81.3%        | 47.11%    |
| TSLA   | 2-3%       | 135    | 81.5%      | 5.4           | 80.0%        | 0.77%     |
| TSLA   | 3-5%       | 175    | 76.0%      | 5.9           | 75.4%        | -3.40%    |
| TSLA   | 5-8%       | 86     | 75.6%      | 6.3           | 73.3%        | 12.89%    |
| NVDA   | 1-2%       | 202    | 85.6%      | 4.5           | 85.1%        | 107.61%   |
| NVDA   | 2-3%       | 127    | 81.9%      | 4.7           | 81.9%        | 33.71%    |
| NVDA   | 3-5%       | 152    | 84.9%      | 4.8           | 84.2%        | 45.28%    |
| NVDA   | 5-8%       | 68     | 79.4%      | 5.7           | 76.5%        | 34.39%    |

---

## Key Findings

**NVDA** showed the most consistent edge across all drop thresholds — win rates between
79–86% with positive average PnL at every level tested.

**TSLA** performed strongly at the 1-2% and 2-3% thresholds but showed a slightly negative
average PnL at the 3-5% range, suggesting mean reversion is less reliable after larger drops.

Both tickers hit the 50% profit target early on **75–85% of all trades**, averaging
4-6 days to exit. This supports the thesis that IV crush and mean reversion combine
to decay put premiums faster than time alone.

---

## Notes

- Results are estimated using price recovery as a proxy for options P&L
- Does not account for IV at entry, strike selection, or bid/ask spread
- Average PnL % is sensitive to outlier recovery events, particularly at smaller drop thresholds where large rebounds can disproportionately skew results.
As a result, win rate provides a more stable indicator of signal consistency, while Avg PnL should be interpreted with caution.
- See `README.md` for full methodology and limitations
```

---
