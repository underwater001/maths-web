# Maths Web (SSC CGL Quant)

A knowledge web for **SSC CGL Tier 1 and Tier 2 Quantitative Aptitude**, built from previous-year questions (PYQs). Every PYQ is filed under the question type it tests; every question type carries its formulas, standard method, fast method, ultra-calculation trick and option-elimination trick. Same idea as the Current Affairs Web, with maths content.

## Structure

```
Topic  →  Concept  →  Question type  →  PYQs (year, shift, paper) + practice variants
```

- **Topic** (e.g. Profit & Loss): a branch of the syllabus. The seed tree is in `data/nodes.json`.
- **Concept**: a formula or idea a topic is built on (e.g. successive discount).
- **Question type**: one recurring pattern of question (e.g. "single equivalent discount for two discounts"). This is the unit you practise.
- Dashed links join related nodes across topics (Percentage, Ratio, Profit & Loss and SI/CI share ideas).

## Data model (planned, `data/`)

| File | Holds |
|---|---|
| `nodes.json` | Topics, concepts and question types. Fields: `label`, `kind` (`topic` / `concept` / `qtype`), `parent`, `order`, `summary`, `links`, `priority` |
| `formulas.json` | Formulas, each attached to a concept. Fields: `id`, `node`, `text`, `notes` |
| `methods.json` | Per question type: `standard`, `fast`, `ultra` (calculation trick), `eliminate` (using the options alone), `traps` |
| `papers.json` | Each paper/shift: exam, tier, year, date, shift, PDF `link` |
| `pyqs/<exam>-<year>.json` | The PYQs: `id`, `paper`, `qtype`, `q`, `options`, `answer`, `solution` |
| `practice/<qtype>.json` | Practice variants at the same level and one level harder, with answers verified by code |

## Rules

- **Nothing unverified goes in.** Every PYQ answer is recomputed in code. Every shortcut is tested on random numbers before it is saved.
- **Priority** of a question type = how often it repeats across Tier 1 and Tier 2 PYQs (`high` / `medium` / `low`).
- **No PDFs in the repo** (it is public). Only links.
- Practice questions are written fresh, not copied from other sites.

## Status

| Done | Where |
|---|---|
| Seed topic tree (6 subjects, 28 topics) | `data/nodes.json` |
| First source: SSC CGL Tier 1, 12 Sep 2025, shifts 1-3 (Adda247 *similar papers*, not official), Quant Q51-Q75 | `data/papers.json` |
| All 75 Quant questions classified to a topic, answers recomputed in code | `data/pyq_index.json`, `tools/verify_2025-09-12.py` |
| **Partnership** finished end to end: 4 concepts' worth of formulas, 4 question types, 7 PYQs, 16 verified practice questions | `data/formulas.json`, `methods.json`, `pyqs/partnership.json`, `practice/partnership.json` |

```
python3 tools/verify_2025-09-12.py     # recompute all 75 PYQ answers
python3 tools/build_partnership.py     # verify + write the Partnership data
```

## Notes on the sources

- The 12 Sep 2025 papers are **similar papers** written by a coaching institute, so topic counts reflect that publisher's style (for example no geometry-theorem questions at all), not SSC's. Priorities stay provisional until official papers are added.
- PYQs are stored as condensed restatements with the original numbers plus the paper and question number. The PDFs themselves are not in the repo; `data/papers.json` links to them.
- PDF text extraction loses stacked fractions and roots, so every question containing them is read from the page image before it is stored.
