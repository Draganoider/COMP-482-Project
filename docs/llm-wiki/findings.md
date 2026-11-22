# Findings

Measurements from running **this repository's code**, newest first. Every entry needs its
conditions (see [README.md](README.md)). File an **Experiment result** issue if that's easier, then
copy the result here. The report's results section is written from this page only.

**AI assistants:** never add a number you didn't get from a run, and never fill a table with
expected values (AGENTS.md hard rule 1).

---

## Hypotheses to test

What the analysis predicts and the experiments must confirm or refute. Filled in from the proposal's
evaluation plan. Whoever answers one moves it into a dated entry under Results.

| # | Hypothesis (from the analysis) | Experiment | Status |
|---|---|---|---|
| H1 | Edmonds-Karp's augmenting-path count stays within its O(VE) bound and its time within O(VE²); Ford-Fulkerson's depends on the flow value, so it can win when flows are small | E1 | Open |
| H2 | Closing a road on a minimum cut always lowers the max flow. Roads on no minimum cut can lower it too (closing one can create a new, smaller cut), so the cut alone can't rank closures and E2 re-solves for every road | E2 | Open |
| H3 | Widening a min-cut road is not always the best single road to widen: with several minimum cuts it may change nothing, which brute force will show | E3 | Open |
| H4 | With no fire, the cars out within *T* never exceed layer 1's rate × *T* or the number of households that can reach a shelter at all, and approach the smaller of the two as *T* grows (Ford and Fulkerson's temporally repeated flows give the exact form, with the routes' travel times). Road closures and a later evacuation order push it lower | E4 | Open |
| H5 | The max-flow plan never gets fewer cars out than everyone taking their shortest route, and the gap is largest when one shelter is nearest to most households | E5 | Open |

---

## Entry format

```markdown
### <short title> (YYYY-MM-DD)

**Hypothesis:** H<n>, or what you set out to learn.
**Command:** the exact command from the README, with its arguments.
**Commit:** short hash. **Machine:** CPU, RAM, OS, language version. Plugged in, nothing else running?
**Inputs:** generator or dataset, sizes, seed(s), repetitions per size.
**Result:**

| n | Algorithm A (median ms) | Algorithm B (median ms) | Ops A | Ops B |
|---|---|---|---|---|

**Plot:** `results/<file>.png`
**What it shows:** one or two sentences. Does it confirm the hypothesis? Where does it not?
**Caveats:** anything that limits it (small sizes, noisy machine, one seed).
```

---

## Results
### Pacific Palisades Road Network (2026-11-21)

**Hypothesis:** We wanted to see if we could download real road data from Pacific Palisades and use it for our wildfire evacuation project.

**Commands:**

```bash
python experiments/fetch_roads.py
python experiments/convert_roads.py
python experiments/create_sample.py
python experiments/Validate_sample.py
```

**Commit:** Not committed yet.

**Machine:** Mac, Python 3.11.

**Inputs:**
- Road data from OpenStreetMap using OSMnx.
- A 3 km area around Pacific Palisades.
- Estimated road capacity of 800 cars per hour for each directional lane.
- A smaller sample with 30 nodes and 55 edges for testing.

**Results:**

We downloaded the Pacific Palisades road network and found 874 nodes and 2,303 directed road edges.

Out of those edges, 1,198 had lane information and 1,105 were missing it. Because of this, we used estimated lane counts for roads that did not have that information.

We also found 813 possible starting nodes near residential roads. Out of those, 811 could reach one of our selected exits, while 2 could not.

We identified La Mesa Drive and Palisades Drive as two possible exit roads because they connect to roads outside our study area.

After assigning capacities, we converted the road network into our team's FlowNetwork format. The conversion worked, and the number of nodes and edges stayed the same.

We then created a smaller network with 30 nodes and 55 edges to test the algorithms.

For the maximum-flow test, NetworkX gave us 1,600 cars per hour. Our team's Edmonds-Karp algorithm also gave us 1,600 cars per hour. It found 1 augmenting path and scanned 117 edges.

**What it shows:** We were able to download real road data, assign capacities, and convert it into the format our project uses. We also tested our team's Edmonds-Karp algorithm and got the same answer as NetworkX for our sample.

**Caveats:** The road capacities are estimates because we do not have exact traffic information for every road. Some roads were also missing lane information. The two exit roads are only possible exits for our model, and we still need to do more testing with larger networks and different road conditions.

### E1: Ford-Fulkerson vs Edmonds-Karp (2026-11-21)

**Hypothesis:** We wanted to compare Ford-Fulkerson and Edmonds-Karp to see which algorithm runs faster when the network gets larger.

**Commands:**

```bash
python experiments/e1_max_flow.py
python experiments/plot_e1.py
```

**Commit:** Not committed yet.

**Machine:** Mac, Python 3.11.

**Inputs:**
- Randomly generated networks with 30, 100, 300, and 1,000 nodes.
- Random seed of 42.
- Maximum random edge capacity of 100.
- An additional path connecting the source to the sink.
- Each algorithm was tested five times per network.
- Pacific Palisades road network with 874 nodes and 2,303 directed edges.

**Results:**

We tested both algorithms using random networks of different sizes. Both algorithms returned the same maximum-flow values for each network.

In the synthetic-network tests, Edmonds-Karp was faster than Ford-Fulkerson in the runs we recorded. As the networks got larger, both algorithms took longer to finish.

We also tested both algorithms on the Pacific Palisades road network.

| Algorithm | Median Time (ms) | Maximum Flow |
|---|---:|---:|
| Ford-Fulkerson | 0.5613 | 3200 |
| Edmonds-Karp | 0.5984 | 3200 |

For the Pacific Palisades test, Ford-Fulkerson was slightly faster. Both algorithms returned the same maximum flow.

**Plot:** `results/e1_max_flow.png`

**CSV Files:** `results/e1_max_flow.csv` and `results/e1_palisades.csv`

**What it shows:** Edmonds-Karp was faster in our synthetic-network tests, while Ford-Fulkerson was slightly faster on the real road network. Both algorithms produced matching maximum-flow results.

**Caveats:** We only used one random seed and four synthetic network sizes. We also added a path to make sure the source could reach the sink. Our road capacities are estimates, and the Pacific Palisades test used only one source and sink. More testing would help us understand how the algorithms perform in other situations.

### E2: Road Closure Analysis (2026-11-21)

**Hypothesis:** We wanted to find out which road closures would have the biggest effect on evacuation capacity and whether those roads were part of the minimum cut.

**Command:**

```bash
python experiments/e2_road_closures.py
```

**Commit:** Not committed yet.

**Machine:** Mac, Python 3.11.

**Inputs:**
- Pacific Palisades road network with 874 nodes and 2,303 directed edges.
- Source node: 123082625
- Sink node: 13418556508
- Each directed road was closed individually by setting its capacity to zero.

**Results:**

The original maximum flow was 3,200 cars per hour, which matched the minimum-cut capacity. The minimum cut contained 2 directed road edges.

We tested all 2,303 directed road edges to see how much the maximum flow decreased when each one was closed.

| Road Edge ID | Capacity Lost (cars/hour) | In Original Minimum Cut? |
|---|---:|---|
| 2636 | 1600 | Yes |
| 2638 | 1600 | Yes |
| 2640 | 1600 | No |
| 4540 | 1600 | No |
| 56 | 800 | No |
| 64 | 800 | No |
| 70 | 800 | No |
| 80 | 800 | No |
| 84 | 800 | No |
| 90 | 800 | No |

Four road edges caused a capacity loss of 1,600 cars per hour. Two were part of the original minimum cut, while the other two were not.

**Plot:** `results/e2/e2_top_closures.png`

**CSV:** `results/e2/e2_road_closures.csv`

**What it shows:** Some roads outside the original minimum cut can still cause a large decrease in maximum flow when closed. This means checking only the original minimum cut is not enough to identify every road that could affect evacuation capacity.

**Caveats:** The road capacities are estimates, and we only used one source and sink. Each directed edge was tested separately, so closing a two-way physical street could have a different effect. The results show how the model behaves, not necessarily what would happen during a real wildfire evacuation.

### E3: Best Road to Widen (2026-11-22)

**Hypothesis:** We wanted to find out which road would improve evacuation capacity the most if we added one lane. We also wanted to see whether roads in the minimum cut were always the best ones to widen.

**Command:**

```bash
python experiments/e3_best_road_to_widen.py
```

**Commit:** Not committed yet.

**Machine:** Mac, Python 3.11.

**Inputs:**
- Pacific Palisades road network with 874 nodes and 2,303 directed edges.
- Source node: 123082625
- Sink node: 13418556508
- Each directed road was tested with an additional 800 cars/hour of capacity.
- Two small synthetic networks were used to test different bottlenecks.

**Results:**

The original maximum flow for the Pacific Palisades network was 3,200 cars per hour. We tested widening all 2,303 directed roads individually by adding 800 cars per hour to each road.

None of the roads increased the maximum flow. This suggests that widening only one road is not enough to improve the flow for our selected source and sink.

We also tested two smaller networks to understand why.

| Network | Original Maximum Flow | Best Widening Gain |
|---|---:|---:|
| Pacific Palisades | 3200 | 0 |
| Equal bottlenecks | 100 | 0 |
| Single bottleneck | 100 | 800 |

In the equal-bottleneck network, widening either road did not improve maximum flow because the other road still limited it.

In the single-bottleneck network, widening the road with capacity 100 increased maximum flow from 100 to 900. Widening the other road did not help.

**Plot:** `results/e3/e3_widening_comparison.png`

**CSV Files:** `results/e3/e3_widening_gains.csv` and `results/e3/e3_synthetic.csv`

**What it shows:** A road being part of the minimum cut does not always mean widening it will improve maximum flow. Sometimes other bottlenecks prevent