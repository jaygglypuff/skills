# humanize

A [Claude Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that rewrites AI-generated prose so it reads like a specific person wrote it, using the pattern catalogue from [**Wikipedia:Signs of AI writing**](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

It ships with a standalone scanner that works without Claude, so you can use the checker on its own.

---

## What it does

AI prose regresses to the mean. It sands off specific, unusual, concrete detail and replaces it with generic, positive, inflated description. Wikipedia's editors describe the effect as a portrait blurring from a sharp photograph into a generic sketch while the caption shouts louder and louder about how important the subject is: the writing becomes **less specific and more exaggerated at the same time**.

So the fix has two halves, and most people only do the first:

1. **Subtract the machine.** Inflated significance, hollow analysis, formulaic structure, rhythmic tics.
2. **Add the human.** Specificity, an actual stance, uneven rhythm, the texture of someone who knows the subject.

Deleting em dashes gets you to neutral. Neutral still reads as machine-made.

## What it is not

Not a de-AI-detector tool. Detectors are unreliable in both directions, and a Stanford study found seven of them flagged 61.3% of human-written TOEFL essays by non-native English speakers as AI. Writing to beat them damages prose and proves nothing.

Not a banned-words list either. Wikipedia's page says so explicitly, and this skill follows that:

> This list is not a ban on certain words, phrases, or punctuation. Not all text featuring these indicators is AI-generated... These are potential signs of a problem, not the problem itself.

If your ideas are generic, editing can't fix that. The honest answer in that case is that the content needs someone with real knowledge, not a better edit.

---

## Install

### As a Claude Skill

Download `humanize.skill` from [Releases](../../releases), or build it yourself:

```bash
./build.sh          # produces humanize.skill
```

Then upload it in Claude, or drop the `humanize/` folder into your skills directory.

Once installed, it triggers on things like *"humanize this"*, *"make it sound less like ChatGPT"*, *"remove the AI tells"*, or *"this was written by AI, fix it"*.

### Scanner only, no Claude

```bash
git clone https://github.com/YOUR-USERNAME/humanize-skill.git
cd humanize-skill
python3 humanize/scripts/ai_tells.py path/to/your/content --verbose
```

Python 3.8+. `beautifulsoup4` is optional and only improves HTML parsing:

```bash
pip install beautifulsoup4
```

---

## Using the scanner

```bash
# one file
python3 humanize/scripts/ai_tells.py article.md --verbose

# a whole site or repo
python3 humanize/scripts/ai_tells.py ./content --verbose --json report.json

# in CI, fail the build if it gets worse
python3 humanize/scripts/ai_tells.py ./docs --fail-over 20
```

Handles `.md`, `.html`, `.txt` and `.rst`. Skips `node_modules`, `dist`, `build`, image folders and dot-directories by default; add more with `--skip`.

Try it on the sample:

```bash
$ python3 humanize/scripts/ai_tells.py examples/sample-ai-text.md

  2  puffery / inflated significance
  2  promotional / brochure language
  2  negative parallelism (not X, but Y)
  2  bolded lead-in + colon
  1  superficial -ing analysis tail
  1  vague attribution (weasel)
  1  crutch transition
  1  hollow wrap-up
  1  excessive hedging
  1  rule of three
  1  em dash
  1  Title Case heading
```

### Read the output correctly

**The scanner finds candidates. It does not decide anything.** Every hit needs a human judgment, and the test is one question:

> If I delete this, is any information lost?

Nothing lost means it was decoration. Something lost means keep it.

The same pattern can be a tic or a fact depending on context:

| Pattern | Rewrite | Keep |
|---|---|---|
| Rule of three | "fast, simple, and powerful" — three abstractions picked for cadence | "Ilocos Sur, La Union and Pangasinan" — there are genuinely three, and which three matters |
| Em dash | dropped where a comma belongs, several per page | a real parenthetical from a writer who uses them |
| "Not X, but Y" | "It isn't a product, it's a philosophy" | "the figure is total capacity, not usable capacity" — the contrast *is* the information |

On a real site I recently ran this against, ~100 of the flagged three-item lists were provinces, appliances and equipment. All were kept. Stripping them to satisfy a checklist would have made the writing worse.

---

## What's in here

```
humanize/
  SKILL.md                          the workflow Claude follows
  references/
    signs-of-ai-writing.md          the full taxonomy, five buckets
    rewrite-patterns.md             before/after pairs + judgment table
  scripts/
    ai_tells.py                     the scanner
examples/
  sample-ai-text.md                 deliberately bad text, for testing
tests/
  test_ai_tells.py                  regression tests
```

The taxonomy follows Wikipedia's own five groupings: **Language and tone**, **Style**, **Markup**, **Citations**, and **Communication intended for the user**. Two patterns are singled out by editors as the strongest signals: *undue emphasis on symbolism and importance*, and *superficial analyses*.

---

## Honest caveats

**The Wikipedia page could not be fetched directly.** `en.wikipedia.org` was cache-only in the environment where this was built, so the taxonomy was reconstructed from detailed secondary coverage of the page rather than from the page itself. The bucket structure, the specific tells and the caveats are faithful as far as I can verify, but **please diff `references/signs-of-ai-writing.md` against the live page** and open a PR for anything that has drifted.

**The patterns expire.** "Delve" was the 2023 giveaway and has faded. "Unlock", "harness" and "leverage" are on the same path. Newer models already suppress em dashes. Treat every word list here as perishable.

**The scanner had a real bug until recently.** Multi-word patterns were compiled with `re.X`, which strips literal spaces, so puffery, hedging, weasel words and several other checks silently matched nothing. Fixed, with regression tests in `tests/` so it can't come back. If you forked before that, re-pull.

**Over-correction is a real failure mode.** Strip out every device that might look artificial and the result reads stiffer and *more* obviously machine-made. Every fragment, every wink at the reader, a plain useful word swapped for a worse one because it appeared on a list. If a rule would make a sentence worse, the sentence wins.

---

## Contributing

Especially welcome:

- Corrections against the live Wikipedia page
- New tells, with real examples
- False positives the scanner produces on genuinely human writing
- Translations of the taxonomy

See [CONTRIBUTING.md](CONTRIBUTING.md). Please run `python3 tests/test_ai_tells.py` before opening a PR.

---

## Licence

Deliberately split, because part of this is derived work:

- **Code** (`humanize/scripts/`, `tests/`): [MIT](LICENSE).
- **Prose** (`humanize/SKILL.md`, `humanize/references/`): [CC BY-SA 4.0](LICENSE-DOCS), matching Wikipedia's licence, because `signs-of-ai-writing.md` is derived from Wikipedia:Signs of AI writing. Share-alike applies if you redistribute modified versions.

Attribution details in [NOTICE](NOTICE).

Not affiliated with or endorsed by the Wikimedia Foundation or Anthropic.
