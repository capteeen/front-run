# Hygiene: ticker status, CA audits, fake liquidity, bots, endorsements

Everything in this file is a rule that came from a loss or a near-miss. Thresholds are starting points; when the market shifts, update them here with the date and the reason.

Contents
1. Ticker status (CHECKER)
2. CA audit (AUDITOR)
3. The ~1.4% rule and fee traps
4. Fake liquidity and wash detection
5. Bot flow and shill farms
6. Holder concentration and insiders
7. Endorsement and disavowal checks
8. Cross-chain and clone rules
9. Age and second-wave rules
10. Reporting template

## 1. Ticker status (CHECKER)

Run `scripts/check_ticker.py TICKER [TICKER ...]`. It searches DexScreener across all chains for exact symbol and name matches, then variants.

- TAKEN: same ticker or same name with mcap (or FDV when mcap is missing) over $50K, or 24h volume over $10K, on any chain; or a clone under 48h old with real traction (volume rising, liquidity over $20K).
- DUST: exists but under $10K mcap with near-zero volume. Usable. Say it exists, give the CA and chain, and note that the user's launch must beat it with a real site and post.
- EMPTY: nothing on DexScreener; then confirm on pump.fun search (name and ticker) and GeckoTerminal. Only then write "0 hits".

Always check: plural/singular, "THE" prefix, hyphen and space variants, common misspellings, number swaps (NINE1NINE vs 919), and near-duplicates that confuse buyers (FABLE vs FABLES, LAUNCH vs LAUNCHCAT). Always report bigger coins on other chains under the same word, and dead coins under the same word (a word that already printed and died carries baggage).

A "0 hits" claim that turns out wrong is the most embarrassing error this desk makes. VERIFY rechecks every EMPTY verdict by itself before output.

## 2. CA audit (AUDITOR)

Run `scripts/check_ca.py <CA> [--chain solana]`. Then write the audit in this order:

1. Verdict line: ALIVE / DEAD / CLONE / RUG RISK / WASH.
2. Identity: chain, ticker, display name, whether ticker equals name, icon description, links on the pair (site, X, Telegram), what the pump.fun or DexScreener page links as the source.
3. Numbers: mcap, FDV, liquidity, 1h and 24h volume, 5m / 1h / 6h / 24h change, buys vs sells (1h and 24h), pair created time and migration time in WAT, age.
4. Contract: token program (Token vs Token-2022), mint authority, freeze authority, metadata update authority, transfer fee config (basis points, max fee, fee authority live or null), permanent delegate, transfer hook. On EVM: tax, renounced, proxy that can pause, honeypot simulation result.
5. Holders: holder count, top 10 share, dev share, launch buy and whether it was sold, insiders flagged by RugCheck, bundled or sniper wallets by Bubblemaps, fresh-wallet share.
6. Socials: account creation date vs follower count, post count, whether the site says "CA soon" while the coin trades, whether the shills are templated.
7. Clones: same name on other chains and other CAs with their numbers; which one is the OG (earliest with real liquidity) and which one the attention moved to.
8. Dead signals: graduated then near-zero volume, DexScreener barely indexes it, liquidity under $5K, no social posts in 24h, chart flat after a spike.
9. One-line recommendation: skip, momentum only, OG to hold, or clean.

## 3. The ~1.4% rule and fee traps

Standard pump.fun coins cost roughly 1.4% round trip in platform fees. Anything materially above that is a trap unless the user chose it on purpose.

- Token-2022 transfer fee (3%, 4.5%/4.5%) fails the rule. If the fee authority is live, the deployer can change it at any time. Report both the fee and the authority.
- Robinhood Chain, Base, BSC and ETH coins: check tax and sell simulation before writing "clean". A pool where liquidity roughly equals market cap is usually a fake pool.
- "Fees to X person" setups (creator fees routed to a GitHub, an X handle or a charity): report whether the person has publicly accepted that route. If not, treat the claim as marketing.
- Pads that promise 100% buyback-and-burn: report whether a burn has actually happened (supply burned so far), not the promise.

## 4. Fake liquidity and wash detection

Flag and name the pattern:

- Mcap or FDV far above liquidity with no history (hundreds of thousands of dollars of "mcap" on a few hundred dollars of liquidity): fake mcap. Skip.
- Liquidity roughly equal to mcap on a brand-new EVM pool: fake pool until a real sell is shown.
- 1h volume above 10 to 20 times liquidity: wash or bot churn. Report the ratio.
- Volume in the millions on a pool with near-zero liquidity: fabricated volume. Skip and say why.
- A CA with a huge "mcap" that DexScreener barely indexes: not real.

## 5. Bot flow and shill farms

- Buys vastly outnumbering sells (tens of thousands of buys against a few thousand sells, or more than ten thousand buys on under $100K hourly volume): bot flow. Momentum only at best.
- Identical shill text from accounts with under 100 followers, created recently, posting the same CA: caller farm. Not a signal.
- An X account created years ago with one post and few followers now fronting a coin: bought handle.
- A site that says "CA soon" while the coin trades: the site and the coin are not the same team, or nobody is home.
- "Insider" and "fresh wallet" percentages from scanners: report the number and the tool; do not round it into a verdict without the other checks.

## 6. Holder concentration and insiders

- Report top 10 share, dev share, and the largest single unlabeled holder. A single unlabeled contract or wallet holding half the supply is a concentration risk regardless of the chart.
- Under 150 holders with top 10 over 50%: thin. Expect air pockets.
- Launch-buy sold already: say so. It changes the story of any "fee-funded" promise.

## 7. Endorsement and disavowal checks

Before recommending any coin tied to a person, product or project:

- Has the person or project acknowledged any CA? Which one? Link the post.
- Has the person disavowed ("there is no token", "nothing to do with crypto")? A disavowal means momentum only and no front-run of that person's name or project name.
- Are fees being routed to someone who has not opted in? Report it as unendorsed.
- If several CAs fight over a name and the person has not picked one, say "PvP across N CAs, no dev pick, momentum only".

## 8. Cross-chain and clone rules

- Search the word on every chain, not just Solana. A Base or HyperEVM original changes the Solana story (a Solana clone of a non-transferable HyperEVM token never stuck).
- Robinhood Chain and Arc copies with recognizable vanity addresses (repeated digits) and no socials: ignore in valuation, mention in the avoid list.
- When attention moves from an OG to a new CA with the event in its name, say so explicitly: which CA has the flow now, which one is bleeding.
- Clones 12 to 48h after the original: no distribution. Say it in the verdict.

## 9. Age and second-wave rules

- Under 1h old: expect 50% wicks. Say so in every under-1h audit.
- A "cleanest new CA" can rug within the hour after it is written up. Recheck every recommended CA at the start of the next run and open with a correction if it died.
- Second waves come from the source updating (a blog update, a court date, a store date, a contest close, an official account replying). Put the next catalyst and its time in WAT on every audit.

## 10. Reporting template

```
$TICKER "Display Name" (chain) - one-line why it matters
CA <address> · ~$<mcap> mcap · $<liq> liq · $<vol1h> 1h vol · <chg1h>% 1h / <chg24h>% 24h · <buys>/<sells> 1h · ~<age> old · created <HH:MM WAT> · migrated <HH:MM WAT>
Links: Dex · pump.fun · site · X · source post
Hygiene: <program> · fee <x>% (authority live/null) · mint <on/off> · freeze <on/off> · metadata <mutable/locked> · <holders> holders · top10 <x>% · dev <x>% · insiders <n> (<tool>) · bundles <x>% (<tool>)
Flags: <fake liq / wash / bot flow / bought handle / CA soon / disavowed / unendorsed fees>
Clones: <OG CA and numbers> · <bigger copy on other chain> · avoid <CA> (reason)
Risk: <age, concentration, catalyst dependency, PvP>
Verdict: ALIVE | DEAD | CLONE | RUG RISK | WASH · <one-line recommendation>
```
