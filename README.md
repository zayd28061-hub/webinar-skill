# /webinar

A Claude Code skill that builds a **complete, presentation-grade sales webinar deck** — 120 to 190 slides, every slide written, every speaker note written, rendered into a browser presentation you can run live or export to PDF.

It is not a slide generator. It is the webinar structure, the psychology behind each act, the slide-copy laws, and a renderer — packaged so the model interviews you properly before it writes anything.

---

## Install

```bash
git clone https://github.com/USER/webinar-skill.git ~/.claude/skills/webinar
```

Or drop it into a single project instead of globally:

```bash
git clone https://github.com/USER/webinar-skill.git .claude/skills/webinar
```

Restart Claude Code. Type `/webinar`.

## Use

```
/webinar
```

It runs four phases before writing a single slide:

1. **The interview** — 10 questions in 4 batches, open-ended, never multiple choice. Offer, ICP and exclusion, price and deliverables, the enemy, your named mechanism, the paradigm shift, your closest client, the three real objections, what happens in week one, logistics and your why. It pushes back when an answer is vague, because "anyone" is not an ICP.
2. **Documents** — old scripts, offer docs, sales call transcripts, analytics. Transcripts are worth more than everything else combined; they contain your audience's exact words, and the pain act is a transcription exercise, not a writing exercise.
3. **Guidelines and inspiration** — brand files, `DESIGN.md`, fonts, colours, decks you want it to look like.
4. **Images** — product shots, screenshots, charts.

Then it writes a slide plan for your approval, writes `deck.json`, renders `deck.html`, and runs an automated quality check.

You also get the registration page copy, the six-message reminder sequence, and the five-message follow-up.

## What is inside

| File | What it holds |
|---|---|
| `SKILL.md` | The interview, the build process, the ten-point quality bar |
| `references/deck-architecture.md` | The nine acts, a timing map, and how they expand to 150+ slides |
| `references/psychology.md` | Why each act exists — the commitment ladder, the paradigm shift, the specificity rule, why "the choice" act converts |
| `references/slide-craft.md` | Twelve copy laws and twelve slide archetypes |
| `references/design-system.md` | The visual system, the type scale, and a named list of what makes a deck look AI-generated |
| `references/benchmarks.md` | Every published webinar figure with its source, plus the economics model and the diagnosis order |
| `scripts/build_deck.py` | `deck.json` → a self-contained presentation HTML, zero dependencies |

## The renderer

```bash
python3 scripts/build_deck.py deck.json deck.html
```

No dependencies. Pure standard library. Outputs one self-contained HTML file.

| Key | Action |
|---|---|
| `→` `space` `click` | next |
| `←` `backspace` | previous |
| `S` | speaker notes, with the next slide previewed |
| `G` | grid overview — click any slide to jump, for Q&A |
| `F` | fullscreen |
| `P` | print view, then Save as PDF, one slide per page |

It also prints a quality report on every build: slides over the word limit, slides with more than one accent word, missing speaker notes, and stretches where the same archetype repeats too long.

## Slide spec

```json
{
  "meta": {
    "title": "The Rate Read",
    "theme": { "bg": "#0E2A2E", "surface": "#133337", "text": "#F4F1ED",
               "muted": "#7E9A9B", "accent": "#DBC9B8", "line": "#1C4449" }
  },
  "slides": [
    { "act": "01 · The pain",
      "type": "statement",
      "text": "You open the dashboard at eleven at night.",
      "note": "Concrete. Specific time. No adjectives." }
  ]
}
```

`[[word]]` marks the **one** accent word on a slide. One per slide maximum, and on most slides, zero. That rarity is the entire visual mechanism.

**Types:** `cover` `section` `statement` `keyword` `number` `contrast` `list` `build` `quote` `proof` `diagram` `stack` `question` `image` `price` `cta` `close`

## The three ideas it is built on

**The slide is the subtitle. The presenter is the voice.** The moment a slide contains a full spoken sentence, the audience reads ahead, finishes before you do, and stops listening. The slide and the speaker note never share words.

**One beat per slide.** A 70-minute webinar at 150 slides averages 28 seconds a slide. Slides that hold for three minutes are the most common reason a webinar dies, because visual change is what resets attention.

**The order is the content.** Most decks have roughly the right things in the wrong sequence. Credentials before value, a paradigm shift compressed into one slide, no "you could do this alone" act, and no first-week slide — those four errors account for most dead webinars.

## Sources

The structure is drawn from the Gadzhi / Monetise webinar funnel playbook, cross-checked against Russell Brunson's Perfect Webinar and 22 published benchmark reports (beknownonline.com across 12,400 B2B webinars, scaleforimpact.co, livestorm.co, on24.com). Every figure in `references/benchmarks.md` carries its source.

## Licence

MIT. Take it, change it, ship it.
