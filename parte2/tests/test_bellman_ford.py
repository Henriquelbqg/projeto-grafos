import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "parte1" / "src"))

from graphs.graph import Graph
from graphs.algorithms import bellman_ford

def test_bellman_ford_no_negative_cycle():
    g = Graph(directed=True)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", -2)

    dist, parent, ciclo = bellman_ford(g, "A")

    assert ciclo is False
    assert dist["C"] == -1


def test_bellman_ford_detect_negative_cycle():
    g = Graph(directed=True)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", -2)
    g.add_edge("C", "A", -2)

    dist, parent, ciclo = bellman_ford(g, "A")

    assert ciclo is True
