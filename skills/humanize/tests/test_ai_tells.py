#!/usr/bin/env python3
"""
Regression tests for the scanner.

Run:  python3 tests/test_ai_tells.py

The most important test here is test_multiword_patterns_match. Multi-word
patterns were once compiled with re.X, which strips literal whitespace from a
pattern, so every phrase containing a space silently matched nothing. Half the
checks were dead and the scanner reported a clean bill on text that was full of
tells. If that regresses, these tests fail loudly.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "humanize", "scripts"))
import ai_tells  # noqa: E402


def flags(text):
    """Category -> list of matches."""
    return {k: v for k, v in ai_tells.flags_for(text).items() if v}


def cats(text):
    return set(flags(text))


class TestMultiWordPatterns(unittest.TestCase):
    """Every check whose pattern contains a space. These are the ones re.X broke."""

    CASES = [
        ("puffery / inflated significance",
         "The bridge stands as a testament to the era.",
         "plain sentence about a bridge being built in 1954."),
        ("puffery / inflated significance",
         "The reform played a pivotal role in the outcome.", None),
        ("promotional / brochure language",
         "A breathtaking, world-class destination.",
         "A large car park with 200 spaces."),
        ("editorialising",
         "It is important to note that the figures are provisional.",
         "The figures are provisional."),
        ("superficial -ing analysis tail",
         "Output rose 4%, highlighting its importance to the sector.",
         "Output rose 4% because the second line came online."),
        ("vague attribution (weasel)",
         "Experts say the method is sound.",
         "Ostrom's 1990 study found the method sound."),
        ("vague attribution (weasel)",
         "Some critics argue the opposite.", None),
        ("crutch transition",
         "Furthermore, the results were consistent.",
         "The results were consistent."),
        ("hollow wrap-up",
         "In conclusion, the choice depends on your needs.",
         "Pick the 30 if you run two aircons."),
        ("excessive hedging",
         "This may potentially help in many cases.",
         "This cuts the evening load by about a third."),
        ("challenges-and-prospects formula",
         "Despite its strengths, the platform faces challenges.",
         "The platform cannot do three-phase."),
        ("knowledge-cutoff disclaimer",
         "As of my last update, the figure was unclear.",
         "As of March 2026 the figure was 12."),
        ("assistant chatter",
         "Certainly! Here is your article.",
         "The article follows."),
    ]

    def test_multiword_patterns_match(self):
        for category, positive, _ in self.CASES:
            with self.subTest(category=category, text=positive):
                self.assertIn(category, cats(positive),
                              f"{category!r} failed to match: {positive!r}")

    def test_clean_text_does_not_match(self):
        for category, _, negative in self.CASES:
            if negative is None:
                continue
            with self.subTest(category=category, text=negative):
                self.assertNotIn(category, cats(negative),
                                 f"{category!r} false-positived on: {negative!r}")


class TestStructuralPatterns(unittest.TestCase):

    def test_negative_parallelism(self):
        for t in ["It's not just a battery, it's peace of mind.",
                  "We sell hours, not watts.",
                  "Less noise, more sleep."]:
            with self.subTest(text=t):
                self.assertIn("negative parallelism (not X, but Y)", cats(t))

    def test_rule_of_three(self):
        self.assertIn("rule of three", cats("It is fast, simple, and powerful."))

    def test_em_dash(self):
        self.assertIn("em dash", cats("The roof — all of it — was replaced."))

    def test_bolded_lead_in(self):
        for t in ["- **Scalability:** the system scales easily",
                  "* **Reliability**: you can rely on it"]:
            with self.subTest(text=t):
                self.assertIn("bolded lead-in + colon", cats(t))

    def test_title_case_heading(self):
        self.assertTrue(ai_tells.title_case_headings(
            ["Key Considerations For Modern Adoption"]))

    def test_sentence_case_heading_is_not_flagged(self):
        self.assertFalse(ai_tells.title_case_headings(
            ["Key considerations for modern adoption"]))

    def test_proper_nouns_do_not_trip_title_case(self):
        self.assertFalse(ai_tells.title_case_headings(
            ["Working across La Union and Ilocos Sur"]))


class TestBurstiness(unittest.TestCase):

    def test_uniform_text_has_low_spread(self):
        uniform = " ".join(["The system charges during the daylight hours here."] * 6)
        b = ai_tells.burstiness(uniform)
        self.assertIsNotNone(b)
        self.assertLess(b["sd"], 2.0)
        self.assertEqual(b["pct_short"], 0.0)

    def test_bursty_text_has_short_sentences(self):
        bursty = ("The roof runs the house all day and puts what is left into the "
                  "battery. At night the battery takes over. Nobody does anything. "
                  "It works.")
        b = ai_tells.burstiness(bursty)
        self.assertGreater(b["pct_short"], 25.0)

    def test_too_short_returns_none(self):
        self.assertIsNone(ai_tells.burstiness("One sentence only."))


class TestJudgment(unittest.TestCase):
    """Cases the scanner SHOULD flag but a human should then keep. Documents
    the known false-positive surface so nobody 'fixes' it by weakening it."""

    def test_real_enumeration_is_still_flagged(self):
        # Correct behaviour: flag it, and let the human keep it.
        self.assertIn("rule of three",
                      cats("We work in Ilocos Sur, La Union and Pangasinan."))

    def test_meaningful_contrast_is_still_flagged(self):
        self.assertIn("negative parallelism (not X, but Y)",
                      cats("The figure is total capacity, not usable capacity."))


class TestFileHandling(unittest.TestCase):

    def test_markdown_headings_are_extracted(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as fh:
            fh.write("# A Heading Here For Testing\n\nSome body text.\n")
            path = fh.name
        try:
            chunks, headings = ai_tells.prose_from_md(path)
            self.assertIn("A Heading Here For Testing", headings)
        finally:
            os.unlink(path)

    def test_html_strips_script_and_style(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                         encoding="utf-8") as fh:
            fh.write("<html><body><script>var breathtaking=1;</script>"
                     "<p>Plain body copy.</p></body></html>")
            path = fh.name
        try:
            chunks, _ = ai_tells.prose_from_html(path)
            joined = " ".join(chunks)
            self.assertIn("Plain body copy.", joined)
            self.assertNotIn("breathtaking", joined)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
