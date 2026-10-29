#!/usr/bin/env python3
"""Pre-launch presence check: domains and Telegram groups for a word.

Usage:
  python3 presence_check.py gabagool
  python3 presence_check.py gabagool --tlds fun,lol,xyz,gg,wtf,meme,app,io,com --json

What it checks:
  domains   <word>.<tld> resolving in DNS, and for resolving ones the HTTP status and <title>
  telegram  t.me/<word>, t.me/<word>sol, t.me/<word>coin, t.me/<word>portal (public preview page)
What it cannot check without auth: X handles and X mentions. Do those by hand (X search, latest tab)
and write the counts into the ledger row.

A fresh resolving domain with a "CA soon" page, or a Telegram group with members, means someone
is prepping the name: the verdict is "launch now or drop", not "open".
"""
from __future__ import annotations

import argparse
import html
import re
import socket
import sys

from _common import fmt_wat, http_text, now_wat, write_json

DEFAULT_TLDS = ["fun", "lol", "xyz", "gg", "wtf", "meme", "app", "io", "com", "sol"]
TG_SUFFIXES = ["", "sol", "coin", "portal", "_sol", "onsol"]


def resolves(host: str) -> bool:
    try:
        socket.getaddrinfo(host, 443)
        return True
    except socket.gaierror:
        return False
    except OSError:
        return False


def title_of(text: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    return html.unescape(m.group(1)).strip()[:120] if m else ""


def dns_available() -> bool:
    """Canary: if a known domain does not resolve, DNS is blocked here and no verdict is possible."""
    return resolves("dexscreener.com") or resolves("pump.fun")


def check_domains(word: str, tlds: list[str]) -> list[dict]:
    out = []
    if not dns_available():
        return [{"domain": f"{word}.{tld}", "resolves": None, "note": "DNS unavailable; no verdict"} for tld in tlds]
    for tld in tlds:
        host = f"{word}.{tld}"
        r = {"domain": host, "resolves": resolves(host)}
        if r["resolves"]:
            status, text = http_text(f"https://{host}")
            r["http_status"] = status
            r["title"] = title_of(text) if text else ""
            low = text.lower()
            r["ca_soon"] = ("ca soon" in low) or ("ca:" in low and "soon" in low)
            r["mentions_pump"] = "pump.fun" in low
        out.append(r)
    return out


def check_telegram(word: str) -> list[dict]:
    out = []
    for suf in TG_SUFFIXES:
        handle = f"{word}{suf}"
        status, text = http_text(f"https://t.me/{handle}")
        r = {"handle": handle, "url": f"https://t.me/{handle}", "http_status": status}
        if text:
            exists = "tgme_page_title" in text
            r["exists"] = exists
            m = re.search(r'tgme_page_extra">([^<]+)<', text)
            r["extra"] = html.unescape(m.group(1)).strip() if m else ""
            t = re.search(r'tgme_page_title">\s*<span[^>]*>([^<]+)<', text)
            r["title"] = html.unescape(t.group(1)).strip() if t else ""
        else:
            r["exists"] = None
        out.append(r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("word")
    ap.add_argument("--tlds", default=",".join(DEFAULT_TLDS))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    word = re.sub(r"[^a-z0-9-]", "", args.word.lower().replace("$", ""))
    if not word:
        print("word must contain letters or digits", file=sys.stderr)
        return 2
    tlds = [t.strip() for t in args.tlds.split(",") if t.strip()]
    result = {
        "word": word,
        "checked_wat": fmt_wat(now_wat()),
        "domains": check_domains(word, tlds),
        "telegram": check_telegram(word),
        "x": "not checked (needs auth): search X latest tab for $" + word.upper() + " and the new-account list by hand",
    }
    if args.json:
        write_json(result, None)
        return 0
    print(f"Presence check for '{word}' as of {result['checked_wat']}")
    dns_blocked = all(d["resolves"] is None for d in result["domains"])
    live = [d for d in result["domains"] if d["resolves"]]
    if dns_blocked:
        print("Domains: DNS unavailable here; no verdict on domains")
    else:
        print(f"Domains resolving: {len(live)}/{len(result['domains'])}")
    for d in live:
        print(f"  {d['domain']:<22} HTTP {d.get('http_status')}  title: {d.get('title') or '-'}"
              f"{'  CA SOON' if d.get('ca_soon') else ''}{'  mentions pump.fun' if d.get('mentions_pump') else ''}")
    tg = [t for t in result["telegram"] if t.get("exists")]
    print(f"Telegram groups found: {len(tg)}")
    for t in tg:
        print(f"  {t['url']:<40} {t.get('title') or ''}  {t.get('extra') or ''}")
    unreach = [t for t in result["telegram"] if t.get("exists") is None]
    if unreach:
        print(f"  could not reach {len(unreach)} t.me pages")
    print(result["x"])
    signal = bool(live or tg)
    if signal:
        print("Verdict: someone may be prepping this name: launch now or drop")
    elif dns_blocked or (unreach and len(unreach) == len(result["telegram"])):
        print("Verdict: no verdict (network checks could not run here); redo from a machine with open DNS/HTTPS")
    else:
        print("Verdict: no public prep signals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
