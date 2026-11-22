import csv
import subprocess
import sys
from pathlib import Path

import osmnx as ox

from evac.edmonds_karp import edmonds_karp
from evac.min_cut import min_cut
from evac.network import FlowNetwork
from evac.what_ifs import widening_gains

# Load the Pacific Palisades road network
G = ox.load_graphml("data/raw/palisades_roads.graphml")

network = FlowNetwork()

# Add all intersections
for node in G.nodes:
    network.add_node(node)

# Add all directed roads
for u, v, _key, data in G.edges(keys=True, data=True):
    network.add_edge(u, v, int(data["capacity"]))

print("Road network loaded!")
print("Nodes:", network.num_nodes)
print("Edges:", network.num_edges)

# Use the same source and sink from our previous experiments
source = 123082625
sink = 13418556508

# Calculate the original maximum flow
baseline_result = edmonds_karp(network, source, sink)
baseline_flow = baseline_result.value

# Find the minimum cut
cut = min_cut(network, baseline_result, source)

print("\nOriginal maximum flow:", baseline_flow)
print("Minimum-cut capacity:", cut.capacity)
print("Roads in minimum cut:", len(cut.cut_edges))

# Select one road from the minimum cut
road_id = cut.cut_edges[0]

# Copy the network and reset its flow
widened_network = network.copy()
widened_network.reset_flow()

# Add the estimated capacity of one directional lane
original_capacity = widened_network.capacity(road_id)
widened_network.set_capacity(road_id, original_capacity + 800)

# Calculate maximum flow after widening
widened_result = edmonds_karp(widened_network, source, sink)

gain = widened_result.value - baseline_flow

print("\nRoad tested:", road_id)
print("Original road capacity:", original_capacity)
print("New road capacity:", original_capacity + 800)
print("Maximum flow after widening:", widened_result.value)
print("Capacity gained:", gain)

# Test widening every road by 800 cars/hour
gains = widening_gains(
    network,
    source,
    sink,
    edmonds_karp,
    added_capacity=800
)

# Sort roads from highest gain to lowest gain
ranked_roads = sorted(
    gains.items(),
    key=lambda item: item[1],
    reverse=True
)

print("\nTOP 10 ROADS TO WIDEN")

for road_id, gain in ranked_roads[:10]:
    print(
        "Road:", road_id,
        "| Capacity gained:", gain,
        "| In minimum cut:", road_id in cut.cut_edges
    )
# Summarize all widening results
positive_gains = [
    gain for gain in gains.values()
    if gain > 0
]

print("\nROAD WIDENING SUMMARY")
print("Roads tested:", len(gains))
print("Roads with positive gain:", len(positive_gains))
print("Largest capacity gain:", max(gains.values()))

# Small network to test road widening
small_network = FlowNetwork()

small_network.add_edge(0, 1, 100)
small_network.add_edge(1, 2, 100)

small_gains = widening_gains(
    small_network,
    0,
    2,
    edmonds_karp,
    added_capacity=800
)

print("\nSMALL NETWORK TEST")
print("Baseline maximum flow:", edmonds_karp(small_network, 0, 2).value)
print("Widening gains:", small_gains)

# Synthetic network with one bottleneck
bottleneck_network = FlowNetwork()

bottleneck_network.add_edge(0, 1, 100)
bottleneck_network.add_edge(1, 2, 1000)

bottleneck_gains = widening_gains(
    bottleneck_network,
    0,
    2,
    edmonds_karp,
    added_capacity=800
)

print("\nSINGLE BOTTLENECK TEST")
print("Baseline maximum flow:", edmonds_karp(bottleneck_network, 0, 2).value)
print("Widening gains:", bottleneck_gains)

# Compare minimum-cut roads with brute-force widening
cut_roads = set(cut.cut_edges)

best_gain = max(gains.values())

best_roads = [
    road_id
    for road_id, gain in gains.items()
    if gain == best_gain
]

print("\nMINIMUM CUT VS BRUTE FORCE")
print("Minimum-cut roads:", sorted(cut_roads))
print("Best widening gain:", best_gain)
print("Number of roads tied for best:", len(best_roads))
print("Best roads in minimum cut:", len(cut_roads.intersection(best_roads)))

# Compare minimum cut and widening on synthetic networks
for name, test_network, test_gains in [
    ("Equal bottlenecks", small_network, small_gains),
    ("Single bottleneck", bottleneck_network, bottleneck_gains)
]:
    # Work on a copy so the original network stays unchanged
    test_copy = test_network.copy()
    test_copy.reset_flow()

    result = edmonds_karp(test_copy, 0, 2)
    test_cut = min_cut(test_copy, result, 0)

    best_gain = max(test_gains.values())

    print(f"\n{name.upper()}")
    print("Minimum-cut roads:", test_cut.cut_edges)
    print("Minimum-cut capacity:", test_cut.capacity)
    print("Best widening gain:", best_gain)

    for road_id in test_gains:
        print(
            "Road:", road_id,
            "| Gain:", test_gains[road_id],
            "| In minimum cut:", road_id in test_cut.cut_edges
        )
# Save the road-widening results
Path("results/e3").mkdir(parents=True, exist_ok=True)

with open("results/e3/e3_widening_gains.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "road_id",
        "original_capacity",
        "added_capacity",
        "capacity_gain",
        "in_min_cut"
    ])

    for road_id, gain in ranked_roads:
        writer.writerow([
            road_id,
            network.capacity(road_id),
            800,
            gain,
            road_id in cut.cut_edges
        ])

print("\nResults saved to results/e3/e3_widening_gains.csv")

# Save the synthetic network results
with open("results/e3/e3_synthetic.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "network",
        "road_id",
        "baseline_flow",
        "widening_gain",
        "in_min_cut"
    ])

    for name, test_network, test_gains in [
        ("Equal bottlenecks", small_network, small_gains),
        ("Single bottleneck", bottleneck_network, bottleneck_gains)
    ]:
        test_copy = test_network.copy()
        test_copy.reset_flow()

        result = edmonds_karp(test_copy, 0, 2)
        test_cut = min_cut(test_copy, result, 0)

        for road_id, gain in test_gains.items():
            writer.writerow([
                name,
                road_id,
                result.value,
                gain,
                road_id in test_cut.cut_edges
            ])

print("Synthetic results saved to results/e3/e3_synthetic.csv")

# Create the graph after saving the experiment results
sys.stdout.flush()

subprocess.run(
    [sys.executable, "experiments/plot_e3.py"],
    check=True
)
