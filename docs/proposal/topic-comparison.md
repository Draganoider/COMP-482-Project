# Topic comparison — from the implementation side

Input for the team's topic discussion (plan Q1), written 2026-10-20 by the Implementation Lead. It
compares the outline's ideas on **how hard they are to build, test and measure**, not on which is
most interesting; that's the team's call. Effort estimates are judgement, not measurement.

## For every topic

- **Real data is usually too small to time.** A campus graph has a few hundred nodes; every
  algorithm finishes in microseconds. Plan two kinds of input from the start: the real dataset for
  the story and the correctness examples, and a **seeded synthetic generator** that scales to
  10⁵–10⁶ elements for the runtime experiments.
- **The outline asks for 2+ algorithms and experiments that check the analysis.** The easiest
  topics to grade well have two algorithms whose analyses predict **different** winners on
  different inputs (sparse vs dense, small vs large alphabet). A crossover in a plot, predicted by
  the analysis, is the strongest evidence a report can show.
- **A brute-force oracle** makes testing cheap: run both on thousands of small random inputs and
  compare. Every topic below has one.

## At a glance

| # | Topic | Data effort | Correctness oracle | The experiment that shows the analysis | Risk |
|---|---|---|---|---|---|
| 1 | Campus navigator | **High**: build the CSUN walkway graph (OpenStreetMap helps) | Dijkstra, Bellman-Ford and Floyd-Warshall must agree; all paths on tiny graphs | Array vs binary-heap priority queue: O(V²) vs O((V+E) log V), crossover on dense vs sparse graphs | Building the campus graph eats time; accessibility mode needs careful modelling |
| 2 | Degree roadmap planner | Low: the CS catalogue, entered by hand | All topological orders of tiny DAGs; min semesters = longest path | Weak: everything is linear time. The stretch goal (credit cap) is where the interesting result is | Baseline is thin for 5 people; the credit-cap version is NP-hard, so "optimal" needs brute force or ILP |
| 3 | Huffman compressor | **Low**: public text corpora (Canterbury, Project Gutenberg) | Decode(encode(x)) = x; optimality against brute force on tiny alphabets; the entropy bound | Compressed size vs fixed-length codes and vs gzip; heap vs sorted-list construction time | Bit-level I/O is fiddly. Only one core algorithm, so the second needs care (word-level Huffman, or the heap comparison) |
| 4 | Diff and plagiarism checker | **Low**: any text or source files | Exponential brute-force LCS on short strings | O(nm) time and memory, then the stretch: Hirschberg's linear-space LCS, with memory measured | Low. Diff output formatting is the only tedious part |
| 5 | Cheapest network design | **Low**: city coordinates (public lists) plus synthetic graphs | Kruskal and Prim must give the same total weight; all spanning trees of tiny graphs | Kruskal vs Prim on sparse vs dense graphs: a clean predicted crossover. Stretch: k-clustering with plots | Low. Well defined, and the stretch goal visualises well |
| 6 | Wildfire evacuation planner | **High**: LA road network with capacities, which have to be estimated from lanes and road type | Max flow = min cut value; all cuts of tiny graphs | Ford-Fulkerson vs Edmonds-Karp augmenting-path counts and time; the bottleneck-closure what-if | Data modelling and its assumptions dominate. The strongest real-world story |
| 7 | Our own idea | Depends | Required by the outline (compare with brute force) | Depends | Proposal must be very precise to be approved |

## Notes per topic

**1. Campus navigator.** Three shortest-path algorithms plus two priority queues give plenty of
parallel work. The heap vs array comparison is a textbook crossover. The cost is the graph: someone
spends a week on building IDs, coordinates, walkways and stairs. OpenStreetMap's footpath data
around CSUN can be the starting point.

**2. Degree roadmap planner.** Easy to build, but the baseline algorithms are all O(V + E), so the
runtime experiments have little to show. It becomes a strong project only with the credit-cap
stretch goal, showing where the greedy plan stops being optimal against an exact solver on small
catalogues.

**3. Huffman compressor.** The safest choice: well understood, easy data, an easy oracle. The
outline asks to compare against fixed-length codes on at least 5 corpora, which is cheap. Watch the
"2+ algorithms" bar: frame it as character vs word-level Huffman, plus the priority-queue
comparison.

**4. Diff and plagiarism checker.** DP gives the cleanest asymptotic experiments (time and memory
both grow as n·m), and Hirschberg's algorithm turns the stretch goal into a measurable memory
result. Similarity scoring (edit distance) gives the "real problem" angle.

**5. Cheapest network design.** Kruskal (union-find) vs Prim (heap) is the clearest "the analysis
predicts which wins where" experiment of the list. k-clustering on a real dataset makes good figures
for the report and slides.

**6. Wildfire evacuation planner.** The most compelling story and the most modelling: road
capacities, shelter locations, and what a "vehicles per hour" bound means. Good if a teammate wants
to own the data, risky otherwise.

## From the implementation side

- **Lowest risk with a strong evaluation:** 5 (MST) and 4 (Diff/LCS).
- **Safest overall:** 3 (Huffman), if the second algorithm is framed carefully.
- **Highest payoff, highest data cost:** 1 (Campus navigator) and 6 (Wildfire evacuation).
- **Needs its stretch goal to be strong:** 2 (Degree roadmap).

A combination is allowed and can be strong. For example, MST clustering on the same campus graph as
the navigator reuses one dataset across two course concepts.
