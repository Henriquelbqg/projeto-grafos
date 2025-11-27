import sys
import pytest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "parte1" / "src"))

from graphs.graph import Graph
from graphs.algorithms import dijkstra

def test_dijkstra_basic_path():
    g = Graph(directed=False)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)

    dist, path = dijkstra(g, "A", "C")

    assert dist == 3
    assert path == ["A", "B", "C"]


def test_dijkstra_reject_negative_weights():
    g = Graph(directed=False)
    g.add_edge("A", "B", -1)

    with pytest.raises(ValueError):
        dijkstra(g, "A", "B")
