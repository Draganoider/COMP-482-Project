# Plan

The project's status, deadlines, people, decisions and open questions. What's graded is in
[assignments/project-outline.md](assignments/project-outline.md).

## Status

| Phase | Submit on Canvas | Due | Status |
|---|---|---|---|
| 1. Team formation | Team details | *TBD* | In progress: repository set up 2026-10-20 |
| 2. Proposal | 2–3 page PDF | *TBD* | Not started. Topic not chosen |
| 3. Final report | 8–12 page PDF, repository link, slides (if any) | *TBD* | Not started |

## Team and roles

Everyone codes and everyone writes. The roles say who coordinates what, from the outline.

| Role | Coordinates | Who |
|---|---|---|
| Project Lead | Meetings, deadlines, submitting deliverables | *TBD* |
| Algorithms Lead | Pseudocode, correctness proofs, runtime analysis | *TBD* |
| Implementation Lead | Code structure, testing, the repository README | Yevhen Mishchenko (@Draganoider) |
| Experiments Lead | Datasets, benchmark scripts, result plots | *TBD* |
| Report and Presentation Lead | Report organisation and editing, slides | *TBD* |

Where two roles meet, the default owner:

| Thing | Owner | Works with |
|---|---|---|
| Algorithm modules and the shared data structures | Implementation | Algorithms (does it match the pseudocode?) |
| Brute-force cross-checks and the test suite | Implementation | Algorithms |
| Input generators, experiment entry points, plots | Experiments | Implementation (structure, one-command rule) |
| `findings.md` entries | Whoever ran it | Experiments |
| Report sections | Report lead assigns | Each section's author |

## Decisions

Newest first. A decision is not reopened without new evidence; add a new line that supersedes the
old one instead of editing it.

| # | Date | Decision | Why |
|---|---|---|---|
| D5 | 2026-10-20 | `test` is the default branch; `main` stays protected as the release branch. Supersedes the "default branch" part of D2 | GitHub only closes issues from `Closes #N`, uses new templates and targets new pull requests on the default branch. All of those should happen on `test` |
| D4 | 2026-10-20 | The language is chosen with the topic, not before | The best fit depends on the problem (libraries, timing accuracy, plotting). The repo was set up language-neutral |
| D3 | 2026-10-20 | No AI attribution lines in commits or pull requests; AI use is disclosed in the README's *AI usage* section | One honest disclosure in a place a grader reads, instead of noise in every commit. Teammate `Co-authored-by` stays allowed |
| D2 | 2026-10-20 | `main` is the default branch and protected (pull request from `test`, one approval, CI green). `test` takes reviewed pull requests, and direct commits only for small fixes | `main` always holds what we submitted. Small fixes shouldn't wait for a review |
| D1 | 2026-10-20 | The repository is public, under @Draganoider | Branch protection on a private repository needs a paid GitHub plan |

## Open questions

| # | Question | Who answers | Answer |
|---|---|---|---|
| Q1 | Which topic? [topic-comparison.md](proposal/topic-comparison.md) has the options from the implementation side | Team | |
| Q2 | Which language? | Team, after Q1 | |
| Q3 | The three due dates | Project Lead, from Canvas | |
| Q4 | Does the course's AI policy accept our *AI usage* disclosure, or does it ask for more (per-assignment statements, logs)? | Project Lead, instructor | |
| Q5 | Is a public repository acceptable for this course while the semester runs? | Project Lead, instructor | |
| Q6 | Which textbook and pseudocode style does the course expect (likely Kleinberg and Tardos, *Algorithm Design*)? | Algorithms Lead | |
| Q7 | Are slides or a presentation required, or optional? | Project Lead, instructor | |
