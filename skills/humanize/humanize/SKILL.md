---
name: humanize
description: Rewrite AI-generated or AI-sounding prose so it reads like a specific human wrote it, using the pattern catalogue from Wikipedia:Signs of AI writing (WikiProject AI Cleanup). Use this skill whenever someone asks to "humanize", "de-AI", "make this sound human", "remove the AI tells", "it sounds like ChatGPT wrote it", or wants marketing copy, a website, blog posts, essays, emails, documentation or product content edited so it stops sounding machine-generated. Also use it when auditing existing writing for AI tells, or when the user says content "was written by AI" and wants it fixed. Applies to whole sites and repositories, not just single passages.
---

# Humanize

Rewrite text so it reads like a particular person wrote it, not like the statistical average of the internet.

The reference catalogue is Wikipedia's **Signs of AI writing**, maintained by WikiProject AI Cleanup. It is a *descriptive* field guide built from thousands of real examples, not a rulebook. Its own disclaimer matters and governs how this skill is applied:

> This list is not a ban on certain words, phrases, or punctuation. Not all text featuring these indicators is AI-generated... These are potential signs of a problem, not the problem itself.

So the goal is never "zero matches on a checklist." The goal is prose a specific human would actually write. Read `references/signs-of-ai-writing.md` for the full taxonomy before doing substantive work, and `references/rewrite-patterns.md` for worked before/after pairs.

## The core insight

AI prose regresses to the mean. It sands off specific, unusual, concrete facts and replaces them with generic, positive, inflated description. Wikipedia's editors describe the effect as shouting louder and louder that a portrait shows an important person while the portrait itself blurs from a sharp photograph into a generic sketch: the subject becomes simultaneously **less specific and more exaggerated**.

That gives the two-part fix:

1. **Subtract the machine.** Remove inflated significance, hollow analysis, formulaic structure, and rhythmic tics.
2. **Add the human.** Put back specificity, an actual stance, uneven rhythm, and the texture of someone who knows the subject.

Step 2 is the one people skip. Deleting em dashes only gets you to neutral, and neutral still reads as machine-made.

## Workflow

### 1. Establish the preservation register — do this first

Before changing a word, list what must survive untouched. Editing this by accident is worse than leaving a tell in. Preserve:

- **Brand, product and model names** exactly as written, including capitalisation and spacing.
- **Numbers**: prices, capacities, tolerances, dates, percentages, phone numbers, measurements. If a number is wrong, flag it; never quietly "improve" it.
- **Legal, compliance and disclaimer text**, warranty terms, and anything that reads like it was cleared by somebody.
- **Claims of fact.** Humanizing changes how something is said, never whether it is true. If a rewrite would strengthen or weaken a claim, keep the original claim.
- **Deliberate voice**: a house style, second-language phrasing, regional idiom, another language, code, technical identifiers.
- **Structure that carries meaning**: navigation labels, form fields, headings people navigate by, anchors, alt text that describes a real image.

When in doubt, treat it as preserved and mention it rather than rewriting it.

### 2. Inventory the tells

Run `scripts/ai_tells.py` over the target to get a quantitative baseline:

```bash
python3 scripts/ai_tells.py <path> --verbose
python3 scripts/ai_tells.py <path> --json before.json   # to diff against later
```

It reads `.html`, `.md`, `.txt` and `.rst`, skips code, comments and
`node_modules`, and reports counts per category plus sentence-length statistics.
`--help` lists the rest.

The script finds candidates. It does not decide anything. Every hit still needs human judgment, and the script will miss tells that only a reader notices.

For short passages, skip the script and read.

### 3. Judge each hit: crutch or content?

This is the whole job, and it is where a careless pass does damage.

A pattern is a **tell** when it exists for rhythm, emphasis or the appearance of insight. The same pattern is **legitimate** when it carries information.

| Pattern | Tell (rewrite) | Legitimate (keep) |
|---|---|---|
| Rule of three | "fast, simple, and powerful" — three abstractions chosen for cadence | "Ilocos Norte, La Union and Pangasinan" — there are genuinely three, and which three matters |
| Em dash | dropped where a comma or full stop belongs, several per page | a real parenthetical in a writer who uses them consistently |
| "Not X, but Y" | "It isn't a product, it's a philosophy" | "The figure is total capacity, not usable capacity" — the contrast is the actual point |
| Short declarative | a mic-drop fragment after every claim | genuine emphasis, used once |
| Boldface | every key term bolded like a textbook | one bolded warning that matters |

Ask of each candidate: **if I delete this, is any information lost?** If nothing is lost, it was decoration. If something is lost, keep it and move on.

### 4. Rewrite

Work in passes rather than trying to fix everything in one read.

**Pass A, subtract:**
- Cut inflated significance. "Plays a vital role in" becomes "does" or the sentence goes.
- Delete `-ing` tails that fake analysis: ", highlighting its importance", ", reflecting broader trends". If the analysis is real, make it a full sentence with a specific claim. If it isn't, delete it.
- Replace vague attribution with a named source, or drop the claim. "Experts say" is not evidence.
- Remove hollow wrap-ups. "In conclusion" paragraphs restate what the reader just read.
- Cut crutch transitions: Furthermore, Moreover, Additionally.
- Take a position where the evidence supports one instead of hedging.
- Reduce em dashes to the density a human writing that genre would use.
- Convert Title Case headings to sentence case. Remove decorative emoji bullets.
- Delete leftover assistant chatter and placeholders.

**Pass B, break the rhythm:**
Uniform sentence length is one of the strongest and least-noticed tells. Human writing is bursty: fragments next to long sentences. In text flagged as human, more than a quarter of sentences run five words or shorter; in AI-flagged text, under four percent do.

Read the passage aloud, or check the sentence-length spread the script reports. Then vary it deliberately. Split one long sentence, join two short ones, let one run long. Do not swing to the opposite failure of making every sentence a punchy fragment, which reads as AI trying to sound human.

**Pass C, add the human:**
- Replace one vague claim per section with a number, a name, a date, or a concrete example.
- Restore anything specific the AI generalised away.
- Let the sentence begin with "I", "So", "You", "But" where that is how the person talks.
- Keep an opinion or a real reaction if the genre allows it.

### 5. Verify

Re-run the script and compare. Then do the part the script cannot do: **read it end to end as a reader**, not as an editor scanning for patterns. Check that:

- Every preserved item survived byte-identical. Diff the numbers.
- Nothing changed meaning. A humanizing pass that alters a warranty term has failed regardless of how it reads.
- Links, markup, anchors and formatting still work.
- It does not now read as over-corrected: forced slang, jammed-in fragments, personality applied like paint.

## What failure looks like

Two directions, both common.

**Under-corrected:** the vocabulary changed but the shape didn't. Same paragraph lengths, same triplets, same balanced hedging. This happens when someone runs a find-and-replace on banned words and calls it done.

**Over-corrected:** every sentence is a fragment, every third line is a wink at the reader, and a plain useful word got swapped for a worse one because it appeared on a list. Wikipedia and practitioners both warn that stripping out every human-sounding device makes writing *more* obviously artificial, not less. If a rule would make a sentence worse, the sentence wins.

The test to apply at the end: **does this sound like something the actual author would write, or like an AI imitating a human?**

## A note on detectors

Do not write to beat AI detectors. They are unreliable in both directions. A Stanford study found seven detectors misclassified 61.3% of human-written TOEFL essays by non-native English speakers as AI-generated. Optimising against them will damage good writing and prove nothing.

The point of this skill is not to disguise authorship. It is to make sure the finished text carries the author's actual judgment, specificity and voice. If the ideas underneath are generic, no amount of rewriting fixes that, and the honest report to the user is that the content needs a person with real knowledge, not a better edit.

## Reference files

- `references/signs-of-ai-writing.md` — the full taxonomy, organised the way the Wikipedia page organises it: Language and tone, Style, Markup, Citations, Communication intended for the user. Read this before a substantive pass.
- `references/rewrite-patterns.md` — before/after pairs for each category, plus the judgment calls on when to leave a pattern alone.
- `scripts/ai_tells.py` — the scanner. Run it for a baseline and again to verify.
