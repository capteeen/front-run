# Scripts

Standard library only (Python 3.10+). The only optional dependency is `websockets` for the live pump.fun stream. Every script prints "could not reach ..." instead of inventing a number.

| Script | Use it for | Example |
|---|---|---|
| `check_ticker.py` | ticker status across all chains, variants, near-duplicates | `python3 check_ticker.py GABAGOOL JAJAJA` |
| `check_ca.py` | full CA audit: numbers, Solana authorities and Token-2022 fees, holders, clones, flags, verdict | `python3 check_ca.py <CA>` |
| `new_tokens.py` | taking layer: latest paid profiles and boosts, new pairs for a word, live pump.fun new-token stream | `python3 new_tokens.py --profiles --keywords gabagool` |
| `presence_check.py` | domains and Telegram groups for a word (someone prepping it?) | `python3 presence_check.py gabagool` |
| `watchlist.py` | the ledger: add, update, due rechecks, STALE marks, calendar | `python3 watchlist.py due` |

Run them from the `scripts/` folder or with `PYTHONPATH=scripts`. Set `SOLANA_RPC_URL` to a paid RPC for the taking layer; the public endpoint rate-limits.

Thresholds (TAKEN/DUST, wash ratios, bot-flow ratios, fee rule) live at the top of each script and mirror `references/hygiene.md`. Change them in both places with a dated note in `references/lessons.md`.

Typical hourly flow:

```
python3 watchlist.py due                       # what to recheck first
python3 check_ca.py <runner CA>                # audit each runner on the board
python3 check_ticker.py A B C D E              # satellite names
python3 presence_check.py a                    # top candidates
python3 new_tokens.py --profiles --boosts --keywords a,b,c
python3 watchlist.py update <id> --status EMPTY --kit brief
```

During a launch window, keep `python3 new_tokens.py --stream --keywords <word>,<variant>` running in a second terminal.
