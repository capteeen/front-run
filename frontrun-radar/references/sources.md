# Sources: where to look, by lane

Every lane below is a standing search list. The agent in that lane scans all of it each sweep and adds anything new it finds to the ledger with a confidence tag. Accounts are named by category, not handle, on purpose: handles change, get suspended or get bought. Build the live handle list in the ledger notes and verify each handle exists before relying on it.

Contents
1. Market boards (META)
2. AI lane (RADAR-AI)
3. Tech lane (RADAR-TECH)
4. Crypto lane (RADAR-CRYPTO)
5. Culture and gaming lane (RADAR-CULTURE)
6. Macro and politics lane (RADAR-MACRO)
7. Demand signal boards (cross-check)
8. Endpoints the scripts use
9. Added from postmortems (append-only, dated)

## 1. Market boards (META)

- pump.fun: trending, "about to graduate", fresh graduations in the last 6h, search by ticker and by name. Also the pump.fun landing and marketing pages themselves (a past dig found unminted mascot characters on the official landing page).
- DexScreener: Solana trending, top gainers 1h / 6h / 24h, new pairs, latest paid profiles, latest boosts, top boosts. Same for Robinhood Chain, BSC, Base, ETH, HyperEVM, Arc. Cross-chain copies of a Solana runner usually appear within minutes; a bigger copy on another chain changes the verdict.
- GeckoTerminal trending (Solana and others) as a second opinion when DexScreener barely indexes a coin.
- Other launchpads: bonk.fun, Stonk Fun, four.meme (BSC Chinese crowd), Flaunch (Base), Clanker (Base), Virtuals, Zora. Rotation between pads is itself a narrative (a boycott, a contest, a new fee mechanic).
- Venue and platform tokens: when a pad's own token moves, coins paired with it move with it. Track paired-token launches (coins paired with a creator coin, a pad token, or a big memecoin instead of SOL).
- RugCheck, Bubblemaps, Larpcheck-style tools, honeypot checkers (EVM): for insiders, bundles, fresh wallets, dev sells, sell simulation.
- Solscan / Solana RPC: creation time, migration time, authorities, holders, Token-2022 extensions.
- X search (latest tab) for each runner's ticker and CA: who called it, with what follower counts, whether the shill posts are templated.

## 2. AI lane (RADAR-AI), highest priority

- Lab accounts and blogs: Anthropic, OpenAI, Google DeepMind, xAI, Meta AI, Mistral, DeepSeek, Moonshot (Kimi), Qwen / Alibaba, Zhipu, MiniMax, Nvidia, Microsoft AI, Amazon, Apple ML.
- CEO and staff posts: the CEOs, research leads, and the staff who tease launches the night before. Note each lab's shipping habit (weekday, US morning slot, "tomorrow" teasers).
- Leakers and trackers: accounts that diff API model lists, arena codenames, CLI configs, GitHub eval configs, app bundles. Build the list from who was first on the last three leaks. Verify each handle exists.
- Arena leaderboards (LMArena and peers): anonymous codenames in battles are the earliest public trace of a model. Food, mineral, animal and place codenames recur; map codename to shipped product when it lands and keep the table.
- API model lists, SDK release notes, docs and pricing pages, status pages: diff them. A new model string in a third-party eval site's code or a coding CLI is a leak with a receipt.
- GitHub: new org repos, commits mentioning model strings, config files with unreleased names. HuggingFace: new org repos, weight uploads, model cards.
- App store listings, app teardown posts, Chrome extension updates.
- AI drama and quotes: filings (an S-1 risk-factor line), hearings, viral demos, "AI said X" posts, benchmark claims, math or science claims ("solved half a prize problem"), safety incidents, outages, leaked chats.
- AI product dates: open-weights release dates, API shutoff dates, free-tier end dates, index or leaderboard release days, conference keynotes.

## 3. Tech lane (RADAR-TECH)

- Apple newsroom and rumor trackers, Google, Microsoft, Samsung, Meta, Tesla, SpaceX, Nvidia, Sony, Nintendo.
- Device store dates, preorder dates, delivery dates, OS release dates, keynotes, "in stores" days, regional launches (a Japan-only device launch with a giveaway ran a coin to eight figures and dumped on the draw).
- Physical events: a car at a museum, a plane banner, a blimp, a billboard, a pop-up, a product displayed in public. Physical proof photographs well and becomes icons.
- Outages, breaches, zero-days, hardware bugs, bug-bounty drama, data leaks (a provider showing other users' answers).
- Lawsuits, antitrust rulings, IPO filings and roadshows, earnings dates, executive changes (a head-of-product handover produced a meme runner within the hour).
- Company and founder banners, bios and pinned posts: a line that sits in a banner for months can become the coin the day someone notices it.

## 4. Crypto lane (RADAR-CRYPTO)

- Mainnets, testnets, TGEs, airdrop snapshots and claim dates, token unlock calendars, ETF decision deadlines, exchange listing announcements.
- Exploits, drains, hacks (relief-fund coins appear within hours), founder statements, deleted posts and reposts, display-name changes on founder accounts (a two-minute delete nuked a chart and the founder's temporary display name became a coin).
- Launchpad wars: boycotts, fee mechanics, trading contests with sign-up deadlines, new pad launches, pad mascots and AI agents, "paired with" tricks, free-launch promos.
- Lawsuits against platforms: complaint PDFs are lore mines (exact quotes, page numbers, category names). Read the filing, not the screenshot.
- Tokenized stocks and TradFi crossovers: exchange filings, FAQ PDFs, QR codes in newspaper ads, opt-out windows and their deadlines.
- KOL calls, whale wallets, caller farms. Note which callers post templated shills from fresh accounts; that is a red flag, not a signal.
- Conferences and their keynote days; prediction markets (word-of-the-year, ticker-odds markets) as sentiment.

## 5. Culture and gaming lane (RADAR-CULTURE)

- Games: release dates, trailers, delays, embargo lifts, review-code dates, preload dates, physical ad campaigns (billboards, kiosks, building wraps, blimps, banners), in-world brands and slogans, merch lines, launch-week events, cast lists, partner promos (a sports team playing as the game's city the night before launch).
- Movies and TV: release dates, trailers, finales, viral clips (a years-old animated clip can run on one platform repost), cast deaths and tributes (see guardrails: tribute tone, no exploitation, and in this skill death-based coins are off the table).
- Music: album drops, tours, viral sounds, chart records.
- Streamers and creators: safewords, catchphrases, staged bits, country tours, nicknames in other languages (a Chinese nickname for a US streamer ran a BSC coin to eight figures).
- Animals and zoos: new births and names (three baby capybaras named "I love you" in Vietnamese; a baby koala), famous pets and their owners' blogs (a famous meme dog's household), zoo deaths and successors.
- Sports: finals, transfers, records, viral quotes, boycotts, sponsor exits.
- Holidays and seasonal drops: Halloween items, Thanksgiving, Black Friday, Christmas, New Year, Ramadan, Valentine's, April Fools, national days.
- Food and brand limited drops; fast-food items returning; brand collabs.
- Faces and reaction images: a photo of an animal or object with a face that does 1M+ views in a few hours; find the original poster, the real name, the location, the poster's own words in replies.

## 6. Macro and politics lane (RADAR-MACRO)

- Elections, debates, hearings, court orders with dates, redaction fights, FOIA drops, viral congressional lines ("backed by nothing"), staff firings and short tenures, press-secretary-style memes.
- Regulation and agency moves: SEC, FCC, CFTC, Treasury and Mint announcements (a commemorative coin hitting banks), export controls, tariffs.
- Billionaire and politician posts: exact replies, insults, challenges, one-word posts. The exact phrase is the ticker; the paraphrase is not.
- Fed dates, CPI days, jobs days for macro-meme rotations.

Skip rules for this lane: no coins on a person in crisis, no coins on arrests, no slurs, no race-bait. See `guardrails.md`.

## 7. Demand signal boards (cross-check)

- X trending and X search latest tab: phrase velocity (views per hour, quote-tweet rate), "CA?" replies, "who's launching this" replies, caller "watching" posts without a CA.
- Google Trends breakout terms; TikTok trending sounds and hashtags; Reddit front pages of r/technology, r/gaming, r/ChatGPT, r/singularity, r/CryptoCurrency, r/wallstreetbets.
- Polymarket and Kalshi: new markets and markets with fast-rising volume.
- Mindshare trackers where available.
- Telegram: group creation for a word (t.me/<word>, t.me/<word>sol), member counts.
- Domains: <word>.fun, .lol, .xyz, .gg, .wtf, .meme, .app resolving means someone is building.

## 8. Endpoints the scripts use

- DexScreener search: `https://api.dexscreener.com/latest/dex/search?q=<query>` (all chains; filter base token symbol and name yourself)
- DexScreener token pairs: `https://api.dexscreener.com/tokens/v1/<chainId>/<address>` (chainId: solana, ethereum, bsc, base, hyperevm, etc.)
- DexScreener latest profiles: `https://api.dexscreener.com/token-profiles/latest/v1`
- DexScreener latest boosts: `https://api.dexscreener.com/token-boosts/latest/v1`, top boosts: `https://api.dexscreener.com/token-boosts/top/v1`
- Solana RPC (default public `https://api.mainnet-beta.solana.com`, set `SOLANA_RPC_URL` for a paid endpoint): `getAccountInfo` jsonParsed on the mint for authorities, program (Token vs Token-2022) and extensions (transferFeeConfig, permanentDelegate, transferHook); `getTokenLargestAccounts` for holder concentration; `getTokenSupply`.
- PumpPortal data websocket `wss://pumpportal.fun/api/data` with `{"method":"subscribeNewToken"}` streams new pump.fun tokens in real time (optional dependency `websockets`). This is the earliest signal that a name is being taken.
- GeckoTerminal public API as a fallback for pools DexScreener indexes slowly.

Rate limits exist on all of these. Cache within a run, batch tickers, and never retry a refused call in a loop.

## 9. Added from postmortems (append-only, dated)

Add one line per fix: date, what was missed, the source or keyword added. Example lines from past runs (keep yours below them):

- 2026-10-26: missed a leadership-change meme at a social platform; added "executive handover posts from product leads" to the Tech lane.
- 2026-10-26: missed a Vietnamese zoo naming story; added "zoo births and names, non-English sources" to Culture.
- 2026-10-27: missed a Chinese-nickname BSC runner; added "Chinese nicknames for Western creators, four.meme board" to Culture and Market boards.
