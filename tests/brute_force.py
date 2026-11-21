"""Brute-force minimum-cut checker for small flow networks."""

from itertools import combinations
from evac.network import FlowNetwork


def brute_force_min_cut(network: FlowNetwork, s, t):
    """Find the minimum cut by checking every possible partition."""

    nodes = [node for node in network.nodes() if node != s and node != t]

    best_capacity = float("inf")
    best_cut = set()


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

    return best_capacity, best_cut

