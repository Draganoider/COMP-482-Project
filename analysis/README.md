# Analysis

The written half of the algorithms: the precise problem, the pseudocode, why each algorithm is
correct, and how fast it is. The report's *Algorithm design / methodology* section is built from
these pages. Owner: the Algorithms Lead; everyone writes the parts for what they build.

Write it the way the course does ([course-conventions.md](../docs/llm-wiki/course-conventions.md)):
Kleinberg and Tardos's notation and proof forms, numbered pseudocode under an *Input* / *Output*
header.

## Pages

| Page | What | Layer | Status |
|---|---|---|---|
| `problem.md` | The precise problem: input, output, what counts as correct, what is optimised. Detailed enough to write the brute force from | 1, 2 | To write, for the proposal |
| `max-flow.md` | Ford-Fulkerson and Edmonds-Karp: pseudocode, correctness, running time | 1 | To write |
| `min-cut.md` | Finding the min cut from the residual graph; max-flow min-cut; closing and widening roads | 1 | To write |
| `fire-spread.md` | Fire arrival times by Dijkstra over map cells | 2 | Later |
| `time-expanded.md` | The time-expanded network: why its max flow is the most cars that reach a shelter in time; the link to layer 1's rate × time | 2 | Later |
| `shortest-routes.md` | The shortest-route plan, and why the max-flow plan can never do worse | 2 | Later |

Add the page to this table when you start it.

## Each algorithm page has

1. **Problem:** what it takes and returns, in the notation of `problem.md`.
2. **Pseudocode:** numbered lines, naming the data structure each step uses.
3. **Correctness:** the claim, then the proof.
4. **Running time:** the bound, in the input's own measures (V, E, the flow value), and which data
   structure it assumes.
5. **Implementation:** the module in `src/evac/` that implements it, and any place the code departs
   from the pseudocode (AGENTS.md hard rule 3).
6. **Checked by:** the tests and the experiments (E1–E5) that test its claims.

Proofs drafted with an AI assistant are drafts until the Algorithms Lead has checked them
(AGENTS.md, *For AI agents specifically*).
