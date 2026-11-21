
"""Find a minimum cut from completed maximum flow using BFS.

Implements proposal section 3 and MinCut from analysis/min-cut.md section 3.
"""

from collections import deque
from dataclasses import dataclass

from evac.network import FlowNetwork, Node
from evac.results import MaxFlowResult


@dataclass
class MinCut:
    """Store the result of a minimum-cut calculation."""

    reachable: set[Node]
    cut_edges: list[int]
    capacity: int


def min_cut(network: FlowNetwork, result: MaxFlowResult, s: Node) -> MinCut:
    """Find the minimum cut after a completed maximum-flow calculation.

    The capacity check verifies agreement with the supplied flow value.
    It does not independently prove that the network has maximum flow.
    """

    if s not in network:
        raise ValueError("source must exist in the network")

    if result is None:
        raise ValueError("a maximum-flow result is required")

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

    if capacity != result.value:
        raise ValueError(
            f"minimum-cut capacity {capacity} does not match "
            f"maximum-flow value {result.value}"
        )

    return MinCut(
        reachable=reachable,
        cut_edges=cut_edges,
        capacity=capacity,
    )
