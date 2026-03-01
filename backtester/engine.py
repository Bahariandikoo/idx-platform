"""
Simple Backtesting Engine for IDX Trading Platform
No external dependencies — pure pandas logic.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class Trade:
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    shares: int
    pnl: float
    pnl_pct: float
    side: str = "LONG"


@dataclass
class BacktestResult:
    trades: List[Trade] = field(default_factory=list)
    equity_curve: pd.Series = None

    @property
    def total_trades(self): return len(self.trades)

    @property
    def win_rate(self):
        if not self.trades: return 0
        wins = sum(1 for t in self.trades if t.pnl > 0)
        return wins / len(self.trades) * 100

    @property
    def total_return(self):
        if self.equity_curve is None or len(self.equity_curve) == 0: return 0
        return (self.equity_curve.iloc[-1] / self.equity_curve.iloc[0] - 1) * 100

    @property
    def max_drawdown(self):
        if self.equity_curve is None: return 0
        roll_max = self.equity_curve.cummax()
        drawdown = (self.equity_curve - roll_max) / roll_max * 100
        return drawdown.min()

    @property
    def sharpe_ratio(self):
        if self.equity_curve is None: return 0
        returns = self.equity_curve.pct_change().dropna()
        if returns.std() == 0: return 0
        return (returns.mean() / returns.std()) * np.sqrt(252)

    @property
    def avg_return_per_trade(self):
        if not self.trades: return 0
        return np.mean([t.pnl_pct for t in self.trades])

    def summary(self) -> dict:
        return {
            "Total Trades": self.total_trades,
            "Win Rate (%)": round(self.win_rate, 2),
            "Total Return (%)": round(self.total_return, 2),
            "Max Drawdown (%)": round(self.max_drawdown, 2),
            "Sharpe Ratio": round(self.sharpe_ratio, 2),
            "Avg Return/Trade (%)": round(self.avg_return_per_trade, 2),
        }


def run_backtest(
    df: pd.DataFrame,
    signal_fn: Callable[[pd.DataFrame], pd.Series],
    initial_capital: float = 10_000_000,
    position_size_pct: float = 0.95,
) -> BacktestResult:
    df = df.copy()
    df["signal"] = signal_fn(df)
    # Shift signal by 1 to avoid lookahead bias — execute on NEXT candle
    df["signal"] = df["signal"].shift(1).fillna(0)

    capital = initial_capital
    position = 0
    entry_price = 0
    entry_date = None
    equity = []
    trades = []

    for i, (date, row) in enumerate(df.iterrows()):
        sig = row["signal"]
        price = row["close"]

        if sig == 1 and position == 0:
            shares = int((capital * position_size_pct) / price)
            if shares > 0:
                position = shares
                entry_price = price
                entry_date = date
                capital -= shares * price

        elif sig == -1 and position > 0:
            exit_price = price
            pnl = (exit_price - entry_price) * position
            pnl_pct = (exit_price - entry_price) / entry_price * 100
            capital += position * exit_price
            trades.append(Trade(
                entry_date=str(entry_date)[:10],
                exit_date=str(date)[:10],
                entry_price=round(entry_price, 2),
                exit_price=round(exit_price, 2),
                shares=position,
                pnl=round(pnl, 2),
                pnl_pct=round(pnl_pct, 2),
            ))
            position = 0

        total_equity = capital + (position * price if position > 0 else 0)
        equity.append(total_equity)

    equity_curve = pd.Series(equity, index=df.index)
    return BacktestResult(trades=trades, equity_curve=equity_curve)


# ─── BUILT-IN STRATEGIES ─────────────────────────────────────────────

def rsi_strategy(df: pd.DataFrame, oversold: int = 30, overbought: int = 70) -> pd.Series:
    """Buy when RSI < oversold, sell when RSI > overbought."""
    from indicators.indicators import rsi
    rsi_vals = rsi(df)
    signal = pd.Series(0, index=df.index)
    signal[rsi_vals < oversold] = 1
    signal[rsi_vals > overbought] = -1
    return signal


def macd_crossover_strategy(df: pd.DataFrame) -> pd.Series:
    """Buy on MACD bullish crossover, sell on bearish crossover."""
    from indicators.indicators import macd
    macd_df = macd(df)
    signal = pd.Series(0, index=df.index)
    prev_hist = macd_df["histogram"].shift(1)
    signal[(macd_df["histogram"] > 0) & (prev_hist <= 0)] = 1
    signal[(macd_df["histogram"] < 0) & (prev_hist >= 0)] = -1
    return signal


def ema_crossover_strategy(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.Series:
    """Buy when fast EMA crosses above slow EMA, sell when it crosses below."""
    from indicators.indicators import ema
    ema_fast = ema(df, fast)
    ema_slow = ema(df, slow)
    signal = pd.Series(0, index=df.index)
    prev_fast = ema_fast.shift(1)
    prev_slow = ema_slow.shift(1)
    signal[(ema_fast > ema_slow) & (prev_fast <= prev_slow)] = 1
    signal[(ema_fast < ema_slow) & (prev_fast >= prev_slow)] = -1
    return signal


def ema_9_21_strategy(df: pd.DataFrame) -> pd.Series:
    """Buy when EMA 9 crosses above EMA 21, sell when EMA 21 crosses above EMA 9."""
    from indicators.indicators import ema
    ema_9  = ema(df, 9)
    ema_21 = ema(df, 21)
    prev_9  = ema_9.shift(1)
    prev_21 = ema_21.shift(1)
    signal = pd.Series(0, index=df.index)
    signal[(ema_9 > ema_21) & (prev_9 <= prev_21)] = 1
    signal[(ema_9 < ema_21) & (prev_9 >= prev_21)] = -1
    return signal