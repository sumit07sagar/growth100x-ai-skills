# Template picker — match the JOKE STRUCTURE, not the topic

The single biggest quality lever: identify the *shape* of the joke first, then pick the
template whose panels embody that shape. A meme lands when the format itself carries half
the punchline. All IDs below are memegen.link template IDs (209 total on the API — use
`make_meme.py search <keyword>` for anything not listed).

Line order matters. Run `make_meme.py info <id>` if unsure; examples below show order.

## Preference / comparison (X is bad, Y is good)

| id | Format | Lines (in order) |
|---|---|---|
| `drake` | Drakeposting | 1: rejected thing, 2: approved thing |
| `pooh` | Tuxedo Winnie the Pooh | 1: plain version, 2: fancy version of same thing |
| `db` | Distracted Boyfriend | 1: girlfriend (the neglected thing), 2: boyfriend (who), 3: passing girl (shiny new thing) — CHECK with `info db` |
| `gb` | Galaxy Brain (4 panels) | escalating "enlightenment", best when the "genius" final step is actually dumb (or secretly right) |
| `midwit` | IQ bell curve | 1: low-IQ take, 2: midwit cope (the long overcomplicated one), 3: high-IQ take (same as #1) — the joke is dumb & genius agree |

## Denial / coping / things are on fire

| id | Format | Use when |
|---|---|---|
| `fine` | This is Fine | someone ignoring an obvious disaster |
| `panik-kalm-panik` | Panik/Kalm/Panik | 1: scary thing, 2: false relief, 3: worse realization |
| `astronaut` | Always Has Been | shocking realization that was true all along (4 lines: setup Q, "always has been", …) — `info astronaut` |
| `afraid` | Afraid to Ask Andy | everyone pretends to know X, nobody dares ask |
| `harold` | Hide the Pain Harold | forced smile through suffering |

## Fake equivalence / mislabeling

| id | Format | Use when |
|---|---|---|
| `pigeon` | Is This a Pigeon? | someone confidently mislabels a thing. 1: who, 2: the thing, 3: "is this a X?" |
| `same` | They're the Same Picture | two "different" things that are identical. 1+2: the two things, 3: ALWAYS pass "" — the Pam subtitle is baked into the template image; writing it again duplicates it |
| `spiderman` | Spider-Man Pointing | two identical actors accusing each other |
| `woman-cat` | Woman Yelling at Cat | angry accusation vs unbothered party. 1: yell, 2: cat's deadpan reply |

## Plans that fall apart / self-sabotage

| id | Format | Use when |
|---|---|---|
| `gru` | Gru's Plan (4 lines) | steps 1-2 sensible, step 3 is the flaw, line 4 repeats line 3 (the double-take) |
| `wkh` | Who Killed Hannibal? | someone causes the problem then asks how it happened |
| `nails` | Hammering Nails Into Sand | confident effort, doomed method |
| `exit` | Left Exit 12 | car swerving to the irresponsible choice. 1: straight (sensible), 2: exit (what we do), 3: car label |
| `pool` | Mother Ignoring Drowning Kid | misplaced priorities. 1: favored kid, 2: drowning kid, 3: mother |

## Mock / dismiss / condescend

| id | Format | Use when |
|---|---|---|
| `spongebob` | Mocking Spongebob | mocking a quote — write line 2 In AlTeRnAtInG cApS yourself |
| `wonka` | Condescending Wonka | patronizing "oh, you do X?" |
| `kermit` | But That's None of My Business | passive-aggressive observation |
| `wddth` | We Don't Do That Here | politely shutting down a norm |
| `khaby-lame` | Khaby Lame Shrug | the obvious simple solution everyone overcomplicates |

## Hype / success / greed

| id | Format | Use when |
|---|---|---|
| `stonks` | Stonks | dumb decision framed as financial genius |
| `money` | Shut Up and Take My Money | instant enthusiasm for a product |
| `success` | Success Kid | small win celebrated hard |
| `oprah` | You Get a Car | giving everyone the same thing indiscriminately |
| `millers` | You Guys Are Getting Paid? (4 lines) | discovering others get something you never did |

## Questions / suspicion / realization

| id | Format | Use when |
|---|---|---|
| `fry` | Futurama Fry | "not sure if X or Y" |
| `philosoraptor` | Philosoraptor | fake-deep shower thought |
| `rollsafe` | Roll Safe | flawed galaxy-logic life hack ("can't fail if you never try") |
| `keanu` | Conspiracy Keanu | "what if…" paranoid thought |
| `scc` | Sudden Clarity Clarence | mid-party realization |
| `dwight` | Schrute Facts | "False." + pedantic correction |

## Group dynamics / arguments

| id | Format | Use when |
|---|---|---|
| `chair` | American Chopper Argument (6 lines) | heated argument where BOTH sides have a point |
| `handshake` | Epic Handshake | two rivals agreeing on one thing. 1: arm A, 2: arm B, 3: the shared thing |
| `balloon` | Running Away Balloon | held back from the thing you want. 1: you, 2: the balloon (goal), 3: what holds you back |
| `buzz` | X, X Everywhere | something suddenly ubiquitous |
| `elmo` | Elmo Choosing Cocaine (5 lines) | choosing the obviously worse option enthusiastically |

## Escalation formats (3-8 lines — check `info` first)

`ptj` Phoebe teaching Joey (8) · `wallet` Patrick's wallet denial loop (8) · `perfection` (6) ·
`stop` Stop it Patrick (6) · `spirit` fake Spirit Halloween costume (5) · `made` I Made This (5) ·
`right` Anakin & Padme "for the better, right?" (5) · `reveal` Scooby Doo unmasking (4) ·
`noah` What the Hell is This (4)

## Caption-writing rules (this is where memes die)

- **Short.** Each panel ≤ ~8 words. If a line wraps 3+ times, cut it.
- **Specific beats generic.** "SEO guys renaming their service to GEO" > "people rebranding things".
- **The punchline lives in the LAST panel.** Everything before is setup. Don't spoil early.
- **Don't explain the joke.** No "😂 so true!" energy inside the image, no hashtags in the image.
- **Casual register.** lowercase often reads funnier than Title Case; never corporate voice.
- **The reader must feel seen.** Target a pain the audience has personally felt this month.

## When NO template fits

Use custom mode (`make_meme.py custom`) with a user-supplied or generated base image, or
build a labeled-object meme in HTML/PIL. But try hard to fit a known template first —
recognition is 50% of why memes feel "trendy". If the topic is riding a very recent trend
(< 3 months old, likely not on memegen), search the web for the format's panel structure and
recreate it faithfully with PIL rather than approximating.
