import heapq


# ============================================================
# BFS (não ponderado)
# ============================================================
def bfs(graph, source):
    visited = set()
    queue = [source]

    ordem = []
    camadas = {source: 0}
    ciclos = []

    visited.add(source)

    while queue:
        u = queue.pop(0)
        ordem.append(u)

        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                camadas[v] = camadas[u] + 1
                queue.append(v)
            else:
                # ciclo encontrado (não dirigido → evita duplicar)
                if len(ciclos) < 5 and v != source:
                    ciclos.append((u, v))

    return {
        "ordem": ordem,
        "camadas": camadas,
        "ciclos": ciclos
    }


# ============================================================
# DFS (com detecção de ciclos e classificação de arestas)
# ============================================================
def dfs(graph, source):
    visited = set()
    ordem = []
    ciclos = []
    arestas_class = []  # (u,v,tipo)

    def dfs_visit(u, parent):
        visited.add(u)
        ordem.append(u)

        for v in graph.neighbors(u):
            if v not in visited:
                arestas_class.append((u, v, "tree"))
                dfs_visit(v, u)
            else:
                if v != parent:
                    # ciclo
                    if len(ciclos) < 5:
                        ciclos.append((u, v))
                    arestas_class.append((u, v, "back"))

    dfs_visit(source, None)

    return {
        "ordem": ordem,
        "ciclos": ciclos,
        "arestas_class": arestas_class
    }


# ============================================================
# Dijkstra (somente pesos >= 0)
# ============================================================

def dijkstra(graph, origem, destino):
    # distâncias
    dist = {v: float('inf') for v in graph.vertices()}
    dist[origem] = 0

    # pai para reconstruir o caminho
    parent = {v: None for v in graph.vertices()}

    # heap
    pq = [(0, origem)]

    while pq:
        custo_u, u = heapq.heappop(pq)

        if custo_u > dist[u]:
            continue

        # Se chegamos ao destino, podemos parar (opcional)
        if u == destino:
            break

        # NOVO FORMATO: u -> (v, peso)
        for (v, peso) in graph.neighbors(u):
            novo_custo = dist[u] + peso

            if novo_custo < dist[v]:
                dist[v] = novo_custo
                parent[v] = u
                heapq.heappush(pq, (novo_custo, v))

    # reconstruir caminho
    caminho = []
    atual = destino

    if dist[atual] == float('inf'):
        return float('inf'), []  # sem caminho

    while atual is not None:
        caminho.append(atual)
        atual = parent[atual]

    caminho.reverse()
    return dist[destino], caminho


# ============================================================
# Bellman–Ford (permite pesos negativos, detecta ciclo negativo)
# ============================================================
def bellman_ford(graph, origem):
    dist = {v: float("inf") for v in graph.vertices()}
    pai = {v: None for v in graph.vertices()}

    dist[origem] = 0.0

    V = graph.vertices()
    edges = []

    # monta lista de arestas
    for u in V:
        for aresta in graph.vizinhos(u):
            edges.append((aresta.origem, aresta.destino, aresta.peso))

    # relaxamento (|V|-1) vezes
    for _ in range(len(V) - 1):
        alterou = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pai[v] = u
                alterou = True
        if not alterou:
            break

    # verificação de ciclo negativo
    ciclo_negativo = False
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            ciclo_negativo = True
            break

    return dist, pai, ciclo_negativo