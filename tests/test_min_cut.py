from evac.min_cut import min_cut
from evac.network import FlowNetwork
from brute_force import brute_force_min_cut


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

    # Manually send a maximum flow of 12 units.
    network.push(edge_sa, 7)
    network.push(edge_at, 7)
    network.push(edge_sb, 5)
    network.push(edge_bt, 5)

    cut = min_cut(network, None, "S")

    assert cut.capacity == 12
    assert cut.reachable == {"S", "A"}
    assert set(cut.cut_edges) == {edge_sb, edge_at}

