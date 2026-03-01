"""
IDX Telegram Alert Bot — Optimized Version
Concurrent fetching + bulk download + daily cache

Setup:
1. Isi TELEGRAM_TOKEN dan CHAT_ID di bawah
2. pip install requests apscheduler yfinance pandas
3. Jalankan: python alert_bot.py
4. Test manual: python alert_bot.py test
"""

import requests
import pandas as pd
import numpy as np
import time
import logging
import sqlite3
import os
import sys
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import yfinance as yf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data.fetcher import ALL_IDX_STOCKS

import os

# ─── CONFIG — Pakai environment variables ───────────────────────────

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID        = os.environ.get("CHAT_ID", "")

WATCHLIST        = ALL_IDX_STOCKS
FAST_EMA         = 20
SLOW_EMA         = 50
CACHE_HOUR       = 6
CACHE_MINUTE     = 0
ALERT_HOUR       = 7
ALERT_MINUTE     = 0
MAX_WORKERS      = 20
BULK_BATCH_SIZE  = 50
MIN_VOLUME       = 500_000
REQUEST_DELAY    = 0.1
CACHE_DB         = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache.db")

# ─── LOGGING ────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("alert_bot.log")],
)
log = logging.getLogger(__name__)

# ─── CACHE ──────────────────────────────────────────────────────────

def get_cache_conn():
    conn = sqlite3.connect(CACHE_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_cache (
            ticker TEXT, cache_date TEXT, data BLOB,
            PRIMARY KEY (ticker, cache_date)
        )
    """)
    conn.commit()
    return conn

def save_to_cache(ticker, df):
    if df.empty: return
    conn = get_cache_conn()
    conn.execute("INSERT OR REPLACE INTO daily_cache VALUES (?,?,?)",
                 (ticker, str(date.today()), df.to_json()))
    conn.commit()
    conn.close()

def load_from_cache(ticker):
    conn = get_cache_conn()
    row = conn.execute("SELECT data FROM daily_cache WHERE ticker=? AND cache_date=?",
                       (ticker, str(date.today()))).fetchone()
    conn.close()
    if row:
        df = pd.read_json(row[0])
        df.index = pd.to_datetime(df.index, unit="ms")
        return df
    return pd.DataFrame()

def get_cached_tickers():
    conn = get_cache_conn()
    rows = conn.execute("SELECT ticker FROM daily_cache WHERE cache_date=?",
                        (str(date.today()),)).fetchall()
    conn.close()
    return [r[0] for r in rows]

# ─── BULK FETCH ──────────────────────────────────────────────────────

def bulk_fetch_and_cache(tickers):
    already_cached = get_cached_tickers()
    to_fetch = [t for t in tickers if t not in already_cached]
    if not to_fetch:
        log.info("✅ All tickers already cached today")
        return

    log.info(f"📥 Bulk fetching {len(to_fetch)} tickers in batches of {BULK_BATCH_SIZE}...")
    start   = time.time()
    success = 0
    failed  = 0
    batches = [to_fetch[i:i+BULK_BATCH_SIZE] for i in range(0, len(to_fetch), BULK_BATCH_SIZE)]

    for idx, batch in enumerate(batches):
        try:
            log.info(f"  Batch {idx+1}/{len(batches)} — {len(batch)} tickers...")
            raw = yf.download(
                tickers=" ".join(batch), period="3mo", interval="1d",
                group_by="ticker", auto_adjust=True, progress=False, threads=True,
            )
            if raw.empty:
                failed += len(batch)
                continue

            for ticker in batch:
                try:
                    df = raw.copy() if len(batch) == 1 else (
                        raw[ticker].copy() if ticker in raw.columns.get_level_values(0)
                        else None
                    )
                    if df is None or df.empty: failed += 1; continue
                    df = df.dropna(subset=["Close"])
                    if len(df) < SLOW_EMA: failed += 1; continue
                    df.columns = [c.lower() for c in df.columns]
                    df.index   = pd.to_datetime(df.index).tz_localize(None)
                    if df["volume"].tail(10).mean() < MIN_VOLUME: failed += 1; continue
                    save_to_cache(ticker, df)
                    success += 1
                except:
                    failed += 1

            time.sleep(REQUEST_DELAY)
        except Exception as e:
            log.error(f"  Batch {idx+1} failed: {e}")
            failed += len(batch)

    log.info(f"✅ Done in {time.time()-start:.1f}s — {success} cached, {failed} skipped")

# ─── SIGNAL DETECTION ────────────────────────────────────────────────

def calc_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def check_crossover(ticker):
    try:
        df = load_from_cache(ticker)
        if df.empty or len(df) < SLOW_EMA + 2: return None

        ef = calc_ema(df["close"], FAST_EMA)
        es = calc_ema(df["close"], SLOW_EMA)

        if ef.iloc[-1] > es.iloc[-1] and ef.iloc[-2] <= es.iloc[-2]:
            sig_type = "BUY"
        elif ef.iloc[-1] < es.iloc[-1] and ef.iloc[-2] >= es.iloc[-2]:
            sig_type = "SELL"
        else:
            return None

        return {
            "ticker":    ticker,
            "type":      sig_type,
            "price":     df["close"].iloc[-1],
            "price_chg": (df["close"].iloc[-1] - df["close"].iloc[-2]) / df["close"].iloc[-2] * 100,
            "ema_fast":  ef.iloc[-1],
            "ema_slow":  es.iloc[-1],
            "avg_vol":   df["volume"].tail(5).mean(),
        }
    except:
        return None

def scan_all_concurrent(tickers):
    buy_signals, sell_signals = [], []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_crossover, t): t for t in tickers}
        for future in as_completed(futures):
            r = future.result()
            if r:
                (buy_signals if r["type"] == "BUY" else sell_signals).append(r)
    buy_signals.sort(key=lambda x: x["price_chg"], reverse=True)
    sell_signals.sort(key=lambda x: x["price_chg"])
    return buy_signals, sell_signals

# ─── TELEGRAM ────────────────────────────────────────────────────────

def send_telegram(message):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"},
            timeout=10,
        )
        if r.status_code != 200:
            log.error(f"Telegram error: {r.text}")
    except Exception as e:
        log.error(f"Telegram failed: {e}")

def fmt_vol(v):
    if v >= 1_000_000_000: return f"{v/1_000_000_000:.1f}B"
    if v >= 1_000_000:     return f"{v/1_000_000:.1f}M"
    return f"{v:,.0f}"

def send_signals(buys, sells, scanned, elapsed):
    now = datetime.now().strftime("%d %b %Y %H:%M")
    if not buys and not sells:
        send_telegram(
            f"📊 <b>IDX Daily Scan</b> — {now}\n\n"
            f"🔍 Scanned <b>{scanned} saham</b> dalam <b>{elapsed:.1f}s</b>\n"
            f"📈 EMA {FAST_EMA} / EMA {SLOW_EMA} Crossover\n\n"
            "😴 Tidak ada sinyal hari ini."
        )
        return

    if buys:
        msg = f"🚀 <b>BUY — EMA {FAST_EMA}/{SLOW_EMA}</b>  |  {now}\n"
        msg += f"⚡ Scan {scanned} saham dalam {elapsed:.1f}s\n"
        msg += "━" * 28 + "\n\n"
        for s in buys:
            msg += (
                f"🟢 <b>{s['ticker']}</b>  Rp {s['price']:,.0f} "
                f"<i>({s['price_chg']:+.1f}%)</i>\n"
                f"   EMA{FAST_EMA}: {s['ema_fast']:,.0f}  EMA{SLOW_EMA}: {s['ema_slow']:,.0f}  "
                f"Vol: {fmt_vol(s['avg_vol'])}\n\n"
            )
        msg += f"<b>{len(buys)} saham</b> | <i>Bukan rekomendasi. DYOR!</i>"
        send_telegram(msg)
        time.sleep(0.5)

    if sells:
        msg = f"⚠️ <b>SELL — EMA {FAST_EMA}/{SLOW_EMA}</b>  |  {now}\n"
        msg += f"⚡ Scan {scanned} saham dalam {elapsed:.1f}s\n"
        msg += "━" * 28 + "\n\n"
        for s in sells:
            msg += (
                f"🔴 <b>{s['ticker']}</b>  Rp {s['price']:,.0f} "
                f"<i>({s['price_chg']:+.1f}%)</i>\n"
                f"   EMA{FAST_EMA}: {s['ema_fast']:,.0f}  EMA{SLOW_EMA}: {s['ema_slow']:,.0f}  "
                f"Vol: {fmt_vol(s['avg_vol'])}\n\n"
            )
        msg += f"<b>{len(sells)} saham</b> | <i>Bukan rekomendasi. DYOR!</i>"
        send_telegram(msg)
        time.sleep(0.5)

    send_telegram(
        f"📋 <b>Summary</b> — {now}\n\n"
        f"🔍 Scanned: {scanned} saham dalam {elapsed:.1f}s\n"
        f"🟢 BUY:  {len(buys)} saham\n"
        f"🔴 SELL: {len(sells)} saham\n"
    )

# ─── JOBS ────────────────────────────────────────────────────────────

def job_fetch_cache():
    if datetime.now().weekday() >= 5:
        log.info("📅 Weekend — skipped"); return
    log.info("📥 Daily cache fetch starting...")
    bulk_fetch_and_cache(WATCHLIST)

def job_scan_and_alert():
    if datetime.now().weekday() >= 5:
        log.info("📅 Weekend — skipped"); return

    log.info("🔍 Daily scan starting...")
    start  = time.time()
    cached = get_cached_tickers()
    to_scan = [t for t in WATCHLIST if t in cached]

    if not to_scan:
        log.warning("⚠️ No cache found — fetching first...")
        bulk_fetch_and_cache(WATCHLIST)
        cached  = get_cached_tickers()
        to_scan = [t for t in WATCHLIST if t in cached]

    log.info(f"⚡ Scanning {len(to_scan)} tickers with {MAX_WORKERS} threads...")
    buys, sells = scan_all_concurrent(to_scan)
    elapsed = time.time() - start

    log.info(f"✅ Done in {elapsed:.1f}s — BUY: {len(buys)}, SELL: {len(sells)}")
    send_signals(buys, sells, len(to_scan), elapsed)

# ─── SCHEDULER ───────────────────────────────────────────────────────

def start_scheduler():
    scheduler = BlockingScheduler(timezone="Asia/Jakarta")
    scheduler.add_job(job_fetch_cache,  CronTrigger(hour=CACHE_HOUR,  minute=CACHE_MINUTE,  timezone="Asia/Jakarta"), id="fetch")
    scheduler.add_job(job_scan_and_alert, CronTrigger(hour=ALERT_HOUR, minute=ALERT_MINUTE, timezone="Asia/Jakarta"), id="scan")

    log.info("🤖 IDX Alert Bot started!")
    log.info(f"📥 Cache fetch : jam {CACHE_HOUR:02d}:{CACHE_MINUTE:02d} WIB")
    log.info(f"🔔 Scan & alert: jam {ALERT_HOUR:02d}:{ALERT_MINUTE:02d} WIB")
    log.info(f"📋 Watching    : {len(WATCHLIST)} stocks")
    log.info(f"⚡ Workers     : {MAX_WORKERS} threads | Batch: {BULK_BATCH_SIZE}")

    send_telegram(
        "🤖 <b>IDX Alert Bot aktif!</b>\n\n"
        f"📋 Memantau <b>{len(WATCHLIST)} saham</b>\n"
        f"📈 EMA {FAST_EMA} / EMA {SLOW_EMA} Crossover\n"
        f"📥 Cache: jam {CACHE_HOUR:02d}:{CACHE_MINUTE:02d} WIB\n"
        f"🔔 Alert: jam {ALERT_HOUR:02d}:{ALERT_MINUTE:02d} WIB\n"
        f"⚡ {MAX_WORKERS} concurrent threads\n\n"
        "✅ Bot siap!"
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped.")

# ─── ENTRY POINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Set environment variables TELEGRAM_TOKEN dan CHAT_ID dulu!")
        print("   Railway: Settings → Variables → Add")
        print("   Local: export TELEGRAM_TOKEN=xxx && export CHAT_ID=xxx")
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else ""

    if cmd == "test":
        log.info("🧪 Test mode — fetch + scan sekarang...")
        bulk_fetch_and_cache(WATCHLIST)
        job_scan_and_alert()
    elif cmd == "fetch":
        log.info("📥 Fetch cache only...")
        bulk_fetch_and_cache(WATCHLIST)
    elif cmd == "scan":
        log.info("🔍 Scan from cache only...")
        job_scan_and_alert()
    else:
        start_scheduler()
