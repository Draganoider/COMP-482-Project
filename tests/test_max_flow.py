"""Ford-Fulkerson checks."""

from collections import defaultdict

import networkx as nx
import pytest
from conftest import to_networkx

from evac.ford_fulkerson import ford_fulkerson
from evac.generators import random_network
from evac.network import FlowNetwork


def assert_valid_flow(network, result, s, t):
    """Check individual road capacities, conservation, and the reported value."""
    balance = defaultdict(int)
    assert set(result.flow) == set(network.edges())
    for e in network.edges():
        f = result.flow[e]
        assert 0 <= f <= network.capacity(e)
        assert network.flow(e) == f
        balance[network.tail(e)] -= f
        balance[network.head(e)] += f
    for node in network.nodes():
        assert balance[node] == (-result.value if node == s else result.value if node == t else 0)


def brute_force_cut_value(network, s, t):
    """Independent small-input check: enumerate all s-t cuts, including parallel roads."""
    other = [node for node in network.nodes() if node != s and node != t]
    best = None
    for mask in range(1 << len(other)):
        source_side = {s}
        source_side.update(node for i, node in enumerate(other) if mask & (1 << i))
        capacity = sum(
            network.capacity(e)
            for e in network.edges()
            if network.tail(e) in source_side and network.head(e) not in source_side
        )
        best = capacity if best is None else min(best, capacity)
    return best


def test_ford_fulkerson_matches_networkx_on_1000_seeded_networks(random_networks):
    for network in random_networks:
        s, t = 0, network.num_nodes - 1
        expected = nx.maximum_flow_value(to_networkx(network), s, t)
        result = ford_fulkerson(network, s, t)
        assert result.value == expected
        assert_valid_flow(network, result, s, t)


def test_ford_fulkerson_matches_brute_force_on_small_networks():
    # Replace this local checker when issue #8 is finished.
    for seed in range(100):
        network = random_network(2 + seed % 11, 3 * (2 + seed % 11), 8, seed)
        expected = brute_force_cut_value(network, 0, network.num_nodes - 1)
        assert ford_fulkerson(network, 0, network.num_nodes - 1).value == expected


def test_ford_fulkerson_no_path_and_isolated_nodes():
    network = FlowNetwork()
    network.add_edge("s", "a", 5)
    network.add_node("t")
    result = ford_fulkerson(network, "s", "t")
    assert result.value == result.augmenting_paths == 0
    assert_valid_flow(network, result, "s", "t")


def test_ford_fulkerson_one_edge_and_exact_counters():
    network = FlowNetwork()
    edge = network.add_edge("s", "t", 7)
    result = ford_fulkerson(network, "s", "t")
    assert (result.value, result.flow[edge]) == (7, 7)
    assert result.augmenting_paths == 1
    assert result.edges_scanned == 2  # first successful search, then the failed search
    assert_valid_flow(network, result, "s", "t")


def test_ford_fulkerson_parallel_edges_keep_separate_flows():
    network = FlowNetwork()
    first = network.add_edge("s", "t", 3)
    second = network.add_edge("s", "t", 4)
    result = ford_fulkerson(network, "s", "t")
    assert result.value == 7
    assert result.flow[first] == 3 and result.flow[second] == 4
    assert result.augmenting_paths == 2
    assert_valid_flow(network, result, "s", "t")


def test_ford_fulkerson_kleinberg_tardos_chapter_7_example():
    network = FlowNetwork()
    network.add_edge("s", "u", 20)
    network.add_edge("s", "v", 10)
    network.add_edge("u", "v", 30)
    network.add_edge("u", "t", 10)
    network.add_edge("v", "t", 20)

    result = ford_fulkerson(network, "s", "t")

    assert result.value == 30
    assert_valid_flow(network, result, "s", "t")


def test_ford_fulkerson_can_cancel_flow_using_a_reverse_edge():
    network = FlowNetwork()
    # First path uses a->b; the second must undo that choice through b->a.
    for u, v in [
        ("s", "y"),
        ("s", "x"),
        ("x", "a"),
        ("y", "b"),
        ("a", "c"),
        ("a", "b"),
        ("b", "t"),
        ("c", "t"),
    ]:
        edge = network.add_edge(u, v, 1)
        if (u, v) == ("a", "b"):
            bridge = edge
    pushed = []
    push = network.push

    def recording_push(e, amount):
        pushed.append(e)
        push(e, amount)

    network.push = recording_push
    result = ford_fulkerson(network, "s", "t")
    assert result.value == 2
    assert result.flow[bridge] == 0
    assert bridge in pushed and bridge ^ 1 in pushed  # pushed along a->b, then undone via b->a
    assert_valid_flow(network, result, "s", "t")


def test_ford_fulkerson_super_terminals_and_flow_snapshot():
    roads = FlowNetwork()
    roads.add_edge("home1", "junction", 2)
    roads.add_edge("home2", "junction", 3)
    roads.add_edge("junction", "shelter", 4)
    network = roads.with_super_terminals(["home1", "home2"], ["shelter"])
    result = ford_fulkerson(network, "s", "t")
    assert result.value == 4
    assert_valid_flow(network, result, "s", "t")
    network.reset_flow()
    assert sum(result.flow.values()) > 0  # result does not change when network is reset


def test_ford_fulkerson_resets_previous_flow():
    network = FlowNetwork()
    edge = network.add_edge("s", "t", 5)
    network.push(edge, 2)
    assert ford_fulkerson(network, "s", "t").value == 5
    assert ford_fulkerson(network, "s", "t").value == 5


def test_ford_fulkerson_deep_10000_node_network():
    network = FlowNetwork()
    for u in range(9999):
        network.add_edge(u, u + 1, 1)
    result = ford_fulkerson(network, 0, 9999)
    assert result.value == result.augmenting_paths == 1
    assert_valid_flow(network, result, 0, 9999)


def test_ford_fulkerson_10000_node_random_network():
    network = random_network(10_000, 20_000, 10, seed=482)
    expected = nx.maximum_flow_value(to_networkx(network), 0, 9_999)
    result = ford_fulkerson(network, 0, 9_999)
    assert result.value == expected
    assert_valid_flow(network, result, 0, 9_999)


@pytest.mark.parametrize("source,sink", [(0, 0), (0, 2)])
def test_ford_fulkerson_rejects_invalid_terminals(source, sink):
    network = FlowNetwork()
    network.add_edge(0, 1, 1)
    with pytest.raises((ValueError, KeyError)):
        ford_fulkerson(network, source, sink)
