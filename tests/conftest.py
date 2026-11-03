"""Helpers the network, max-flow and min-cut tests share: NetworkX conversion and random networks.

NetworkX is a reference for the tests only, never imported in src/ (AGENTS.md, hard rule 3).
Import the plain functions with `from conftest import to_networkx, small_random_network`, or use
the fixtures below.
"""

import random

import networkx as nx
import pytest

from evac.generators import random_network
from evac.network import FlowNetwork

RANDOM_NETWORK_COUNT = 1000


def to_networkx(network: FlowNetwork) -> nx.DiGraph:
    """The network as a NetworkX DiGraph with a `capacity` on each edge, for cross-checks.

    A DiGraph has one edge per ordered pair, so parallel roads are merged into one edge whose
    capacity is their sum; that keeps every max-flow and min-cut value the same. Super-terminal
    edges are included like any other.
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(network.nodes())
    for e in network.edges():
        u, v = network.tail(e), network.head(e)
        if graph.has_edge(u, v):
            graph[u][v]["capacity"] += network.capacity(e)
        else:
            graph.add_edge(u, v, capacity=network.capacity(e))
    return graph


def small_random_network(seed: int, max_nodes: int = 12, max_capacity: int = 20) -> FlowNetwork:
    """A random network of 2..max_nodes nodes, small enough for brute force, picked by `seed`.

    The seed picks the size as well as the roads, so a run over many seeds covers sparse, dense
    and disconnected networks. Use 0 as the source and `num_nodes - 1` as the sink.
    """
    rng = random.Random(seed)
    n = rng.randint(2, max_nodes)
    m = rng.randint(0, 3 * n)
    return random_network(n, m, max_capacity, seed)


@pytest.fixture
def random_networks() -> list[FlowNetwork]:
    """RANDOM_NETWORK_COUNT fresh small random networks, for seeds 0, 1, 2, ... in order.

    Built anew for each test, so a test can push flow without affecting another.
    """
    return [small_random_network(seed) for seed in range(RANDOM_NETWORK_COUNT)]


@pytest.fixture
def nx_digraph():
    """`to_networkx`, as a fixture."""
    return to_networkx
