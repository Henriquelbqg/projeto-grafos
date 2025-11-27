class Graph:
    """
    Estrutura unificada para:
    - Parte 1 (Recife): grafo não-direcionado, pesos positivos
    - Parte 2 (Dataset maior): grafo possivelmente direcionado, pesos positivos/negativos
    """

    def __init__(self, directed=False):


        self.directed = directed
        self.adj = {}



    def add_vertex(self, v):
        """Adiciona um vértice mesmo que ele não tenha arestas."""
        if v not in self.adj:
            self.adj[v] = []



    def add_edge(self, u, v, weight=1.0, directed=None):
        """
        Adiciona uma aresta ao grafo.
        Para Parte 1: directed = False
        Para Parte 2: directed = True ou False, dependendo do dataset
        """

        if directed is None:
            directed = self.directed


        self.add_vertex(u)
        self.add_vertex(v)


        self.adj[u].append((v, weight))


        if not directed:
            self.adj[v].append((u, weight))



    def neighbors(self, v):
        """Retorna lista de vizinhos: [(vizinho, peso), ...]."""
        return self.adj.get(v, [])



    def vertices(self):
        return list(self.adj.keys())



    def edges(self):
        """
        Retorna lista de arestas no formato:
        [(u, v, peso), ...]
        """
        lista = []
        for u in self.adj:
            for (v, w) in self.adj[u]:
                lista.append((u, v, w))
        return lista



    def __len__(self):
        return len(self.adj)



    def __contains__(self, v):
        return v in self.adj



    def __repr__(self):
        tipo = "Direcionado" if self.directed else "Não-direcionado"
        return f"<Graph {tipo} | V={len(self.adj)}>"

    def vizinhos(self, v):
        """Compatibilidade com versão antiga — retorna apenas os nomes dos vizinhos."""
        return [x for (x, _) in self.adj.get(v, [])]
