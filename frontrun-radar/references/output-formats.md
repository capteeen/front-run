# Output formats

Use these templates exactly. The user reads these on a phone between launches; the order (verdict, live board, ideas, pick, checks) is what makes them usable. Angle brackets are slots. Every CA gets its DexScreener link; every claim gets its source link.

Contents
1. Footer (every output)
2. Dig (hourly or on demand)
3. CA audit
4. Ticker check
5. Front-run list
6. Theme ideas
7. Satellite map
8. Launch kit (see launch-pack.md for contents)
9. Daily recap
10. Tech radar (morning)
11. Rebuild scan (other-chain tech to rebuild on Solana)
12. Alert
13. Missed-runner postmortem
14. Nothing-this-hour

## 1. Footer (every output)

```
Checked: <sources and tools actually used, with times>
Not checked: <what was skipped and why>
Could not reach: <endpoints or pages that failed>
Next: <one concrete next step>
Related idea: <one improved or combined idea building on earlier ideas in this conversation>
```

## 2. Dig

```
<HH:MM> WAT dig

Correction: <only if a previous pick died, dumped or turned out taken; facts and the new CA or status>

A) LIVE MARKET (as of HH:MM WAT)

1. $<TICKER> "<Display name>" (<chain>) - <one line: why this is the pick>
   CA <address> · ~$<mcap> mcap · $<liq> liq · $<vol1h> 1h vol · <chg1h>% 1h / <chg6h>% 6h / <chg24h>% 24h · <buys>/<sells> 1h · ~<age> old · created <HH:MM WAT>
   Links: Dex <url> · pump.fun <url> · site <url> · X <url> · source <url>
   Hygiene: <program> · fee <x>% (<authority>) · mint <on/off> · freeze <on/off> · metadata <mutable/locked> · <holders> holders · top10 <x>% · dev <x>% · insiders <n> (<tool>)
   Lore: <what happened, who, when, exact quote with link>
   What CT is missing: <the angle nobody has traded, with source>
   Avoid: <clone CA> (<reason: fake liq / wash / tax / no socials>) · <clone CA> (<reason>)
   Risk: <age, concentration, PvP, catalyst dependency, disavowal>
   Next catalyst: <event> at <HH:MM WAT, date> (<confidence>)

2. ...

3. ...

Skipped this hour: <name> (<reason>) · <name> (<reason>) · <names covered earlier today unchanged>

B) MINT IDEAS (checked open at HH:MM WAT)

1. $<TICKER> - display "<name>" · <EMPTY / DUST $x CA ...> · <launch now / prep / only if parent holds>
   Why: <one line tying it to the runner or catalyst>
   Bio: <paste-ready, under the create-page limit>
   Pitch: <why someone buys this instead of the runner>
   Hygiene: <platform> · <fee setup> · <paired token and its real CA if the meta is paired> · <creator-fee route if any and whether it is endorsed>
   Icon: <direction in one line; mascot or object; no official logos>
   Links: <source 1> · <source 2> · <related CA>
   Risk: <one line>

2. ...

Taken or weak: <names checked and rejected with status>

If one this hour: $<X>. If two: $<X> then $<Y>.

<footer>
```

## 3. CA audit

Use the reporting template at the end of `hygiene.md`. Verdict line first.

## 4. Ticker check

```
$<TICKER> - <EMPTY / DUST / TAKEN> as of HH:MM WAT
Exact matches: <chain> <CA> ~$<mcap> · $<liq> liq · <age> · <link>
Variants: <TICKERS> <status> · THE<TICKER> <status> · <misspelling> <status>
Near-duplicates to warn buyers about: <TICKERX ~$...>
Other chains: <chain> ~$<mcap> (<link>)
Dead history: <coin that printed and died under this word, date, peak>
Pre-launch signals: domains <which resolve> · telegram <exists/none> · X mentions last hour <n> · new pump tokens matching <n>
Verdict: <launch now / prep / drop> - <one line>
<footer>
```

## 5. Front-run list

```
Front-run list, next <14> days (as of HH:MM WAT)

1. Launch now (window open today)
- <catalyst> · <CONFIRMED/LIKELY/RUMOR> · <date, HH:MM WAT> · <source> · best $<T> (<status>) · backup $<T2> (<status>) · site: <one-line mechanic> · risk: <one line>

2. Launch soon (catalyst within 7 days)
- ...

3. Dated, next two weeks (calendar)
- <date> <event> · $<T> (<status>) · <source>

4. Secondary but clean
- ...

5. Reserve bench (ready if a meta rotates)
- ...

6. Don't touch
- <name>: <already printed / already launched / big coin on other chain / brand fake without phrase hook / crisis or death story / disavowed>

How I'd sequence it: tonight <...>; this week <...>; next week <...>; reserve <...>.
<footer>
```

## 6. Theme ideas ("get ideas for <theme>")

```
<Theme> ideas (as of HH:MM WAT)

Current state: <dates, latest official moves, physical ads, slogans, cast, events, each with a link>

Already burned: <name ~$mcap chain> · <name ~$mcap chain> · ...

Best 5 (ranked, forge score /25)
1. $<T> (<score>) - <why> · hook source <link> · site: <mechanic> · launch <when>
2. ...

Other open names: <one line each>

Avoid: <names with reasons>

Pick: $<T> (and $<T2>) at <time>.
<footer>
```

## 7. Satellite map

```
Satellites of $<RUNNER> (as of HH:MM WAT)
Runner: CA · ~$mcap · liq · age · link · what it is

Already taken in-cluster: <name ~$mcap> · <name ~$mcap> · ...

Still open (checked HH:MM WAT)
1. $<T> - <family: root / promise / verb / quote / unit / set / object / sequence / non-English> · <EMPTY/DUST> · <one-line why> · bio: <one line>
2. ...

If you only mint two: $<T> then $<T2>. Third: $<T3>.
Window closes: <event and time in WAT that ends the meta>
<footer>
```

## 8. Launch kit

Contents and order in `launch-pack.md`. Open with the GO / NO-GO block and the paste-ready coin fields so the user can mint from the first screen.

## 9. Daily recap

```
What you missed today in memecoins, <Month D>

- $<TICKER> hit $<peak> on <CHAIN> off <catalyst in plain words>, then <what happened>, it's at $<now> now
- $<TICKER> ...
(10 to 15 lines, ranked by what mattered, each with the number as of now; mix wins and collapses; one line per coin; chain always named)

Missed by the desk today: <coins over $500K that were not in the ledger, one line each, with the fix>
```

Plain words, no CT jargon, no links inside the bullets (links go in a separate "Sources" block if the user asks).

## 10. Tech radar (morning)

```
Tech radar, <Day Mon D> (scan ~HH:MM WAT)

What's already live
- <story> · <coin ~$mcap chain, link> · <one line on whether it is real, a fake pool, or dumping>

Early narratives you could launch first
1. <story> (<confidence>, <source>) - no coins yet / only dust
   $<T> - <site concept in one line>
   $<T2> - <site concept>
2. ...

Reveals in the next 48h
- <date HH:MM WAT> <event> · have $<T> ready · name the coin after whatever wins / ships

Watch: <one or two items not yet strong enough>
<footer>
```

## 11. Rebuild scan (other-chain tech to rebuild on Solana)

```
Other-chain tech to rebuild on Solana (as of HH:MM WAT)

Ship first: $<A> (<source project>) → $<B> → $<C>

1. <Project> $<T> (<chain>, ~$<FDV>) - <site> · <Dex>
   What it does: <mechanic in two lines>
   Why Solana lacks it: <one line>
   Rebuild: <what to keep, what to drop, what to make Solana-native>
   Names: $<CLEAN1> / <Display> · or $<CLEAN2> / <Display>  (one clean product word; no mashups)
2. ...

Skip: <projects and why: overlaps, pump clone, already on Solana, weak loop>
<footer>
```

## 12. Alert

```
ALERT | HH:MM WAT | <CONFIRMED/LIKELY/RUMOR>
Catalyst: <one line> · <link>
Ticker: $<T> (<status>, checked HH:MM)
Backup: $<T2> (<status>)
Window: <how long it stays open and why>
Action: launch now / prep / skip
Competition: <CA ~$mcap · liq · age · link> or none
Evidence: <the pre-launch signal that fired, with link>
```

## 13. Missed-runner postmortem

```
Missed runners, last 24h (as of HH:MM WAT)
- $<T> peaked $<x> on <chain> · catalyst: <what> started <HH:MM WAT, date> · coin launched <HH:MM WAT> · first public signal: <post/source, time> · why we missed it: <not scanning X / wrong lane / lag> · fix: <source, account, keyword or calendar entry added to sources.md>
```

## 14. Nothing-this-hour

```
<HH:MM> WAT: nothing worth depth this hour.
Scanned: <boards and lanes> · top movers were <3 names with one-word reasons to skip>.
Ledger rechecks: <names rechecked, any status changes>.
<footer>
```
