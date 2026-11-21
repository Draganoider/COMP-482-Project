import osmnx as ox
import networkx as nx
from pathlib import Path

# Location we want to study
place = "Pacific Palisades, Los Angeles, California, USA"


# Approximate center of Pacific Palisades
center = (34.0481, -118.5269)

# Download roads within 3 km of the center
G = ox.graph_from_point(
    center,
    dist=3000,
    network_type="drive"
)

# Count intersections and road connections
print("Number of nodes:", len(G.nodes))
print("Number of edges:", len(G.edges))

print("\nSample road attributes:")

for u, v, key, data in list(G.edges(keys=True, data=True))[:5]:
    print(data)

# Count roads with and without lane information
with_lanes = 0
without_lanes = 0

for u, v, key, data in G.edges(keys=True, data=True):
    if "lanes" in data:
        with_lanes += 1
    else:
        without_lanes += 1

print("\nLANE INFORMATION")
print("Road edges with lane data:", with_lanes)
print("Road edges missing lane data:", without_lanes)


from collections import Counter

# Count road types that are missing lane information
missing_by_type = Counter()

for u, v, key, data in G.edges(keys=True, data=True):
    if "lanes" not in data:
        road_type = data.get("highway", "unknown")

        if isinstance(road_type, list):
            road_type = road_type[0]

        missing_by_type[road_type] += 1

print("\nMISSING LANES BY ROAD TYPE")

for road_type, count in missing_by_type.most_common():
    print(road_type, ":", count)
# Inspect lane counts and road directions
from collections import Counter

lane_examples = Counter()
oneway_counts = Counter()

for u, v, key, data in G.edges(keys=True, data=True):
    road_type = data.get("highway", "unknown")
    lanes = data.get("lanes", "missing")
    oneway = data.get("oneway", False)

    lane_examples[str(lanes)] += 1
    oneway_counts[str(oneway)] += 1

print("\nLANE VALUE DISTRIBUTION")
for lanes, count in lane_examples.most_common(10):
    print(lanes, ":", count)

print("\nONE-WAY INFORMATION")
for direction, count in oneway_counts.items():
    print(direction, ":", count)

# Check lane counts for residential roads
residential_lanes = Counter()

for u, v, key, data in G.edges(keys=True, data=True):
    if data.get("highway") == "residential":
        lanes = str(data.get("lanes", "missing"))
        residential_lanes[lanes] += 1

print("\nRESIDENTIAL ROAD LANE COUNTS")

for lanes, count in residential_lanes.most_common():
    print(lanes, ":", count)


# Summarize residential lane data
total_residential = sum(residential_lanes.values())
missing_residential = residential_lanes["missing"]

print("\nRESIDENTIAL ROAD SUMMARY")
print("Total residential edges:", total_residential)
print("Missing lane information:", missing_residential)

missing_percentage = (
    missing_residential / total_residential
) * 100

print("Missing percentage:", round(missing_percentage, 2), "%")

# Temporary capacity model for testing
TEST_CAPACITY_PER_LANE = 800

def estimate_capacity(lanes_per_direction):
    return lanes_per_direction * TEST_CAPACITY_PER_LANE


print("\nCAPACITY TEST")
print("1 lane:", estimate_capacity(1), "cars/hour")
print("2 lanes:", estimate_capacity(2), "cars/hour")
print("3 lanes:", estimate_capacity(3), "cars/hour")

# Estimate capacity for a directed road edge
def assign_capacity(data):
    lanes = data.get("lanes")
    oneway = data.get("oneway", False)

    # Use a temporary default if lane data is missing
    if lanes is None:
        total_lanes = 2 if not oneway else 1

    elif isinstance(lanes, str) and lanes.isdigit():
        total_lanes = int(lanes)

    elif isinstance(lanes, int):
        total_lanes = lanes

    else:
        # Ambiguous values will need separate handling
        total_lanes = 2 if not oneway else 1

    # Estimate lanes available in each direction
    if oneway:
        directional_lanes = total_lanes
    else:
        directional_lanes = max(1, total_lanes // 2)

    return estimate_capacity(directional_lanes)


print("\nROAD CAPACITY FUNCTION TEST")

road1 = {"highway": "residential", "lanes": "2", "oneway": False}
road2 = {"highway": "residential", "lanes": "2", "oneway": True}
road3 = {"highway": "residential", "oneway": False}

print("Two-way road:", assign_capacity(road1))
print("One-way road:", assign_capacity(road2))
print("Missing lane data:", assign_capacity(road3))

# Assign estimated capacity to every road edge
for u, v, key, data in G.edges(keys=True, data=True):
    data["capacity"] = assign_capacity(data)

# Verify that every edge has a positive integer capacity
capacities = [
    data["capacity"]
    for u, v, key, data in G.edges(keys=True, data=True)
]

assert len(capacities) == G.number_of_edges()
assert all(isinstance(c, int) and c > 0 for c in capacities)

print("\nNETWORK CAPACITY RESULTS")
print("Road edges processed:", len(capacities))
print("Minimum capacity:", min(capacities))
print("Maximum capacity:", max(capacities))
print("All capacities are positive integers!")


# Find intersections near the study-area boundary
center_lat = 34.0481
center_lon = -118.5269

boundary_candidates = []

for node, data in G.nodes(data=True):
    lat = data["y"]
    lon = data["x"]

    # Approximate distance from center in meters
    north_south = (lat - center_lat) * 111_000
    east_west = (lon - center_lon) * 92_000

    distance = (north_south**2 + east_west**2)**0.5

    if distance >= 2500:
        boundary_candidates.append((node, round(distance)))

print("\nPOSSIBLE BOUNDARY INTERSECTIONS")
print("Candidates found:", len(boundary_candidates))

for node, distance in boundary_candidates[:10]:
    print("Node:", node, "Distance:", distance, "meters")


# Check outgoing connections for boundary candidates
possible_exits = []

for node, distance in boundary_candidates:
    outgoing = G.out_degree(node)

    if outgoing > 0:
        possible_exits.append((node, distance, outgoing))

print("\nBOUNDARY NODES WITH OUTGOING ROADS")
print("Candidates:", len(possible_exits))

for node, distance, outgoing in possible_exits[:10]:
    print(
        "Node:", node,
        "Distance:", distance,
        "Outgoing edges:", outgoing
    )

# Look for major roads near the study-area boundary
major_types = {
    "primary",
    "secondary",
    "tertiary",
    "trunk",
    "motorway",
    "primary_link",
    "secondary_link",
    "tertiary_link",
    "trunk_link",
}

exit_road_candidates = []

for u, v, key, data in G.edges(keys=True, data=True):
    road_type = data.get("highway", "")

    if isinstance(road_type, list):
        road_type = road_type[0]

    if road_type in major_types:
        if any(node == v for node, _, _ in possible_exits):
            exit_road_candidates.append({
                "road": data.get("name", "Unnamed road"),
                "type": road_type,
                "node": v,
                "capacity": data["capacity"]
            })

print("\nPOTENTIAL MAJOR EXIT ROADS")
print("Candidates found:", len(exit_road_candidates))

for road in exit_road_candidates[:10]:
    print(road)

# Use the node nearest the study-area center
start_node = ox.distance.nearest_nodes(
    G, X=center_lon, Y=center_lat
)

# Find nodes reachable by driving from the center
reachable = nx.descendants(G, start_node)
reachable.add(start_node)

reachable_exits = []

for road in exit_road_candidates:
    if road["node"] in reachable:
        reachable_exits.append(road)

print("\nREACHABLE EXIT-ROAD CANDIDATES")
print("Candidates:", len(reachable_exits))

for road in reachable_exits[:10]:
    print(road)

# Find nodes with only one road connection
dead_end_nodes = []

for node in G.nodes:
    neighbors = set(G.predecessors(node)) | set(G.successors(node))

    if len(neighbors) == 1:
        dead_end_nodes.append(node)

print("\nDEAD-END OR TERMINAL NODES")
print("Number found:", len(dead_end_nodes))


# Find terminal nodes near the study-area boundary
boundary_terminal_nodes = []

for node in dead_end_nodes:
    data = G.nodes[node]

    lat = data["y"]
    lon = data["x"]

    north_south = (lat - center_lat) * 111_000
    east_west = (lon - center_lon) * 92_000

    distance = (north_south**2 + east_west**2)**0.5

    if distance >= 2500:
        boundary_terminal_nodes.append((node, round(distance)))

print("\nBOUNDARY TERMINAL NODES")
print("Candidates found:", len(boundary_terminal_nodes))

for node, distance in boundary_terminal_nodes[:10]:
    print("Node:", node, "Distance:", distance, "meters")


print("\nBOUNDARY TERMINAL ROAD DETAILS")

for node, distance in boundary_terminal_nodes:
    incoming = list(G.in_edges(node, keys=True, data=True))
    outgoing = list(G.out_edges(node, keys=True, data=True))

    if incoming:
        u, v, key, data = incoming[0]
        print(
            "Node:", node,
            "| Road:", data.get("name", "Unnamed"),
            "| Direction: incoming",
            "| Distance:", distance
        )
    elif outgoing:
        u, v, key, data = outgoing[0]
        print(
            "Node:", node,
            "| Road:", data.get("name", "Unnamed"),
            "| Direction: outgoing",
            "| Distance:", distance
        )


# Check terminal nodes that allow outgoing traffic
outgoing_terminals = []

for node, distance in boundary_terminal_nodes:
    incoming_count = G.in_degree(node)
    outgoing_count = G.out_degree(node)

    if outgoing_count > 0:
        outgoing_terminals.append(node)

    print(
        "Node:", node,
        "| Incoming:", incoming_count,
        "| Outgoing:", outgoing_count
    )

print("\nBOUNDARY TERMINAL DIRECTION SUMMARY")
print("Total boundary terminals:", len(boundary_terminal_nodes))
print("Terminals with outgoing edges:", len(outgoing_terminals))


# Download a larger network to check roads beyond our boundary
larger_G = ox.graph_from_point(
    center,
    dist=3500,
    network_type="drive"
)

# Check which terminal nodes connect to roads outside our graph
confirmed_crossings = []

for node in outgoing_terminals:
    if node not in larger_G:
        continue

    for neighbor in larger_G.successors(node):
        if neighbor not in G:
            confirmed_crossings.append((node, neighbor))

print("\nBOUNDARY-CROSSING CONNECTIONS")
print("Connections found:", len(confirmed_crossings))

for node, neighbor in confirmed_crossings[:10]:
    print("Inside node:", node, "Outside node:", neighbor)


# Identify road names for possible boundary crossings
print("\nBOUNDARY CROSSING ROAD DETAILS")

for inside_node, outside_node in confirmed_crossings:
    road_edges = larger_G.get_edge_data(inside_node, outside_node)

    if road_edges:
        for key, data in road_edges.items():
            print(
                "Road:", data.get("name", "Unnamed"),
                "| Type:", data.get("highway", "Unknown"),
                "| Inside node:", inside_node,
                "| Outside node:", outside_node,
                "| One-way:", data.get("oneway", False)
            )


# Compare distances of possible boundary crossings
def distance_from_center(node, graph):
    lat = graph.nodes[node]["y"]
    lon = graph.nodes[node]["x"]

    north_south = (lat - center_lat) * 111_000
    east_west = (lon - center_lon) * 92_000

    return (north_south**2 + east_west**2)**0.5


print("\nOUTWARD ROAD CONNECTION CHECK")

for inside_node, outside_node in confirmed_crossings:
    inside_distance = distance_from_center(inside_node, larger_G)
    outside_distance = distance_from_center(outside_node, larger_G)

    print(
        "Inside node:", inside_node,
        "| Inside distance:", round(inside_distance),
        "| Outside distance:", round(outside_distance),
        "| Moving outward:", outside_distance > inside_distance
    )

# Identify intersections connected to residential roads
residential_start_nodes = set()

for u, v, key, data in G.edges(keys=True, data=True):
    road_type = data.get("highway", "")

    if isinstance(road_type, list):
        is_residential = "residential" in road_type
    else:
        is_residential = road_type == "residential"

    if is_residential:
        residential_start_nodes.add(u)
        residential_start_nodes.add(v)

print("\nRESIDENTIAL STARTING NODES")
print("Total:", len(residential_start_nodes))

for node in sorted(residential_start_nodes)[:10]:
    print("Starting node:", node)


# Find residential nodes that can reach a candidate exit
exit_nodes = {inside for inside, outside in confirmed_crossings}

# Reverse the graph to find nodes that can reach the exits
reverse_G = G.reverse(copy=False)

nodes_reaching_exits = set()

for exit_node in exit_nodes:
    if exit_node in G:
        nodes_reaching_exits.update(
            nx.descendants(reverse_G, exit_node)
        )
        nodes_reaching_exits.add(exit_node)

usable_start_nodes = residential_start_nodes & nodes_reaching_exits

print("\nRESIDENTIAL ACCESS TO CANDIDATE EXITS")
print("Residential candidates:", len(residential_start_nodes))
print("Candidates able to reach an exit:", len(usable_start_nodes))
print(
    "Candidates unable to reach an exit:",
    len(residential_start_nodes) - len(usable_start_nodes)
)
# Save the downloaded network
output = Path("data/raw")
output.mkdir(parents=True, exist_ok=True)

ox.save_graphml(G, filepath=output / "palisades_roads.graphml")

print("Road network saved successfully!")