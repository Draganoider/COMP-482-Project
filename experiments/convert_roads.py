
import osmnx as ox

from evac.network import FlowNetwork

# Load the road network we already downloaded
G = ox.load_graphml("data/raw/palisades_roads.graphml")

# Create the team's FlowNetwork
network = FlowNetwork()

# Add every intersection
for node in G.nodes:
    network.add_node(node)


# Add roads and retain their FlowNetwork edge IDs
road_mapping = {}

for u, v, key, data in G.edges(keys=True, data=True):
    capacity = int(data["capacity"])
    edge_id = network.add_edge(u, v, capacity)

    road_mapping[(u, v, key)] = edge_id

# Verify each road's capacity
for u, v, key, data in G.edges(keys=True, data=True):
    edge_id = road_mapping[(u, v, key)]

    assert network.capacity(edge_id) == int(data["capacity"])
    assert network.tail(edge_id) == u
    assert network.head(edge_id) == v

print("\nINDIVIDUAL ROAD VERIFICATION")
print("Roads verified:", len(road_mapping))
print("Every road's capacity and direction match!")

# Verify the conversion
print("\nFLOW NETWORK CONVERSION")
print("Original nodes:", G.number_of_nodes())
print("Converted nodes:", network.num_nodes)

print("Original edges:", G.number_of_edges())
print("Converted edges:", network.num_edges)

assert network.num_nodes == G.number_of_nodes()
assert network.num_edges == G.number_of_edges()

print("FlowNetwork conversion successful!")


# Temporary test using residential starting intersections
# and two candidate exit nodes

candidate_exits = [271821708, 14109380556]

# Select 10 residential intersections for the initial test
residential_nodes = set()

for u, v, _key, data in G.edges(keys=True, data=True):
    road_type = data.get("highway", "")

    if isinstance(road_type, list):
        is_residential = "residential" in road_type
    else:
        is_residential = road_type == "residential"

    if is_residential:
        residential_nodes.add(u)
        residential_nodes.add(v)

# Exclude exits from the starting-node selection
test_starts = sorted(residential_nodes - set(candidate_exits))[:10]

# Create a separate network with super-terminals
test_network = network.with_super_terminals(
    sources=test_starts,
    sinks=candidate_exits
)

print("\nSUPER-TERMINAL TEST")
print("Starting nodes:", len(test_starts))
print("Candidate exits:", len(candidate_exits))
print("Total network nodes:", test_network.num_nodes)
print("Total network edges:", test_network.num_edges)


# Verify converted road capacities
original_total = sum(
    int(data["capacity"])
    for u, v, key, data in G.edges(keys=True, data=True)
)

converted_total = network.total_capacity()

print("\nCAPACITY VERIFICATION")
print("Original total capacity:", original_total)
print("Converted total capacity:", converted_total)

assert original_total == converted_total

print("All road capacities preserved!")
