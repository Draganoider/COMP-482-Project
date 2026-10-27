# Proposal skeleton

A starting point for the proposal, for the Report and Presentation Lead (@nicolebonillaa) to move
into the tool the team writes in (plan Q8) and hand out. Each section has an owner, a length, and
the points already agreed in [docs/plan.md](../../docs/plan.md). **The bullets are notes, not the
text**: each owner writes their section in their own words.

**Length:** 2–3 pages, about 1,500 words with the tables. The word counts below add up to that;
trim before adding.

**Before writing:**

- [ ] Due date from Canvas (plan Q3, @msoemoe18)
- [ ] Where we write it: Google Docs, Overleaf or Word (plan Q8, @nicolebonillaa)
- [ ] Section owners confirmed by @nicolebonillaa
- [ ] The three open choices in section 2 decided by @aartigapo and @JuanRazoCS1

---

## Title and team

**Owner:** @nicolebonillaa · a few lines

- Working title: *Wildfire Evacuation Planner: Max Flow and Min Cut on Los Angeles Roads*
- Course, semester, instructor
- The five members and their roles, from [the plan](../../docs/plan.md#team-and-roles)

## 1. Introduction

**Owner:** @nicolebonillaa · ~150 words

- **Why it matters:** in the January 2025 Palisades fire, mandatory evacuation orders covered
  about 30,000 people. Sunset Boulevard and Pacific Coast Highway gridlocked, and a bulldozer had
  to push abandoned cars aside ([Fox LA](https://foxla.com/news/palisades-fire-abandoned-cars)).
  A hillside neighbourhood with few roads out depends on how much those roads can carry.
- **The question:** how many cars per hour can the roads move to shelters, and which roads limit
  it?
- **What we'll do:** answer it with max flow and min cut on the real road network, prove the
  algorithms correct, and check the analysis with experiments.
- **Related work, one sentence:** Borgwardt et al. (2024) model wildfire evacuation as max flow on
  a time-expanded network; we implement and compare the algorithms ourselves, starting from the
  static problem.

## 2. Problem statement

**Owner:** @aartigapo · ~250 words · *the section the rest depends on: write it first*

The outline's test: precise enough that someone could write the brute-force solution from it.

- **Input:** a directed graph *G* = (*V*, *E*): intersections are nodes, each direction of a road
  is an edge with a capacity *c*(*e*) in cars per hour. A set *H* ⊆ *V* of household nodes and a
  set *S* ⊆ *V* of shelter nodes.
- **Model:** a super-source *s* with an edge of unlimited capacity to every household node; an edge
  of unlimited capacity from every shelter to a super-sink *t*.
- **Output 1:** the value of a maximum *s*–*t* flow: the most cars per hour the roads can deliver
  to shelters.
- **Output 2:** a minimum *s*–*t* cut: the roads that limit it (the bottlenecks).
- **What-if 1 (closure):** for each road *e*, the max flow of *G* without *e*. Which closures cost
  the most?
- **What-if 2 (widening):** for each road *e*, the max flow with *c*(*e*) raised by one lane. Which
  single road is best to widen?
- **Open choices to decide:**
  1. A two-way road: two edges, each with that direction's lanes?
  2. "Widen by one lane" in cars per hour: how much?
  3. Which shelters (real sites, or where the network leaves the area)?

## 3. Algorithms

**Owner:** @aartigapo · ~300 words · Kleinberg and Tardos chapter 7, since network flow is taught
last (plan Q9)

| Algorithm | Solves | Running time | What the report proves |
|---|---|---|---|
| Ford-Fulkerson (DFS augmenting paths) | Max flow | O(*E* · *f*\*) for integer capacities | Correctness via the max-flow min-cut theorem; termination |
| Edmonds-Karp (BFS, shortest augmenting paths) | Max flow | O(*V* *E*²) | The O(*V* *E*) bound on augmentations |
| Residual-graph search | Min cut from a max flow | O(*V* + *E*) | The set reachable from *s* gives a minimum cut |
| Brute force over all cuts | Min cut, small graphs only | O(2^*V* · *E*) | Used to check the two above |
| Re-solve per road | Closure and widening what-ifs | *E* max-flow runs | Why the min cut alone can't rank closures |

- Name the course concepts: network flow, BFS/DFS, max-flow min-cut, brute force.
- One sentence on why Ford-Fulkerson might still win on our data: its bound depends on the flow
  value, which can be small (experiment E1 tests it).

## 4. Data

**Owner:** @JuanRazoCS1 · ~200 words

- **Roads:** Pacific Palisades from OpenStreetMap, downloaded with OSMnx: road type, lanes, speed
  limits. © OpenStreetMap contributors, ODbL.
- **Capacity:** cars per hour per lane by road type, from the Highway Capacity Manual. Name the
  figures and the source once confirmed; they are assumptions, and the report will say so.
- **Shelters:** depends on choice 3 above.
- **Households:** where cars start. Census blocks if needed; for the static problem every household
  node only needs to exist.
- **Synthetic networks:** a seeded generator of growing graphs, because the real network is too
  small to show how running time grows.
- **Size:** say how many nodes and edges once downloaded. Don't estimate it.

## 5. Evaluation plan

**Owner:** @JuanRazoCS1 · ~250 words · the hypotheses are in
[findings.md](../../docs/llm-wiki/findings.md#hypotheses-to-test)

**Correctness:** every algorithm is checked against brute force on thousands of small random graphs,
and against NetworkX's max flow as a reference (tests only).

| # | Question | Measure | Expected |
|---|---|---|---|
| E1 | Which max-flow algorithm is faster, and do they meet their bounds? | Time and augmenting paths on real and synthetic graphs | Edmonds-Karp within O(*V* *E*) augmentations; Ford-Fulkerson depends on the flow value |
| E2 | Which closures cost the most? | Max flow with each road removed | Min-cut roads always lower it; others can too |
| E3 | Is the min cut a good guide to which road to widen? | Min-cut choice vs brute force over all roads | It can fail when there are several minimum cuts |

- **Method:** fixed seeds, repeated runs, medians, sizes across orders of magnitude, log-log plots
  ([benchmarking.md](../../docs/llm-wiki/benchmarking.md)).
- **Stretch experiments** E4 and E5 belong to the stretch goals (section 7).

## 6. Implementation

**Owner:** @Draganoider · ~150 words

- Python 3.11+, our own implementations; NetworkX only in tests, to check our answers.
- pytest for correctness, ruff for style, CI on every change; OSMnx for the roads, matplotlib for
  plots.
- The repository README runs every experiment with one command, and each writes its tables and
  plots to `results/`, so every number in the report can be regenerated.
- Repository link.

## 7. Stretch goals

**Owner:** @nicolebonillaa, from the plan · ~120 words · clearly marked as stretch

- **Fire extension:** a fire spreading from an ignition point (Dijkstra over map cells, with wind)
  closes roads over time. Max flow on a time-expanded network gives how many cars reach a shelter
  before their roads close (E4).
- **Shortest-route comparison:** everyone drives their shortest route to the nearest shelter
  (Dijkstra on the roads), against the max-flow plan (E5).
- **Map app** for the presentation: start a fire, watch the cars, see the bottlenecks.

## 8. Timeline and roles

**Owner:** @msoemoe18 · ~120 words or a table

| Milestone | Owner | Done by |
|---|---|---|
| Proposal submitted | @msoemoe18 | *due date* |
| Road data and capacities | @JuanRazoCS1 | |
| Problem statement and proofs drafted | @aartigapo | |
| Max flow, min cut, what-ifs, with tests | @Draganoider | |
| Experiments E1–E3 recorded | @JuanRazoCS1 | |
| Stretch goals, if time allows | Everyone | |
| Report and slides | @nicolebonillaa | *due date* |

## References

**Owner:** @nicolebonillaa · from [docs/references.md](../../docs/references.md)

- Kleinberg and Tardos, *Algorithm Design* (chapter 7)
- Borgwardt et al., *Evacuation Planning on Time-Expanded Networks with Integrated Wildfire
  Information*, arXiv 2410.14500
- OpenStreetMap and OSMnx; the Highway Capacity Manual; the Fox LA report

---

**For everyone writing:** no number goes in without a source or a run behind it (AGENTS.md hard
rule 1). Proofs are sketched here and written properly in [analysis/](../../analysis/README.md).
