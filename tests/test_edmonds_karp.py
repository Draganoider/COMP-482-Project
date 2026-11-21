
"""Tests for the Edmonds-Karp maximum-flow algorithm."""

from collections import deque
from unittest.mock import patch

import networkx as nx
import pytest
from conftest import small_random_network, to_networkx

from evac.edmonds_karp import edmonds_karp
from evac.ford_fulkerson import ford_fulkerson
from evac.generators import random_network
from evac.network import FlowNetwork


def test_edmonds_karp_simple_network():
    network = FlowNetwork()

    network.add_edge("S", "A", 10)
    network.add_edge("S", "B", 5)
    network.add_edge("A", "T", 7)
    network.add_edge("B", "T", 8)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 12
    assert result.augmenting_paths == 2
    assert result.edges_scanned > 0


def test_edmonds_karp_disconnected():
    network = FlowNetwork()

    network.add_edge("S", "A", 10)
    network.add_edge("B", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 0
    assert result.augmenting_paths == 0
    assert result.edges_scanned > 0


def test_edmonds_karp_zero_capacity():
    network = FlowNetwork()

    network.add_edge("S", "A", 0)
    network.add_edge("A", "T", 10)
    network.add_edge("S", "B", 5)
    network.add_edge("B", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 5
    assert result.augmenting_paths == 1
    assert result.edges_scanned > 0


def test_edmonds_karp_shortest_path():
    network = FlowNetwork()

    network.add_edge("S", "A", 5)
    network.add_edge("A", "T", 5)

    network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 10
    assert result.augmenting_paths == 2
    assert result.edges_scanned > 0


def test_edmonds_karp_scanned_counter():
    network = FlowNetwork()

    network.add_edge("S", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 5
    assert result.augmenting_paths == 1
    assert result.edges_scanned == 2


def test_edmonds_karp_prefers_shortest_path():
    network = FlowNetwork()

    network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    edge_sa = network.add_edge("S", "A", 5)
    edge_at = network.add_edge("A", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 10
    assert result.augmenting_paths == 2
    assert network.flow(edge_sa) == 5
    assert network.flow(edge_at) == 5


def test_edmonds_karp_against_networkx():
    for seed in range(1000):
        network = random_network(
            n=6,
            m=12,
            max_capacity=20,
            seed=seed,
        )

        graph = nx.DiGraph()
        graph.add_nodes_from(network.nodes())

        for edge in network.edges():
            u = network.tail(edge)
            v = network.head(edge)
            capacity = network.capacity(edge)

            if graph.has_edge(u, v):
                graph[u][v]["capacity"] += capacity
            else:
                graph.add_edge(u, v, capacity=capacity)

        result = edmonds_karp(network, 0, 5)
        expected = nx.maximum_flow_value(graph, 0, 5)

        assert result.value == expected, (
            f"Maximum flow mismatch for seed {seed}: "
            f"Edmonds-Karp={result.value}, NetworkX={expected}"
        )


def test_edmonds_karp_augmentation_bound():
    for seed in range(1000):
        network = random_network(
            n=6,
            m=12,
            max_capacity=20,
            seed=seed,
        )

        result = edmonds_karp(network, 0, 5)

        v = network.num_nodes
        e = network.num_edges

        assert result.augmenting_paths <= v * e, (
            f"Augmentation bound exceeded for seed {seed}: "
            f"paths={result.augmenting_paths}, V={v}, E={e}"
        )


def test_edmonds_karp_same_source_and_sink():
    network = FlowNetwork()
    network.add_edge("S", "T", 5)

    with pytest.raises(ValueError, match="source and sink must be different"):
        edmonds_karp(network, "S", "S")


def test_edmonds_karp_nonexistent_nodes():
    network = FlowNetwork()
    network.add_edge("S", "T", 5)

    with pytest.raises(KeyError, match="source and sink must exist"):
        edmonds_karp(network, "X", "T")

    with pytest.raises(KeyError, match="source and sink must exist"):
        edmonds_karp(network, "S", "X")


def test_edmonds_karp_chooses_shortest_path():
    network = FlowNetwork()

    edge_sb = network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    edge_sa = network.add_edge("S", "A", 5)
    network.add_edge("A", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 10
    assert result.augmenting_paths == 2
    assert network.flow(edge_sa) == 5
    assert network.flow(edge_sb) == 5


def test_edmonds_karp_uses_reverse_edge():
    network = FlowNetwork()

    network.add_edge("S", "A", 1)
    network.add_edge("S", "B", 1)
    network.add_edge("A", "C", 1)
    network.add_edge("A", "D", 1)
    network.add_edge("B", "C", 1)
    network.add_edge("C", "T", 1)
    network.add_edge("D", "T", 1)

    pushed_edges = []
    original_push = network.push

    def record_push(edge, amount):
        pushed_edges.append(edge)
        original_push(edge, amount)

    with patch.object(network, "push", side_effect=record_push):
        result = edmonds_karp(network, "S", "T")

    assert result.value == 2
    assert any(network.is_reverse(edge) for edge in pushed_edges)


def test_edmonds_karp_shortest_path_first():
    network = FlowNetwork()

    network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    network.add_edge("S", "A", 5)
    edge_at = network.add_edge("A", "T", 5)

    pushed_edges = []
    original_push = network.push

    def record_push(edge, amount):
        pushed_edges.append(edge)
        original_push(edge, amount)

    with patch.object(network, "push", side_effect=record_push):
        result = edmonds_karp(network, "S", "T")

    assert result.value == 10
    assert result.augmenting_paths == 2
    assert pushed_edges[0] == edge_at


def check_flow_validity(network, result, source, sink):
    """Verify capacity constraints and flow conservation."""

    balance = {node: 0 for node in network.nodes()}

    assert set(result.flow) == set(network.edges())

    for edge in network.edges():
        flow = result.flow[edge]
        capacity = network.capacity(edge)

        assert 0 <= flow <= capacity

        u = network.tail(edge)
        v = network.head(edge)

        balance[u] -= flow
        balance[v] += flow

        assert network.flow(edge) == flow

    for node in network.nodes():
        if node not in (source, sink):
            assert balance[node] == 0

    assert balance[source] == -result.value
    assert balance[sink] == result.value


def test_edmonds_karp_flow_validity_random():
    """Check capacity and conservation on 1000 seeded networks."""

    for seed in range(1000):
        network = small_random_network(seed)
        sink = network.num_nodes - 1

        result = edmonds_karp(network, 0, sink)

        check_flow_validity(network, result, 0, sink)


def test_edmonds_karp_matches_ford_fulkerson():
    """Compare both algorithms on 1000 seeded networks."""

    for seed in range(1000):
        network = small_random_network(seed)
        sink = network.num_nodes - 1

        ek_network = network.copy()
        ff_network = network.copy()

        ek_result = edmonds_karp(ek_network, 0, sink)
        ff_result = ford_fulkerson(ff_network, 0, sink)

        expected = nx.maximum_flow_value(
            to_networkx(network), 0, sink
        )

        assert ek_result.value == ff_result.value == expected
        check_flow_validity(ek_network, ek_result, 0, sink)
        check_flow_validity(ff_network, ff_result, 0, sink)


def test_edmonds_karp_parallel_roads():
    """Parallel roads should contribute their capacities separately."""

    network = FlowNetwork()

    edge_1 = network.add_edge("S", "A", 3)
    edge_2 = network.add_edge("S", "A", 4)
    network.add_edge("A", "T", 10)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 7
    assert result.flow[edge_1] == 3
    assert result.flow[edge_2] == 4

    check_flow_validity(network, result, "S", "T")


def test_edmonds_karp_classic_network():
    """Check the standard six-node maximum-flow example."""

    network = FlowNetwork()

    edges = [
        ("S", "A", 16),
        ("S", "C", 13),
        ("A", "B", 12),
        ("A", "C", 10),
        ("B", "C", 9),
        ("C", "A", 4),
        ("C", "D", 14),
        ("D", "B", 7),
        ("B", "T", 20),
        ("D", "T", 4),
    ]

    for u, v, capacity in edges:
        network.add_edge(u, v, capacity)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 23
    check_flow_validity(network, result, "S", "T")


def residual_shortest_distance(network, source, sink):
    """Return the BFS distance to the sink in the residual graph."""

    queue = deque([(source, 0)])
    visited = {source}

    while queue:
        u, distance = queue.popleft()

        if u == sink:
            return distance

        for edge in network.out_edges(u):
            v = network.head(edge)

            if network.residual(edge) > 0 and v not in visited:
                visited.add(v)
                queue.append((v, distance + 1))

    return None


def test_every_augmentation_uses_shortest_path():
    """Every augmentation must follow a shortest residual path."""

    for seed in range(100):
        network = small_random_network(seed)
        sink = network.num_nodes - 1

        verify_shortest_augmentations(network, 0, sink)


def verify_shortest_augmentations(network, source, sink):
    """Verify that every augmentation uses a shortest residual path."""

    original_push = network.push
    pending_edges = []
    pending_amount = None
    expected_distance = None
    checked_paths = 0

    def record_push(edge, amount):
        nonlocal pending_amount, expected_distance, checked_paths

        if not pending_edges:
            expected_distance = residual_shortest_distance(
                network, source, sink
            )
            assert expected_distance is not None
            assert amount > 0
            pending_amount = amount

        assert amount == pending_amount
        assert network.residual(edge) >= amount
        pending_edges.append(edge)

        if len(pending_edges) == 1:
            assert network.head(edge) == sink
        else:
            previous = pending_edges[-2]
            assert network.head(edge) == network.tail(previous)

        if network.tail(edge) == source:
            assert len(pending_edges) == expected_distance

            for path_edge in pending_edges:
                original_push(path_edge, amount)

            checked_paths += 1
            pending_edges.clear()
            pending_amount = None
            expected_distance = None

    with patch.object(network, "push", side_effect=record_push):
        result = edmonds_karp(network, source, sink)

    assert not pending_edges
    assert checked_paths == result.augmenting_paths


def test_edmonds_karp_fewer_augmentations_than_dfs():
    """Show a seeded network where DFS uses more augmentations than BFS."""

    network = random_network(
        n=8,
        m=20,
        max_capacity=10,
        seed=45,
    )

    ff_network = network.copy()
    ek_network = network.copy()

    ff_result = ford_fulkerson(ff_network, 0, 7)
    ek_result = edmonds_karp(ek_network, 0, 7)

    assert ff_result.value == 10
    assert ek_result.value == 10

    assert ff_result.augmenting_paths == 5
    assert ek_result.augmenting_paths == 4
    assert ff_result.augmenting_paths > ek_result.augmenting_paths

    check_flow_validity(ff_network, ff_result, 0, 7)
    check_flow_validity(ek_network, ek_result, 0, 7)
