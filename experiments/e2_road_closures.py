import csv
import subprocess
import sys
from pathlib import Path

import osmnx as ox

from evac.edmonds_karp import edmonds_karp
from evac.min_cut import min_cut
from evac.network import FlowNetwork

# Load the Pacific Palisades road network
G = ox.load_graphml("data/raw/palisades_roads.graphml")

network = FlowNetwork()

for node in G.nodes:
    network.add_node(node)

for u, v, _key, data in G.edges(keys=True, data=True):
    network.add_edge(u, v, int(data["capacity"]))

print("Road network loaded!")
print("Nodes:", network.num_nodes)
print("Edges:", network.num_edges)

# Use the same source and sink from Issue #11
source = 123082625
sink = 13418556508

# Calculate the original maximum flow
baseline_result = edmonds_karp(network, source, sink)
baseline_flow = baseline_result.value

print("\nOriginal maximum flow:", baseline_flow)

# Find the minimum cut
cut = min_cut(network, baseline_result, source)

print("Minimum-cut capacity:", cut.capacity)
print("Number of roads in the minimum cut:", len(cut.cut_edges))

# Choose one road from the minimum cut
road_id = cut.cut_edges[0]

print("\nTesting road:", road_id)

# Copy the network and reset its flow before closing a road
closed_network = network.copy()
closed_network.reset_flow()
closed_network.set_capacity(road_id, 0)

# Recalculate maximum flow after the closure
closed_result = edmonds_karp(closed_network, source, sink)

capacity_lost = baseline_flow - closed_result.value

print("Maximum flow after closure:", closed_result.value)
print("Capacity lost:", capacity_lost)

# Test every road individually
closure_results = []

for road_id in network.roads():
    # Make a fresh copy for each closure
    closed_network = network.copy()
    closed_network.reset_flow()
    closed_network.set_capacity(road_id, 0)

    # Calculate flow after closing this road
    closed_result = edmonds_karp(closed_network, source, sink)

    capacity_lost = baseline_flow - closed_result.value

    closure_results.append({
        "road_id": road_id,
        "capacity_lost": capacity_lost,
        "new_max_flow": closed_result.value,
        "in_min_cut": road_id in cut.cut_edges
    })

# Sort roads by largest loss first
closure_results.sort(
    key=lambda road: road["capacity_lost"],
    reverse=True
)

print("\nTOP 10 MOST IMPORTANT ROAD CLOSURES")

for road in closure_results[:10]:
    print(
        "Road:", road["road_id"],
        "| Capacity lost:", road["capacity_lost"],
        "| In minimum cut:", road["in_min_cut"]
    )
    # Save all road closure results
Path("results/e2").mkdir(parents=True, exist_ok=True)

with open("results/e2/e2_road_closures.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "road_id",
            "capacity_lost",
            "new_max_flow",
            "in_min_cut"
        ]
    )

    writer.writeheader()
    writer.writerows(closure_results)

print("\nResults saved to results/e2/e2_road_closures.csv")

# Generate the graph after saving the CSV results
sys.stdout.flush()

subprocess.run(
    [sys.executable, "experiments/plot_e2.py"],
    check=True
)
