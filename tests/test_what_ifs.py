
"""Tests for road closure and widening what-if calculations."""

from types import SimpleNamespace

import networkx as nx
import pytest

from evac.generators import random_network
from evac.network import FlowNetwork
from evac.what_ifs import closure_losses, widening_gains


def networkx_solver(network, s, t):
    """Reference maximum-flow solver for testing only."""
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

    return SimpleNamespace(
        value=nx.maximum_flow_value(graph, s, t)
    )


def make_network():
    """Create a small network with two evacuation routes."""
    network = FlowNetwork()

    edge_sa = network.add_edge("S", "A", 10)
    edge_at = network.add_edge("A", "T", 7)
    edge_sb = network.add_edge("S", "B", 5)
    edge_bt = network.add_edge("B", "T", 8)

    return network, edge_sa, edge_at, edge_sb, edge_bt


def test_closure_losses():
    network, edge_sa, edge_at, edge_sb, edge_bt = make_network()

    losses = closure_losses(network, "S", "T", networkx_solver)

    assert losses[edge_sa] == 7
    assert losses[edge_at] == 7
    assert losses[edge_sb] == 5
    assert losses[edge_bt] == 5


def test_widening_gains():
    network, edge_sa, edge_at, edge_sb, edge_bt = make_network()

    gains = widening_gains(network, "S", "T", networkx_solver, 5)

    assert gains[edge_sa] == 0
    assert gains[edge_at] == 3
    assert gains[edge_sb] == 3
    assert gains[edge_bt] == 0


def test_what_ifs_preserve_original_network():
    network, *_ = make_network()

    original_capacities = {
        edge: network.capacity(edge) for edge in network.edges()
    }

    original_residuals = {
        edge: network.residual(edge)
        for road in network.edges()
        for edge in (road, road ^ 1)
    }

    closure_losses(network, "S", "T", networkx_solver)
    widening_gains(network, "S", "T", networkx_solver, 5)

    assert {
        edge: network.capacity(edge) for edge in network.edges()
    } == original_capacities

    assert {
        edge: network.residual(edge)
        for road in network.edges()
        for edge in (road, road ^ 1)
    } == original_residuals


def test_what_ifs_monotonicity():
    network, *_ = make_network()

    losses = closure_losses(network, "S", "T", networkx_solver)
    gains = widening_gains(network, "S", "T", networkx_solver, 5)

    assert all(loss >= 0 for loss in losses.values())
    assert all(gain >= 0 for gain in gains.values())


def test_widening_invalid_capacity():
    network, *_ = make_network()

    for invalid_capacity in (-1, 2.5, True):
        with pytest.raises(ValueError, match="nonnegative integer"):
            widening_gains(
                network,
                "S",
                "T",
                networkx_solver,
                invalid_capacity,
            )


def test_disconnected_network():
    network = FlowNetwork()

    network.add_edge("S", "A", 10)
    network.add_edge("B", "T", 5)

    losses = closure_losses(network, "S", "T", networkx_solver)
    gains = widening_gains(network, "S", "T", networkx_solver, 5)

    assert all(loss == 0 for loss in losses.values())
    assert all(gain == 0 for gain in gains.values())


def test_zero_capacity_road():
    network = FlowNetwork()

    edge_sa = network.add_edge("S", "A", 0)
    network.add_edge("A", "T", 5)

    losses = closure_losses(network, "S", "T", networkx_solver)
    gains = widening_gains(network, "S", "T", networkx_solver, 3)

    assert losses[edge_sa] == 0
    assert gains[edge_sa] == 3


def test_parallel_roads():
    network = FlowNetwork()

    edge_1 = network.add_edge("S", "A", 3)
    edge_2 = network.add_edge("S", "A", 4)
    network.add_edge("A", "T", 10)

    losses = closure_losses(network, "S", "T", networkx_solver)
    gains = widening_gains(network, "S", "T", networkx_solver, 2)

    assert losses[edge_1] == 3
    assert losses[edge_2] == 4
    assert gains[edge_1] == 2
    assert gains[edge_2] == 2


def test_super_terminal_edges_are_not_modified():
    network = FlowNetwork()
    road = network.add_edge("A", "B", 5)

    network = network.with_super_terminals(
        sources=["A"],
        sinks=["B"],
    )

    original_terminal_capacities = {
        edge: network.capacity(edge)
        for edge in network.edges()
        if network.is_terminal_edge(edge)
    }

    losses = closure_losses(network, "s", "t", networkx_solver)
    gains = widening_gains(network, "s", "t", networkx_solver, 5)

    assert set(losses) == {road}
    assert set(gains) == {road}

    assert losses[road] == 5
    assert gains[road] == 5

    assert {
        edge: network.capacity(edge)
        for edge in network.edges()
        if network.is_terminal_edge(edge)
    } == original_terminal_capacities


@pytest.mark.parametrize("seed", range(100))
def test_what_ifs_against_networkx(seed):
    """Compare closure and widening results against NetworkX."""

    network = random_network(
        n=6,
        m=12,
        max_capacity=20,
        seed=seed,
    )

    source = 0
    sink = 5
    added_capacity = 5

    baseline = networkx_solver(network, source, sink).value

    losses = closure_losses(
        network, source, sink, networkx_solver
    )

    gains = widening_gains(
        network, source, sink, networkx_solver, added_capacity
    )

    assert set(losses) == set(network.roads())
    assert set(gains) == set(network.roads())

    for edge in network.roads():
        closed = network.copy()
        closed.reset_flow()
        closed.set_capacity(edge, 0)

        expected_closed = networkx_solver(
            closed, source, sink
        ).value

        widened = network.copy()
        widened.reset_flow()
        widened.set_capacity(
            edge,
            widened.capacity(edge) + added_capacity,
        )

        expected_widened = networkx_solver(
            widened, source, sink
        ).value

        assert losses[edge] == baseline - expected_closed, (
            f"Closure mismatch for seed {seed}, edge {edge}"
        )

        assert gains[edge] == expected_widened - baseline, (
            f"Widening mismatch for seed {seed}, edge {edge}"
        )

        assert losses[edge] >= 0
        assert gains[edge] >= 0
