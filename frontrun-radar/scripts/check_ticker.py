#!/usr/bin/env python3
"""Ticker availability across all chains via DexScreener.

Usage:
  python3 check_ticker.py GABAGOOL JAJAJA "Opt Out"
  python3 check_ticker.py BLIMP --json out.json
  python3 check_ticker.py BLIMP --no-variants

Status rules (references/hygiene.md):
  TAKEN  same ticker or name with mcap/FDV > $50K or 24h volume > $10K on any chain,
         or a clone under 48h old with liquidity > $20K and rising volume
  DUST   exists but under $10K mcap with near-zero volume (usable; say it exists)
  EMPTY  nothing found on DexScreener (then confirm on pump.fun search and GeckoTerminal by hand)

The DexScreener search endpoint caps results; for very common words the exact match
may sit outside the cap, so the script also runs a chain-scoped search. A result of
EMPTY here is a strong signal, not proof. VERIFY still rechecks before output.
"""
from __future__ import annotations

import argparse
import sys
from datetime import timedelta

from _common import (best_pair_per_token, dex_search, fmt_wat, money, now_wat, pct,
                     write_json)

TAKEN_MCAP = 50_000
TAKEN_VOL24 = 10_000
DUST_MCAP = 10_000
CLONE_LIQ = 20_000


def norm(s: str | None) -> str:
    return (s or "").strip().upper().replace("$", "")


def variants(t: str) -> list[str]:
    t = norm(t)
    out = []
    if t.endswith("S") and len(t) > 3:
        out.append(t[:-1])
    else:
        out.append(t + "S")
    out.append("THE" + t)
    if " " in t:
        out.append(t.replace(" ", ""))
    return [v for v in dict.fromkeys(out) if v != t]


def edit_distance_le1(a: str, b: str) -> bool:
    if a == b:
        return False
    if abs(len(a) - len(b)) > 1:
        return False
    i = j = diffs = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
            continue
        diffs += 1
        if diffs > 1:
            return False
        if len(a) > len(b):
            i += 1
        elif len(b) > len(a):
            j += 1
        else:
            i += 1
            j += 1
    diffs += (len(a) - i) + (len(b) - j)
    return diffs <= 1


def classify(matches: list[dict]) -> tuple[str, str]:
    """Return (status, reason) from the best-pair-per-token list."""
    if not matches:
        return "EMPTY", "no exact symbol or name match on DexScreener"
    now = now_wat()
    for m in matches:
        cap = m["mcap"] if m["mcap"] is not None else m["fdv"]
        if (cap or 0) > TAKEN_MCAP or (m["vol_h24"] or 0) > TAKEN_VOL24:
            return "TAKEN", f"{m['chain']} {m['symbol']} {money(cap)} mcap, {money(m['vol_h24'])} 24h vol"
        if m["created_dt"] and (now - m["created_dt"]) < timedelta(hours=48) and (m["liq_usd"] or 0) > CLONE_LIQ:
            return "TAKEN", f"fresh clone on {m['chain']} with {money(m['liq_usd'])} liq ({m['age']} old)"
    return "DUST", "exists below thresholds; usable but say it exists"


def search_word(word: str) -> list[dict] | None:
    """None = DexScreener unreachable (no verdict). [] = nothing found."""
    pairs = dex_search(word)
    if pairs is None:
        return None
    # widen when the cap is hit (30 is the usual page size)
    if len(pairs) >= 30:
        for extra in (f"{word} solana", f"{word} base", f"{word} bsc", f"{word} ethereum"):
            more = dex_search(extra)
            if more:
                pairs.extend(more)
    return pairs


def unreachable(word: str) -> dict:
    return {
        "query": word,
        "ticker": norm(word),
        "checked_wat": fmt_wat(now_wat()),
        "status": "UNREACHABLE",
        "reason": "DexScreener could not be reached; no verdict (do not write EMPTY)",
        "exact_matches": [],
        "near_duplicates": [],
        "variants": {},
        "dexscreener_pairs_scanned": 0,
    }


def check_one(word: str, with_variants: bool = True) -> dict:
    target = norm(word)
    pairs = search_word(word)
    if pairs is None:
        return unreachable(word)
    tokens = list(best_pair_per_token(pairs).values())
    exact_symbol = [t for t in tokens if norm(t["symbol"]) == target]
    exact_name = [t for t in tokens if norm(t["name"]) == target and norm(t["symbol"]) != target]
    near = [t for t in tokens if norm(t["symbol"]) != target and edit_distance_le1(norm(t["symbol"]), target)]
    matches = sorted(exact_symbol + exact_name, key=lambda t: -((t["mcap"] or t["fdv"] or 0)))
    status, reason = classify(matches)
    result = {
        "query": word,
        "ticker": target,
        "checked_wat": fmt_wat(now_wat()),
        "status": status,
        "reason": reason,
        "exact_matches": matches,
        "near_duplicates": sorted(near, key=lambda t: -((t["mcap"] or t["fdv"] or 0)))[:8],
        "variants": {},
        "dexscreener_pairs_scanned": len(pairs),
    }
    if with_variants:
        for v in variants(target):
            vp = search_word(v)
            if vp is None:
                result["variants"][v] = {"status": "UNREACHABLE", "reason": "DexScreener could not be reached", "top": []}
                continue
            vt = [t for t in best_pair_per_token(vp).values() if norm(t["symbol"]) == v or norm(t["name"]) == v]
            vs, vr = classify(sorted(vt, key=lambda t: -((t["mcap"] or t["fdv"] or 0))))
            result["variants"][v] = {"status": vs, "reason": vr, "top": vt[:3]}
    return result


def print_human(r: dict) -> None:
    print(f"${r['ticker']} - {r['status']} as of {r['checked_wat']}  ({r['reason']})")
    if r["exact_matches"]:
        print("  Exact matches:")
        for m in r["exact_matches"][:8]:
            cap = m["mcap"] if m["mcap"] is not None else m["fdv"]
            print(f"    {m['chain']:<10} {m['symbol']:<14} {money(cap):>9} mcap · {money(m['liq_usd']):>8} liq · "
                  f"{money(m['vol_h24']):>8} 24h vol · {pct(m['chg_h24'])} 24h · {m['age']} old · {m['address']}")
            if m["url"]:
                print(f"               {m['url']}")
    if r["near_duplicates"]:
        print("  Near-duplicates to warn buyers about:")
        for m in r["near_duplicates"][:5]:
            cap = m["mcap"] if m["mcap"] is not None else m["fdv"]
            print(f"    {m['chain']:<10} {m['symbol']:<14} {money(cap):>9} mcap · {m['age']} old")
    if r["variants"]:
        print("  Variants:")
        for v, info in r["variants"].items():
            print(f"    {v:<16} {info['status']:<6} {info['reason']}")
    print(f"  Scanned {r['dexscreener_pairs_scanned']} DexScreener pairs. "
          f"EMPTY still needs pump.fun search + GeckoTerminal confirmation before 'mint'.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--json", metavar="PATH", help="write JSON results to PATH ('-' for stdout)")
    ap.add_argument("--no-variants", action="store_true")
    args = ap.parse_args()
    results = []
    for t in args.tickers:
        r = check_one(t, with_variants=not args.no_variants)
        results.append(r)
        print_human(r)
        print()
    if args.json:
        write_json(results, None if args.json == "-" else args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
