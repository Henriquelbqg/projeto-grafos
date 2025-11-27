import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "parte1" / "src"))

from graphs.graph import Graph
from graphs.algorithms import dfs

def test_dfs_detect_cycle():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")

    resultado = dfs(g, "A")
    ordem = resultado.get("ordem", [])
    ciclos = resultado.get("ciclos", [])
    arestas_class = resultado.get("arestas_class", [])

    assert len(ciclos) > 0
    assert "A" in ordem
    assert "B" in ordem
    assert "C" in ordem


    assert len(arestas_class) > 0

    tipos = [tipo for _, _, tipo in arestas_class]
    assert "tree" in tipos
    assert "back" in tipos
