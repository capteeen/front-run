#!/usr/bin/env python3
"""Watchlist ledger: one row per idea, never deleted.

Usage:
  python3 watchlist.py init                                   # create watchlist.json from the template schema
  python3 watchlist.py add --id gabagool --ticker GABAGOOL --display "Claude Gabagool" \
      --catalyst "leaked model codename" --confidence RUMOR --catalyst-time "2026-10-27 18:00" \
      --sources https://x.com/...,https://... --trigger "launch now" --status EMPTY
  python3 watchlist.py update gabagool --status DUST --status-detail "solana <CA> ~$3K" --kit full \
      --pack launch-packs/GABAGOOL/PACK.md
  python3 watchlist.py update gabagool --outcome launched --notes "minted 18:40 WAT"
  python3 watchlist.py due                                    # rows due for recheck; marks STALE
  python3 watchlist.py list [--open] [--json]
  python3 watchlist.py calendar --days 14                     # rows with a catalyst time in the window

Recheck cadence (SKILL.md §8): every 30 min inside 24h of the catalyst, every 6h otherwise.
An EMPTY/DUST verdict older than 30 min is STALE: recheck before any 'mint' line.
All times are WAT (UTC+1). Use --file to point at a different ledger.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

from _common import WAT, now_wat

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "watchlist.json")
DEFAULT_FILE = "watchlist.json"
FMT = "%Y-%m-%d %H:%M"


def load(path: str) -> dict:
    if not os.path.exists(path):
        print(f"{path} not found; run: watchlist.py init", file=sys.stderr)
        sys.exit(2)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path: str, data: dict) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def parse_wat(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.strptime(s, FMT).replace(tzinfo=WAT)
    except ValueError:
        print(f"bad time '{s}', expected 'YYYY-MM-DD HH:MM' in WAT", file=sys.stderr)
        sys.exit(2)


def stamp() -> str:
    return now_wat().strftime(FMT)


def cmd_init(args) -> None:
    if os.path.exists(args.file) and not args.force:
        print(f"{args.file} already exists (use --force to overwrite)")
        return
    with open(TEMPLATE, encoding="utf-8") as f:
        data = json.load(f)
    data["rows"] = []
    save(args.file, data)
    print(f"created {args.file}")


def cmd_add(args) -> None:
    data = load(args.file)
    if any(r["id"] == args.id for r in data["rows"]):
        print(f"row '{args.id}' exists; use update", file=sys.stderr)
        sys.exit(2)
    now = stamp()
    row = {
        "id": args.id,
        "ticker": args.ticker.upper().replace("$", ""),
        "display_name": args.display or "",
        "backup_ticker": (args.backup or "").upper().replace("$", ""),
        "catalyst": args.catalyst or "",
        "confidence": args.confidence or "SINGLE SOURCE",
        "catalyst_time_wat": args.catalyst_time or None,
        "sources": [s for s in (args.sources or "").split(",") if s],
        "status": args.status or "EMPTY",
        "status_detail": args.status_detail or "",
        "last_checked_wat": now,
        "recheck_every_min": args.recheck or 360,
        "competitor_cas": [],
        "prelaunch_signals": {"domains": [], "telegram": [], "x_mentions_1h": 0, "new_tokens_matching": 0},
        "trigger": args.trigger or "hold",
        "kit_status": args.kit or "none",
        "pack_path": args.pack or None,
        "outcome": "open",
        "notes": args.notes or "",
        "created_wat": now,
        "updated_wat": now,
    }
    parse_wat(row["catalyst_time_wat"])
    data["rows"].append(row)
    save(args.file, data)
    print(f"added {row['id']} (${row['ticker']}) status {row['status']} trigger '{row['trigger']}'")


def cmd_update(args) -> None:
    data = load(args.file)
    row = next((r for r in data["rows"] if r["id"] == args.id), None)
    if row is None:
        print(f"no row '{args.id}'", file=sys.stderr)
        sys.exit(2)
    changed = []
    for field in ("ticker", "display", "backup", "catalyst", "confidence", "catalyst_time", "status",
                  "status_detail", "trigger", "kit", "pack", "outcome", "notes", "recheck"):
        val = getattr(args, field, None)
        if val is None:
            continue
        key = {"display": "display_name", "backup": "backup_ticker", "catalyst_time": "catalyst_time_wat",
               "kit": "kit_status", "pack": "pack_path", "recheck": "recheck_every_min"}.get(field, field)
        if key in ("ticker", "backup_ticker"):
            val = val.upper().replace("$", "")
        if key == "catalyst_time_wat":
            parse_wat(val)
        row[key] = val
        changed.append(key)
    if args.sources:
        row["sources"] = list(dict.fromkeys(row.get("sources", []) + [s for s in args.sources.split(",") if s]))
        changed.append("sources")
    if args.competitor:
        row["competitor_cas"] = list(dict.fromkeys(row.get("competitor_cas", []) + [args.competitor]))
        changed.append("competitor_cas")
    if args.status is not None or args.checked:
        row["last_checked_wat"] = stamp()
        changed.append("last_checked_wat")
    row["updated_wat"] = stamp()
    save(args.file, data)
    print(f"updated {row['id']}: {', '.join(changed) or 'nothing'}")


def due_rows(data: dict) -> list[tuple[dict, str]]:
    now = now_wat()
    out = []
    for r in data["rows"]:
        if r.get("outcome") not in (None, "open"):
            continue
        last = parse_wat(r.get("last_checked_wat"))
        cat = parse_wat(r.get("catalyst_time_wat"))
        cadence = int(r.get("recheck_every_min") or 360)
        if cat and abs((cat - now).total_seconds()) <= 86400:
            cadence = min(cadence, 30)
        reason = None
        if last is None or (now - last) > timedelta(minutes=cadence):
            reason = f"recheck due (cadence {cadence} min, last {r.get('last_checked_wat')})"
        if r.get("status") in ("EMPTY", "DUST") and last and (now - last) > timedelta(minutes=30):
            r["status"] = "STALE"
            reason = reason or "open verdict older than 30 min"
        if reason:
            out.append((r, reason))
    return out


def cmd_due(args) -> None:
    data = load(args.file)
    rows = due_rows(data)
    save(args.file, data)  # persists STALE marks
    if not rows:
        print(f"nothing due as of {stamp()} WAT")
        return
    print(f"due for recheck as of {stamp()} WAT:")
    for r, reason in rows:
        print(f"  {r['id']:<18} ${r['ticker']:<12} {r['status']:<6} {r.get('trigger','')!s:<24} {reason}")


def cmd_list(args) -> None:
    data = load(args.file)
    rows = data["rows"]
    if args.open:
        rows = [r for r in rows if r.get("outcome") in (None, "open")]
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    print(f"{len(rows)} rows ({args.file})")
    for r in rows:
        print(f"  {r['id']:<18} ${r['ticker']:<12} {r['status']:<6} kit {r.get('kit_status','none'):<5} "
              f"{r.get('outcome','open'):<8} cat {r.get('catalyst_time_wat') or '-':<16} {r.get('trigger','')}")


def cmd_calendar(args) -> None:
    data = load(args.file)
    now = now_wat()
    end = now + timedelta(days=args.days)
    rows = []
    for r in data["rows"]:
        cat = parse_wat(r.get("catalyst_time_wat"))
        if cat and now - timedelta(hours=6) <= cat <= end:
            rows.append((cat, r))
    rows.sort(key=lambda x: x[0])
    print(f"catalysts in the next {args.days} days (WAT):")
    for cat, r in rows:
        print(f"  {cat.strftime(FMT)}  ${r['ticker']:<12} {r['status']:<6} {r.get('confidence',''):<13} {r.get('catalyst','')}")
    if not rows:
        print("  none")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=DEFAULT_FILE)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_init)

    def common(p):
        p.add_argument("--ticker")
        p.add_argument("--display")
        p.add_argument("--backup")
        p.add_argument("--catalyst")
        p.add_argument("--confidence", choices=["CONFIRMED", "LIKELY", "RUMOR", "SINGLE SOURCE"])
        p.add_argument("--catalyst-time", dest="catalyst_time", help="'YYYY-MM-DD HH:MM' in WAT")
        p.add_argument("--sources", help="comma-separated URLs")
        p.add_argument("--status", choices=["EMPTY", "DUST", "TAKEN", "STALE"])
        p.add_argument("--status-detail", dest="status_detail")
        p.add_argument("--trigger")
        p.add_argument("--kit", choices=["none", "brief", "full"])
        p.add_argument("--pack")
        p.add_argument("--notes")
        p.add_argument("--recheck", type=int, help="minutes between rechecks (default 360)")

    p = sub.add_parser("add")
    p.add_argument("--id", required=True)
    common(p)
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("update")
    p.add_argument("id")
    common(p)
    p.add_argument("--outcome", choices=["open", "launched", "died", "missed", "dropped"])
    p.add_argument("--competitor", help="'chain:CA ~$mcap' to append")
    p.add_argument("--checked", action="store_true", help="stamp last_checked without changing status")
    p.set_defaults(fn=cmd_update)

    p = sub.add_parser("due")
    p.set_defaults(fn=cmd_due)

    p = sub.add_parser("list")
    p.add_argument("--open", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("calendar")
    p.add_argument("--days", type=int, default=14)
    p.set_defaults(fn=cmd_calendar)

    args = ap.parse_args()
    if args.cmd == "add" and args.ticker is None:
        ap.error("add requires --ticker")
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
