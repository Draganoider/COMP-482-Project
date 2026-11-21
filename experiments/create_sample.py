import networkx as nx
import osmnx as ox
from pathlib import Path

# Load the existing road network
G = ox.load_graphml("data/raw/palisades_roads.graphml")

# Choose a starting intersection with several connections
start_node = max(G.nodes, key=lambda n: G.degree(n))

# Use BFS to select 30 connected intersections
undirected_G = G.to_undirected()

sample_nodes = []

for node in nx.bfs_tree(undirected_G, start_node):
    sample_nodes.append(node)

    if len(sample_nodes) == 30:
        break

# Create the sample with those nodes
sample = G.subgraph(sample_nodes).copy()

# Save sample
output = Path("data/palisades_sample.graphml")
output.parent.mkdir(parents=True, exist_ok=True)

ox.save_graphml(sample, filepath=output)

print("\nSMALL NETWORK SAMPLE")
print("Nodes:", sample.number_of_nodes())
print("Edges:", sample.number_of_edges())
print("Saved to:", output)


# Check whether the sample is connected
print("\nSAMPLE CONNECTIVITY CHECK")

weakly_connected = nx.is_weakly_connected(sample)

print("Weakly connected:", weakly_connected)

components = list(nx.weakly_connected_components(sample))

print("Number of components:", len(components))
print("Component sizes:", [len(c) for c in components])

# Verify that all roads have positive capacities
all_valid = all(
    int(data["capacity"]) > 0
    for u, v, key, data in sample.edges(keys=True, data=True)
)

print("All capacities positive:", all_valid)
