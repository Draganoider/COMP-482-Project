"""Seeded random inputs for the tests and experiment E1 (proposal section 4, synthetic networks).

Generation happens here, outside any timed region (AGENTS.md, Writing algorithm code). Each
generator takes an explicit seed and uses its own `random.Random`, so the same seed gives the same
network on every run and machine, whatever else uses the global random module.
"""

import random

from evac.network import FlowNetwork


def random_network(n: int, m: int, max_capacity: int, seed: int) -> FlowNetwork:
    """A random directed network with nodes 0..n-1 and m roads.

    Each road joins two different nodes picked uniformly at random, with a capacity drawn
    uniformly from 1..max_capacity. Parallel roads can occur, as they do in OSM; self-loops can't.
    Nodes with no roads are still in the network. Tests use 0 as the source and n-1 as the sink.
    """
    if n < 0 or m < 0:
        raise ValueError("n and m must be at least 0")
    if m > 0 and n < 2:
        raise ValueError("roads need at least two nodes")
    if max_capacity < 1:
        raise ValueError("max_capacity must be at least 1")
    rng = random.Random(seed)
    network = FlowNetwork()
    for u in range(n):
        network.add_node(u)
    for _ in range(m):
        u, v = rng.sample(range(n), 2)
        network.add_edge(u, v, rng.randint(1, max_capacity))
    return network
