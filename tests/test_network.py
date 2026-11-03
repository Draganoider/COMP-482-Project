"""Tests for the flow network (src/evac/network.py) and the random generator (generators.py)."""

import random

import networkx as nx
import pytest
from conftest import small_random_network, to_networkx

from evac.generators import random_network
from evac.network import FlowNetwork


def snapshot(network):
    """Everything that defines a network, for comparing two of them."""
    return (
        list(network.nodes()),
        [(network.tail(e), network.head(e), network.capacity(e)) for e in network.edges()],
    )


def check_residuals(network):
    """flow + residual = capacity on every road, and the reverse edge's residual = flow."""
    for e in network.edges():
        flow = network.flow(e)
        assert 0 <= flow <= network.capacity(e)
        assert flow + network.residual(e) == network.capacity(e)
        assert network.residual(e ^ 1) == flow
        assert network.capacity(e ^ 1) == 0


# Building


def test_one_line_network():
    network = FlowNetwork()
    e = network.add_edge("a", "b", 5)
    assert network.num_nodes == 2 and network.num_edges == 1
    assert (network.tail(e), network.head(e)) == ("a", "b")
    assert (network.tail(e ^ 1), network.head(e ^ 1)) == ("b", "a")
    assert network.capacity(e) == 5 and network.residual(e) == 5
    assert network.flow(e) == 0 and network.residual(e ^ 1) == 0
    assert network.out_edges("a") == [e] and network.out_edges("b") == [e ^ 1]
    assert not network.is_reverse(e) and network.is_reverse(e ^ 1)


def test_parallel_edges_keep_their_own_ids():
    network = FlowNetwork()
    first = network.add_edge(1, 2, 3)
    second = network.add_edge(1, 2, 4)
    assert first != second
    assert network.out_edges(1) == [first, second]
    network.push(second, 4)
    assert network.flow(first) == 0 and network.flow(second) == 4


def test_two_way_road_is_two_edges():
    network = FlowNetwork()
    there = network.add_edge(1, 2, 6)
    back = network.add_edge(2, 1, 2)
    network.push(there, 6)
    assert network.flow(there) == 6 and network.flow(back) == 0
    assert network.residual(back) == 2


def test_zero_capacity_and_isolated_nodes():
    network = FlowNetwork()
    network.add_node("lonely")
    e = network.add_edge(1, 2, 0)
    assert "lonely" in network and network.out_edges("lonely") == []
    assert network.residual(e) == 0
    with pytest.raises(ValueError):
        network.push(e, 1)


@pytest.mark.parametrize("capacity", [-1, 2.5, 3.0, "3", None])
def test_capacity_must_be_a_whole_number_at_least_zero(capacity):
    with pytest.raises((ValueError, TypeError)):
        FlowNetwork().add_edge(1, 2, capacity)


def test_edge_ids_are_even_and_in_order():
    network = FlowNetwork()
    ids = [network.add_edge(i, i + 1, 1) for i in range(5)]
    assert ids == [0, 2, 4, 6, 8] == list(network.edges())


# Residual graph


def test_push_and_cancel():
    network = FlowNetwork()
    e = network.add_edge("u", "v", 10)
    network.push(e, 7)
    assert (network.flow(e), network.residual(e), network.residual(e ^ 1)) == (7, 3, 7)
    network.push(e ^ 1, 5)  # cancel 5 of the 7
    assert (network.flow(e), network.residual(e), network.residual(e ^ 1)) == (2, 8, 2)


@pytest.mark.parametrize("amount", [-1, 11])
def test_push_rejects_more_than_the_residual_or_negative(amount):
    network = FlowNetwork()
    e = network.add_edge("u", "v", 10)
    with pytest.raises(ValueError):
        network.push(e, amount)
    assert network.flow(e) == 0


def test_cannot_cancel_more_flow_than_there_is():
    network = FlowNetwork()
    e = network.add_edge("u", "v", 10)
    network.push(e, 3)
    with pytest.raises(ValueError):
        network.push(e ^ 1, 4)


def test_flow_is_only_defined_on_roads():
    network = FlowNetwork()
    e = network.add_edge("u", "v", 10)
    for bad in (e ^ 1, 2, -2):
        with pytest.raises(ValueError):
            network.flow(bad)


def test_residuals_stay_consistent_after_random_pushes(random_networks):
    """Definition of done for #5: checked after random pushes on 1,000 seeded random networks."""
    rng = random.Random(482)
    for network in random_networks:
        all_edges = range(2 * network.num_edges)
        for _ in range(50):
            pushable = [e for e in all_edges if network.residual(e) > 0]
            if not pushable:
                break
            e = rng.choice(pushable)
            network.push(e, rng.randint(1, network.residual(e)))
            check_residuals(network)


def test_out_edges_cover_the_residual_graph_once(random_networks):
    """Every edge id, road or reverse, is in exactly one adjacency list: its tail's."""
    for network in random_networks[:100]:
        seen = [e for u in network.nodes() for e in network.out_edges(u)]
        assert sorted(seen) == list(range(2 * network.num_edges))
        for u in network.nodes():
            assert all(network.tail(e) == u for e in network.out_edges(u))


def test_reset_flow_and_copy():
    network = FlowNetwork()
    e = network.add_edge(1, 2, 5)
    network.push(e, 4)
    clone = network.copy()
    assert clone.flow(e) == 4
    network.reset_flow()
    assert network.flow(e) == 0 and network.residual(e) == 5
    assert clone.flow(e) == 4  # the copy is independent
    clone.add_edge(2, 3, 1)
    assert network.num_edges == 1 and 3 not in network


def test_set_capacity_keeps_the_flow():
    network = FlowNetwork()
    e = network.add_edge(1, 2, 5)
    network.push(e, 3)
    network.set_capacity(e, 8)  # widen
    assert (network.capacity(e), network.flow(e), network.residual(e)) == (8, 3, 5)
    network.set_capacity(e, 3)
    assert network.residual(e) == 0
    with pytest.raises(ValueError):
        network.set_capacity(e, 2)  # below the flow
    network.reset_flow()
    network.set_capacity(e, 0)  # close the road
    assert network.residual(e) == 0
    check_residuals(network)


# Super-source and super-sink


def test_super_terminals_join_sources_and_sinks():
    network = FlowNetwork()
    roads = [network.add_edge(1, 2, 4), network.add_edge(2, 3, 6), network.add_edge(1, 3, 5)]
    joined = network.with_super_terminals(sources=[1], sinks=[3])
    assert network.num_edges == 3 and "s" not in network  # the original is unchanged
    assert list(joined.roads()) == roads
    new = [e for e in joined.edges() if joined.is_terminal_edge(e)]
    assert [(joined.tail(e), joined.head(e)) for e in new] == [("s", 1), (3, "t")]
    assert all(joined.is_terminal_edge(e ^ 1) for e in new)
    assert not any(joined.is_terminal_edge(e) for e in roads)


def test_super_terminal_edges_exceed_the_total_road_capacity(random_networks):
    """Definition of done for #5: larger than all road capacity together, and marked."""
    for network in random_networks:
        n = network.num_nodes
        total = network.total_capacity()
        joined = network.with_super_terminals(sources=[0], sinks=[n - 1])
        assert joined.total_capacity() == total  # terminal edges aren't roads
        terminal = [e for e in joined.edges() if joined.is_terminal_edge(e)]
        assert len(terminal) == 2
        assert all(joined.capacity(e) > total for e in terminal)


def test_super_terminals_dont_change_the_max_flow(random_networks):
    """With one source and one sink, the s-t max flow equals the source-sink max flow."""
    for network in random_networks[:200]:
        n = network.num_nodes
        joined = network.with_super_terminals(sources=[0], sinks=[n - 1])
        direct = nx.maximum_flow_value(to_networkx(network), 0, n - 1)
        assert nx.maximum_flow_value(to_networkx(joined), "s", "t") == direct


def test_super_terminals_stay_largest_after_widening_or_adding_roads():
    """Widening a road on the joined network (the what-ifs, #9) must not let a terminal edge
    become the bottleneck."""
    network = FlowNetwork()
    road = network.add_edge(1, 2, 1)
    joined = network.with_super_terminals(sources=[1], sinks=[2])
    terminal = [e for e in joined.edges() if joined.is_terminal_edge(e)]
    joined.push(terminal[0], 1)  # some flow on a terminal edge, which raising must keep
    joined.set_capacity(road, 10)
    assert all(joined.capacity(e) > joined.total_capacity() == 10 for e in terminal)
    assert joined.flow(terminal[0]) == 1
    assert nx.maximum_flow_value(to_networkx(joined), "s", "t") == 10
    joined.add_edge(1, 2, 5)
    assert all(joined.capacity(e) > joined.total_capacity() == 15 for e in terminal)
    with pytest.raises(ValueError):
        joined.set_capacity(terminal[0], 3)  # not a road
    check_residuals(joined)


def test_total_capacity_tracks_changes(random_networks):
    for network in random_networks[:200]:
        for e in list(network.roads())[:3]:
            network.set_capacity(e, network.capacity(e) + 2)
        assert network.total_capacity() == sum(network.capacity(e) for e in network.roads())


def test_super_terminals_with_several_sources_and_sinks():
    network = FlowNetwork()
    network.add_edge("h1", "x", 3)
    network.add_edge("h2", "x", 4)
    network.add_edge("x", "exit1", 2)
    network.add_edge("x", "exit2", 10)
    joined = network.with_super_terminals(["h1", "h2", "h1"], ["exit1", "exit2"])
    assert sum(joined.is_terminal_edge(e) for e in joined.edges()) == 4  # duplicate h1 dropped
    assert nx.maximum_flow_value(to_networkx(joined), "s", "t") == 7


def test_super_terminals_reject_bad_input():
    network = FlowNetwork()
    network.add_edge(1, 2, 1)
    with pytest.raises(KeyError):
        network.with_super_terminals([1], [99])
    with pytest.raises(ValueError):
        network.with_super_terminals([1], [1])
    with pytest.raises(ValueError):
        network.with_super_terminals([1], [2], s=2)
    joined = network.with_super_terminals([1], [2])
    with pytest.raises(ValueError):  # a second pair would break the one-terminal-capacity rule
        joined.copy().with_super_terminals([1], [2], s="s2", t="t2")


# Random networks and the NetworkX conversion


def test_random_network_shape():
    network = random_network(10, 40, 7, seed=1)
    assert list(network.nodes()) == list(range(10))
    assert network.num_edges == 40
    for e in network.edges():
        assert network.tail(e) != network.head(e)
        assert 1 <= network.capacity(e) <= 7


def test_random_network_same_seed_same_network():
    for seed in range(50):
        assert snapshot(random_network(12, 30, 20, seed)) == snapshot(
            random_network(12, 30, 20, seed)
        )
        assert snapshot(small_random_network(seed)) == snapshot(small_random_network(seed))


def test_random_network_different_seeds_different_networks():
    networks = {repr(snapshot(random_network(12, 30, 20, seed))) for seed in range(50)}
    assert len(networks) == 50


def test_random_network_ignores_the_global_random_state():
    random.seed(1)
    first = snapshot(random_network(8, 20, 9, seed=3))
    random.seed(2)
    assert snapshot(random_network(8, 20, 9, seed=3)) == first


@pytest.mark.parametrize(("n", "m", "max_capacity"), [(-1, 0, 1), (1, 1, 5), (5, 3, 0), (5, -1, 5)])
def test_random_network_rejects_bad_sizes(n, m, max_capacity):
    with pytest.raises(ValueError):
        random_network(n, m, max_capacity, seed=0)


def test_random_network_with_no_roads():
    network = random_network(3, 0, 5, seed=0)
    assert network.num_nodes == 3 and network.num_edges == 0


def test_to_networkx_sums_parallel_edges():
    network = FlowNetwork()
    network.add_node("alone")
    network.add_edge(1, 2, 3)
    network.add_edge(1, 2, 4)
    network.add_edge(2, 1, 5)
    graph = to_networkx(network)
    assert set(graph.nodes) == {1, 2, "alone"}
    assert graph[1][2]["capacity"] == 7 and graph[2][1]["capacity"] == 5
    assert graph.number_of_edges() == 2
