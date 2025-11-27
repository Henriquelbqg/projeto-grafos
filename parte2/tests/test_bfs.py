import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "parte1" / "src"))

from graphs.graph import Graph
from graphs.algorithms import bfs

def test_bfs_small_graph():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")

    resultado = bfs(g, "A")
    ordem = resultado.get("ordem", [])
    camadas = resultado.get("camadas", {})


    assert ordem == ["A", "B", "C", "D"]


    assert camadas["A"] == 0
    assert camadas["B"] == 1
    assert camadas["C"] == 1
    assert camadas["D"] == 2
