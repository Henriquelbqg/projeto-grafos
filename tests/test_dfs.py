from src.graphs.graph import Graph
from src.graphs.algorithms import dfs

def test_dfs_detect_cycle():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")  # cria ciclo

    ordem, ciclo = dfs(g, "A")

    assert ciclo is True
    assert "A" in ordem
    assert "B" in ordem
    assert "C" in ordem
