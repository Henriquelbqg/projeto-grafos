from src.graphs.graph import Graph
from src.graphs.algorithms import bfs

def test_bfs_small_graph():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")

    ordem = bfs(g, "A")

    # BFS visita em largura: A → B → C → D
    assert ordem == ["A", "B", "C", "D"]
