# Signs of AI writing — the taxonomy

Condensed from **Wikipedia:Signs of AI writing**, the advice page maintained by
WikiProject AI Cleanup, plus the surrounding editor commentary. The page is a
field guide assembled from thousands of real examples, organised into five
buckets. It is descriptive. Nothing here is a banned word.

Two patterns are singled out by editors as the strongest signals:
**undue emphasis on symbolism and importance**, and **superficial analyses**.

## Contents

1. [Language and tone](#1-language-and-tone)
2. [Style](#2-style)
3. [Markup](#3-markup)
4. [Citations](#4-citations)
5. [Communication intended for the user](#5-communication-intended-for-the-user)
6. [The caveats that govern all of it](#6-the-caveats-that-govern-all-of-it)

---

## 1. Language and tone

The most important bucket. Most real damage lives here.

### 1.1 Undue emphasis on symbolism and importance

AI inflates the significance of whatever it describes. One editor calls this
"a huge tell, possibly *the* tell."

Markers: stands as a testament to · plays a pivotal/crucial/vital/key role ·
underscores the importance of · a watershed moment · leaves a lasting impact ·
enduring legacy · deeply rooted · rich cultural heritage · rich tapestry ·
cemented its place · a beacon of · paved the way for · epitomises · embodies.

The mechanism is worth understanding, because it explains why this is the
master tell. A precise detail ("invented a train-coupling device") becomes a
grand vague one ("a revolutionary titan of industry"). The subject gets
simultaneously **less specific and more exaggerated**. The writing shouts about
importance while the actual portrait blurs.

Fix: state the fact. Let significance be inferred from it, or make the claim of
significance concrete and attributable.

### 1.2 Promotional language

Output reads like a tourism brochure or a press release rather than a
description: breathtaking · must-visit · stunning natural beauty · vibrant ·
nestled · bustling · iconic · world-class · state-of-the-art · unparalleled ·
seamless · robust · boasts.

Note this is a tell *even in genuinely promotional contexts*. Marketing copy
written by a person sells with specifics; AI marketing copy sells with
adjectives.

### 1.3 Editorialising

Unrequested commentary telling the reader how to feel about the information:
it's important to note · it is worth remembering · no discussion would be
complete without · needless to say · it goes without saying.

Fix: delete. If the point deserves emphasis, its position in the paragraph does
that work.

### 1.4 Superficial analyses

A plain factual sentence gets a hollow participial tail that performs analysis
without doing any: "…, highlighting its importance." "…, reflecting broader
trends." "…, underscoring the shift." "…, ensuring efficiency." "…, paving the
way for future growth."

One editor's dataset of rejected drafts found this the **most sensitive and
specific indicator** they tested: present in all the AI articles, none of the
human ones.

Fix: delete the tail, or replace it with a full sentence making a specific
claim someone could disagree with.

### 1.5 Negative parallelism

The most notorious structural tell. "It's not just X, it's Y."

All its shapes count: Not just X, but Y · It isn't about X, it's about Y ·
Not X. Y. · Less X, more Y · X is dead, Y is the future · The real question
isn't X, it's Y · X, not Y. It also appears split across two sentences:
"Most teams think they have a hiring problem. They have a standards problem."

Fix: say the positive claim on its own. The contrast is usually adding drama,
not information. Keep it only where the negated thing is a real, live
misconception the reader actually holds.

### 1.6 Rule of three

Automatic triplets: "speed, efficiency, and innovation." "Creative, smart, and
funny." Wikipedia's note is that LLMs use the structure to make superficial
analysis appear comprehensive.

Fix: use however many items are true. One, two, four. The tell is the triplet
arriving because three is rhythmically satisfying, not because there are three.

### 1.7 Overuse of conjunctions and transitions

Furthermore · Moreover · Additionally · On the other hand · That said ·
Consequently, cycled as connective crutches, often between sentences that need
no connective at all.

### 1.8 Section summaries and hollow conclusions

In conclusion · In summary · Overall · At the end of the day · In essence.
Essay-style wrap-ups that restate what the reader just read.

### 1.9 Vague attributions (weasel wording)

Some critics argue · experts say · industry reports suggest · observers have
noted · it is widely believed · studies show. Authority with no source behind it.

Fix: name the source, or drop the claim. A claim you cannot attribute is a
claim you should not make.

### 1.10 Excessive hedging

May · might · could · often considered · results may vary · generally speaking.
AI rarely takes a stance because the safest statistical output is the balanced
one.

Fix: take the position the evidence supports. Hedge only where the uncertainty
is real, and then say what the uncertainty actually is.

### 1.11 The "Challenges and Future Prospects" formula

A rigid closing section: "Despite its strengths, X faces challenges…" followed
by a vague optimistic flourish. Wikipedia is explicit that **the tell is the
rigid formula, not the mention of challenges.** Real challenges, discussed
specifically, are good writing.

### 1.12 Knowledge-cutoff disclaimers

As of my last update · while specific details are limited · as of my knowledge
cutoff. Almost always a leftover.

### 1.13 Passive, agentless constructions

"X has been described as…" by whom? Passive voice used to smuggle in opinion or
to avoid committing to a subject.

---

## 2. Style

### 2.1 Em dash overuse

The famous one, and the most misunderstood. The precise framing: AI uses em
dashes **more often than non-professional human writing of the same genre**,
and drops them where a human would use a comma, parentheses, or a colon. The
tell is frequency and placement, not the character. Wikipedia's own joke:
no one is taking your em-dashes away.

Fix: reduce density to what the genre and the author normally use. Do not
mechanically purge them from a writer who genuinely writes with them.

### 2.2 Bullet points with bolded lead-ins

The `**Scalability:** the system scales easily` shape — a bolded term, a colon,
then a clause that mostly restates the bolded term. Near-nonexistent in natural
writing.

### 2.3 Excessive boldface

Key terms bolded throughout like a textbook, in patterns that feel mechanical
rather than editorial.

### 2.4 Title Case In Headings

"Key Considerations For Adoption" where the house style is sentence case.

### 2.5 Emoji as bullets or in headings

🚀 🧠 ✅ used as list markers.

### 2.6 Curly quotes and other formatting artefacts

Smart quotes where straight quotes are expected, or inconsistently mixed.

### 2.7 Metronome rhythm

Every sentence a similar medium length, every paragraph about three sentences,
no texture. Human writing is bursty.

The measurable version: in writing flagged as human, **more than a quarter of
sentences run five words or shorter**; in AI-flagged writing, **under four
percent** do. Humans also use more fragments, more question marks, more
parenthetical asides, and open sentences with "I", "So" and "You" rather than
"It", "This" and "In".

### 2.8 Overly clean structure

Perfect parallel section lengths, rigid topic sentences, suspiciously neat
transitions. Real writing is lumpier because real knowledge is lumpier: the
author knows more about some parts than others, and it shows.

---

## 3. Markup

Leftover Markdown asterisks in a non-Markdown context. Fill-in-the-blank
placeholders that were never filled: `[insert detail here]`, `[Your Company]`,
`Lorem ipsum`. Inconsistent heading levels. Stray backticks or code fences.

---

## 4. Citations

Hallucinated or broken references. Invalid DOIs and ISBNs. Real-looking sources
that do not exist. Citations that exist but do not support the claim attached
to them. Over-citation of a single accessible source.

Anything cited must be verified, not just plausible.

---

## 5. Communication intended for the user

The dead giveaways nobody deleted:

"Certainly!" · "Great question!" · "I hope this helps" · "Would you like me
to…" · "As an AI language model…" · "Here is your post:" · "Let me know if
you'd like me to adjust anything" · a trailing offer of further help ·
restating the prompt back before answering.

Also: sycophantic openers, and meta-commentary about the writing itself
("This article will explore…", "In this section we will examine…").

---

## 6. The caveats that govern all of it

These are not footnotes. They change how the list should be used.

**It is descriptive, not prescriptive.** Observations, not rules.

**No single sign proves anything.** LLMs are trained on human writing,
including good human writing. Humans use em dashes, triplets and transitions.
Some of these patterns are just habits of inexperienced writers.

**The tell is density and combination**, not the presence of one pattern.

**Over-banning backfires.** Strip out every device that might look artificial
and the result reads stiffer and *more* obviously machine-made. A short list of
high-signal patterns removed well beats a long list removed mechanically.

**The patterns drift.** "Delve" was the 2023 giveaway and faded. "Unlock",
"harness" and "leverage" are on that path. Newer models already suppress em
dashes. Treat any word list as perishable.

**Context decides.** A literal "underscore", a genuine "challenge", an actual
three-item list are not tells. The word is not the problem.

**Detectors are not the target.** They misclassify heavily in both directions —
a Stanford study found seven detectors flagged 61.3% of human-written TOEFL
essays by non-native English speakers as AI. Writing to beat them damages prose
and proves nothing.

**Humanizing is not laundering.** The purpose is that the finished text carries
the author's real judgment and specificity. If the substance underneath is
generic, editing cannot fix it, and saying so is the useful answer.
