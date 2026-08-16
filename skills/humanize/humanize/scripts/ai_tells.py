#!/usr/bin/env python3
"""
Scan reader-facing copy for the patterns catalogued in
Wikipedia:Signs of AI writing (WikiProject AI Cleanup).

Usage: python3 ai_tells.py <path> [--verbose] [--json out.json]

See --help for all options.
"""
import sys, os, re, json, argparse
from collections import defaultdict
try:
    from bs4 import BeautifulSoup, Comment
    HAVE_BS4 = True
except ImportError:
    HAVE_BS4 = False

SKIP = {"script", "style", "svg", "path", "circle", "rect", "g", "noscript"}

# ---- the checks, grouped the way the Wikipedia page groups them -------------

PUFFERY = (
    r"stands? as a testament|testament to (?:the|its|his|her|their)|"
    r"play(?:s|ing|ed)? an? (?:pivotal|crucial|vital|key|significant|central|important) role|"
    r"underscor(?:es|ing|ed) the|underpin(?:s|ning)? the importance|watershed moment|"
    r"(?:a |an )?(?:lasting|enduring) (?:impact|legacy|impression)|deeply rooted in|"
    r"rich (?:cultural )?(?:heritage|tapestry|history)|hallmark of|epitomi[sz](?:e|es|ed|ing)|"
    r"embod(?:y|ies|ied) the|cement(?:s|ed)? (?:its|his|her|their)|"
    r"solidif(?:y|ies|ied|ying) (?:its|his|her|their)|a beacon of|"
    r"pav(?:e|es|ed|ing) the way for|left an indelible")

PROMO = (
    r"\bbreathtaking\b|\bmust-(?:visit|have|see|try)\b|\bstunning\b|\bvibrant\b|"
    r"\bnestled (?:in|among|between)\b|\bbustling\b|\biconic\b|\bworld-class\b|"
    r"\bstate-of-the-art\b|\bcutting-edge\b|\bunparalleled\b|\bunmatched\b|"
    r"\bpremier destination\b|\brenowned for\b|\bboasts\b|\bseamless(?:ly)?\b|"
    r"\brobust\b|\bholistic\b|\bgame-?chang(?:er|ing)\b|\brevolutioni[sz](?:e|es|ing|ed)\b|"
    r"\btransformative\b|\belevat(?:e|es|ing) your\b|\bunlock the (?:power|potential)\b|"
    r"\bharness the power\b|\bleverage the\b|\bdelve into\b")

EDITORIAL = (
    r"it(?:'s|\u2019s| is) (?:important|worth) (?:to note|noting|remembering|mentioning)|"
    r"it should be noted|no (?:discussion|exploration|list) (?:would be|is) complete|"
    r"needless to say|as we(?:'ve|\u2019ve| have) seen|one might argue|"
    r"it goes without saying|it(?:'s|\u2019s| is) worth mentioning")

SUPERFICIAL = (
    r"[,\u2014\u2013-]\s+(?:highlighting|underscoring|reflecting|showcasing|demonstrating|illustrating|"
    r"emphasi[sz]ing|signal(?:l)?ing|marking|cementing|ensuring|allowing for|paving|"
    r"solidifying|reinforcing|contributing to|serving as)\s")

VAGUE_ATTR = (
    r"(?:some|many|most|several|industry|market) "
    r"(?:critics|experts|observers|analysts|reports|studies|sources|commentators)\b|"
    r"\bexperts (?:say|agree|note|believe|recommend|suggest)\b|"
    r"\bstudies (?:show|suggest|indicate|have shown)\b|"
    r"\bresearch (?:shows|suggests|indicates)\b|"
    r"\bit is (?:widely |generally |often )?(?:believed|considered|regarded|thought|accepted)\b|"
    r"\bis (?:widely|often|generally) (?:considered|regarded|seen as|viewed as)\b|"
    r"\bcritics (?:argue|say|contend)\b")

CONJ = (
    r"(?:^|(?<=[.!?]\s))\s*(?:Furthermore|Moreover|Additionally|In addition|That said|"
    r"On the other hand|Consequently|Nevertheless|Nonetheless|Notably|Importantly|"
    r"Ultimately|Indeed|Overall)\b")

WRAPUP = (
    r"\bIn conclusion\b|\bIn summary\b|\bTo summari[sz]e\b|\bAll in all\b|"
    r"\bAt the end of the day\b|\bIn essence\b|\bTo sum up\b|\bIn closing\b")

HEDGE = (
    r"\b(?:may|might|could) (?:potentially|possibly|conceivably)\b|"
    r"\bresults may vary\b|\bgenerally speaking\b|\bin many cases\b|"
    r"\boften considered\b|\btends? to be seen as\b|\bit depends on (?:a )?(?:variety|number) of\b|"
    r"\bunique needs and (?:circumstances|preferences|goals)\b")

CHALLENGES = (
    r"\bDespite (?:its|these|the|their) (?:strengths|challenges|success|popularity|limitations)|"
    r"[Cc]hallenges and (?:future )?(?:prospects|opportunities|considerations)|"
    r"[Ff]uture (?:prospects|outlook|directions) (?:remain|look|are)")

CUTOFF = (
    r"as of my last (?:update|knowledge)|as an AI language model|"
    r"knowledge cut-?off|while specific details are limited|"
    r"I do not have access to|my training data")

CHATTER = (
    r"(?:^|(?<=[.!?]\s))\s*(?:Certainly|Sure thing|Great question|Of course|Absolutely)[,!]|"
    r"\bI hope this helps\b|\bWould you like me to\b|"
    r"\bHere(?:'s|\u2019s| is) (?:your|the) (?:post|article|draft|revised|updated)\b|"
    r"\bLet me know if\b|\bfeel free to (?:ask|reach out)\b")

NEG_PARALLEL = [
    r"\bnot just\b[^.?!]{2,80}?\bbut\b",
    r"\bit(?:'s| is)n?o?t? (?:about|just)\b[^.?!]{2,60}?\bit(?:'s| is)\b",
    r"\bnot\b[^.?!]{1,60}?,\s*(?:but|it(?:'s| is))\b",
    r"\b(?:is|are|was|were)\s+not\s+[a-z][^.?!]{2,50}?,\s+(?:it|they|that)\s+(?:is|are|was|were)\b",
    r"[\w)]+,\s+not\s+[\w][^.?!]{0,40}?[.?!]",            # "hours, not watts."
    r"\b\w+\s+(?:instead of|rather than)\s+\w+[^.?!]{0,40}?[.?!]",
    r"\bless\b[^.?!]{1,40}?,\s*more\b",
    r"^\s*[A-Z][^.?!]{2,70}?\.\s+(?:It|That|They|We)(?:'s| is| are)\s+(?:actually|really|not)\b",
    r"\bA\s+\w+\s+is\s+\w+,\s+not\s+(?:a\s+)?\w+",         # "A battery is furniture, not a fixture"
    r"\bwhich is (?:the|what) (?:entire|whole|actual)\b",
    r"\bthe (?:name|point|answer|difference) is the\b",
]

# Aphoristic full-stop flourishes: a very short declarative sentence used as a
# rhetorical mic-drop. Common in AI marketing copy.
APHORISM = [
    r"\b(?:is|was)\s+(?:decoration|theatre|theater|a sales tactic|the entire product|the whole point|the promise)\b",
    r"\bby design\.\s*$",
    r"\bwithout theatre\b|\bwithout theater\b",
    r"\bThat(?:'s| is) (?:all|the whole point|it)\.",
    r"\bfull stop\b|\bperiod\.\s*$",
    r"\bis not a system\b|\bis not an answer\b",
]

# Bolded lead-in followed by colon/dash then a restating clause
BOLD_LEADIN = (
    r"(?:^|\n)\s*(?:[-*+]|\d+\.)\s+\*\*[^*\n]{2,45}?:?\*\*:?\s*[—:-]?\s+[a-z]|"
    r"(?:^|\n)\s*<li>\s*<b>[^<\n]{2,45}?:?</b>:?\s*[—:-]?\s+[a-z]")

RULE_OF_THREE = r"\b\w+,\s+\w+(?:\s\w+)?,?\s+and\s+\w+"      # coarse; refined below
TRIPLE_LIST = r"([A-Za-z][\w'-]*(?:\s[\w'-]+){0,2}),\s+([A-Za-z][\w'-]*(?:\s[\w'-]+){0,2}),?\s+and\s+([A-Za-z][\w'-]*(?:\s[\w'-]+){0,2})"

CHECKS = [
    ("puffery / inflated significance", PUFFERY),
    ("promotional / brochure language", PROMO),
    ("editorialising", EDITORIAL),
    ("superficial -ing analysis tail", SUPERFICIAL),
    ("vague attribution (weasel)", VAGUE_ATTR),
    ("crutch transition", CONJ),
    ("hollow wrap-up", WRAPUP),
    ("excessive hedging", HEDGE),
    ("challenges-and-prospects formula", CHALLENGES),
    ("knowledge-cutoff disclaimer", CUTOFF),
    ("assistant chatter", CHATTER),
]

def flags_for(text):
    hits = defaultdict(list)
    for name, pat in CHECKS:
        rx = re.compile(pat, re.I | re.M)
        for m in rx.finditer(text):
            hits[name].append(m.group(0).strip())
    for pat in NEG_PARALLEL:
        for m in re.finditer(pat, text, re.I | re.M):
            hits["negative parallelism (not X, but Y)"].append(m.group(0).strip())
    for pat in APHORISM:
        for m in re.finditer(pat, text, re.I | re.M):
            hits["aphoristic mic-drop"].append(m.group(0).strip())
    for m in re.finditer(BOLD_LEADIN, text):
        hits["bolded lead-in + colon"].append(m.group(0).strip())
    for m in re.finditer(TRIPLE_LIST, text):
        hits["rule of three"].append(m.group(0).strip())
    # em dash
    for m in re.finditer(r"[^\s]*\s?—\s?[^\s]*|&mdash;", text):
        hits["em dash"].append(m.group(0).strip())
    # title case headings handled separately
    return hits

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def burstiness(text):
    sents = sentences(text)
    if len(sents) < 4:
        return None
    lens = [len(s.split()) for s in sents]
    mean = sum(lens) / len(lens)
    var = sum((l - mean) ** 2 for l in lens) / len(lens)
    short = sum(1 for l in lens if l <= 5) / len(lens)
    return {"n": len(lens), "mean": round(mean, 1),
            "sd": round(var ** 0.5, 1), "pct_short": round(short * 100, 1)}

def prose_from_html(path):
    raw = open(path, encoding="utf-8").read()
    if not HAVE_BS4:
        raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
        raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
        txt = re.sub(r"<[^>]+>", "\n", raw)
        return [l.strip() for l in txt.splitlines() if l.strip()], []
    soup = BeautifulSoup(raw, "html.parser")
    for t in soup(list(SKIP)):
        t.decompose()
    # drop HTML comments (editor notes, not reader-facing)
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    chunks, headings = [], []
    for el in soup.find_all(["p", "h1", "h2", "h3", "h4", "li", "summary", "figcaption", "blockquote"]):
        s = re.sub(r"\s+", " ", el.get_text(" ", strip=True))
        if s:
            chunks.append(s)
            if el.name in ("h1", "h2", "h3", "h4"):
                headings.append(s)
    if soup.title and soup.title.string:
        chunks.append(soup.title.string.strip())
    for m in soup.find_all("meta"):
        if m.get("name") == "description" or m.get("property", "").startswith("og:"):
            if m.get("content"):
                chunks.append(m["content"])
    return chunks, headings

def prose_from_md(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    headings = re.findall(r"^#{1,6}\s+(.+)$", raw, re.M)
    body = re.sub(r"^#{1,6}\s+", "", raw, flags=re.M)
    return [l.strip() for l in re.split(r"\n\s*\n", body) if l.strip()], headings

# Ordinary words that Title Case capitalises but sentence case would not.
# Deliberately excludes anything that is commonly part of a proper noun
# (Union, Guide, Park, State, City...) so that place names and brand names in
# a heading do not trip the check.
_COMMON = set("""
about above across after again against all also always among another answer any
approach are around ask asking avoid back before begin beginning behind below best
better between beyond big both build building built can case cases change changing
check choose choosing come common complete considerations consider could create
creating current day days deep detail details different does doing done down during
each early easy effective either else end enough essential even ever every everything
example examples explained fast few final find finding first five following four from
full get getting give given going good great group grow guide happen has have help
here high how however idea ideas important improve improving inside instead into issue
issues its itself just keep key kind know known large last late later learn least
less lesson let level like little long look looking lot made make making many matter
matters may mean means might mistakes modern more most much must need needs never new
next nine none not nothing now number often old once one only open other others our
out over own part parts people perfect place plan point points possible power
practical practices problem problems process put question questions quick read ready
real really reason reasons right rules same second see seven several should side
simple since six small solutions some something start started starting step steps
still stop such take taking tell ten than that their them then there these they thing
things think this those three through time times tips together too top total toward
try trying two under understand understanding until use used useful using very want
way ways well what when where whether which while why will with within without work
working world worst would write writing wrong year years your
""".split())


def title_case_headings(headings):
    """Flag headings in Title Case, ignoring the first word and small words.

    Counts only capitalised words that are ordinary vocabulary (_COMMON).
    A heading full of proper nouns - place names, brands, people - is not
    Title Case, it is just a heading with names in it.
    """
    bad = []
    small = {"a", "an", "and", "the", "or", "of", "to", "in", "on", "for", "with",
             "at", "by", "from", "but", "nor", "is", "as", "vs"}
    for h in headings:
        words = re.findall(r"[A-Za-z][A-Za-z'\u2019-]*", h)
        if len(words) < 3:
            continue
        capped_common = [
            w for w in words[1:]
            if w[0].isupper() and not w.isupper()
            and w.lower() not in small
            and w.lower() in _COMMON
        ]
        if len(capped_common) >= 2:
            bad.append(h)
    return bad


def scan(root, skip_dirs):
    totals, per_file = defaultdict(int), {}
    if os.path.isfile(root):
        walker = [(os.path.dirname(root) or ".", [], [os.path.basename(root)])]
        base_for_rel = os.path.dirname(root) or "."
    else:
        walker = os.walk(root)
        base_for_rel = root
    for base, dirs, files in walker:
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        for fn in sorted(files):
            p = os.path.join(base, fn)
            if fn.endswith(".html") or fn.endswith(".htm"):
                chunks, headings = prose_from_html(p)
            elif fn.endswith((".md", ".markdown", ".txt", ".rst")):
                chunks, headings = prose_from_md(p)
            else:
                continue
            text = "\n".join(chunks)
            if not text.strip():
                continue
            hits = flags_for(text)
            tc = title_case_headings(headings)
            if tc:
                hits["Title Case heading"] = tc
            counts = {k: len(v) for k, v in hits.items() if v}
            if counts:
                per_file[os.path.relpath(p, base_for_rel)] = {
                    "counts": counts,
                    "examples": {k: v[:6] for k, v in hits.items() if v},
                    "burstiness": burstiness(text)}
                for k, n in counts.items():
                    totals[k] += n
    return totals, per_file


def main():
    ap = argparse.ArgumentParser(
        prog="ai_tells.py",
        description="Scan prose for the patterns catalogued in "
                    "Wikipedia:Signs of AI writing (WikiProject AI Cleanup).",
        epilog="The script finds candidates, not verdicts. A flagged sentence is only a "
               "problem if removing the flagged part loses no information. If it loses "
               "information, leave it alone.")
    ap.add_argument("path", help="file or directory to scan (.html, .md, .txt, .rst)")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="list every match with its file and sentence-length stats")
    ap.add_argument("--json", metavar="FILE",
                    help="also write full results to FILE as JSON")
    ap.add_argument("--skip", metavar="DIR", action="append", default=[],
                    help="directory name to skip; repeatable "
                         "(node_modules, .git and dot-dirs are always skipped)")
    ap.add_argument("--fail-over", type=int, metavar="N", default=None,
                    help="exit 1 if total flags exceed N (useful in CI)")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        ap.error(f"no such file or directory: {args.path}")

    skip = set(args.skip) | {"node_modules", "vendor", "dist", "build", "images", "img"}
    totals, per_file = scan(args.path, skip)
    total = sum(totals.values())

    print("=" * 72)
    print("AI-TELL INVENTORY  (Wikipedia:Signs of AI writing categories)")
    print("=" * 72)
    if not totals:
        print("  no flags found")
    for k, n in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"{n:5d}  {k}")
    print(f"\nTotal flags: {total} across {len(per_file)} file(s)")

    if args.verbose:
        for f, d in sorted(per_file.items()):
            print("\n" + "-" * 72)
            print(f, " sentences:", d["burstiness"])
            for k, ex in d["examples"].items():
                print(f"  [{k}] ({d['counts'][k]})")
                for e in ex:
                    print(f"       - {e[:160]}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"totals": dict(totals), "files": per_file}, fh, indent=1)
        print(f"\nfull results written to {args.json}")

    if not args.verbose and total:
        print("\nRun again with --verbose to see each match.")

    if args.fail_over is not None and total > args.fail_over:
        print(f"\nFAIL: {total} flags exceeds threshold of {args.fail_over}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
