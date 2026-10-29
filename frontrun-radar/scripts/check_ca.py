#!/usr/bin/env python3
"""Contract address audit: DexScreener numbers + Solana mint checks + clone search.

Usage:
  python3 check_ca.py <CA>                      # Solana by default
  python3 check_ca.py <CA> --chain base         # EVM chains: DexScreener numbers + clone search only
  python3 check_ca.py <CA> --rpc https://...    # paid Solana RPC (or set SOLANA_RPC_URL)
  python3 check_ca.py <CA> --json audit.json

What it reports (references/hygiene.md §CA audit):
  numbers: mcap, FDV, liquidity, 1h/24h volume, 5m/1h/6h/24h change, buys vs sells, age, created time in WAT
  contract (Solana): token program, mint/freeze authority, Token-2022 transfer fee + fee authority,
                     permanent delegate, transfer hook, on-mint metadata update authority when present
  holders (Solana): top-20 token accounts as a share of supply (the largest is often the pool; read it that way)
  clones: other tokens with the same symbol on any chain, and which one is the earliest with liquidity
  flags: fake liq, liq ~ mcap on a fresh pool, wash (vol/liq), bot flow (buys vs sells), dead, under 1h

Verdicts: ALIVE | DEAD | CLONE | RUG RISK | WASH. The verdict is a starting point for the
human audit (socials, endorsement, Bubblemaps, RugCheck), not a replacement for it.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import timedelta

from _common import (best_pair_per_token, dex_search, dex_token_pairs, fmt_wat, http_json,
                     money, now_wat, pair_numbers, pct, write_json)

TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
TOKEN_2022 = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
PUBLIC_RPC = "https://api.mainnet-beta.solana.com"


def rpc(url: str, method: str, params: list):
    data = http_json(url, method="POST", body={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
                     use_cache=False)
    if not data or "result" not in data:
        return None
    return data["result"]


def solana_mint_info(ca: str, rpc_url: str) -> dict:
    out: dict = {"checked": False}
    res = rpc(rpc_url, "getAccountInfo", [ca, {"encoding": "jsonParsed"}])
    if not res or not res.get("value"):
        out["error"] = "mint account not found or RPC unreachable"
        return out
    val = res["value"]
    owner = val.get("owner")
    out["checked"] = True
    out["program"] = "Token-2022" if owner == TOKEN_2022 else ("Token" if owner == TOKEN_PROGRAM else owner)
    parsed = ((val.get("data") or {}).get("parsed") or {})
    info = parsed.get("info") or {}
    out["mint_authority"] = info.get("mintAuthority")
    out["freeze_authority"] = info.get("freezeAuthority")
    out["decimals"] = info.get("decimals")
    out["supply_raw"] = info.get("supply")
    out["extensions"] = []
    fee = None
    for ext in info.get("extensions") or []:
        name = ext.get("extension")
        state = ext.get("state") or {}
        out["extensions"].append(name)
        if name == "transferFeeConfig":
            newer = state.get("newerTransferFee") or {}
            older = state.get("olderTransferFee") or {}
            fee = {
                "basis_points": newer.get("transferFeeBasisPoints", older.get("transferFeeBasisPoints")),
                "maximum_fee": newer.get("maximumFee", older.get("maximumFee")),
                "fee_authority": state.get("transferFeeConfigAuthority"),
                "withdraw_authority": state.get("withdrawWithheldAuthority"),
            }
        if name == "permanentDelegate":
            out["permanent_delegate"] = state.get("delegate")
        if name == "transferHook":
            out["transfer_hook_program"] = state.get("programId")
        if name == "tokenMetadata":
            out["metadata_update_authority"] = state.get("updateAuthority")
            out["metadata_name"] = state.get("name")
            out["metadata_symbol"] = state.get("symbol")
    out["transfer_fee"] = fee
    if "metadata_update_authority" not in out:
        out["metadata_update_authority"] = "not checked (Metaplex metadata PDA; check on Solscan)"
    # holders
    largest = rpc(rpc_url, "getTokenLargestAccounts", [ca])
    supply = None
    try:
        supply = float(out["supply_raw"]) if out["supply_raw"] is not None else None
    except (TypeError, ValueError):
        supply = None
    if largest and largest.get("value") and supply:
        accts = largest["value"]
        amounts = []
        for a in accts:
            try:
                amounts.append(float(a.get("amount") or 0))
            except (TypeError, ValueError):
                amounts.append(0.0)
        top10 = sum(amounts[:10]) / supply * 100 if supply else None
        top1 = amounts[0] / supply * 100 if amounts and supply else None
        out["top1_account_pct"] = round(top1, 2) if top1 is not None else None
        out["top10_accounts_pct"] = round(top10, 2) if top10 is not None else None
        out["holders_note"] = ("top accounts include pools and bonding curves; a ~50%+ single account "
                               "on a pump.fun coin is usually the curve or LP, not a wallet; "
                               "confirm on Solscan / Bubblemaps")
    else:
        out["holders_note"] = "could not reach getTokenLargestAccounts"
    return out


def flags_for(n: dict, mint: dict | None, chain: str) -> list[str]:
    flags = []
    cap = n["mcap"] if n["mcap"] is not None else n["fdv"]
    liq = n["liq_usd"] or 0
    if cap and liq < 2_000 and cap / max(liq, 1) > 500:
        flags.append(f"FAKE LIQ: {money(cap)} mcap on {money(liq)} liq")
    if chain != "solana" and cap and liq and 0.7 <= (liq / cap) <= 1.3 and n["created_dt"] and \
            (now_wat() - n["created_dt"]) < timedelta(hours=6):
        flags.append("LIQ ~ MCAP on a fresh EVM pool: probable fake pool until a real sell is shown")
    if n["vol_h1"] and liq:
        ratio = n["vol_h1"] / liq
        if ratio > 20:
            flags.append(f"WASH: 1h vol is {ratio:.0f}x liquidity")
        elif ratio > 10:
            flags.append(f"churn: 1h vol is {ratio:.0f}x liquidity")
    b, s = n["buys_h1"] or 0, n["sells_h1"] or 0
    if b > 3_000 and b > 8 * max(s, 1):
        flags.append(f"BOT FLOW: {b} buys vs {s} sells in 1h")
    if n["created_dt"] and (now_wat() - n["created_dt"]) < timedelta(hours=1):
        flags.append("UNDER 1H OLD: expect 50% wicks")
    if liq < 5_000 or (n["vol_h24"] or 0) < 1_000:
        flags.append("DEAD SIGNALS: liq under $5K or 24h vol under $1K")
    if mint and mint.get("checked"):
        fee = mint.get("transfer_fee")
        if fee and (fee.get("basis_points") or 0) > 0:
            bp = fee["basis_points"]
            auth = fee.get("fee_authority")
            flags.append(f"TRANSFER FEE {bp / 100:.2f}% (fee authority {'LIVE' if auth else 'null'}): fails the ~1.4% rule")
        if mint.get("mint_authority"):
            flags.append("MINT AUTHORITY LIVE")
        if mint.get("freeze_authority"):
            flags.append("FREEZE AUTHORITY LIVE")
        if mint.get("permanent_delegate"):
            flags.append("PERMANENT DELEGATE set (can move tokens)")
        if mint.get("transfer_hook_program"):
            flags.append("TRANSFER HOOK set (program can block transfers)")
    return flags


def verdict_for(n: dict, flags: list[str], clones: list[dict], ca: str) -> str:
    text = " ".join(flags)
    if "FAKE LIQ" in text or "WASH" in text:
        return "WASH"
    if "DEAD SIGNALS" in text:
        return "DEAD"
    if any(f.startswith(("TRANSFER FEE", "MINT AUTHORITY", "FREEZE AUTHORITY", "PERMANENT DELEGATE")) for f in flags):
        return "RUG RISK"
    # clone: a same-symbol token with bigger cap and earlier creation exists
    cap = n["mcap"] if n["mcap"] is not None else (n["fdv"] or 0)
    for c in clones:
        ccap = c["mcap"] if c["mcap"] is not None else (c["fdv"] or 0)
        if c["address"] != ca and ccap > (cap or 0) * 2 and c["created_dt"] and n["created_dt"] and c["created_dt"] < n["created_dt"]:
            return "CLONE"
    return "ALIVE"


def audit(ca: str, chain: str, rpc_url: str) -> dict:
    pairs = dex_token_pairs(chain, ca)
    out: dict = {"ca": ca, "chain": chain, "checked_wat": fmt_wat(now_wat())}
    if pairs is None:
        out["error"] = "DexScreener could not be reached; no verdict"
        out["verdict"] = "UNREACHABLE"
        return out
    if not pairs:
        out["error"] = "not indexed on DexScreener for this chain (wrong chain, too new, or dead)"
        out["verdict"] = "NOT INDEXED"
        return out
    nums = [pair_numbers(p) for p in pairs]
    nums = [n for n in nums if (n["address"] or "").lower() == ca.lower()] or nums
    best = max(nums, key=lambda n: n["liq_usd"] or 0)
    out["best_pair"] = best
    out["all_pairs"] = [{"dex": n["dex"], "quote": n["quote_symbol"], "liq": n["liq_usd"], "vol_h1": n["vol_h1"],
                         "url": n["url"]} for n in nums]
    out["vol_h1_all_pairs"] = sum((n["vol_h1"] or 0) for n in nums)
    out["vol_h24_all_pairs"] = sum((n["vol_h24"] or 0) for n in nums)
    mint = solana_mint_info(ca, rpc_url) if chain == "solana" else {"checked": False, "note": "EVM: check tax, renounced, proxy/pause, honeypot simulation by hand"}
    out["mint"] = mint
    # clones by symbol
    clones = []
    out["clone_search"] = "ok"
    if best["symbol"]:
        found = dex_search(best["symbol"])
        if found is None:
            out["clone_search"] = "could not reach DexScreener search; clone status unknown"
        else:
            tokens = list(best_pair_per_token(found).values())
            sym = (best["symbol"] or "").upper()
            clones = [t for t in tokens if (t["symbol"] or "").upper() == sym]
            clones.sort(key=lambda t: (t["created_dt"] or now_wat()))
    out["same_symbol_tokens"] = clones
    og = next((c for c in clones if (c["liq_usd"] or 0) > 5_000), None)
    out["earliest_with_liquidity"] = og
    out["flags"] = flags_for(best, mint, chain)
    out["verdict"] = verdict_for(best, out["flags"], clones, ca)
    return out


def print_human(a: dict) -> None:
    if a.get("error"):
        print(f"VERDICT: {a.get('verdict', 'NO VERDICT')} · {a['ca']} ({a['chain']}): {a['error']}")
        return
    b = a["best_pair"]
    cap = b["mcap"] if b["mcap"] is not None else b["fdv"]
    print(f"VERDICT: {a['verdict']}  ·  as of {a['checked_wat']}")
    print(f"${b['symbol']} \"{b['name']}\" ({b['chain']}) · {b['dex']} · paired vs {b['quote_symbol']}")
    print(f"CA {a['ca']} · ~{money(cap)} mcap · {money(b['fdv'])} FDV · {money(b['liq_usd'])} liq · "
          f"{money(a['vol_h1_all_pairs'])} 1h vol · {money(a['vol_h24_all_pairs'])} 24h vol")
    print(f"Change: {pct(b['chg_m5'])} 5m / {pct(b['chg_h1'])} 1h / {pct(b['chg_h6'])} 6h / {pct(b['chg_h24'])} 24h · "
          f"{b['buys_h1']}/{b['sells_h1']} buys/sells 1h · {b['buys_h24']}/{b['sells_h24']} 24h")
    print(f"Created {b['created_wat']} · ~{b['age']} old · boosts {b['boosts']} · labels {b['labels']}")
    print(f"Links: Dex {b['url']}")
    for w in b["websites"]:
        print(f"       site {w}")
    for s in b["socials"]:
        print(f"       {s}")
    m = a["mint"]
    if m.get("checked"):
        fee = m.get("transfer_fee")
        fee_s = "none" if not fee or not fee.get("basis_points") else \
            f"{fee['basis_points'] / 100:.2f}% (authority {'LIVE' if fee.get('fee_authority') else 'null'})"
        print(f"Contract: {m['program']} · mint auth {'LIVE' if m.get('mint_authority') else 'null'} · "
              f"freeze auth {'LIVE' if m.get('freeze_authority') else 'null'} · transfer fee {fee_s} · "
              f"metadata update auth {m.get('metadata_update_authority')}")
        if m.get("extensions"):
            print(f"          extensions: {', '.join(m['extensions'])}")
        if m.get("top10_accounts_pct") is not None:
            print(f"Holders: top1 account {m['top1_account_pct']}% · top10 accounts {m['top10_accounts_pct']}% "
                  f"({m['holders_note']})")
        else:
            print(f"Holders: {m.get('holders_note')}")
    else:
        print(f"Contract: {m.get('error') or m.get('note')}")
    if a["same_symbol_tokens"]:
        print("Same symbol on any chain (earliest first):")
        for c in a["same_symbol_tokens"][:8]:
            ccap = c["mcap"] if c["mcap"] is not None else c["fdv"]
            tag = " <- this CA" if (c["address"] or "").lower() == a["ca"].lower() else ""
            print(f"   {c['chain']:<10} {money(ccap):>9} mcap · {money(c['liq_usd']):>8} liq · {c['age']:>6} old · {c['address']}{tag}")
        og = a.get("earliest_with_liquidity")
        if og:
            print(f"   earliest with liquidity (OG candidate): {og['chain']} {og['address']} ({og['age']} old)")
    if a.get("clone_search") != "ok":
        print(f"Clones: {a.get('clone_search')}")
    print("Flags: " + ("; ".join(a["flags"]) if a["flags"] else "none from the automated checks"))
    print("Still by hand: socials age vs followers, templated shills, 'CA soon' sites, endorsement/disavowal, "
          "Bubblemaps bundles, RugCheck insiders, launch-buy sold?")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ca")
    ap.add_argument("--chain", default="solana")
    ap.add_argument("--rpc", default=os.environ.get("SOLANA_RPC_URL", PUBLIC_RPC))
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()
    a = audit(args.ca.strip(), args.chain.strip().lower(), args.rpc)
    print_human(a)
    if args.json:
        write_json(a, None if args.json == "-" else args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
