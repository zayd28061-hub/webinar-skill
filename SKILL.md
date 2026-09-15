---
name: webinar
description: Build a complete, presentation-grade webinar deck (100-200 slides) plus the surrounding funnel. Interviews you deeply on offer, ICP, mechanism, proof and objections, ingests your docs, brand guidelines, inspiration and images, then writes and renders every slide. Use when the user says "/webinar", "build my webinar", "webinar slides", "webinar deck", "masterclass slides", "write my webinar script", or "presentation for my offer".
---

# /webinar — the webinar deck builder

You are building a **live-presented sales webinar**: a 60-90 minute argument that ends in a purchase decision. Not a lecture. Not a slide document. A sequenced psychological argument where the slides are the subtitles and the presenter is the voice.

The deck is normally **120-180 slides**. That is not a lot of content, it is one beat per slide. A 70 minute webinar at 150 slides averages 28 seconds a slide. Slides that hold for three minutes are the single most common reason a webinar dies.

---

## Hard rules, non-negotiable

1. **Never write the deck before the interview is finished.** A deck built on assumptions is worthless and obvious.
2. **One idea per slide.** If a slide needs the word "and", it is two slides.
3. **The slide carries the keyword. The mouth carries the sentence.** Never put the spoken sentence on the slide. Never read a slide out loud.
4. **Max 7 words on a headline slide. Max 14 words on any slide, ever.** Exception: one quote slide and the offer stack.
5. **Never invent proof.** If the user has no client result, no number, no testimonial, say so on the slide plan and route around it. Fabricated proof is the fastest way to destroy a deck.
6. **Titles are claims, not labels.** "Agenda" is dead. "You do not have a lead problem" is alive.
7. **Every slide gets a speaker note.** The note is what they say. The slide is what the audience reads. They are never the same words.
8. **Ask before overwriting** an existing deck, brand file, or DESIGN.md.

---

## Phase 1 — The interview (10 questions, asked in 4 batches)

Ask these **open-ended, in bulk batches, never as multiple choice**. Wait for each batch before sending the next. Push back if an answer is vague: "anyone" is not an ICP, "get results" is not an outcome.

**Batch A — the offer and the room (Q1-Q3)**

1. Finish this sentence out loud, the way you would say it to a friend: **"I help ___ do ___ so they can ___."** One outcome. Not three.
2. **Who exactly is in the room, and who is it explicitly NOT for?** Give me revenue band, what they already tried, what they believe about themselves that is wrong. The exclusion sentence is the highest-leverage line in the whole deck, it is what makes everyone else feel chosen.
3. **What is the price, what do they actually get (list the deliverables), and is there a guarantee?** People buy a list of things, not an outcome alone.

**Batch B — the mechanism and the enemy (Q4-Q6)**

4. **What have they already tried that stopped working, in their words?** This becomes the enemy. Name a behaviour, never a person or a company.
5. **What do you call your method, and what are its 3 steps?** A tip is free advice anyone can find. A named method is something only you have. Three steps maximum — more and they stop believing they can do it.
6. **What is the paradigm shift?** Not "here is a better way to do what you have been trying." It is "what you have been trying to do is solving the wrong problem, and here is the actual problem." If you cannot state this in one sentence, the webinar has no spine. This is the most important answer in the interview.

**Batch C — proof, objections, and the first week (Q7-Q9)**

7. **The client closest to the room** — not your biggest result, the one most like the people watching. Where they started, what happened, how long it took. And your single best real number.
8. **The three objections you actually hear** in real conversations, in their words. Not the ones you imagine.
9. **What do they actually DO in week one with you? Monday morning, not the outcome in six months.** This is the most skipped slide in every deck on earth and it is the one that decides the sale.

**Batch D — logistics and why (Q10)**

10. **Traffic source (warm list / cold ads / organic), what happens after the webinar (book a call or buy directly), target number of clients from this one, and why you personally do this.** The why goes on a slide in act 3, never slide one.

If they have run a webinar before, also ask for: registered, turned up, bought, booked. Score it against `references/benchmarks.md` and open the deck build with a diagnosis instead of a plan.

## Phase 2 — Documents

> "Drop in anything you already have: old webinar scripts, your offer doc, sales call transcripts, onboarding docs, analytics exports, client testimonials, your DMs, past decks. Paths or paste. Sales call transcripts are worth more than everything else combined because they contain their exact words."

Read every file given. Mine specifically for: their literal phrasing (goes into the pain act verbatim), objections, and any real number.

## Phase 3 — Guidelines and inspiration

> "Any brand guidelines, a DESIGN.md, a style guide, fonts, colours? And any decks or presentations whose look you want — links, screenshots, or a name."

- If a `DESIGN.md` or brand file exists in the project, **read it and obey it**.
- If they give inspiration images, read them and extract: type scale, contrast ratio, layout density, accent discipline, whether type sits on image or on flat ground.
- If they give nothing, propose a system and get approval before rendering. Default to `references/design-system.md`.

## Phase 4 — Images

> "Any images you want in? Product shots, screenshots, your face, client screenshots, charts, diagrams. Give me paths and tell me roughly where each belongs."

Copy them next to the deck and reference by relative path. **Never AI-generate or alter a real product image or a real person's photo.** If a slide needs a visual that does not exist, draw it as inline SVG instead.

## Phase 5 — The build

1. **Write the slide plan first** — a numbered list of every slide with its act, archetype, and headline. Show it to the user. Get a yes. This is cheap to change now and expensive to change later.
2. Read all five reference files before writing a single slide:
   - `references/deck-architecture.md` — the 9 acts and how they expand to 150 slides
   - `references/psychology.md` — why each act exists and what breaks it
   - `references/slide-craft.md` — the copy laws and the 12 slide archetypes
   - `references/design-system.md` — the visual system and layout rules
   - `references/benchmarks.md` — every cited webinar number with its source
3. Write `deck.json` — the full spec, every slide, every speaker note.
4. Render: `python3 scripts/build_deck.py deck.json deck.html`
5. Open it, arrow through it, check for: any slide with more than 14 words, two consecutive slides making the same point, an act that runs long, a missing speaker note.
6. Deliver the deck, plus the registration page copy, the 6-message reminder sequence, and the 5-message follow-up.

Then offer, without building unless asked: registration page build, ad scripts, organic fill-the-room content, and the economics model (how many registrations they need for their target).

---

## The deck spec format

```json
{
  "meta": {
    "title": "The Rate Read",
    "subtitle": "how to find the leak",
    "presenter": "Zayd",
    "theme": {
      "bg": "#0E2A2E", "surface": "#133337", "text": "#FFFFFF",
      "muted": "#8FAFAF", "accent": "#DBC9B8", "line": "#1E4449",
      "display": "'Inter', sans-serif", "body": "'Inter', sans-serif",
      "mono": "'DM Mono', monospace"
    }
  },
  "slides": [
    {
      "act": "The frame",
      "type": "statement",
      "kicker": "01",
      "text": "You do not have a [[lead]] problem.",
      "note": "What they say out loud here. Never the same words as the slide."
    }
  ]
}
```

`[[word]]` wraps the **one** accent word on a slide. One per slide maximum. On many slides, zero.

**Slide types:** `cover` `section` `statement` `keyword` `number` `contrast` `list` `build` `quote` `proof` `diagram` `stack` `question` `image` `price` `cta` `close`

Full field reference for each type is in `references/slide-craft.md`.

---

## Quality bar

Before delivering, the deck must pass all ten:

1. Could a stranger, arrowing through it silently with no presenter, follow the argument? If not, the sequence is wrong.
2. Is the paradigm shift a genuine reframe, or a dressed-up tactic? A tactic is not a webinar.
3. Does the pain act use their words, with lived specificity, or adjectives? "Frustrated" is a failure. "You open the dashboard at 11pm and close it again" is right.
4. Does credibility appear only after value, and only the part relevant to this subject? No bios.
5. Are there 3-5 demonstrations spaced through the content, of varying type?
6. Does "the choice" genuinely admit they could do it alone? If it does not, the offer reads as a trap.
7. Is the price stated once, without defence, with silence after?
8. Is there exactly one call to action with no alternatives?
9. Does any slide have more than 14 words? Does any slide have two accent words?
10. Does the first week slide exist? It is the one that decides it.
