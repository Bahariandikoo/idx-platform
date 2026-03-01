"""
Technical Indicators for IDX Trading Platform
Uses pandas-ta under the hood, plus custom indicators
"""

import pandas as pd
import numpy as np


# ─── TREND INDICATORS ───────────────────────────────────────────────

def ema(df: pd.DataFrame, period: int = 20) -> pd.Series:
    return df["close"].ewm(span=period, adjust=False).mean()


def sma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    return df["close"].rolling(window=period).mean()


def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return pd.DataFrame({
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }, index=df.index)


def bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> pd.DataFrame:
    middle = sma(df, period)
    std = df["close"].rolling(window=period).std()
    return pd.DataFrame({
        "upper": middle + std_dev * std,
        "middle": middle,
        "lower": middle - std_dev * std,
    }, index=df.index)


# ─── MOMENTUM INDICATORS ─────────────────────────────────────────────

def rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    lowest_low = df["low"].rolling(window=k_period).min()
    highest_high = df["high"].rolling(window=k_period).max()
    k = 100 * (df["close"] - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return pd.DataFrame({"k": k, "d": d}, index=df.index)


# ─── VOLUME INDICATORS ───────────────────────────────────────────────

def obv(df: pd.DataFrame) -> pd.Series:
    """On-Balance Volume"""
    direction = np.sign(df["close"].diff())
    return (direction * df["volume"]).fillna(0).cumsum()


def vwap(df: pd.DataFrame) -> pd.Series:
    """Volume Weighted Average Price"""
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    return (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()


# ─── CUSTOM IDX INDICATORS ───────────────────────────────────────────

def idx_momentum_score(df: pd.DataFrame) -> pd.Series:
    """
    Custom momentum score combining RSI + MACD signal + price vs EMA.
    Returns score from -100 (very bearish) to +100 (very bullish).
    """
    rsi_val = rsi(df)
    macd_df = macd(df)
    ema_20 = ema(df, 20)

    # Normalize RSI: 50 = neutral
    rsi_score = (rsi_val - 50) * 2  # -100 to +100

    # MACD histogram direction
    macd_score = np.sign(macd_df["histogram"]) * 50

    # Price above/below EMA20
    ema_score = np.where(df["close"] > ema_20, 50, -50)

    return (rsi_score * 0.4 + macd_score * 0.4 + ema_score * 0.2)


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add all indicators to a OHLCV dataframe. Returns enriched dataframe."""
    df = df.copy()

    df["ema_20"] = ema(df, 20)
    df["ema_50"] = ema(df, 50)
    df["sma_200"] = sma(df, 200)

    macd_df = macd(df)
    df["macd"] = macd_df["macd"]
    df["macd_signal"] = macd_df["signal"]
    df["macd_hist"] = macd_df["histogram"]

    bb = bollinger_bands(df)
    df["bb_upper"] = bb["upper"]
    df["bb_middle"] = bb["middle"]
    df["bb_lower"] = bb["lower"]

    df["rsi"] = rsi(df)
    stoch = stochastic(df)
    df["stoch_k"] = stoch["k"]
    df["stoch_d"] = stoch["d"]

    df["obv"] = obv(df)
    df["vwap"] = vwap(df)
    df["momentum_score"] = idx_momentum_score(df)

    return df
