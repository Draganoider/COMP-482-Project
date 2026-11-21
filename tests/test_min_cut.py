
"""Tests for minimum-cut and brute-force implementations."""

import pytest
from brute_force import brute_force_min_cut

from evac.edmonds_karp import edmonds_karp
from evac.ford_fulkerson import ford_fulkerson
from evac.generators import random_network
from evac.min_cut import min_cut
from evac.network import FlowNetwork
from evac.results import MaxFlowResult


def make_result(network, value):
    """Create a result for a network with manually completed flow."""
    return MaxFlowResult(
        value=value,
        flow={edge: network.flow(edge) for edge in network.edges()},
        augmenting_paths=0,
        edges_scanned=0,
    )


def test_brute_force_min_cut():
    network = FlowNetwork()

    network.add_edge("S", "A", 10)
    network.add_edge("S", "B", 5)
    network.add_edge("A", "T", 7)
    network.add_edge("B", "T", 8)

    capacity, source_side = brute_force_min_cut(network, "S", "T")

    assert capacity == 12
    assert source_side == {"S", "A"}


def test_min_cut_with_completed_flow():
    network = FlowNetwork()

    edge_sa = network.add_edge("S", "A", 10)
    edge_sb = network.add_edge("S", "B", 5)
    edge_at = network.add_edge("A", "T", 7)
    edge_bt = network.add_edge("B", "T", 8)

    network.push(edge_sa, 7)
    network.push(edge_at, 7)
    network.push(edge_sb, 5)
    network.push(edge_bt, 5)

    result = make_result(network, 12)
    cut = min_cut(network, result, "S")

    assert cut.capacity == 12
    assert cut.reachable == {"S", "A"}
    assert set(cut.cut_edges) == {edge_sb, edge_at}


def test_min_cut_disconnected():
    network = FlowNetwork()

    network.add_edge("S", "A", 10)
    network.add_edge("B", "T", 5)

    result = make_result(network, 0)
    cut = min_cut(network, result, "S")

    assert cut.capacity == 0
    assert cut.cut_edges == []
    assert cut.reachable == {"S", "A"}

    brute_capacity, _ = brute_force_min_cut(network, "S", "T")
    assert brute_capacity == 0


def test_min_cut_zero_capacity():
    network = FlowNetwork()

    network.add_edge("S", "A", 0)
    network.add_edge("A", "T", 10)

    result = make_result(network, 0)
    cut = min_cut(network, result, "S")

    assert cut.capacity == 0
    assert cut.reachable == {"S"}
    assert cut.cut_edges == [0]

    brute_capacity, _ = brute_force_min_cut(network, "S", "T")
    assert brute_capacity == 0


def test_min_cut_excludes_super_terminal_edges():
    network = FlowNetwork()

    road = network.add_edge("A", "B", 5)

    network = network.with_super_terminals(
        sources=["A"],
        sinks=["B"],
    )

    network.push(road, 5)

    source_edge = next(
        edge for edge in network.edges()
        if network.tail(edge) == "s"
    )
    sink_edge = next(
        edge for edge in network.edges()
        if network.head(edge) == "t"
    )

    network.push(source_edge, 5)
    network.push(sink_edge, 5)

    result = make_result(network, 5)
    cut = min_cut(network, result, "s")

    assert cut.capacity == 5
    assert cut.cut_edges == [road]
    assert all(
        not network.is_terminal_edge(edge)
        for edge in cut.cut_edges
    )

    brute_capacity, _ = brute_force_min_cut(network, "s", "t")
    assert brute_capacity == 5


def test_min_cut_rejects_incorrect_flow_value():
    network = FlowNetwork()
    network.add_edge("S", "T", 5)

    result = make_result(network, 5)

    with pytest.raises(ValueError, match="does not match"):
        min_cut(network, result, "S")


def test_min_cut_rejects_missing_source():
    network = FlowNetwork()
    network.add_edge("S", "T", 5)

    result = make_result(network, 0)

    with pytest.raises(ValueError, match="source must exist"):
        min_cut(network, result, "X")


def test_brute_force_invalid_inputs():
    network = FlowNetwork()
    network.add_edge("S", "T", 5)

    with pytest.raises(ValueError, match="must be different"):
        brute_force_min_cut(network, "S", "S")

    with pytest.raises(ValueError, match="must exist"):
        brute_force_min_cut(network, "X", "T")


@pytest.mark.parametrize(
    "algorithm",
    [ford_fulkerson, edmonds_karp],
)
def test_min_cut_random_networks(algorithm):
    """Compare max flow, minimum cut, and brute force on 1000 networks."""

    for seed in range(1000):
        network = random_network(
            n=6,
            m=12,
            max_capacity=20,
            seed=seed,
        )

        source = 0
        sink = 5

        result = algorithm(network, source, sink)
        cut = min_cut(network, result, source)

        brute_capacity, _ = brute_force_min_cut(
            network, source, sink
        )

        assert result.value == cut.capacity, (
            f"Flow and cut mismatch for seed {seed}"
        )

        assert cut.capacity == brute_capacity, (
            f"Brute-force mismatch for seed {seed}"
        )

        assert sink not in cut.reachable

        assert all(
            not network.is_terminal_edge(edge)
            for edge in cut.cut_edges
        )
