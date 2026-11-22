
import networkx as nx
import osmnx as ox

from evac.network import FlowNetwork

try:
    from evac.edmonds_karp import edmonds_karp
except ImportError:
    edmonds_karp = None

# Load the connected sample network
G = ox.load_graphml("data/palisades_sample.graphml")

# Convert MultiDiGraph into DiGraph for max-flow testing
flow_graph = nx.DiGraph()

for u, v, _key, data in G.edges(keys=True, data=True):
    capacity = int(data["capacity"])

    # Combine capacities of parallel roads
    if flow_graph.has_edge(u, v):
        flow_graph[u][v]["capacity"] += capacity
    else:
        flow_graph.add_edge(u, v, capacity=capacity)

# Select nodes with a valid directed path
source = next(iter(flow_graph.nodes))

reachable = nx.descendants(flow_graph, source)

if not reachable:
    raise ValueError("No reachable destination found")

sink = sorted(reachable)[-1]

# Calculate maximum flow using NetworkX
flow_value = nx.maximum_flow_value(
    flow_graph,
    source,
    sink,
    capacity="capacity"
)

print("\nNETWORKX MAX-FLOW VALIDATION")
print("Source:", source)
print("Sink:", sink)
print("Maximum flow:", flow_value)
print("Sample nodes:", G.number_of_nodes())
print("Sample edges:", G.number_of_edges())


# Convert the sample into the team's FlowNetwork
team_network = FlowNetwork()

for node in G.nodes:
    team_network.add_node(node)

for u, v, _key, data in G.edges(keys=True, data=True):
    team_network.add_edge(u, v, int(data["capacity"]))

# Run the team's Edmonds-Karp algorithm
if edmonds_karp is None:
    raise SystemExit(
        "Edmonds-Karp is not available yet. "
        "Merge the feature/edmonds-karp branch before running this comparison."
    )
result = edmonds_karp(team_network, source, sink)

print("\nTEAM VS NETWORKX COMPARISON")
print("NetworkX max flow:", flow_value)
print("Team max flow:", result.value)
print("Augmenting paths:", result.paths)
print("Edges scanned:", result.scanned)

assert result.value == flow_value, "Maximum-flow results do not match!"

print("SUCCESS: Both algorithms produced the same maximum flow!")
