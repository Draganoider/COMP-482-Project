"""Find a minimum cut from a completed maximum flow using BFS."""

from collections import deque
from dataclasses import dataclass

from evac.network import FlowNetwork, Node


@dataclass
class MinCut:
    """Store the result of a minimum-cut calculation."""

    reachable: set[Node]
    cut_edges: list[int]
    capacity: int


def min_cut(network: FlowNetwork, result, s: Node) -> MinCut:
    """Find the minimum cut after a maximum-flow calculation."""

    reachable = {s}
    queue = deque([s])

    while queue:
        u = queue.popleft()

        for edge in network.out_edges(u):
            v = network.head(edge)

            if network.residual(edge) > 0 and v not in reachable:
                reachable.add(v)
                queue.append(v)

    cut_edges = []
    capacity = 0

    for edge in network.roads():
        u = network.tail(edge)
        v = network.head(edge)

        if u in reachable and v not in reachable:
            cut_edges.append(edge)
            capacity += network.capacity(edge)

    return MinCut(
        reachable=reachable,
        cut_edges=cut_edges,
        capacity=capacity,
    )
