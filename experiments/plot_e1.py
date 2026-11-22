
import csv
from pathlib import Path

import matplotlib.pyplot as plt

nodes = []
ff_times = []
ek_times = []

# Read the experiment results
with open("results/e1/e1_max_flow.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        nodes.append(int(row["nodes"]))
        ff_times.append(float(row["ff_median_ms"]))
        ek_times.append(float(row["ek_median_ms"]))

# Plot both algorithms
plt.plot(nodes, ff_times, marker="o", label="Ford-Fulkerson")
plt.plot(nodes, ek_times, marker="o", label="Edmonds-Karp")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Number of nodes")
plt.ylabel("Median running time (ms)")
plt.title("E1: Maximum-Flow Algorithm Performance")
plt.legend()
plt.grid(True)

# Save the graph
Path("results").mkdir(exist_ok=True)
plt.savefig("results/e1/e1_max_flow.png", dpi=150, bbox_inches="tight")

print("Graph saved to results/e1/e1_max_flow.png")
