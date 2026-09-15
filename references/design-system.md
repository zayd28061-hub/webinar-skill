# Design system — how a webinar deck should look

A sales deck is watched on a laptop, in a browser tab, at 1200px wide, half-attention, often with a face in the corner. Every decision below follows from that.

## The five laws

1. **Dark ground.** A white deck at full screen for 70 minutes is fatiguing and reads as a corporate training. A near-black warm ground reads as a broadcast. Never pure `#000` — it is flat and kills the sense of depth. Use a warm or cool near-black.
2. **Type is the design.** No stock photography, no icon sets, no clip art, no gradient mesh. The one asset that always looks premium is well-set type with enough space around it.
3. **One accent, used almost never.** A single accent colour, appearing on roughly one word per slide and on many slides not at all. The rarity is the mechanism. The instant everything is accented, nothing reads as important and the deck looks like a template.
4. **Massive scale contrast.** Headline 96-200px. Labels 11-13px. Nothing in between on the same slide. Timid type sizing is the number one tell of an amateur deck.
5. **Space is not empty.** A slide with four words and enormous margins reads as confidence. A slide filled to the edges reads as a person who is not sure which part matters.

## Grid and safe area

- 16:9, authored at **1600 × 900**.
- **Safe margin: 96px** on all sides. Nothing crosses it except a deliberate full-bleed image.
- Optical centring: type blocks sit **~4% above** true vertical centre or the slide looks like it is sinking.
- Two horizontal positions only: **hard left at the margin**, or **centred**. Pick one per act and stay with it, so a switch means something.

## Type scale

| Role | Size | Weight | Tracking |
|---|---|---|---|
| Keyword slide | 160-200px | 700 | -0.045em |
| Headline | 96-120px | 700 | -0.04em |
| Statement | 64-80px | 700 | -0.035em |
| Sub | 28-32px | 300 | -0.01em |
| Body / list item | 24-28px | 300 | 0 |
| Number | 200-280px | 700 | -0.05em |
| Label / kicker | 11-13px | 400, mono | 0.22em, uppercase |

Tight negative tracking on display sizes is what separates a deck from a slide template. Line height on display type: **0.95-1.05**. Body: 1.5.

**One display family, one body weight, one mono for labels.** Three families total is already the ceiling.

## Colour

Whatever the brand palette, structure it as:

- `bg` — the ground, near-black, warm or cool but never `#000`
- `surface` — 4-8% lighter, for cards and the offer stack only
- `text` — off-white, never pure `#FFF` at large sizes (it vibrates on dark)
- `muted` — ~50% of text luminance, for labels, sources and dimmed build items
- `accent` — one word per slide, maximum
- `line` — barely visible hairlines, 1px

If a project has a `DESIGN.md` or brand guidelines, take the palette from there and map it onto these six roles rather than inventing new ones.

## Motion

Cross-fade between slides at 200ms, nothing else. No slide-in, no push, no flip, no bounce. Movement between slides steals attention from the word on the slide, which is the only thing the motion was supposed to serve.

The one exception: `build` slides, where the newly revealed item fades up over 200ms while the previous ones drop to `muted`. That motion carries meaning — it is the sequence of the argument becoming visible.

## What makes a deck look AI-generated

Named so it can be avoided:
- Three-column feature grids with icons
- Rounded-rectangle cards on every slide
- Gradient text
- Emoji as section markers
- Every slide with a title in the top-left and a bulleted body
- Centre-aligned body copy in paragraphs
- Purple-to-blue gradients
- Stock photos of laptops, handshakes, or people pointing at whiteboards
- Titles like "Key Benefits", "Our Process", "Why Choose Us"

The correction for all of them is the same: fewer elements, larger type, more space, and a title that makes a claim.

## Presentation mechanics

The rendered deck must:
- Run fullscreen in a browser with **arrow keys / space** to advance
- Have a **speaker-notes view** (`S`) showing the current note and the next slide
- Have a **grid overview** (`G`) for jumping during Q&A
- Print cleanly to PDF, one slide per page
- Show slide number and act name in a corner at low opacity
- **Never go blank at the end** — hold on the CTA through Q&A, because that is where most of the buying happens
