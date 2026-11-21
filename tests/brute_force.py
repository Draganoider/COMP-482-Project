
"""Brute-force minimum-cut checker for small flow networks."""

from itertools import combinations

from evac.network import FlowNetwork, Node


def brute_force_min_cut(
    network: FlowNetwork, s: Node, t: Node
) -> tuple[int, set[Node]]:
    """Find the minimum cut by checking every possible partition."""

    if s == t:
        raise ValueError("source and sink must be different")

    if s not in network or t not in network:
        raise ValueError("source and sink must exist in the network")

    nodes = [node for node in network.nodes() if node != s and node != t]

    best_capacity = float("inf")
    best_cut: set[Node] = set()

    for size in range(len(nodes) + 1):
        for group in combinations(nodes, size):
            source_side = {s} | set(group)
            cut_capacity = 0

            for edge in network.edges():
                u = network.tail(edge)
                v = network.head(edge)

                if u in source_side and v not in source_side:
                    cut_capacity += network.capacity(edge)

            if cut_capacity < best_capacity:
                best_capacity = cut_capacity
                best_cut = source_side

    return int(best_capacity), best_cut
