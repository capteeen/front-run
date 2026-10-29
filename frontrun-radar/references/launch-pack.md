# Launch pack: contents, icon rules, copy rules, link order

A launch pack is everything the user needs to go from "I want to launch $X" to pressing create, posting, and defending the coin for its first two hours. The user is often minutes from minting, so the pack is delivered in two parts: the mint block first (status, fields, bio, icon direction, links), then the full pack. Save each pack to `launch-packs/<TICKER>/PACK.md` from `templates/PACK.md`, with the icon files beside it.

Contents
1. GO / NO-GO block
2. Coin fields (create page)
3. Icon rules
4. Bios (three versions)
5. Buy pitch and lore block
6. Links, in share order
7. X, Telegram, callout, community post, thesis
8. Site brief
9. Timing, kill switch, checklists
10. What goes in the website and X fields
11. Sibling packs

## 1. GO / NO-GO block

```
$<TICKER> - <GO / NO-GO / GO WITH CAVEAT> as of HH:MM WAT
Ticker: <EMPTY/DUST/TAKEN> (exact + variants, all chains, pump.fun search)
Pre-launch signals: domains <...> · telegram <...> · X mentions last hour <n> · new pump tokens matching <n>
Catalyst: <still live? source still up? confidence>
Competition: <CAs with numbers> or none
Window: <open / closing at HH:MM WAT because ... / gone>
```

NO-GO reasons that end the kit: ticker taken with liquidity and a post; the person or project disavowed; the story is a death, illness, arrest, crisis, a minor, or a slur (see guardrails); the window is gone (clone 12 to 48h after the original).

## 2. Coin fields (create page)

Fill every field the platform shows:

- Name (display): the human name, not the ticker ("Claude Gabagool", "x/place", "Opt Out").
- Ticker: uppercase, short, no brand mashups. If the platform allows non-Latin script and the angle is non-English, the display name carries the script and the ticker carries the romanization.
- Description: the short bio (section 4). Check the field's character limit on the live create page; keep a 230-character version and a 400-character version ready.
- Website: the primary proof link (the leak post, the blog post, the billboard photo, the filing) until the user has a site. Never the brand's official site.
- X: the user's own account or the coin's new account. Never the brand's or the person's official account; that reads as an official claim.
- Telegram: optional; include only if the user runs it.
- Platform and fee setup: plain pump.fun with standard fees (about 1.4% round trip) is the default. No Token-2022 transfer fee. No tracker or sniper fee add-ons unless the user asks. If the meta is paired launches, set the paired token to the real parent CA (verified, not a dust copy) and turn on holder rewards the way the runner did.
- Creator fee routing: only to a route the recipient has publicly accepted. Otherwise fees stay with the user.
- Image: the chosen icon, square, exported large (check the platform's current upload limit on the create page).

## 3. Icon rules

What prints: a mascot or an object with a face, flat, one or two colours, on black or one saturated field, readable at 48px inside a circle. Food characters, animals with one prop, a single glyph. The lore lives in the name and bio; the icon only needs to be instantly readable and a little funny.

What dies: text cards, code screenshots, walls of filing text, photoreal deli photos, anything that needs to be read.

Rules:
- Three concepts, ranked, each with a ready image-generation prompt (style, subject, pose, colours, background, "centered, square, no text").
- The same mark for coin icon, favicon and X pfp; a 1500x500 X banner (black bar, mark left, wordmark right) and a 1200x630 OG image.
- No official logos, wordmarks, product art or brand colour schemes copied. A style nod is fine; a trademark is not.
- No photographs of private individuals or minors. Public billboards and public campaign photos are reference for an original drawing, not the icon itself.
- When the user asks for a specific style (doodle lines, a lab's palette, a scratchy hand-drawn look), produce it, but still without the brand's actual mark.
- If the user does not like the icons, ask which of the three directions is closest and remix that one; do not restart from zero.

## 4. Bios (three versions)

- Short (pump bio, 230 characters or less): the hook, the receipt, the variants, the one-word tail. Ends with a plain "Unofficial. Not affiliated with <brand/person>." when a real brand or person is involved.
- Long (400 characters): adds the context chain (the family of names, why now, what is taken) and the same disclaimer.
- Plain English (for people who are not on CT): no jargon, no "CT", no "dust", no "0 hits". Three sentences a normal person understands.

Rules: say what leaked or happened, where, and when; never claim official, partner, charity or "fees go to X" unless true and accepted; never promise price; never use a slur or a minor's name.

## 5. Buy pitch and lore block

- Buy pitch: two lines. Why this ticker instead of the runner; what refreshes attention (every clip, every filing, every blog update). Honest about what it is: a meme on a receipt, not equity.
- Lore block: the full story in order (what, who, when, exact quotes, the codename table or the timeline), each line with its link. This is what the user pastes to the group when someone asks "what is this".

## 6. Links, in share order

1. Core proof first: the leak post, the blog post, the filing page, the billboard photo, the clip.
2. Context second: the mapping thread, the docs page, the second outlet.
3. "Why now" third: the dated catalyst (the sign-up close, the hearing, the release date, the "this week" post).
4. The user's own CA and DexScreener link last, added after mint.

Give the one-liner for group chats under the links.

## 7. X, Telegram, callout, community post, thesis

- X handles: three options with availability as of the check time; bio under 160 characters; pinned post; a four-post launch thread (hook, receipt, why now, disclaimer plus CA); ten reply lines for the comments.
- Telegram: group name, pinned message, three rules.
- Callout (for caller boxes, under 2,000 characters): "Calling $T at ~$<mcap>." then why in five lines, sources as bare URLs, "DYOR. Not financial advice."
- Community post: lore first, CA and Dex link, then sources. Do not open with "just launched" unless the user asks for a launch announcement.
- Long thesis: natural prose, 400 to 700 words, no bullet lists, honest about what the coin is and is not, ends on the one-word tail. Saved as THESIS.md.

## 8. Site brief

One page. Hero mechanic tied to the meme (a counter, a board, a reveal, a progress bar tied to mcap, a fake-but-obviously-a-joke global counter). Copy-CA button in the header. Nav: Coin · How · X. Near-black base and one accent. Clean sans for headings, mono for numbers. Footer disclaimer. Any joke counter reads as a joke, never as real data. Optional X player-card embed so the link renders inside posts.

## 9. Timing, kill switch, checklists

- Timing: exact launch time in WAT relative to the catalyst; what signal to watch; what the second wave is and when.
- Kill switch: the catalyst is denied, a bigger clone with a post and liquidity appears, the person disavows, the parent in a paired meta posts capitulation, the meta's new launches stop graduating.
- Pre-launch checklist: ticker and variants rechecked within 5 minutes; pre-launch signals rechecked; links work; image uploaded at the right size; burner launch wallet funded; site has a CA slot; first posts drafted; callout drafted.
- Post-launch watch (first 2 hours): copycats every 15 minutes (`scripts/new_tokens.py` filtered on the word), holder concentration, volume vs liquidity, X mentions, whether the catalyst confirmed or died. Report at 15, 30, 60, 120 minutes.

## 10. What goes in the website and X fields

Website: the main proof link (best lore receipt) until a site exists. X: the user's own account, or leave blank until a coin account exists. Never the brand's or the person's official account.

## 11. Sibling packs

When the user asks why a sibling name was not recommended, answer with the table: name, what it maps to, status, why it ranked lower (already shipped, crowded, weaker surprise). Then offer the sibling packs; the user may want the whole family.
