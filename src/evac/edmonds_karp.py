
"""Edmonds-Karp maximum-flow algorithm using BFS."""

from collections import deque

from evac.max_flow_result import MaxFlowResult
from evac.network import FlowNetwork, Node


def edmonds_karp(network: FlowNetwork, s: Node, t: Node) -> MaxFlowResult:
    """Calculate maximum flow using BFS augmenting paths."""

    if s == t:
        raise ValueError("source and sink must be different")

    if s not in network or t not in network:
        raise ValueError("source and sink must exist in the network")

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
                paths=paths,
                scanned=scanned,
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
