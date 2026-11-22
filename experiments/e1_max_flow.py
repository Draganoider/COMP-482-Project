import csv
import statistics
import subprocess
import sys
import time
from pathlib import Path

import osmnx as ox

from evac.edmonds_karp import edmonds_karp
from evac.ford_fulkerson import ford_fulkerson
from evac.generators import random_network
from evac.network import FlowNetwork

sys.stdout.flush()

subprocess.run(
    [sys.executable, "experiments/plot_e1.py"],
    check=True
)

# Different network sizes
sizes = [30, 100, 300, 1000]

results = []

run_results = []

for n in sizes:
    # Generate a network
    network = random_network(
        n=n,
        m=n * 2,
        max_capacity=100,
        seed=42
    )
    for node in range(n - 1):
        network.add_edge(node, node + 1, 100)
        ff_times = []
        ek_times = []

    # Repeat each test 5 times
    for i in range(5):
        start = time.perf_counter()
        ff_result = ford_fulkerson(network, 0, n - 1)
        ff_time = (time.perf_counter() - start) * 1000
        ff_times.append(ff_time)

        start = time.perf_counter()
        ek_result = edmonds_karp(network, 0, n - 1)
        ek_time = (time.perf_counter() - start) * 1000
        ek_times.append(ek_time)

        # Both algorithms should produce the same answer
        assert ff_result.value == ek_result.value
        ff_paths = ff_result.augmenting_paths
        ff_scanned = ff_result.edges_scanned

        ek_paths = ek_result.augmenting_paths
        ek_scanned = ek_result.edges_scanned
        run_results.append({
            "algorithm": "Ford-Fulkerson",
            "nodes": n,
            "edges": n * 2 + (n - 1),
            "seed": 42,
            "repetition": i + 1,
            "max_flow": ff_result.value,
            "time_ms": ff_time,
            "augmenting_paths": ff_result.augmenting_paths,
            "edges_scanned": ff_result.edges_scanned
        })

        run_results.append({
            "algorithm": "Edmonds-Karp",
            "nodes": n,
            "edges": n * 2 + (n - 1),
            "seed": 42,
            "repetition": i + 1,
            "max_flow": ek_result.value,
            "time_ms": ek_time,
            "augmenting_paths": ek_result.augmenting_paths,
            "edges_scanned": ek_result.edges_scanned
        })

    print(f"\nNetwork size: {n} nodes")
    print(f"Maximum flow: {ff_result.value}")
    print(f"Ford-Fulkerson median: {statistics.median(ff_times):.4f} ms")
    print(f"Edmonds-Karp median: {statistics.median(ek_times):.4f} ms")

    print("Ford-Fulkerson augmenting paths:", ff_paths)
    print("Ford-Fulkerson edges scanned:", ff_scanned)
    print("Edmonds-Karp augmenting paths:", ek_paths)
    print("Edmonds-Karp edges scanned:", ek_scanned)

    results.append({
        "nodes": n,
        "edges": n * 2 + (n - 1),
        "max_flow": ff_result.value,
        "ff_median_ms": statistics.median(ff_times),
        "ek_median_ms": statistics.median(ek_times)
    })

Path("results/e1").mkdir(parents=True, exist_ok=True)

with open("results/e1/e1_max_flow.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "nodes", "edges", "max_flow",
        "ff_median_ms", "ek_median_ms"
    ])

    writer.writeheader()
    writer.writerows(results)

print("\nResults saved to results/e1/e1_max_flow.csv")

# Test the Pacific Palisades road network

G = ox.load_graphml("data/raw/palisades_roads.graphml")

road_network = FlowNetwork()

for node in G.nodes:
    road_network.add_node(node)

for u, v, _key, data in G.edges(keys=True, data=True):
    road_network.add_edge(u, v, int(data["capacity"]))

print("\nPacific Palisades road network loaded!")
print("Nodes:", road_network.num_nodes)
print("Edges:", road_network.num_edges)

# Compare both algorithms on the real road network
source = 123082625
sink = 13418556508

# Repeat the real-road comparison 5 times
ff_road_times = []
ek_road_times = []
road_run_results = []

for i in range(5):
    start = time.perf_counter()
    ff_road = ford_fulkerson(road_network, source, sink)
    ff_time = (time.perf_counter() - start) * 1000
    ff_road_times.append(ff_time)

    start = time.perf_counter()
    ek_road = edmonds_karp(road_network, source, sink)
    ek_time = (time.perf_counter() - start) * 1000
    ek_road_times.append(ek_time)

    assert ff_road.value == ek_road.value
    road_run_results.append({
        "algorithm": "Ford-Fulkerson",
        "nodes": road_network.num_nodes,
        "edges": road_network.num_edges,
        "source": source,
        "sink": sink,
        "repetition": i + 1,
        "max_flow": ff_road.value,
        "time_ms": ff_time,
        "augmenting_paths": ff_road.augmenting_paths,
        "edges_scanned": ff_road.edges_scanned
    })

    road_run_results.append({
        "algorithm": "Edmonds-Karp",
        "nodes": road_network.num_nodes,
        "edges": road_network.num_edges,
        "source": source,
        "sink": sink,
        "repetition": i + 1,
        "max_flow": ek_road.value,
        "time_ms": ek_time,
        "augmenting_paths": ek_result.augmenting_paths,
        "edges_scanned": ek_result.edges_scanned
    })


    print(f"Run {i + 1}: FF = {ff_time:.4f} ms, EK = {ek_time:.4f} ms")

print("\nPACIFIC PALISADES COMPARISON")
print("Maximum flow:", ff_road.value)
print("Ford-Fulkerson median:", round(statistics.median(ff_road_times), 4), "ms")
print("Edmonds-Karp median:", round(statistics.median(ek_road_times), 4), "ms")
print("SUCCESS: Both algorithms agree!")

# Save the Pacific Palisades results
with open("results/e1/e1_palisades.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "nodes", "edges", "max_flow",
        "ff_median_ms", "ek_median_ms"
    ])

    writer.writerow([
        road_network.num_nodes,
        road_network.num_edges,
        ff_road.value,
        statistics.median(ff_road_times),
        statistics.median(ek_road_times)
    ])

print("\nPacific Palisades results saved to results/e1/e1_palisades.csv")

with open("results/e1/e1_max_flow_runs.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "algorithm",
        "nodes",
        "edges",
        "seed",
        "repetition",
        "max_flow",
        "time_ms",
        "augmenting_paths",
        "edges_scanned"
    ])

    writer.writeheader()
    writer.writerows(run_results)

print("\nIndividual runs saved to results/e1/e1_max_flow_runs.csv")

with open("results/e1/e1_palisades_runs.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "algorithm", "nodes", "edges", "source", "sink",
        "repetition", "max_flow", "time_ms",
        "augmenting_paths", "edges_scanned"
    ])

    writer.writeheader()
    writer.writerows(road_run_results)

print("Road runs saved to results/e1/e1_palisades_runs.csv")
