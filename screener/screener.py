"""
IDX Stock Screener
Filter stocks from your watchlist based on technical conditions.
"""

import pandas as pd
from typing import Dict
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.fetcher import fetch_ticker,ALL_IDX_STOCKS
from indicators.indicators import add_all_indicators


def screen_stocks(
    tickers: list = None,
    rsi_min: float = 0,
    rsi_max: float = 100,
    min_momentum_score: float = -100,
    require_above_ema20: bool = False,
    require_macd_bullish: bool = False,
    min_volume: int = 0,
) -> pd.DataFrame:
    """
    Screen IDX stocks based on technical criteria.

    Returns a DataFrame with one row per stock that passes all filters.
    """
    if tickers is None:
        tickers = ALL_IDX_STOCKS

    results = []

    for ticker in tickers:
        try:
            df = fetch_ticker(ticker, period="6mo")
            if df.empty or len(df) < 50:
                continue

            df = add_all_indicators(df)
            latest = df.iloc[-1]

            # Apply filters
            if not (rsi_min <= latest["rsi"] <= rsi_max):
                continue
            if latest["momentum_score"] < min_momentum_score:
                continue
            if require_above_ema20 and latest["close"] < latest["ema_20"]:
                continue
            if require_macd_bullish and latest["macd_hist"] <= 0:
                continue
            if latest["volume"] < min_volume:
                continue

            # Calculate recent performance
            week_ago = df["close"].iloc[-5] if len(df) >= 5 else df["close"].iloc[0]
            month_ago = df["close"].iloc[-20] if len(df) >= 20 else df["close"].iloc[0]

            results.append({
                "Ticker": ticker,
                "Close": round(latest["close"], 0),
                "RSI": round(latest["rsi"], 1),
                "MACD Hist": round(latest["macd_hist"], 2),
                "Momentum Score": round(latest["momentum_score"], 1),
                "Above EMA20": "✅" if latest["close"] > latest["ema_20"] else "❌",
                "1W Change %": round((latest["close"] / week_ago - 1) * 100, 2),
                "1M Change %": round((latest["close"] / month_ago - 1) * 100, 2),
                "Volume": int(latest["volume"]),
            })

        except Exception as e:
            print(f"[SKIP] {ticker}: {e}")

    if not results:
        return pd.DataFrame()

    return pd.DataFrame(results).sort_values("Momentum Score", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    print("🔍 Screening IDX stocks with RSI < 40 (oversold candidates)...\n")
    df = screen_stocks(rsi_max=40)
    print(df.to_string(index=False))
