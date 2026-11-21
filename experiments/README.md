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

## Pacific Palisades Road Network

We use OpenStreetMap road data downloaded through OSMnx for a study area centered near Pacific Palisades, California. The initial network contains 874 nodes and 2,303 directed road edges. Each edge has an estimated capacity in cars per hour, based on lane information and provisional assumptions.

Some roads do not include lane information, so default lane counts are used. These assumptions will be documented and verified before the final report.

Residential roads are used to identify potential evacuation starting intersections. Preliminary analysis found 813 residential starting-node candidates, with 811 able to reach at least one of the two currently selected candidate exit nodes. These exits are not yet verified evacuation destinations.

The road data has been converted into the project's FlowNetwork format, preserving all 874 nodes, 2,303 directed edges, and their individual modeled capacities.

A small sample containing 30 nodes and 55 directed edges is saved in data/palisades_sample.graphml. This sample is weakly connected and all its edges have positive capacities.
To reproduce the results, run:
```bash
python experiments/fetch_roads.py
python experiments/convert_roads.py
python experiments/create_sample.py
```
The scripts require the project's Python dependencies, including OSMnx and NetworkX. Downloading road data also requires internet access.

## Maximum-Flow Validation

We validated the 30-node Pacific Palisades sample using NetworkX and our team's Edmonds-Karp implementation.

Both algorithms produced a maximum flow of 1,600 cars per hour using the same source, sink, directed edges, and estimated road capacities.

The team's Edmonds-Karp algorithm found 1 augmenting path and scanned 117 edges.

This test confirms that both implementations agree on the selected sample network. Additional testing is needed to evaluate other source-sink pairs and larger networks.

To reproduce the validation, run:
```bash
python experiments/Validate_sample.py
```

## Road Capacity Assumptions

Road capacities are estimated using lane information from OpenStreetMap. Each road is assigned a capacity in cars per hour based on the number of lanes available in its direction of travel.

For preliminary testing, we use an estimated capacity of 800 cars per hour per directional lane.

For example:

One directional lane: 800 cars/hour

Two directional lanes: 1,600 cars/hour

Three directional lanes: 2,400 cars/hour

For two-way roads, the total lane count is divided between both travel directions. For one-way roads, all lanes are assigned to the permitted direction.

Some OpenStreetMap roads are missing lane information. In those cases, default lane counts are used to estimate their capacities.

In our downloaded network, 1,105 of the 2,303 directed road edges did not contain lane information. Among the 1,884 residential road edges, 1,051 were missing lane information.

These capacities are provisional modeling assumptions rather than measured road throughput. They will need to be justified against the Highway Capacity Manual or another appropriate transportation-engineering reference before being treated as realistic evacuation estimates.

## Evacuation Starting Nodes and Exit Selection

For our wildfire evacuation model, we identify potential starting locations using residential roads in the Pacific Palisades network.

Intersections connected to residential roads are treated as possible evacuation starting nodes. This is a simplified approach because we do not have individual household or population data.

Our analysis identified 813 residential starting-node candidates.

For evacuation exits, we examined intersections near the boundary of our study area and compared them with a larger road network to identify roads extending outside the selected area.

Two potential boundary-crossing roads were identified:

La Mesa Drive

Palisades Drive

These roads were selected as preliminary exit candidates because they connect nodes inside the study network to nodes outside it.

We also checked whether the residential starting nodes could reach at least one candidate exit using directed road connections.

Of the 813 residential starting-node candidates, 811 could reach at least one of the selected exit nodes, while 2 could not.

These exits are preliminary modeling choices. They have not yet been verified as safe or officially designated wildfire evacuation routes.

For the current network model, residential intersections represent potential evacuation origins, and boundary-crossing roads represent potential exits. Future improvements could incorporate population data, road closures, and official evacuation-route information.