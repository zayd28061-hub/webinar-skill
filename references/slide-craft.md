# Slide craft — the copy laws and the 12 archetypes

## The governing idea

**The slide is the subtitle. The presenter is the voice.**

A webinar slide is not a document, a handout, or a memory aid. It is a visual anchor that holds one word or one image in the room while the presenter talks. The moment a slide contains a full spoken sentence, the audience reads ahead, finishes before you do, and stops listening. You have trained them to skim.

Consequence: the slide and the speaker note must **never contain the same words**.

---

## The copy laws

1. **One idea per slide.** If it needs "and", split it. If it needs a comma joining two clauses, split it.
2. **Seven words on a headline slide. Fourteen words maximum on any slide.** Two exceptions across the whole deck: one quote, and the offer stack.
3. **Keyword, not sentence.** Strip every article, hedge and connective the eye does not need. "The reason most coaches never get past this point is that they are guessing" → **"They are guessing."**
4. **Titles are claims, not labels.** "Agenda" → "What you will be able to do in an hour." "About me" → the one number. "Case study" → the result.
5. **Numbers get their own slide, at 200px+.** A number buried in a sentence is decoration. A number alone on a slide is evidence.
6. **One accent word per slide, maximum. Usually zero.** The rarity is the entire mechanism. If everything is highlighted, nothing is. Mark it `[[like this]]`.
7. **Their nouns, not yours.** Mine sales-call transcripts and DMs for the exact words. "Leads" not "top-of-funnel acquisition". The pain act is a transcription exercise, not a writing exercise.
8. **No lists longer than three.** Anything longer becomes a `build` — one item per slide, the earlier ones dimmed.
9. **No adjectives in the pain act.** "Frustrated", "overwhelmed", "struggling" are how the presenter feels about the audience. Replace every one with a concrete observable action at a specific time of day.
10. **Never end a slide on a comma or a colon.** A slide is a complete beat, not a fragment waiting for the next one.
11. **Punctuation earns its place.** Full stops are fine and good. Exclamation marks are never fine. Ellipses are a tell.
12. **Read every slide aloud as written.** If it sounds like something a person would actually say, it is probably too long for a slide.

### The 25-second test

Average a live webinar at one slide per 25-35 seconds. If a slide needs three minutes of talking, it is hiding four slides inside it. Split it and the energy of the whole session changes, because visual change is what resets attention.

---

## The 12 archetypes

Each has a `type` in `deck.json`. Fields are listed; everything is optional except `type` and `note`.

### `cover`
Opening frame. `title`, `subtitle`, `presenter`, `kicker`.
Holds for 10 seconds while people arrive. No logos, no "welcome".

### `section`
Act divider. `kicker` (act number), `title` (a claim, not a label).
Full-bleed accent-free. Its job is a hard visual reset so the audience feels the gear change. Roughly one per act, 8-10 in a full deck.

### `statement`
The workhorse — 40% of a deck. `text` (≤14 words), optional `sub` (≤10 words).
Big display type, centred or hard-left. Nothing else on the slide.

### `keyword`
`text` — one to three words, enormous (140-200px).
The highest-impact slide in the deck and the most underused. Use it on the paradigm shift, on the enemy's name, on the method's name, on the number that hurts.

### `number`
`value` (the figure, huge), `label` (what it is), optional `source`.
Never more than one number. Two numbers is a `contrast`.

### `contrast`
`left: {label, items[]}`, `right: {label, items[]}`.
What they do now vs what this replaces it with. Three items each, maximum. The most persuasive layout in the deck and it works because the eye does the arguing.

### `list`
`title`, `items[]` (max 3).
Use sparingly. Above three items, switch to `build`.

### `build`
`title`, `items[]`, `upto` (how many are revealed on this slide).
Emit the same slide N times with `upto` 1, 2, 3… Earlier items dim, the current one is live. This is how you present the sixteen-item list without a wall of text.

### `quote`
`text` (their words, verbatim, ≤30 words), `attrib`.
Only for the audience's own language or a client's. Never for a famous person — a quote from a billionaire in a sales webinar reads as filler.

### `proof`
`headline`, `start` (where they began), `event` (what happened), `duration` (how long), optional `img`.
Structured so the three facts land in a fixed order every time. Do not dress it up; the structure is the credibility.

### `diagram`
`title`, `svg` (inline SVG string) or `nodes[]` for the built-in flow renderer.
Draw the mechanism. A mechanism the audience can see is a mechanism they can repeat, and a mechanism they can repeat is one they believe.

### `stack`
`rows[]` of `{item, value}`, `total`, `price`.
The offer stack. The one slide allowed to be dense, because its density is the point — it is a visual argument about the value gap.

Also available: `question` (one question, silence, huge type), `image` (`src`, `caption`, full-bleed), `price` (`value`, `terms`), `cta` (`text`, `action`, `url`), `close` (final holding frame during Q&A, with the CTA still visible — most of the buying happens in Q&A and the screen must not go blank).

---

## Speaker notes

Every slide has a `note`. The note is a **spoken paragraph**, not bullets. Write it the way the presenter talks: contractions, short sentences, one idea, and a physical instruction where it matters.

```
"Hold here. Say nothing for three seconds. Let them read it.
Then: 'That number is not a marketing number. It's the number of
people who raised their hand and then never heard from you again.'"
```

Include the stage directions that change the room:
- **hold** — stay on this slide and be silent
- **advance fast** — three slides in fifteen seconds, this is a rhythm burst
- **check chat** — engagement beat, ask for a one-word answer
- **name the loop** — refer back to the promise from act 0

---

## Deck rhythm

Vary the archetypes. Six `statement` slides in a row and the audience stops seeing them. The pattern that holds a room:

```
statement · statement · keyword · statement · number · contrast · statement
· build · build · build · quote · section
```

Run a check before delivering: never more than four of the same type consecutively, and at least one `keyword`, `number` or `contrast` every eight slides.
