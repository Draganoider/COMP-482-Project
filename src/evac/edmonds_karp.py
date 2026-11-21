"""Edmonds-Karp maximum-flow algorithm using BFS.

Implements proposal section 3 and the pseudocode in analysis/max-flow.md section 2: MaxFlow, with
FindPath using a queue (BFS), so each augmenting path is a shortest one, and Augment. `scanned`
counts every residual edge examined, as on FindPath's line 5.
"""

from collections import deque

from evac.network import FlowNetwork, Node
from evac.results import MaxFlowResult


def edmonds_karp(network: FlowNetwork, s: Node, t: Node) -> MaxFlowResult:
    """Calculate maximum flow using BFS augmenting paths."""

    if s == t:
        raise ValueError("source and sink must be different")

    if s not in network or t not in network:
        raise KeyError("source and sink must exist in the network")

    network.reset_flow()

    max_flow = 0
    paths = 0
    scanned = 0

    while True:
        parent = {s: None}
        queue = deque([s])

        while queue and t not in parent:
            u = queue.popleft()

            for edge in network.out_edges(u):
                scanned += 1
                v = network.head(edge)

                if network.residual(edge) > 0 and v not in parent:
                    parent[v] = edge
                    queue.append(v)

                    if v == t:
                        break

        if t not in parent:
            return MaxFlowResult(
                value=max_flow,
                flow={e: network.flow(e) for e in network.edges()},
                augmenting_paths=paths,
                edges_scanned=scanned,
            )

        path = []
        v = t

        while v != s:
            edge = parent[v]
            path.append(edge)
            v = network.tail(edge)

        bottleneck = min(network.residual(edge) for edge in path)

        for edge in path:
            network.push(edge, bottleneck)

        max_flow += bottleneck
        paths += 1
