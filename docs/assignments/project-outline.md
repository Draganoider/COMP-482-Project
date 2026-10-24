# Project outline — summary

A summary, in our words, of the *COMP 482 Group Project Guide*. The original PDF is on Canvas; it
isn't committed because this repository is public. **When this page and the PDF disagree, the PDF
wins.** Fix this page, and note the change in [../plan.md](../plan.md).

## What a strong project does

The project is worth **25% of the course grade**. It must:

1. **State the problem precisely.**
2. **Prove** why the chosen algorithms are correct and **analyse** how fast they are.
3. **Check that analysis with experiments.**

Code alone isn't enough: **the analysis and the evidence carry most of the grade.**

## Phases

| Phase | What the team does | Submit on Canvas |
|---|---|---|
| 1. Team formation | Form a team of 5, set up communication and a shared Git repository | Team details |
| 2. Proposal | Define the problem, choose algorithms and data, plan the experiments, assign roles | 2–3 page PDF |
| 3. Final report | Define, implement, experiment, document | 8–12 page PDF, repository link, slides (if any) |

## Code requirements

- Any programming language.
- **The repository README explains how to run every experiment with one command each.**

## Proposal

One 2–3 page PDF per team: title, problem statement, proposed methods and algorithms, data,
evaluation plan, and so on. Checklist in [report/proposal/](../../report/proposal/README.md).

## Final report

One 8–12 page PDF per team, with the repository link and slides if any. Recommended structure:

1. **Title page:** members' names and project details.
2. **Project contributions:** each member's contributions to algorithm design, coding, test cases,
   experiments and writing.
3. **Introduction:** why the problem matters, the approach, the contributions.
4. **Algorithm design / methodology:** pseudocode, correctness arguments, runtime analysis, data
   structures, implementation details.
5. **Results and discussion:** datasets, results, visualisations, findings, hypothesis validation,
   strengths and limitations.
6. **References:** textbooks, datasets, articles, and any external code used.

Section owners and evidence sources: [report/final/](../../report/final/README.md).

## Roles (suggested, not required)

Project Lead, Algorithms Lead, Implementation Lead, Experiments Lead, Report and Presentation Lead.
Every member contributes to both code and writing. Who holds which is in
[../plan.md](../plan.md#team-and-roles).

## Project ideas

Teams are encouraged to propose their own. The outline's starting points:

| # | Idea | Course concepts |
|---|---|---|
| 1 | Campus navigator | Graphs, shortest paths, heaps |
| 2 | Degree roadmap planner | DAGs, DFS, topological sort, greedy interval partitioning |
| 3 | Huffman file compressor | Greedy, heaps |
| 4 | Diff and plagiarism checker | Dynamic programming (LCS, edit distance) |
| 5 | Cheapest network design | MST, union-find, heaps, greedy |
| 6 | Wildfire evacuation planner | Network flow, min cut, shortest paths |
| 7 | Our own idea | Any 2+ course concepts on a real problem, at the same bar, compared with brute force |

Each idea has a baseline goal and a stretch goal; both are summarised, with the implementation
effort, in [the topic comparison](../research/2026-10-20-topic-comparison.md).
