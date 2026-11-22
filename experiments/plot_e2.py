
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

roads = []

# Read the road-closure results
with open("results/e2/e2_road_closures.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        roads.append({
            "road_id": int(row["road_id"]),
            "capacity_lost": int(row["capacity_lost"]),
            "in_min_cut": row["in_min_cut"] == "True"
        })

# Select the 10 roads with the greatest capacity loss
roads.sort(key=lambda road: road["capacity_lost"], reverse=True)
top_roads = roads[:10]

road_ids = [str(road["road_id"]) for road in top_roads]
losses = [road["capacity_lost"] for road in top_roads]

colors = [
    "orange" if road["in_min_cut"] else "steelblue"
    for road in top_roads
]

plt.figure(figsize=(10, 5))
plt.bar(road_ids, losses, color=colors)

plt.xlabel("Road edge ID")
plt.ylabel("Maximum-flow capacity lost (cars/hour)")
plt.title("E2: Top 10 Road Closures by Capacity Loss")
plt.grid(axis="y", alpha=0.3)

# Explain the colors


plt.legend(handles=[
    Patch(color="orange", label="In original minimum cut"),
    Patch(color="steelblue", label="Not in original minimum cut")
])

Path("results/e2").mkdir(parents=True, exist_ok=True)
plt.savefig("results/e2/e2_top_closures.png", dpi=150, bbox_inches="tight")

print("Graph saved to results/e2/e2_top_closures.png")
