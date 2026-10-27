# Plan

The project's status, scope, people, decisions and open questions. What's graded is in
[assignments/project-outline.md](assignments/project-outline.md).

## Status

| Phase | Submit on Canvas | Due | Status |
|---|---|---|---|
| 1. Team formation | Team details | *TBD* | Done 2026-10-23: team of five, roles agreed, repository shared |
| 2. Proposal | 2–3 page PDF | *TBD* | Next. Checklist in [report/proposal/](../report/proposal/README.md) |
| 3. Final report | 8–12 page PDF, repository link, slides (if any) | *TBD* | Not started |

## Scope

**Topic 6, the Wildfire Evacuation Planner**, built in three layers. Layer 1 alone meets the
outline's bar; each later layer starts only when the one before it works and is tested.

| Layer | What | Course concepts | Status |
|---|---|---|---|
| **1. Main deliverable** | The outline's baseline and stretch goals: a Los Angeles road network (Pacific Palisades, from OpenStreetMap) with capacities in cars per hour. Max flow gives the cars per hour the roads can move to **shelters**; min cut finds the bottleneck roads. Then: the capacity lost when each bottleneck road closes, and the best single road to widen, against brute force | Max flow (Ford-Fulkerson, Edmonds-Karp), max-flow min-cut, brute force | Not started |
| **2. Our extension** | A fire that closes roads as it spreads (Dijkstra over map cells, with wind). Max flow on a time-expanded network: how many cars reach a shelter before their roads close. Compared with everyone driving their shortest route to the nearest shelter (Dijkstra on the roads) | Dijkstra, max flow, graph modelling | Not started |
| **3. Presentation** | A map app: start a fire, watch every car (flow decomposition), see the bottlenecks. It only displays what the Python code computes. Built last, cut first if time runs short | Flow decomposition | Not started |

The experiments that check the analysis, by layer. Their hypotheses are tracked in
[findings.md](llm-wiki/findings.md#hypotheses-to-test).

| # | Layer | Question |
|---|---|---|
| E1 | 1 | Which max-flow algorithm is faster on our inputs, and does each stay within its bound? |
| E2 | 1 | Which road closures cost the most capacity? |
| E3 | 1 | Is the min cut a good guide to which road to widen, against brute force? |
| E4 | 2 | How much does the fire cost, and how does the result relate to layer 1's rate × time? |
| E5 | 2 | How much better is the max-flow plan than everyone taking their shortest route? |

The concept page shared with the team on 2026-10-23 (link in the team's Discord) shows the three
layers and a clickable sketch on made-up data.

## Team and roles

Everyone codes and everyone writes. The roles say who coordinates what, from the outline.

| Role | Coordinates | Who |
|---|---|---|
| Project Lead | Meetings, deadlines, submitting deliverables | May Thu Soe Moe (@msoemoe18) |
| Algorithms Lead | Problem statement, pseudocode, correctness proofs, runtime analysis | @aartigapo |
| Implementation Lead | Code structure, testing, the repository README | Yevhen Mishchenko (@Draganoider) |
| Experiments Lead | Datasets, experiment scripts, result plots | Juan Razo (@JuanRazoCS1) |
| Report and Presentation Lead | Report organisation and editing, slides | Nicole (@nicolebonillaa) |

Where two roles meet, the default owner:

| Thing | Owner | Works with |
|---|---|---|
| Problem statement, pseudocode, proofs in `analysis/` | Algorithms | Implementation (does the code match?) |
| Algorithm modules in `src/` and the shared data structures | Implementation | Algorithms |
| Brute-force cross-checks and the test suite in `tests/` | Implementation | Algorithms |
| Road data and input generators in `data/`, experiment scripts in `experiments/`, plots in `results/` | Experiments | Implementation (structure, one-command rule) |
| `findings.md` entries | Whoever ran it | Experiments |
| Proposal and report in `report/` | Report and Presentation, sections assigned to everyone | Each section's author |
| Deadlines and Canvas submissions | Project | Everyone |

## Decisions

Newest first. A decision is not reopened without new evidence; add a new line that supersedes the
old one instead of editing it.

| # | Date | Decision | Why |
|---|---|---|---|
| D9 | 2026-10-23 | Folders by deliverable: `analysis/`, `src/`, `tests/`, `experiments/`, `results/`, `data/`, `report/`, `app/`, with `docs/` for how we work | Most of the grade is the report and its evidence, so the writing and the results get first-class places beside the code, and every number traces from `experiments/` to `results/` to `report/` |
| D8 | 2026-10-23 | Python for all the code: 3.11 or newer, pytest, ruff. NetworkX only as a reference in tests, never in `src/` | The team agreed. Python's data and plotting libraries (OSMnx, matplotlib) fit the problem; the graded algorithms must be our own (AGENTS.md hard rule 3) |
| D7 | 2026-10-23 | Three layers, with the outline's baseline as the main deliverable (see *Scope*). Destinations are shelters | The baseline is what the outline grades; the fire and the app add to it without putting it at risk |
| D6 | 2026-10-23 | Topic 6, the Wildfire Evacuation Planner, chosen by the team | Supersedes D4's "language chosen with the topic": both are now chosen |
| D5 | 2026-10-20 | `test` is the default branch; `main` stays protected as the release branch. Supersedes the "default branch" part of D2 | GitHub only closes issues from `Closes #N`, uses new templates and targets new pull requests on the default branch. All of those should happen on `test` |
| D4 | 2026-10-20 | The language is chosen with the topic, not before | The best fit depends on the problem (libraries, timing accuracy, plotting). The repo was set up language-neutral |
| D3 | 2026-10-20 | No AI attribution lines in commits or pull requests; AI use is disclosed in the README's *AI usage* section | One honest disclosure in a place a grader reads, instead of noise in every commit. Teammate `Co-authored-by` stays allowed |
| D2 | 2026-10-20 | `main` is the default branch and protected (pull request from `test`, one approval, CI green). `test` takes reviewed pull requests, and direct commits only for small fixes | `main` always holds what we submitted. Small fixes shouldn't wait for a review |
| D1 | 2026-10-20 | The repository is public, under @Draganoider | Branch protection on a private repository needs a paid GitHub plan |

## Open questions

| # | Question | Who answers | Answer |
|---|---|---|---|
| Q1 | Which topic? | Team | **Topic 6** (D6), 2026-10-23. The comparison that informed it is [a dated snapshot](research/2026-10-20-topic-comparison.md) |
| Q2 | Which language? | Team | **Python** (D8), 2026-10-23 |
| Q3 | The three due dates | Project Lead, from Canvas | |
| Q4 | Does the course's AI policy accept our *AI usage* disclosure, or does it ask for more (per-assignment statements, logs)? | Project Lead, instructor | |
| Q5 | Is a public repository acceptable for this course while the semester runs? | Project Lead, instructor | |
| Q6 | Which textbook and pseudocode style does the course expect? | Algorithms Lead | **Answered 2026-10-22** from the lecture slides: Kleinberg and Tardos (main), Cormen et al. (second). Style in [course-conventions.md](llm-wiki/course-conventions.md) |
| Q7 | Are slides or a presentation required, or optional? | Project Lead, instructor | |
| Q8 | Where do we write the proposal and report together (Google Docs, Overleaf, Word)? | Report and Presentation Lead | |
| Q9 | Network flow is taught last in the course. Who reads Kleinberg and Tardos chapter 7 first, and when? | Algorithms Lead | |
