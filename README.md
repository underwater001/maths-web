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
