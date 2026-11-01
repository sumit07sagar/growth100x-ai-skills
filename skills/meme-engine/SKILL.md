---
name: meme-engine
description: Trendy-meme production engine. Given any topic, frustration, hot take, news item, or bit of context, find the funniest angle, pick the meme format whose structure fits the joke (or research what's trending right now), generate one finished meme image, and deliver it with a ready-to-post caption. Use this whenever the user says "meme this", "make a meme", "run the meme engine", asks for a funny/relatable image about a topic, wants meme content for Twitter/X, LinkedIn, WhatsApp or a client, or just rants about something and asks you to make it shareable — even if they never say the word "meme".
---

# Meme Engine

Turn any topic into one finished, shareable meme image. The user gives context ("meme this:
clients who ghost after the proposal"); you deliver a single image that would make the target
audience stop scrolling.

## Why one meme, not options

The user wants a finished asset, not a brainstorm. Commit to the strongest angle. If they
don't like it, they'll say so and you iterate — that loop is faster than presenting three
mediocre options.

## Workflow

### 1. Find the joke (most important step)

Before touching any tool, work out what's actually funny here. Ask: who is the audience, what
pain or absurdity do they *personally* feel, and what's the gap between how things are
presented vs how they really are? That gap is almost always the joke. Write the punchline as
one sentence first. If you can't state the joke in one sentence, you don't have one yet —
dig for a sharper angle rather than proceeding with a weak one.

If the user's context is thin (just "make a meme about AI"), pick the freshest specific angle
yourself rather than asking — a meme about "AI" is nothing; a meme about "founders calling a
system prompt their proprietary AI model" is something.

### 2. Trend check (only when it earns its keep)

Do ONE quick web search when: the topic is tied to current news, the user asked for
"trending", or the meme will be posted to a fast-moving feed (Twitter/X). Search for what
angle/discourse is hot on the topic right now — newsjacking a live conversation multiplies reach.
Skip the search entirely for evergreen relatable humor; don't let research delay a 2-minute task.

### 3. Pick the format

Read `references/templates.md` and match the STRUCTURE of your joke (comparison, denial,
fake-equivalence, plan-falls-apart, escalation…) to a template. The format should carry half
the punchline. If nothing in the reference fits, run
`python3 scripts/make_meme.py search <keyword>` against the live API (209 templates),
and only fall back to custom-image mode after that.

### 4. Write the caption text

Follow the caption rules at the bottom of `references/templates.md`: short lines, punchline
last, specific over generic, casual register, never explain the joke. Check the template's
line order with `make_meme.py info <id>` when unsure — wrong line order ruins the joke.

### 5. Generate

```bash
python3 scripts/make_meme.py template <id> "line 1" "line 2" -o <output>.jpg
# or, for a user-supplied / generated base image:
python3 scripts/make_meme.py custom <image> --top "..." --bottom "..." -o <output>.jpg
```

Save to a `meme-engine-output/` folder in the working folder, named `YYYY-MM-DD-<slug>.jpg`.

### 6. Verify by LOOKING at it

Open the generated image with the Read tool and actually look: text not clipped or
overflowing, lines on the right panels, joke reads in under 3 seconds. A meme with mangled
text is worse than no meme. If a line is squeezed, shorten the text and regenerate — don't
ship it hoping it's fine.

### 7. Deliver

Present the image file to the user, plus:

- **Suggested post caption** — one casual line to accompany the image on social (the image
  carries the joke; the caption just tees it up or adds a wink). No hashtag spam.
- One line on why this format/angle (a sentence, not an essay).

If the user gives feedback ("less niche", "make it about X instead"), regenerate — iteration
is cheap, so treat feedback as a new punchline hunt, not just a text swap.

## Quality bar

A meme earns a share when the viewer thinks "this is literally me / my job / my client".
Generic = dead on arrival. If your draft caption would work for any industry, it's too
generic — sharpen until it could only have been written by someone inside the audience's world.
