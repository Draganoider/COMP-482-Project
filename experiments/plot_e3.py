
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

networks = []
road_labels = []
gains = []
colors = []

with open("results/e3/e3_synthetic.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        networks.append(row["network"])
        road_labels.append(f'{row["network"]}\nRoad {row["road_id"]}')
        gains.append(int(row["widening_gain"]))
        colors.append(
            "orange" if row["in_min_cut"] == "True" else "steelblue"
        )

plt.figure(figsize=(10, 5))
plt.bar(road_labels, gains, color=colors)

plt.xlabel("Network and road edge")
plt.ylabel("Maximum-flow gain (cars/hour)")
plt.title("E3: Effect of Widening One Road")
plt.grid(axis="y", alpha=0.3)


plt.legend(handles=[
    Patch(color="orange", label="In original minimum cut"),
    Patch(color="steelblue", label="Not in original minimum cut")
])

Path("results/e3").mkdir(parents=True, exist_ok=True)
plt.savefig("results/e3/e3_widening_comparison.png", dpi=150, bbox_inches="tight")

print("Graph saved to results/e3/e3_widening_comparison.png")
