# Course conventions

How COMP 482 wants pseudocode, proofs and runtime analysis written, so the report reads the way the
course grades. **Still to confirm** with the lectures and the textbook (plan Q6); the Algorithms
Lead owns this page. Until confirmed, the entries below are the standard forms, not the course's
stated preference.

## Textbook

*To confirm.* The course's topics (interval partitioning, greedy stays ahead, network flow
applications) match Kleinberg and Tardos, *Algorithm Design*. Once confirmed, cite it in
[../references.md](../references.md) and use its notation.

## Pseudocode

- Numbered lines, so proofs and the runtime analysis can refer to them ("line 7 runs at most E
  times").
- Name the data structure each operation uses (`Q.extract-min()`), since it decides the runtime.
- Each algorithm module in the code names the pseudocode it implements (AGENTS.md, *Writing
  algorithm code*).

## Correctness arguments

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
