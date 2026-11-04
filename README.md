# Maths Web: SSC CGL Quant question bank

**Live site:** https://underwater001.github.io/maths-web/

A question bank for SSC CGL Tier 1 and Tier 2 Quant. Every past question can be played as a quiz, sorted by topic, question type, difficulty and how often it is asked, and each one comes with the solution, the fastest way in, how to eliminate options and the traps.

## Using the site

| Tab | What it is for |
|---|---|
| **Web** | A map of the syllabus: subject → topic → concept → question type. Tap an end dot and that topic opens in Learn. |
| **Question bank → By topic** | One card per topic: how many past and practice questions, difficulty mix, your progress and the methods you keep getting wrong. |
| **Question bank → Mixed practice** | Every question as a card. Filter by topic, type, difficulty, likelihood, technique, source and your progress. |
| **Sources** | Every paper (with its link) and the outside reading. Links appear only here, never on question cards. |

**Learn** takes one topic in order:

1. Overview
2. Each concept: the idea and its formulas
3. Each question type under it: how to spot it (the cue), the standard, fast, ultra-calc and elimination methods, the traps
4. The quiz, one question at a time: past questions (easiest first), then practice at the same level, then harder ones

After each answer you see the solution, the fastest way in and why each wrong option is wrong. The result page lists the methods you missed, and wrong answers can be replayed. Your place and scores are kept in your browser only.

## What is in it now

18 topics are live. All 75 questions from the three 12 September 2025 shifts are filed and playable.

Two levels of build (see "Tiers" below): **full** topics have practice and harder questions on top of the past questions; **quiz** topics have the past questions with solutions and a short method per type, and practice comes later.

| Topic | Level | Past questions | Practice | Question types |
|---|---|---|---|---|
| Profit, loss & discount | full | 8 | 46 | 5 |
| Partnership | full | 7 | 36 | 4 |
| Mensuration 2D | quiz | 8 | none yet | 4 |
| Percentage | quiz | 6 | none yet | 4 |
| Average | quiz | 6 | none yet | 3 |
| Mixture & alligation | quiz | 5 | none yet | 4 |
| Simplification & BODMAS | quiz | 4 | none yet | 3 |
| Ratio & proportion | quiz | 4 | none yet | 3 |
| Simple & compound interest | quiz | 4 | none yet | 4 |
| Time & work | quiz | 4 | none yet | 4 |
| Time, speed & distance | quiz | 4 | none yet | 4 |
| Surds & indices | quiz | 3 | none yet | 2 |
| Mensuration 3D | quiz | 3 | none yet | 3 |
| Ratios & identities (trigonometry) | quiz | 3 | none yet | 3 |
| Algebraic identities | quiz | 2 | none yet | 2 |
| Linear equations | quiz | 2 | none yet | 1 |
| Quadrilaterals & polygons | quiz | 1 | none yet | 1 |
| Data interpretation | quiz | 1 | none yet | 1 |

No questions filed yet (they appear as dim dots on the map): Number system, HCF & LCM, Ages, Quadratic equations, Inequalities & maxima/minima, Lines & angles, Triangles, Circles, Heights & distances, Statistics.

**Next:** upgrade quiz topics to full, starting with the most asked (Mensuration 2D, Percentage, Average).

## Things to know about the data

- **Likelihood is rough.** It rests on 3 shifts, and they are *similar papers* by a coaching institute, not official CGL papers (for example there are no geometry-theorem questions at all). It stays provisional until official papers are added.
- **Quiz-level topics** mostly have auto-written wrong-option notes ("does not match the worked answer") instead of named common mistakes, and no ultra-calc layer.
- **Source quirks:** S2 Q72 (cyclic quadrilateral) is not a real cyclic quadrilateral, and S2 Q63 option (a) is printed oddly in the paper. Both are noted in their solutions.

## Adding material

Send a PDF, photos, or open a PDF in the browser. The routine for each paper:

1. **File the paper**: add `data/papers/<id>.json` (details plus one row per Quant question: number, topic, keyed option, answer) and a verifier in `tools/papers/` that recomputes every answer from the question's own numbers.
2. **Give every question a quiz the same day**: in `tools/topics/<topic_with_underscores>.py` (copy `_template.py` for a new topic) add the concepts, question types, formulas, one method per type and the past questions. The build fails with "N filed question(s) in <topic> have no quiz yet" until this is done.
3. **Run `python3 tools/check.py --browser`.** It re-verifies everything, rebuilds only what changed and tests the page. Nothing goes live unless it passes.
4. **Commit and push to `main`**; GitHub Pages serves the repo root.

A new paper is one file. A new topic is one entry in `data/tree.json` plus one module. Nothing else has to change.

### Tiers

Set `TIER` at the top of a topic module.

| | `"quiz"` | `"full"` (default) |
|---|---|---|
| Past questions with checked answers, solutions, wrong-option notes | yes | yes |
| Short method per type (cue, standard, fast, eliminate, traps) | yes | yes |
| Ultra-calc layer | no | yes |
| Practice | none | at least 3 same-level and 3 harder per type, one of them Hard |

Start every new topic as `quiz` so nothing filed waits, then upgrade it to `full`.

If an option is not a plain number (a ratio such as "5:9", a mixed number such as "15 5/6 days"), pass `optvals=[...]` to `pyq(...)`. `bank.ratio_val` and `bank.mixed_val` convert them.

## How it is built

```
data/tree.json            subjects and topics                       hand-kept
data/papers/<id>.json     one file per paper                        source of truth
tools/topics/<topic>.py   one module per topic: content + checks    source of truth
data/shards/<topic>.json  built per topic                           generated
data/core.json            built, small: nodes, papers, stats        generated
index.html                the whole front end
```

The page loads `core.json` first and fetches a topic's shard only when that topic is opened, so start-up stays fast as the data grows. Each shard records a hash of its sources, and `tools/build.py` refuses to assemble from a stale one.

## Checks that run in code

- **Past-question answers** are recomputed from their own numbers and must match the keyed option and no other.
- **Wrong-option notes** each carry a check, and a note that does not hold for its option fails the build.
- **Practice answers** (full tier) are found twice by different methods and must agree.
- **No gaps**: every filed question has a quiz and every quiz has a filed question.
- **Coverage** (full tier): enough same-level and harder practice per type, including a Hard one.
- **Shortcuts** are random-tested against the slow method with exact fractions.
- **Structure**: parents, links, formulas, methods and technique tags must all exist.

## How difficulty and likelihood are worked out

**Difficulty** uses one rubric for every question:

| Input | Points |
|---|---|
| Steps in the full solution | 1–2 steps = 1, 3–4 = 2, 5 or more = 3 |
| Extra concepts combined | +1 each |
| Heavy numbers | +1 |
| A wrong option is a common-mistake result | +1 |

Up to 2 is Easy, 3–4 Medium, 5 or more Hard.

**Likelihood** is the share of analysed shifts that contained the question type: High at 2/3 or more, Medium at 1/3 or more, Low below that. Shifts count, not questions: a type asked twice in one shift is not "asked a lot". Every figure is shown with its sample size.

## Rules

- Nothing unverified goes in.
- No PDFs in this public repo. Questions are stored as condensed restatements with the original numbers, plus paper and question number.
- Practice questions are written fresh. Web research is kept as links with notes in the topic's `REFS`, never copied text, and every shortcut is re-derived and tested before use.
- PDF text extraction loses stacked fractions and roots, so those questions are read from the page image first.

## Commands

```
python3 tools/check.py              # verify papers, rebuild stale topics, test shortcuts, assemble core.json
python3 tools/check.py --browser    # the same, plus the browser test (Playwright + Chrome)
python3 tools/build_topic.py profit-loss --force
python3 tools/test_shortcuts.py partnership
python3 tools/make_artifact.py OUT.html    # one self-contained page with all data inlined
```
