# Pre-launch detection: knowing before it launches

The user's standing instruction: "everything launched, we should know before it happens." Nobody sees every launch, but almost every launch leaves a trail minutes, hours or weeks ahead. This file organizes those trails into layers by lead time. PRELAUNCH scans all layers every sweep and raises an alert when a name on the ledger shows any of these signs.

Contents
1. The five layers
2. Calendar layer (weeks ahead)
3. Leak layer (days to hours ahead)
4. Velocity layer (hours to minutes ahead)
5. Taking layer (seconds to minutes ahead): is someone minting my word right now
6. Satellite layer (the 10 minutes after a runner appears)
7. Rotation layer (metas forming)
8. Alert rules
9. What this cannot do

## 1. The five layers

| Layer | Lead time | What it catches |
|---|---|---|
| Calendar | weeks | dated events: releases, keynotes, store dates, hearings, unlocks, contests |
| Leak | days to hours | model strings, codenames, configs, filings, trademark and FCC records, teasers |
| Velocity | hours to minutes | a post going viral before a coin exists; demand signals |
| Taking | seconds to minutes | a name being minted, a domain resolving, a group created, a paid profile |
| Satellite | 10 minutes after a runner | the cluster around a runner before it is farmed |

A name that appears in two layers at once (a leak plus velocity, a calendar item plus a domain resolving) is the highest-priority alert.

## 2. Calendar layer (weeks ahead)

Keep a rolling 30-day calendar in the ledger. Sources per lane are in `sources.md`. Each entry: event, exact time converted to WAT, confidence tag, two source links, the words people will use that day, and the ticker candidates already checked for it.

Typical entries: game release, embargo lift, review-code date, preload date, delivery date; device "in stores" day, keynote, OS release; open-weights release date, API shutoff date, index release day, conference keynote; mainnet, TGE, unlock, ETF decision, listing; trading-contest sign-up close (to the hour); hearing, court deadline, redaction fight, election day; album drop, finale, tour date; zoo and pet events the owner announced; seasonal items with end dates; sports fixtures that tie into a launch (a team playing as a fictional city the night before a game release).

Recheck calendar tickers at 72h, 24h, 6h and 2h before the event. Most calendar names are taken between 24h and 6h before; a name still open at 24h should be minted or dropped, not watched.

## 3. Leak layer (days to hours ahead)

- Model strings and codenames in third-party eval sites, coding CLIs, SDK diffs, GitHub eval configs, app bundles, arena battles. A leaked string with a receipt is a launchable name even before the product ships. Keep the codename-to-product table current so the next codename on the list is known before it leaks widely.
- Filings: S-1s, 8-Ks, court complaints and amended complaints, FAQ PDFs, trademark filings, FCC device filings, domain registrations by companies, job posts naming unreleased products.
- Teasers: an official account posting "tomorrow", a puzzle, a countdown site, a changed banner, a changed bio, a pinned post swap.
- Journalist and leaker "exclusive" posts; embargoed-story tells (several outlets quiet on one topic, then a burst at the same minute).
- Physical world: ads going up (billboard photos appear on local accounts days before the campaign is covered), venue bookings, museum displays.

Each leak item becomes a ledger row with trigger "launch when confirmed" or "launch T-24h", plus the words to check. Check the words immediately; leaks get minted within hours.

## 4. Velocity layer (hours to minutes ahead)

Signs a post is about to become a coin:

- A post from an account with under 5,000 followers crossing 100K views in under an hour, or any post crossing 1M views in a few hours, on a visual (an animal face, an object, a reaction image) or a quotable line.
- Quote-tweet rate rising; replies filled with "CA?", "someone launch this", "ticker?", "who's dev"; callers posting "watching" without a CA.
- The same phrase appearing in several big accounts' posts within an hour.
- Mentions-per-hour jumping an order of magnitude (10/hr to 300/hr) on a name or phrase.
- Prediction-market pages for the event getting millions of views.
- Google Trends breakout on a new term; TikTok sound climbing.

Action: run the satellite map on the post itself (poster's name, the subject's real name, the exact caption, the object, the location, the non-English form), check all names, and alert with "launch now" on the ones still open. The original poster's own words in the replies are the best bios.

## 5. Taking layer (seconds to minutes ahead): is someone minting my word right now

For every name the user wants (every ledger row with kit status brief or full), check these every sweep, and every 5 minutes inside the launch window:

- pump.fun new-token stream (PumpPortal websocket, `scripts/new_tokens.py --stream`) filtered by the word and its variants. A match means the name is being taken this second.
- DexScreener latest profiles and boosts (`scripts/new_tokens.py --profiles`): a paid profile or boost on a token minutes old means a team is spending on that name.
- DexScreener search for the word: any new pair in the last hour.
- Domains: `<word>.fun`, `.lol`, `.xyz`, `.gg`, `.wtf`, `.meme`, `.app`, `.io` resolving (`scripts/presence_check.py`). A fresh resolving domain with a "CA soon" page is a launch in progress.
- Telegram: `t.me/<word>`, `t.me/<word>sol`, `t.me/<word>coin` existing with members.
- X: a new account named after the word created in the last 24h; "$WORD" mentioned in the last hour by anyone; a caller posting the word with "soon".
- Cross-chain: the same word appearing on Robinhood Chain, Base or BSC first; Solana usually follows within minutes.
- Fresh tokens with the same name on several chains inside a few minutes: a clone war is starting; the OG decides within the hour.

Action when any of these fires on a ledger name: alert immediately with "launch now or drop" and the evidence. Being second by ten minutes is usually being last.

## 6. Satellite layer (the 10 minutes after a runner appears)

Covered in `satellite-mapping.md`. The timing rule: the map must be done within 10 minutes of the runner appearing on the board, with every name checked and the top two packed. After an hour the cluster is farmed. Past clusters were fully taken (backwards spelling, test launch, animal, mascot) within a few hours by the platform team itself.

## 7. Rotation layer (metas forming)

Count launches per theme per hour on pump.fun and DexScreener new pairs. A theme going from 0 or 1 runners to 3 or more in under 6h is a rotation alert: stock-ticker backronyms, paired-with-parent launches, anti-pad boycotts, AI-cyber, quantum, codename leaks, a game's launch campaign. On a rotation alert, pre-generate the cluster for that theme (every stock ticker not yet taken, every laugh word, every pad promise) and check them all before the second wave.

Exhaustion alert: new launches in the theme stop graduating, or the parent of a paired meta posts "capitulation". Stop recommending satellites in an exhausted theme.

## 8. Alert rules

- One alert per name per trigger. Do not re-alert on the same evidence.
- Alert format in `output-formats.md` §Alert: time, confidence, catalyst with link, ticker status with check time, backup, window length, action (launch now / prep / skip), competition.
- Alerts about a name being taken carry the competitor's CA and numbers so the user can decide to still launch (if the competitor is dust with no site) or drop (if it has liquidity and a post).
- Never alert without a live recheck in the last 5 minutes.

## 9. What this cannot do

- It cannot see private group chats, unlisted sites or a team's wallet before they act. The first signal for a fully private launch is the mint itself; the stream in the taking layer is the only defense, and it only helps the user beat clones, not the OG.
- X search and view counts can lag or be rate limited; say when a velocity read is partial.
- The public Solana RPC and DexScreener rate-limit; use a paid RPC for the taking layer when the user has one.
- Nothing here predicts which open name will run. It only makes sure the user is not surprised, and that when a name runs, the user had the chance to be first.
