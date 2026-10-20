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

## Current state

**20 October 2026: Phase 1 (team formation).** The repository and its conventions are set up. **The
topic and the language are not chosen yet**; the team decides them together for the proposal.
[docs/proposal/topic-comparison.md](docs/proposal/topic-comparison.md) compares the outline's ideas
from the implementation side. No code exists yet, so CI runs only the repository hygiene checks.

Update this paragraph when a phase starts or finishes, or the topic or language is decided.

## Stack

| Piece | Choice |
|---|---|
| Language | **Not decided** (see [docs/plan.md](docs/plan.md#open-questions)) |
| Tests | Decided with the language |
| Plots | Decided with the language |
| CI | GitHub Actions: [.github/workflows/ci.yml](.github/workflows/ci.yml) |

When the language is chosen, fill in this table, *Repo layout*, *Getting set up*, the CI test job,
`.gitignore`, `/check` in [.claude/commands/](.claude/commands/), and the README's commands.

## Repo layout

| Path | Contents |
|---|---|
| `docs/` | The plan, the assignment summary, the llm-wiki, the proposal and report drafts. [docs/README.md](docs/README.md) maps them |
| `.github/` | CI, the pull request templates, the issue forms and the link checker |
| `.claude/` | Claude Code settings and slash commands, shared by the team |
| `.scratch/` | Your own throwaway files. Gitignored; nothing in it is ever committed |

Planned once the language is chosen (rename to the language's conventions):

| Path | Contents |
|---|---|
| `src/` | The algorithms, one module per algorithm, plus the data structures they share |
| `tests/` | Correctness tests, including the brute-force cross-checks |
| `experiments/` | One entry point per experiment, each runnable with one command |
| `results/` | What the experiments write: CSV tables and plots. The ones the report uses are committed |
| `data/` | Small datasets, committed, with their source in `docs/references.md`. Large ones go in `data/raw/`, gitignored and downloaded by a script |

## Branching and pull requests

- **`main`** is the default branch and **protected**: changes arrive only as a pull request from
  `test`, approved by one teammate, with CI green. It holds what was submitted, tagged per phase.
- **`test`** is where all work lands. Not protected.
- Work branches come off `test`: `feature/...`, `fix/...`, `exp/...` (experiments),
  `docs/...`, `chore/...`.

```bash
git switch test && git pull
git switch -c feature/short-name
# ... work, commit ...
git push -u origin feature/short-name
gh pr create --base test            # NOT main, which is the default
```

**`--base test` matters.** `main` is the default branch, so GitHub proposes `main` for every new
pull request. A pull request into `main` from anything but `test` is wrong; retarget it.

**A direct commit to `test` is fine only for a small change:** a typo, a broken link, a doc
correction, formatting, or a one-line fix that doesn't change what an algorithm computes or what an
experiment measures. Anything else, and anything you're unsure about, goes through a pull request.
A direct commit still needs CI green and a changelog line if it's notable.

Merging:
- **Into `test`: squash and merge**, with a message that says what and why.
- **`test` into `main`: create a merge commit**, never squash, or the branches drift apart. Use the
  submission template: `gh pr create --base main --head test --template submission.md`.

## Working conventions

- **Commits:** short imperative subject (`Add Dijkstra with a binary heap`), the *why* in the body
  when it isn't obvious. No tool attribution (hard rule 5).
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
