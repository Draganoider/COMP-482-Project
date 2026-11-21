"""Ford-Fulkerson with DFS augmenting paths.

Implements proposal section 3 and the pseudocode in analysis/max-flow.md section 2: MaxFlow, with
FindPath using a stack (DFS), and Augment. `_find_path` is FindPath and counts `scanned` on its
line 5; the loop in `ford_fulkerson` is MaxFlow.
"""

from evac.network import FlowNetwork, Node
from evac.results import MaxFlowResult


def _find_path(network: FlowNetwork, s: Node, t: Node) -> tuple[list[int], int]:
    """Find one residual s-t path with an iterative DFS, count examined edges."""
    stack = [s]
    marked = {s}
    parent: dict[Node, int] = {}
    scanned = 0

    while stack:
        u = stack.pop()
        for e in network.out_edges(u):
            scanned += 1
            v = network.head(e)
            if network.residual(e) <= 0 or v in marked:
                continue
            marked.add(v)
            parent[v] = e
            if v == t:
                path = []
                while v != s:
                    e = parent[v]
                    path.append(e)
                    v = network.tail(e)
                path.reverse()
                return path, scanned
            stack.append(v)

    return [], scanned


def ford_fulkerson(network: FlowNetwork, s: Node, t: Node) -> MaxFlowResult:
    """Compute max flow by repeatedly pushing along a DFS residual path.

    Resets any existing flow on the network, then updates the network in place.
    """
    if s == t:
        raise ValueError("source and sink must be different")
    if s not in network or t not in network:
        raise KeyError("source and sink must be nodes in the network")

    network.reset_flow()
    value = paths = scanned = 0
    while True:
        path, examined = _find_path(network, s, t)
        scanned += examined
        if not path:
            break
        bottleneck = min(network.residual(e) for e in path)
        for e in path:
            network.push(e, bottleneck)
        value += bottleneck
        paths += 1

    return MaxFlowResult(
        value=value,
        flow={e: network.flow(e) for e in network.edges()},
        augmenting_paths=paths,
        edges_scanned=scanned,
    )
