# COMP 482 group project — instructions for AI agents and humans

The COMP 482 (Algorithms) group project at CSUN: a team of five designs, implements, analyses and
tests algorithms from the course on a real problem, then proves and measures what they claim.
Worth 25% of the course grade.

> **This file is the single source of truth for every AI agent working in this repository:**
> Claude Code, Codex, Cursor, Copilot, Gemini CLI and the rest. Agent-specific files
> ([CLAUDE.md](CLAUDE.md), [.github/copilot-instructions.md](.github/copilot-instructions.md)) are
> thin pointers to this one. **Put rules here, not in those.**
>
> Humans should read it too. [CONTRIBUTING.md](CONTRIBUTING.md) is the short version, and
> [REVIEWING.md](REVIEWING.md) is the reviewer's side of a pull request.

## Read this first

1. **[docs/plan.md](docs/plan.md):** status, deadlines, the team and roles, decisions so far, and
   the open questions. Decisions recorded there are not relitigated without new evidence.
2. **[docs/assignments/project-outline.md](docs/assignments/project-outline.md):** what is graded.
   When it and anything else in this repo disagree, the outline wins.
3. **The issue you're working on:** its checklist, the files it owns, and what blocks it.
4. **The [llm-wiki](docs/llm-wiki/README.md) page for what you're doing.** Before timing anything,
   [benchmarking.md](docs/llm-wiki/benchmarking.md). Before writing pseudocode or a proof,
   [course-conventions.md](docs/llm-wiki/course-conventions.md). Results so far are in
   [findings.md](docs/llm-wiki/findings.md).

## Where knowledge lives

| What | Where | Write to it when |
|---|---|---|
| Phases, scope, roles, decisions and open questions | [docs/plan.md](docs/plan.md) | A phase starts or ends, a decision would cost more than an hour to reverse, a question is answered |
| What changed | [CHANGELOG.md](CHANGELOG.md) | In the pull request that makes the change, under `[Unreleased]` |
| How things work, setup, and what was measured or learned | [docs/llm-wiki/](docs/llm-wiki/README.md) | The day you measure something, in [findings.md](docs/llm-wiki/findings.md), negative results included; a reference page in the pull request that changes what it describes |

None of these is loaded into every session the way this file is; read the one you need.

## Hard rules

1. **No claim without evidence.** The grade is mostly analysis and evidence, not code.
   - Every algorithm is checked against a brute-force or reference implementation on small inputs,
     in the test suite.
   - Every runtime or quality claim in the report points to an experiment recorded in
     [findings.md](docs/llm-wiki/findings.md), with its conditions (machine, input sizes, seed,
     commit).
   - **AI agents never invent, round or "estimate" a measured number.** If it wasn't run, say so.
2. **Every experiment runs with one command**, listed in the README's *Running the experiments*
   table, and writes its tables and plots to `results/`. Fixed seeds, so a rerun gives the same
   inputs. This is a graded requirement.
3. **Implement the algorithm that is analysed.** If the code departs from the pseudocode in the
   report (a different data structure, an early exit, a library call), the report says so, or the
   runtime analysis no longer describes the code.
4. **`main` changes only through a reviewed pull request from `test`.** GitHub enforces it. Work
   reaches `test` through a pull request with one teammate's review; a direct commit to `test` is
   allowed only for a small change (see [Branching](#branching-and-pull-requests)).
5. **No AI attribution lines in commits or pull requests:** no `Co-Authored-By` naming a tool, no
   "Generated with" lines. AI use is disclosed once, in the README's
   [AI usage](README.md#ai-usage) section, instead. `Co-authored-by` a **teammate** is fine and
   encouraged for pair work: it feeds the report's contributions section.
6. **Credit what isn't ours.** External code, datasets and articles get a line in
   [docs/references.md](docs/references.md) in the same pull request that brings them in. The
   report's references section is built from it.
7. **The repository is public.** Never commit secrets (`.env`, tokens), personal data, or the
   course's own handouts and solutions. Files over 2 MB don't belong in git: a script downloads
   large datasets into `data/raw/`, which is gitignored.

## Lessons

Mistakes that cost real time here, each with the habit that prevents it and where it happened. Add
one when a one-line habit would have saved an hour, and delete it once a CI check or a test enforces
it. A measurement goes in [findings.md](docs/llm-wiki/findings.md) instead.

- **Try a hypothesis on a small counterexample before writing it down.** H2 first claimed that
  closing a road on no minimum cut can't lower the max flow, but closing one can create a new,
  smaller cut. It went into `findings.md` that way and was only caught in the Codex review of pull
  request #1 (commit 61ba6d9).

## Current state

**23 October 2026: Phase 2 (proposal) is next.** The team chose **topic 6, the Wildfire Evacuation
Planner**, and **Python**, and agreed the roles ([docs/plan.md](docs/plan.md#team-and-roles)). The
project is built in three layers, and **layer 1, the outline's baseline, is the main deliverable**:
max flow for the cars per hour a Los Angeles road network can move to shelters, min cut for the
bottleneck roads, then the closure and widening what-ifs. The fire extension (layer 2) and the map
app (layer 3) come after it; [docs/plan.md](docs/plan.md#scope) has the scope. The folders and the
Python tooling are set up; no algorithm code exists yet.

What has merged is in [CHANGELOG.md](CHANGELOG.md), and where each phase stands is in the plan's
[Status](docs/plan.md#status) table. Update this paragraph when a phase starts or finishes, or a
layer is finished.

## Stack

| Piece | Choice |
|---|---|
| Language | Python 3.11 or newer (3.12 in CI) |
| Package | `evac`, in `src/evac/`, installed in editable mode |
| Tests and style | pytest, ruff (settings in [pyproject.toml](pyproject.toml)) |
| Reference in tests only | NetworkX: our max flow must give the same value. **Never imported in `src/`** (hard rule 3) |
| Road data | OSMnx, added with the data issue |
| Plots | matplotlib, added with the first experiment |
| App (layer 3) | FastAPI, MapLibre, deck.gl; decided in detail when layer 3 starts |
| CI | GitHub Actions: [.github/workflows/ci.yml](.github/workflows/ci.yml), hygiene checks plus ruff and pytest |

A new dependency goes in `pyproject.toml` in the pull request that first uses it, with a line in
[docs/references.md](docs/references.md).

## Getting set up

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Repo layout

Folders follow what we hand in (plan D9): every number in the report comes from an experiment in
`experiments/`, lands in `results/`, and appears in `report/`.

| Path | Contents | Owner |
|---|---|---|
| `analysis/` | Problem statement, pseudocode, correctness proofs, runtime analysis | Algorithms |
| `src/evac/` | The algorithms, one module per algorithm, plus the graph and data structures they share | Implementation |
| `tests/` | Correctness tests, including the brute-force cross-checks | Implementation |
| `experiments/` | One script per experiment (E1–E5), each runnable with one command | Experiments |
| `results/` | What the experiments write: CSV tables and plots. The ones the report uses are committed | Experiments |
| `data/` | Small datasets, committed, with their source in `docs/references.md`. Large downloads go in `data/raw/`, gitignored and fetched by a script | Experiments |
| `report/` | The proposal and the final report: outlines, figures, submitted PDFs | Report and Presentation |
| `app/` | The map app (layer 3). Displays results only; built last | Implementation |
| `docs/` | How we work: the plan, the assignment summary, the llm-wiki, references. [docs/README.md](docs/README.md) maps them | Everyone |
| `.github/` | CI, the pull request templates, the issue forms and the link checker | Implementation |
| `.claude/` | Claude Code settings and slash commands, shared by the team | Implementation |
| `.scratch/` | Your own throwaway files. Gitignored; nothing in it is ever committed | |

## Branching and pull requests

- **`test`** is the default branch, and where all work lands. Not protected.
- **`main`** is the release branch, and **protected**: changes arrive only as a pull request from
  `test`, approved by one teammate, with CI green. It holds what was submitted, tagged per phase.
- Work branches come off `test`: `feature/...`, `fix/...`, `exp/...` (experiments),
  `docs/...`, `chore/...`.

```bash
git switch test && git pull
git switch -c feature/short-name
# ... work, commit ...
git push -u origin feature/short-name
gh pr create                        # into test, the default
```

A pull request into `main` from anything but `test` is wrong; retarget it to `test`. Because `test`
is the default branch, `Closes #N` closes the issue when the pull request merges into `test`.

**A direct commit to `test` is fine only for a small change:** a typo, a broken link, a doc
correction, formatting, or a one-line fix that doesn't change what an algorithm computes or what an
experiment measures. Anything else, and anything you're unsure about, goes through a pull request.
A direct commit still needs CI green and a changelog line if it's notable.

**Merging.** Every merge is a **merge commit**, so each branch stays visible in the history.
Squash and rebase merging are turned off for the repository.

- **Into `test`:** the branch's commits arrive as they are, so keep them tidy: each one says what
  and why.
- **`test` into `main`:** a merge commit too; squashing would give `main` commits `test` doesn't
  have, and the branches would drift apart. Use the submission template:
  `gh pr create --base main --head test --template submission.md`.

## Working conventions

- **Commits:** short imperative subject (`Add Dijkstra with a binary heap`), the *why* in the body
  when it isn't obvious. No tool attribution (hard rule 5).
- **A feature brings its own record, in its own pull request:** a line in
  [CHANGELOG.md](CHANGELOG.md), the llm-wiki page it makes untrue, and an entry in
  [findings.md](docs/llm-wiki/findings.md) if it measured anything. A pull request that needs none
  of them says why in its description. Nobody writes the record afterwards, so nothing is left to
  forget.
- **Changelog:** every notable change adds a line under `## [Unreleased]` in
  [CHANGELOG.md](CHANGELOG.md) in the same pull request, ending with the author's GitHub handle.
  That, the pull request's *Contribution* section and the git history are what the report's
  contributions section is written from.
- **Docs in the same pull request** as the change that makes them untrue: this file's *Current
  state*, [docs/plan.md](docs/plan.md), the README's experiments table, the llm-wiki.
- **Measured something or learned something surprising?** Add it to
  [findings.md](docs/llm-wiki/findings.md) the same day, negative results included.
- **A decision that would cost more than an hour to reverse** gets a line in the decision log in
  [docs/plan.md](docs/plan.md#decisions).
- **Issues own files.** Stick to the files your issue lists; that's how five people work at once
  without merge conflicts.

## Writing algorithm code

- One algorithm per module, with a comment naming the report section and the pseudocode it
  implements.
- Keep the reference (brute-force) implementation as simple as possible: its only job is to be
  obviously correct.
- Where the analysis counts operations (comparisons, relaxations, heap operations), add a counter
  the experiments can read. Operation counts back up a runtime claim far better than wall time
  alone.
- Generate inputs in their own functions, with an explicit seed, and keep generation outside the
  timed region.

## For AI agents specifically

- Write proofs and complexity arguments as drafts for the Algorithms Lead to check. Never present
  one as verified.
- Never fabricate, adjust or extrapolate a measurement, and never fill a results table with
  expected values. An empty cell is honest; an invented one is academic misconduct.
- Don't change [docs/assignments/](docs/assignments/) to match the code. If they disagree, say so.
- Throwaway scripts and outputs go in `.scratch/`, not the repository.
