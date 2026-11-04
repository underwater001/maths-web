# Maths Web (SSC CGL Quant)

A **question bank** and knowledge web for SSC CGL Tier 1 and Tier 2 Quantitative Aptitude, built from previous-year questions (PYQs).

- The **Web** tab is a radial map: subject → topic → concept → question type. Tap an end node (a question type) and you are taken into that topic's **Learn** flow. Other nodes show a short panel with a "Start learning" button.
- **Learn** teaches one topic in order: overview, then each concept (its idea and formulas), then each question type under it (the *cue* that tells you it is this type, the standard / fast / ultra-calc / eliminate methods, traps, variations), then the **quiz**. The quiz runs past questions first (easiest first), then new same-level practice, then harder challenge questions, one at a time, with the solution, the fastest way in, how to eliminate options and why each wrong option is wrong. Results show which methods you keep missing; wrong answers can be replayed. Your place is remembered in this browser.
- The **Question bank** tab has *By topic* (a card per built topic with counts, difficulty mix, your progress and the methods that keep going wrong; opens Learn) and *Mixed practice* (every question as a quiz card, filtered by topic, type, difficulty, likelihood, technique, source and your progress).
- The **Sources** tab lists every paper (with its link, how many questions were filed and built) and the outside reading. Links to papers appear only there, never on question cards.

```
Topic  →  Concept  →  Question type  →  PYQs (paper, question no.) + practice variants
```

A question type is defined by its **solving pattern**: two questions are the same type if the same method solves both after the numbers are changed.

## Adding material (the routine)

Every time new maths material arrives (PDF, photos, a PDF open in the browser):

1. **Paper file.** Add `data/papers/<id>.json`: the paper's details (`exam`, `kind`, `publisher`, `date`, `shift`, `link`, `quant`) and one row per Quant question (`qno`, `topic`, `key`, `answer`, `verified`). Rows must carry a topic id from `data/tree.json`. Write a verifier in `tools/papers/` that recomputes each answer from the question's own numbers.
2. **Topic module.** Every question you file needs a quiz the same day: the build fails ("N filed question(s) in <topic> have no quiz yet") until it has one. For each topic the paper touches, copy `tools/topics/_template.py` to `tools/topics/<topic_with_underscores>.py` (or extend the existing one): concepts and question types, formulas, one method per type (including its `cue`), the PYQs, wrong-option notes, practice, and web references. Practice is a few hand-written items plus items generated from templates (`variants(...)`), so a type gets its extra and harder questions without hand-writing each. Two tiers, set by `TIER` in the module. **`"quiz"`** is the quick way live: the PYQs with checked answers, solutions, notes and one short method per type (no practice, no `ultra`). **`"full"`** (the default) adds the ultra-calc layer and needs at least 3 same-level and 3 harder practice items per type, one of them Hard. Start every new topic as `quiz` so no filed question waits, then upgrade it. When option text is not a plain number (ratios, mixed numbers) pass `optvals=[...]` to `pyq(...)`; `bank.ratio_val` and `bank.mixed_val` convert "5:9" and "15 5/6 days".
3. **Run `python3 tools/check.py`.** It rebuilds only the topics whose sources changed, then assembles `data/core.json`. Nothing is added unless it passes.
4. Commit `data/` and `tools/`. Push; GitHub Pages serves the repo root.

A new topic is one new entry in `data/tree.json` plus one new module. A new paper is one new file. Nothing else is touched, and nothing is rebuilt that did not change.

## How the data scales

```
data/tree.json            subjects and topics (hand-kept)
data/papers/<id>.json     one file per paper, with a row per question                       (source of truth)
tools/topics/<topic>.py   one module per topic: content + the code that verifies it           (source of truth)
data/shards/<topic>.json  BUILT per topic: concepts, types, formulas, methods, PYQs, practice
data/core.json            BUILT, small: all nodes, papers (with per-topic counts), likelihood stats, web references, a light list of every question
```

The page loads `core.json` first and fetches a topic's shard only when that topic is opened or a bank page needs it. Start-up cost therefore does not grow with the number of questions, and shards are cached by the browser (the version is in `core.json`). Each shard records a hash of its sources; `tools/build.py` refuses to assemble from a stale one.

## Difficulty (same rubric for every question)

| Input | Points |
|---|---|
| Steps in the full solution | 1–2 steps = 1, 3–4 = 2, 5 or more = 3 |
| Extra concepts combined | +1 for each beyond the first |
| Heavy numbers (big, or fractions that do not cancel) | +1 |
| A wrong option is the result of a common mistake | +1 |

Score up to 2 is Easy, 3–4 Medium, 5 or more Hard. The inputs are stored with each question, so levels can be recomputed if the rubric changes.

## Likelihood and "most asked"

For each question type and topic: in how many of the analysed shifts did it appear? **High** = at least 2/3 of the shifts, **Medium** = at least 1/3, **Low** = less. The shift count matters more than the question count (a type asked twice in one shift is not "asked a lot"). Stats are kept per exam, so Tier 2 will get its own numbers, and per source kind (official, memory-based, coaching paper). Every figure is shown with its sample size. With few shifts analysed it is a rough guide, not a forecast.

## What is checked in code

- **PYQ answers** are recomputed from the question's own numbers and must match the keyed option and no other.
- **Wrong-option notes**: every note carries a check (the option equals the named mistake's result, or a bound / sign / estimate rules it out). A note that does not hold for its option fails the build.
- **Practice answers** are found twice by different methods; the build fails if they disagree. The three wrong options are the results of named mistakes and must be distinct. Generated items get the same checks; unclean draws and duplicate texts are rejected, ids are stable (`<prefix>-<template>-NN`).
- **Gap gate**: every question in a paper file must have a quiz, and every quiz must have a paper row.
- **Coverage** (full tier): every question type has enough same-level and harder practice, and a Hard one.
- **Shortcuts** are random-tested against the slow method with exact fractions (`tools/shortcuts/<topic>.py`).
- **Structure**: parents, links (mirrored automatically), formulas, methods and techniques must all exist.

## Rules

- Nothing unverified goes in.
- No PDFs in the repo (it is public). PYQs are stored as condensed restatements with the original numbers plus the paper and question number; `data/papers/*.json` links to the source.
- Practice questions are written fresh. Web research is kept as links with notes in the topic's `REFS`, never copied text. Every shortcut seen online is re-derived and tested before use.
- PDF text extraction loses stacked fractions and roots, so every question containing them is read from the page image before it is stored.

## Commands

```
python3 tools/check.py             # everything: verify papers, rebuild stale topics, test shortcuts, assemble core.json
python3 tools/check.py --browser   # also the browser test (Playwright + Chrome)
python3 tools/build_topic.py profit-loss --force
python3 tools/test_shortcuts.py partnership
python3 tools/make_artifact.py OUT.html   # one self-contained page with all data inlined
```

## Status

All 75 Quant questions of the first source (three shifts, 12 September 2025) are filed, recomputed and live as quizzes across 18 topics.

| Tier | Topics | PYQs | Practice |
|---|---|---|---|
| full | Partnership, Profit & loss | 15 | 82 |
| quiz | Average, Percentage, Ratio & proportion, Mixture & alligation, Simple & compound interest, Time & work, Time-speed-distance, Mensuration 2D and 3D, Simplification, Surds & indices, Algebraic identities, Linear equations, Polygons, Trig ratios, Data interpretation | 60 | none yet |

Next: upgrade quiz-tier topics to full (practice templates and an ultra-calc layer), starting with the most asked: Mensuration 2D, Percentage, Average.

## Notes on the sources

- The 12 Sep 2025 papers (Tier 1, shifts 1–3) are **similar papers** by a coaching institute, not official CGL papers, so topic counts reflect that publisher's style (for example no geometry-theorem questions at all). Likelihood stays provisional until official papers are added.
