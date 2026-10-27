# Course conventions

How COMP 482 wants pseudocode, proofs and runtime analysis written, so the report reads the way the
course grades. The Algorithms Lead owns this page. Checked against the lecture slides for weeks 1–10
on 2026-10-22 (the slides themselves are on Canvas, not in this public repository).

## Textbook and syllabus

- **Main textbook: Kleinberg and Tardos, *Algorithm Design*.** Second text: Cormen et al.,
  *Introduction to Algorithms*. Use Kleinberg and Tardos's notation and proof forms first.
- **Taught by week 10:** asymptotic analysis and recurrences, divide and conquer, BFS, DFS and
  topological sort, Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal, Prim, greedy algorithms
  (activity selection, fractional knapsack, Huffman), dynamic programming (0-1 knapsack, matrix
  chain, LCS).
- **Still to come:** binary heaps and search trees, then **network flow** and NP-completeness,
  last in the semester. A flow-based project has to learn max flow from the textbook (Kleinberg
  and Tardos, chapter 7) before the lectures reach it.

## Pseudocode

The lectures write pseudocode as plain English-like statements with indentation, under an
*Input* and *Output* header; the first lectures number the lines, later ones use braces. For the
report:

- An *Input* / *Output* header, then numbered lines, so proofs and the runtime analysis can refer
  to them ("line 7 runs at most E times").
- Name the data structure each operation uses (`Q.extract-min()`), since it decides the runtime.
- Each algorithm module in the code names the pseudocode it implements (AGENTS.md, *Writing
  algorithm code*).

## Correctness arguments

The lectures prove a greedy algorithm correct in two steps: **some optimal solution contains the
greedy choice** (shown by swapping it into an optimal solution, the "cut-and-paste" or exchange
argument), and **optimal substructure** (what's left is optimal for the subproblem, by
contradiction). Dynamic programming is argued from optimal substructure and overlapping
subproblems. Follow the same shape in the report.

The standard proof forms, by algorithm type:

| Algorithm type | Usual proof | Examples |
|---|---|---|
| Greedy | Greedy stays ahead, or an exchange argument | Interval scheduling and partitioning, Huffman |
| MST | The cut property (and the cycle property) | Kruskal, Prim |
| Shortest paths | Induction on the set of finalised vertices; loop invariant | Dijkstra, Bellman-Ford |
| Dynamic programming | Induction on subproblem size, from the recurrence | LCS, edit distance, Floyd-Warshall |
| Graph search | Loop invariant, or properties of the DFS tree | Cycle detection, topological sort |
| Network flow | Max-flow min-cut theorem; termination from integer capacities | Ford-Fulkerson, Edmonds-Karp |

## Runtime analysis

- State the bound in terms of the input's own measures (V and E, n and m, alphabet size), not just
  "n".
- Say which data structure the bound assumes, and what it would be with the alternative. That
  comparison is usually what the experiments test.
- Give space as well as time when the topic is about memory (DP, the diff tool's stretch goal).
