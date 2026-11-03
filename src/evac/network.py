"""The flow network every layer-1 algorithm runs on: road capacities and the residual graph.

Implements the model of plan decision D10 and proposal section 2: intersections are nodes, each
direction of a road is a directed edge with a whole-number capacity in cars per hour, and all homes
join a super-source s and all shelters a super-sink t by edges too large to ever be in a minimum
cut. The residual graph is the one of Kleinberg and Tardos section 7.1.

Representation. Edges live in flat lists indexed by an edge id. `add_edge` creates a pair: the road
itself, with an even id e, and its reverse residual edge, with id e ^ 1 (e + 1). Each node keeps an
adjacency list of the ids of both kinds of edge leaving it in the residual graph, so one step of a
BFS or DFS over the residual graph costs O(degree) and the graph takes O(V + E) space. Only
residual capacities are stored: residual(e) = capacity(e) - flow(e) on a road, and residual(e ^ 1)
= flow(e) on its reverse edge, so `push` keeps the two in step by changing both.

The max-flow algorithms count their own work (augmenting paths, edges scanned) as they walk
`out_edges`; nothing here counts, so the counters measure the algorithm and nothing else.
"""

from collections.abc import Hashable, Iterable, Iterator
from operator import index

Node = Hashable


class FlowNetwork:
    """A directed network with integer capacities and its residual graph.

    Nodes are any hashable ids (OSM node ids, or ints in the tests). Parallel edges between the
    same pair of nodes are allowed and each keeps its own id, so a closure or widening can name one
    road. A two-way road is two calls to `add_edge`, one per direction.
    """

    def __init__(self) -> None:
        self._adj: dict[Node, list[int]] = {}  # node -> ids of residual edges leaving it
        self._head: list[int | Node] = []  # edge id -> the node it points to
        self._residual: list[int] = []  # edge id -> residual capacity
        self._capacity: list[int] = []  # edge id -> capacity (0 on reverse edges)
        self._terminal: list[bool] = []  # edge id -> joins s or t (see with_super_terminals)

    # Building

    def add_node(self, u: Node) -> None:
        """Add node `u` with no edges, if it isn't there already."""
        self._adj.setdefault(u, [])

    def add_edge(self, u: Node, v: Node, capacity: int) -> int:
        """Add a road from `u` to `v` with a whole-number `capacity` of at least 0.

        Adds `u` and `v` if they are new, and the road's reverse residual edge with residual
        capacity 0. Returns the road's edge id, which is even; its reverse edge is `id ^ 1`.
        """
        return self._add_edge(u, v, capacity, terminal=False)

    def _add_edge(self, u: Node, v: Node, capacity: int, terminal: bool) -> int:
        capacity = index(capacity)  # whole numbers only (D10): rejects floats, accepts int-likes
        if capacity < 0:
            raise ValueError(f"capacity must be at least 0, got {capacity}")
        e = len(self._head)
        self.add_node(u)
        self.add_node(v)
        self._head += [v, u]
        self._residual += [capacity, 0]
        self._capacity += [capacity, 0]
        self._terminal += [terminal, terminal]
        self._adj[u].append(e)
        self._adj[v].append(e ^ 1)
        return e

    def set_capacity(self, e: int, capacity: int) -> None:
        """Change road `e`'s capacity, keeping its current flow. For the closure and widening
        what-ifs. Raises ValueError if the flow on `e` would exceed the new capacity."""
        self._check_road(e)
        capacity = index(capacity)
        if capacity < self.flow(e):
            raise ValueError(f"edge {e} carries {self.flow(e)}, more than capacity {capacity}")
        self._capacity[e] = capacity
        self._residual[e] = capacity - self.flow(e)

    def copy(self) -> "FlowNetwork":
        """An independent copy, with the same edge ids, capacities and current flow."""
        other = FlowNetwork()
        other._adj = {u: list(edges) for u, edges in self._adj.items()}
        other._head = list(self._head)
        other._residual = list(self._residual)
        other._capacity = list(self._capacity)
        other._terminal = list(self._terminal)
        return other

    def reset_flow(self) -> None:
        """Set the flow on every edge back to 0, so the network can be solved again."""
        self._residual = list(self._capacity)

    def with_super_terminals(
        self, sources: Iterable[Node], sinks: Iterable[Node], s: Node = "s", t: Node = "t"
    ) -> "FlowNetwork":
        """A copy with a super-source `s` joined to every source and every sink joined to a
        super-sink `t` (D10).

        The new edges have capacity one more than the sum of all road capacities, so no s-t cut
        that contains one can be minimum: the cut of all the roads is always smaller. They are
        marked, so `is_terminal_edge` lets the min cut skip them. Road edge ids are unchanged.
        """
        sources, sinks = list(dict.fromkeys(sources)), list(dict.fromkeys(sinks))
        for u in sources + sinks:
            if u not in self._adj:
                raise KeyError(f"source or sink {u!r} is not a node of the network")
        if set(sources) & set(sinks):
            raise ValueError("a node can't be both a source and a sink")
        for terminal in (s, t):
            if terminal in self._adj:
                raise ValueError(f"super-terminal id {terminal!r} is already a node")
        if s == t:
            raise ValueError("s and t must be different")
        big = self.total_capacity() + 1
        other = self.copy()
        other.add_node(s)
        other.add_node(t)
        for u in sources:
            other._add_edge(s, u, big, terminal=True)
        for v in sinks:
            other._add_edge(v, t, big, terminal=True)
        return other

    # The residual graph, for the max-flow algorithms

    def out_edges(self, u: Node) -> list[int]:
        """Ids of the residual edges leaving `u`: its roads and the reverse edges of roads into
        it. Some may have residual capacity 0. Don't modify the list."""
        return self._adj[u]

    def head(self, e: int) -> Node:
        """The node edge `e` points to."""
        return self._head[e]

    def tail(self, e: int) -> Node:
        """The node edge `e` leaves."""
        return self._head[e ^ 1]

    def residual(self, e: int) -> int:
        """How much more flow edge `e` can take in the residual graph."""
        return self._residual[e]

    def push(self, e: int, amount: int) -> None:
        """Send `amount` more units along residual edge `e`.

        On a road this adds flow; on a reverse edge it cancels flow on its road. Raises ValueError
        if `amount` is negative or more than `residual(e)`.
        """
        if not 0 <= amount <= self._residual[e]:
            raise ValueError(f"can't push {amount} on edge {e}, residual {self._residual[e]}")
        self._residual[e] -= amount
        self._residual[e ^ 1] += amount

    # Roads and their flow

    def flow(self, e: int) -> int:
        """The flow on road `e` (an even id): the reverse edge's residual capacity."""
        self._check_road(e)
        return self._residual[e ^ 1]

    def capacity(self, e: int) -> int:
        """The capacity of edge `e`: the road's, or 0 for a reverse residual edge."""
        return self._capacity[e]

    @staticmethod
    def is_reverse(e: int) -> bool:
        """Whether `e` is a reverse residual edge rather than a road."""
        return e & 1 == 1

    def is_terminal_edge(self, e: int) -> bool:
        """Whether `e` (or the road it reverses) joins the super-source or super-sink."""
        return self._terminal[e]

    def edges(self) -> Iterator[int]:
        """Ids of every road, including the super-terminal edges, in the order they were added."""
        return iter(range(0, len(self._head), 2))

    def roads(self) -> Iterator[int]:
        """Ids of the real roads only, without the super-terminal edges."""
        return (e for e in self.edges() if not self._terminal[e])

    def total_capacity(self) -> int:
        """The sum of the capacities of the real roads."""
        return sum(self._capacity[e] for e in self.roads())

    def nodes(self) -> Iterator[Node]:
        """Every node, in the order they were added."""
        return iter(self._adj)

    @property
    def num_nodes(self) -> int:
        return len(self._adj)

    @property
    def num_edges(self) -> int:
        """The number of roads (super-terminal edges included), not counting reverse edges."""
        return len(self._head) // 2

    def __contains__(self, u: Node) -> bool:
        return u in self._adj

    def _check_road(self, e: int) -> None:
        if not 0 <= e < len(self._head) or self.is_reverse(e):
            raise ValueError(f"{e} is not a road's edge id (roads have even ids)")
