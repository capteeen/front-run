"""Shared helpers for frontrun-radar scripts. Standard library only.

Every network call here returns None on failure and prints a one-line
"could not reach" note to stderr. Scripts must print the failure rather
than invent a number; the skill's first rule is live data only.
"""
from __future__ import annotations

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

WAT = timezone(timedelta(hours=1), name="WAT")
DEXSCREENER = "https://api.dexscreener.com"
USER_AGENT = "frontrun-radar/1.0 (+https://github.com/)"

_cache: dict[str, object] = {}


def now_wat() -> datetime:
    return datetime.now(tz=WAT)


def fmt_wat(dt: datetime | None, with_date: bool = True) -> str:
    if dt is None:
        return "?"
    dt = dt.astimezone(WAT)
    return dt.strftime("%Y-%m-%d %H:%M WAT") if with_date else dt.strftime("%H:%M WAT")


def ms_to_wat(ms: int | float | None) -> datetime | None:
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(float(ms) / 1000.0, tz=timezone.utc).astimezone(WAT)
    except (ValueError, OSError, OverflowError):
        return None


def age_str(created: datetime | None) -> str:
    if created is None:
        return "?"
    delta = now_wat() - created.astimezone(WAT)
    secs = int(delta.total_seconds())
    if secs < 0:
        return "0m"
    if secs < 3600:
        return f"{secs // 60}m"
    if secs < 86400:
        h = secs / 3600
        return f"{h:.1f}h"
    return f"{secs / 86400:.1f}d"


def _ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if cafile and os.path.exists(cafile):
        return ssl.create_default_context(cafile=cafile)
    return ssl.create_default_context()


def http_json(url: str, method: str = "GET", body: dict | None = None, timeout: float = 20.0,
              headers: dict | None = None, use_cache: bool = True):
    """GET/POST JSON. Returns parsed JSON or None. Caches GETs for the process lifetime."""
    key = f"{method} {url} {json.dumps(body, sort_keys=True) if body else ''}"
    if use_cache and key in _cache:
        return _cache[key]
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/json")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
                raw = resp.read()
            parsed = json.loads(raw.decode("utf-8", errors="replace"))
            if use_cache:
                _cache[key] = parsed
            return parsed
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(2.0)
                continue
            print(f"could not reach {url}: HTTP {e.code}", file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError, ssl.SSLError, json.JSONDecodeError, OSError) as e:
            print(f"could not reach {url}: {e}", file=sys.stderr)
            return None
    return None


def http_text(url: str, timeout: float = 15.0) -> tuple[int | None, str]:
    """GET a page as text. Returns (status, text). (None, '') on failure."""
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; frontrun-radar/1.0)")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            return resp.status, resp.read(400_000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError, ssl.SSLError, OSError) as e:
        print(f"could not reach {url}: {e}", file=sys.stderr)
        return None, ""


# ---------- DexScreener ----------

def dex_search(query: str) -> list[dict] | None:
    """None means the endpoint could not be reached (no verdict). [] means no results."""
    url = f"{DEXSCREENER}/latest/dex/search?q={urllib.parse.quote(query)}"
    data = http_json(url)
    if data is None:
        return None
    if not isinstance(data, dict):
        return []
    return data.get("pairs") or []


def dex_token_pairs(chain: str, address: str) -> list[dict] | None:
    """None means unreachable. [] means not indexed on DexScreener for that chain."""
    url = f"{DEXSCREENER}/tokens/v1/{chain}/{address}"
    data = http_json(url)
    if data is None:
        return None
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "pairs" in data:
        return data.get("pairs") or []
    return []


def dex_latest_profiles() -> list[dict]:
    data = http_json(f"{DEXSCREENER}/token-profiles/latest/v1", use_cache=False)
    return data if isinstance(data, list) else []


def dex_latest_boosts() -> list[dict]:
    data = http_json(f"{DEXSCREENER}/token-boosts/latest/v1", use_cache=False)
    return data if isinstance(data, list) else []


def dex_top_boosts() -> list[dict]:
    data = http_json(f"{DEXSCREENER}/token-boosts/top/v1", use_cache=False)
    return data if isinstance(data, list) else []


def pair_numbers(p: dict) -> dict:
    """Pull the numbers the desk reports from one DexScreener pair object."""
    liq = (p.get("liquidity") or {}).get("usd")
    vol = p.get("volume") or {}
    chg = p.get("priceChange") or {}
    tx = p.get("txns") or {}
    h1 = tx.get("h1") or {}
    h24 = tx.get("h24") or {}
    created = ms_to_wat(p.get("pairCreatedAt"))
    base = p.get("baseToken") or {}
    quote = p.get("quoteToken") or {}
    return {
        "chain": p.get("chainId"),
        "dex": p.get("dexId"),
        "pair_address": p.get("pairAddress"),
        "url": p.get("url"),
        "symbol": base.get("symbol"),
        "name": base.get("name"),
        "address": base.get("address"),
        "quote_symbol": quote.get("symbol"),
        "quote_address": quote.get("address"),
        "price_usd": _f(p.get("priceUsd")),
        "mcap": _f(p.get("marketCap")),
        "fdv": _f(p.get("fdv")),
        "liq_usd": _f(liq),
        "vol_m5": _f(vol.get("m5")),
        "vol_h1": _f(vol.get("h1")),
        "vol_h6": _f(vol.get("h6")),
        "vol_h24": _f(vol.get("h24")),
        "chg_m5": _f(chg.get("m5")),
        "chg_h1": _f(chg.get("h1")),
        "chg_h6": _f(chg.get("h6")),
        "chg_h24": _f(chg.get("h24")),
        "buys_h1": _i(h1.get("buys")),
        "sells_h1": _i(h1.get("sells")),
        "buys_h24": _i(h24.get("buys")),
        "sells_h24": _i(h24.get("sells")),
        "created_wat": fmt_wat(created),
        "created_dt": created,
        "age": age_str(created),
        "boosts": (p.get("boosts") or {}).get("active"),
        "labels": p.get("labels") or [],
        "websites": [w.get("url") for w in ((p.get("info") or {}).get("websites") or []) if w.get("url")],
        "socials": [f"{s.get('type')}:{s.get('url')}" for s in ((p.get("info") or {}).get("socials") or []) if s.get("url")],
    }


def _f(x) -> float | None:
    try:
        return None if x is None else float(x)
    except (TypeError, ValueError):
        return None


def _i(x) -> int | None:
    try:
        return None if x is None else int(x)
    except (TypeError, ValueError):
        return None


def money(x: float | None) -> str:
    if x is None:
        return "?"
    if x >= 1_000_000_000:
        return f"${x / 1_000_000_000:.2f}B"
    if x >= 1_000_000:
        return f"${x / 1_000_000:.2f}M"
    if x >= 1_000:
        return f"${x / 1_000:.1f}K"
    return f"${x:.0f}"


def pct(x: float | None) -> str:
    return "?" if x is None else f"{x:+.0f}%"


def best_pair_per_token(pairs: list[dict]) -> dict[str, dict]:
    """Group pairs by (chain, base token address) and keep the most liquid pair for each."""
    best: dict[str, dict] = {}
    for p in pairs:
        n = pair_numbers(p)
        if not n["address"]:
            continue
        key = f"{n['chain']}:{n['address']}"
        cur = best.get(key)
        if cur is None or (n["liq_usd"] or 0) > (cur["liq_usd"] or 0):
            best[key] = n
    return best


def write_json(obj, path: str | None) -> None:
    text = json.dumps(obj, indent=2, default=str)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)
