"""Tests for the Edmonds-Karp maximum-flow algorithm."""

from unittest.mock import patch

import networkx as nx
import pytest

from evac.edmonds_karp import edmonds_karp
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

    # Short path: S -> A -> T
    network.add_edge("S", "A", 5)
    network.add_edge("A", "T", 5)

    # Longer path: S -> B -> C -> T
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

    # Add the longer route first.
    network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    # Add the shorter route second.
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

    # Add the longer route first.
    edge_sb = network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    # Add the shorter route second.
    edge_sa = network.add_edge("S", "A", 5)
    network.add_edge("A", "T", 5)

    result = edmonds_karp(network, "S", "T")

    assert result.value == 10
    assert result.augmenting_paths == 2

    # Both routes must carry their full capacity.
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

    # Add the longer path first.
    network.add_edge("S", "B", 5)
    network.add_edge("B", "C", 5)
    network.add_edge("C", "T", 5)

    # Add the shorter path second.
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

    # The first augmenting path must be the shorter path.
    assert pushed_edges[0] == edge_at
