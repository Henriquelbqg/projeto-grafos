


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

        for v, _ in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                camadas[v] = camadas[u] + 1
                queue.append(v)
            else:

                if len(ciclos) < 5 and v != source:
                    ciclos.append((u, v))

    return {
        "ordem": ordem,
        "camadas": camadas,
        "ciclos": ciclos
    }





def dfs(graph, source):
    visited = set()
    ordem = []
    ciclos = []
    arestas_class = []

    def dfs_visit(u, parent):
        visited.add(u)
        ordem.append(u)

        for v, _ in graph.neighbors(u):
            if v not in visited:
                arestas_class.append((u, v, "tree"))
                dfs_visit(v, u)
            else:
                if v != parent:

                    if len(ciclos) < 5:
                        ciclos.append((u, v))
                    arestas_class.append((u, v, "back"))

    dfs_visit(source, None)

    return {
        "ordem": ordem,
        "ciclos": ciclos,
        "arestas_class": arestas_class
    }







def dijkstra(graph, origem, destino):
    """Calcula caminho mínimo com pesos não negativos."""

    dist = {v: float('inf') for v in graph.vertices()}
    dist[origem] = 0

    parent = {v: None for v in graph.vertices()}

    nao_visitados = set(graph.vertices())

    while nao_visitados:

        u = None
        menor_dist = float('inf')
        for v in nao_visitados:
            if dist[v] < menor_dist:
                menor_dist = dist[v]
                u = v

        if u is None or menor_dist == float('inf'):
            break

        nao_visitados.remove(u)

        if u == destino:
            break

        for (v, peso) in graph.neighbors(u):
            if peso < 0:
                raise ValueError("Dijkstra não aceita pesos negativos.")
            if v not in nao_visitados:
                continue

            novo_custo = dist[u] + peso

            if novo_custo < dist[v]:
                dist[v] = novo_custo
                parent[v] = u

    caminho = []
    atual = destino

    if dist[atual] == float('inf'):
        return float('inf'), []

    while atual is not None:
        caminho.append(atual)
        atual = parent[atual]

    caminho.reverse()
    return dist[destino], caminho





def bellman_ford(graph, origem):
    dist = {v: float("inf") for v in graph.vertices()}
    pai = {v: None for v in graph.vertices()}

    dist[origem] = 0.0

    V = graph.vertices()
    edges = []


    for u in V:
        for (v, peso) in graph.neighbors(u):
            edges.append((u, v, peso))


    for _ in range(len(V) - 1):
        alterou = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pai[v] = u
                alterou = True
        if not alterou:
            break


    ciclo_negativo = False
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            ciclo_negativo = True
            break

    return dist, pai, ciclo_negativo