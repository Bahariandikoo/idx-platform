# 📈 IDX Stonks Platform

Personal trading dashboard for Indonesian stocks (Bursa Efek Indonesia).

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard
```bash
streamlit run dashboard/app.py
```

Then open your browser at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
idx-trading-platform/
├── data/
│   └── fetcher.py          # Fetch IDX data via yfinance (.JK)
├── indicators/
│   └── indicators.py       # RSI, MACD, EMA, BB, VWAP, custom momentum score
├── backtester/
│   └── engine.py           # Backtest engine + 3 built-in strategies
├── screener/
│   └── screener.py         # Filter IDX stocks by technical criteria
├── dashboard/
│   └── app.py              # 🌟 Main Streamlit web app
└── requirements.txt
```

---

## ✨ Features

### 📊 Chart & Indicators
- Interactive candlestick chart with Plotly
- Toggle: EMA 20/50, SMA 200, Bollinger Bands, VWAP
- RSI, MACD subplots
- Signal summary panel (Bullish/Bearish/Neutral)

### ⚙️ Backtesting
- 3 built-in strategies: RSI, MACD Crossover, EMA Crossover
- Adjustable parameters per strategy
- Equity curve visualization
- Full trade log with P&L

### 🔍 Screener
- Scan all watchlist stocks or custom tickers
- Filter by RSI range, momentum score, EMA position, MACD direction
- Results ranked by momentum score

---

## 🇮🇩 Default Watchlist

| Ticker | Company |
|--------|---------|
| BBCA.JK | Bank Central Asia |
| TLKM.JK | Telkom Indonesia |
| ASII.JK | Astra International |
| BMRI.JK | Bank Mandiri |
| BBRI.JK | Bank Rakyat Indonesia |
| GOTO.JK | GoTo Group |
| BREN.JK | Barito Renewables |
| UNVR.JK | Unilever Indonesia |
| ICBP.JK | Indofood CBP |
| PGAS.JK | Perusahaan Gas Negara |

---

## 🛠️ Adding Custom Strategies

In `backtester/engine.py`, add a new function:

```python
def my_strategy(df: pd.DataFrame) -> pd.Series:
    signal = pd.Series(0, index=df.index)
    # Your logic here:
    # signal = 1  → BUY
    # signal = -1 → SELL
    # signal = 0  → HOLD
    return signal
```

Then reference it in `dashboard/app.py` in the strategy selector.

---

## ⚠️ Disclaimer

This tool is for **personal educational use only**. Not financial advice.  
Always Do Your Own Research (DYOR) before trading. 🙏
