#!/usr/bin/env python3
"""Taking-layer watch: is someone minting the word right now?

Usage:
  python3 new_tokens.py --profiles --keywords gabagool,jajaja        # DexScreener latest paid profiles
  python3 new_tokens.py --boosts   --keywords gabagool                # latest + top boosts (someone is spending)
  python3 new_tokens.py --search gabagool --hours 6                   # new pairs for a word in the last N hours
  python3 new_tokens.py --stream --keywords gabagool,jajaja,kusa      # live pump.fun new-token stream (needs: pip install websockets)
  python3 new_tokens.py --stream --keywords-file words.txt --log new_tokens.log

Keywords match case-insensitively against name, symbol, description and URL.
With no keywords, --profiles/--boosts print the latest items; --stream prints every new token.
The stream is the earliest public signal that a name is being taken; run it during a launch window.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import timedelta

from _common import (best_pair_per_token, dex_latest_boosts, dex_latest_profiles, dex_search,
                     dex_top_boosts, fmt_wat, money, now_wat)

PUMPPORTAL_WS = "wss://pumpportal.fun/api/data"


def load_keywords(args) -> list[str]:
    words: list[str] = []
    if args.keywords:
        words += [w.strip() for w in args.keywords.split(",") if w.strip()]
    if args.keywords_file:
        with open(args.keywords_file, encoding="utf-8") as f:
            words += [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return [w.lower() for w in dict.fromkeys(words)]


def hit(words: list[str], *fields) -> list[str]:
    blob = " ".join(str(f or "") for f in fields).lower()
    return [w for w in words if w in blob]


def show_profiles(words: list[str], limit: int) -> None:
    items = dex_latest_profiles()
    if not items:
        print("could not reach DexScreener latest profiles")
        return
    print(f"DexScreener latest paid profiles ({len(items)}), as of {fmt_wat(now_wat())}")
    shown = 0
    for it in items:
        links = " ".join((l.get("url") or "") for l in (it.get("links") or []))
        h = hit(words, it.get("description"), it.get("url"), links, it.get("tokenAddress")) if words else []
        if words and not h:
            continue
        print(f"  {it.get('chainId'):<10} {it.get('tokenAddress')}  {'[' + ','.join(h) + ']' if h else ''}")
        desc = (it.get("description") or "").strip().replace("\n", " ")
        if desc:
            print(f"      {desc[:140]}")
        if it.get("url"):
            print(f"      {it['url']}")
        shown += 1
        if shown >= limit:
            break
    if words and shown == 0:
        print("  no keyword matches in the latest profiles")


def show_boosts(words: list[str], limit: int) -> None:
    for title, items in (("latest boosts", dex_latest_boosts()), ("top boosts", dex_top_boosts())):
        if not items:
            print(f"could not reach DexScreener {title}")
            continue
        print(f"DexScreener {title} ({len(items)}), as of {fmt_wat(now_wat())}")
        shown = 0
        for it in items:
            h = hit(words, it.get("description"), it.get("url"), it.get("tokenAddress")) if words else []
            if words and not h:
                continue
            print(f"  {it.get('chainId'):<10} {it.get('tokenAddress')}  boost {it.get('amount')} (total {it.get('totalAmount')})"
                  f"  {'[' + ','.join(h) + ']' if h else ''}")
            if it.get("url"):
                print(f"      {it['url']}")
            shown += 1
            if shown >= limit:
                break
        if words and shown == 0:
            print("  no keyword matches")


def show_search(word: str, hours: float) -> None:
    pairs = dex_search(word)
    if pairs is None:
        print(f"could not reach DexScreener search for '{word}'; no verdict")
        return
    tokens = list(best_pair_per_token(pairs).values())
    cutoff = now_wat() - timedelta(hours=hours)
    fresh = [t for t in tokens if t["created_dt"] and t["created_dt"] >= cutoff]
    fresh.sort(key=lambda t: t["created_dt"], reverse=True)
    print(f"New pairs matching '{word}' in the last {hours:g}h (as of {fmt_wat(now_wat())}): {len(fresh)}")
    for t in fresh[:25]:
        cap = t["mcap"] if t["mcap"] is not None else t["fdv"]
        print(f"  {t['created_wat']}  {t['chain']:<10} {t['symbol']:<14} {money(cap):>9} mcap · {money(t['liq_usd']):>8} liq · {t['address']}")
        if t["url"]:
            print(f"      {t['url']}")
    if not fresh:
        print("  none (DexScreener only indexes pairs after they trade; pair with --stream for pre-trade signals)")


async def stream(words: list[str], log_path: str | None) -> None:
    try:
        import websockets  # type: ignore
    except ImportError:
        print("the stream needs the 'websockets' package: pip install websockets", file=sys.stderr)
        return
    print(f"streaming pump.fun new tokens from {PUMPPORTAL_WS} (keywords: {', '.join(words) or 'all'})")
    log = open(log_path, "a", encoding="utf-8") if log_path else None
    while True:
        try:
            async with websockets.connect(PUMPPORTAL_WS, ping_interval=20) as ws:
                await ws.send(json.dumps({"method": "subscribeNewToken"}))
                async for raw in ws:
                    try:
                        msg = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    name = msg.get("name")
                    symbol = msg.get("symbol")
                    mint = msg.get("mint")
                    if not mint:
                        continue
                    h = hit(words, name, symbol, msg.get("uri"), msg.get("description")) if words else []
                    if words and not h:
                        continue
                    line = (f"{fmt_wat(now_wat())}  {symbol!s:<14} {name!s:<30} {mint}"
                            f"  {'[' + ','.join(h) + ']' if h else ''}  https://pump.fun/coin/{mint}")
                    print(line, flush=True)
                    if log:
                        log.write(line + "\n")
                        log.flush()
        except (OSError, asyncio.TimeoutError) as e:
            print(f"stream dropped ({e}); reconnecting in 5s", file=sys.stderr)
            await asyncio.sleep(5)
        except Exception as e:  # websockets exceptions vary by version
            print(f"stream error ({e}); reconnecting in 5s", file=sys.stderr)
            await asyncio.sleep(5)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profiles", action="store_true")
    ap.add_argument("--boosts", action="store_true")
    ap.add_argument("--search", metavar="WORD")
    ap.add_argument("--hours", type=float, default=6.0)
    ap.add_argument("--stream", action="store_true")
    ap.add_argument("--keywords", metavar="a,b,c")
    ap.add_argument("--keywords-file", metavar="PATH")
    ap.add_argument("--log", metavar="PATH")
    ap.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()
    words = load_keywords(args)
    ran = False
    if args.profiles:
        show_profiles(words, args.limit)
        ran = True
    if args.boosts:
        show_boosts(words, args.limit)
        ran = True
    if args.search:
        show_search(args.search, args.hours)
        ran = True
    if args.stream:
        asyncio.run(stream(words, args.log))
        ran = True
    if not ran:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
