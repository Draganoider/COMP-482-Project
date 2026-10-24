# Experiments

One script per experiment, each run with **one command** from the repository root, each writing its
tables and plots to `results/`. This is a graded requirement (AGENTS.md hard rule 2). Owner: the
Experiments Lead.

| # | Layer | Question | Script | Status |
|---|---|---|---|---|
| E1 | 1 | Which max-flow algorithm is faster on our inputs, and does each stay within its bound? | `e1_max_flow_algorithms.py` | Planned |
| E2 | 1 | Which road closures cost the most capacity? | `e2_road_closures.py` | Planned |
| E3 | 1 | Is the min cut a good guide to which road to widen, against brute force? | `e3_best_road_to_widen.py` | Planned |
| E4 | 2 | How much does the fire cost, and how does the result relate to layer 1's rate × time? | `e4_fire_cost.py` | Later |
| E5 | 2 | How much better is the max-flow plan than everyone taking their shortest route? | `e5_shortest_routes.py` | Later |

The hypotheses behind each are in [findings.md](../docs/llm-wiki/findings.md#hypotheses-to-test).

## Each experiment

- **Runs as** `python experiments/<script>.py`, with no arguments needed, and is listed in the
  README's *Running the experiments* table in the same pull request.
- **Writes** `results/<e-number>/` only: a CSV with one row per (algorithm, input, size, seed,
  repetition), and the plots, made from that CSV by the same script.
- **Fixes its seeds** and generates inputs outside the timed region.
- **Follows** [benchmarking.md](../docs/llm-wiki/benchmarking.md): repetitions, medians, sizes
  that span orders of magnitude, operation counts as well as time.
- **Is recorded** in [findings.md](../docs/llm-wiki/findings.md) the day it's run, with the
  machine, commit and conditions.
