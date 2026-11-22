# Results and Discussion

## Dataset

We used road-network data from OpenStreetMap through OSMnx to study a 3 km area around Pacific Palisades, California. The network contained 874 nodes and 2,303 directed road edges. We estimated road capacity using 800 cars per hour per directional lane. Since 1,105 road edges did not include lane information, we used estimated lane counts for those roads.

We also identified 813 possible starting nodes near residential roads. Of those, 811 could reach one of our selected exits. We selected possible exit roads including La Mesa Drive and Palisades Drive. These were candidate exits for our model, not official evacuation routes.

## E1: Algorithm Performance

We compared Ford-Fulkerson and Edmonds-Karp using synthetic networks containing 30, 100, 300, and 1,000 nodes. We also tested both algorithms on the Pacific Palisades network. Each algorithm was run five times per network.

| Network | Ford-Fulkerson (ms) | Edmonds-Karp (ms) |
|---|---:|---:|
| 30 nodes | 0.0560 | 0.0585 |
| 100 nodes | 0.3727 | 0.1536 |
| 300 nodes | 1.4406 | 0.9944 |
| 1,000 nodes | 8.7607 | 3.9038 |
| Pacific Palisades | 0.5566 | 0.8503 |

Both algorithms returned the same maximum-flow values. Edmonds-Karp was faster on the synthetic networks with 100, 300, and 1,000 nodes, while Ford-Fulkerson was slightly faster on the 30-node network.

On the Pacific Palisades network, Ford-Fulkerson was also faster. Both algorithms calculated a maximum flow of 3,200 cars per hour.

These results partly support H1. Edmonds-Karp performed better on the larger synthetic networks, but Ford-Fulkerson was faster in some cases. The experiments do not prove the theoretical complexity bounds.

**Figure 1:** `results/e1/e1_max_flow.png`

## E2: Road Closure Analysis

We tested closing each of the 2,303 directed road edges individually to measure changes in maximum flow. The original maximum flow was 3,200 cars per hour, which matched the minimum-cut capacity.

Four road edges caused the largest reduction in maximum flow. Closing edges 2636, 2638, 2640, or 4540 individually reduced the maximum flow by 1,600 cars per hour. However, only edges 2636 and 2638 belonged to the original minimum cut.

These results partly support H2. Closing either edge in the original minimum cut reduced maximum flow, but roads outside that cut also caused large reductions. This demonstrates why testing individual closures gives more information than relying on a single minimum cut.

**Figure 2:** `results/e2/e2_top_closures.png`

## E3: Road Widening Analysis

We tested increasing the capacity of every directed road individually by 800 cars per hour. None of the 2,303 road edges increased the maximum flow beyond the original 3,200 cars per hour.

To understand this result, we also tested two smaller synthetic networks. In the equal-bottleneck network, widening either road did not improve maximum flow because the other road continued to limit capacity. In the single-bottleneck network, widening the bottleneck increased maximum flow from 100 to 900.

These results support H3 by showing that widening a road belonging to a minimum cut does not always improve the network's maximum flow. Multiple bottlenecks may need to be addressed together.

**Figure 3:** `results/e3/e3_widening_comparison.png`

## Strengths and Limitations

One strength of our experiments is that we tested the algorithms on both synthetic networks and real geographic road-network data. We also compared the two maximum-flow algorithms and tested road closures and widening individually to understand how network bottlenecks affect evacuation capacity.

However, our model has several limitations. Road capacities were estimated rather than measured, and many roads were missing lane information. Our experiments also used one selected source and sink, which does not represent all evacuation origins and destinations.

The model does not account for traffic signals, intersection delays, travel time, shelter capacity, or changing conditions during a wildfire. Closing one directed edge is also not necessarily equivalent to closing an entire physical street.

Therefore, the results represent maximum-flow capacity under our simplified assumptions rather than the number of people who could safely evacuate during a real wildfire.

Overall, our experiments showed that the faster maximum-flow algorithm depends on the network being tested. Road closures can reduce evacuation capacity even when the affected roads are outside the original minimum cut, while widening only one road may not improve capacity when other bottlenecks remain.