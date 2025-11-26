from collections import deque
import math
import heapq

# ============================================================
# BFS — Dataset grande (não assume que é pequeno nem denso)
# ============================================================

def bfs_large(graph, source):
    """
    BFS otimizada para o dataset grande.
    Retorna ordem de visita e distâncias em camadas.
    """
    visited = set()
    dist = {}
    order = []

    q = deque([source])
    visited.add(source)
    dist[source] = 0

    while q:
        u = q.popleft()
        order.append(u)

        for (v, _) in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                dist[v] = dist[u] + 1
                q.append(v)

    return order, dist


# ============================================================
# DFS — Dataset grande
# ============================================================

def dfs_large(graph, source):
    """
    DFS iterativa para grafos grandes.
    Retorna ordem de visita e detecção de ciclos.
    """
    visited = set()
    stack = [(source, None)]
    parent = {}
    has_cycle = False
    order = []

    while stack:
        u, p = stack.pop()

        if u not in visited:
            visited.add(u)
            parent[u] = p
            order.append(u)

            for (v, _) in graph.neighbors(u):
                if v not in visited:
                    stack.append((v, u))
                elif v != p:
                    # ciclo encontrado
                    has_cycle = True

    return order, has_cycle


# ============================================================
# Dijkstra — Dataset grande (recusa pesos negativos)
# ============================================================

def dijkstra_large(graph, source, target=None):
    """
    Dijkstra para grafos grandes (Parte 2).
    Recusa pesos negativos.
    """
    # verificação de peso negativo
    for (u, v, w) in graph.edges():
        if w < 0:
            raise ValueError("Dijkstra não permite pesos negativos.")

    dist = {v: math.inf for v in graph.vertices()}
    parent = {v: None for v in graph.vertices()}
    dist[source] = 0

    pq = [(0, source)]  # (distância, nó)

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        if target and u == target:
            break

        for (v, w) in graph.neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, parent


# ============================================================
# Bellman-Ford — Dataset grande (detecta ciclo negativo)
# ============================================================

def bellman_ford_large(graph, source):
    """
    Bellman-Ford completo com detecção de ciclos negativos.
    """
    dist = {v: math.inf for v in graph.vertices()}
    parent = {v: None for v in graph.vertices()}
    dist[source] = 0

    V = graph.vertices()
    E = graph.edges()

    # relaxação |V|-1 vezes
    for _ in range(len(V) - 1):
        updated = False
        for (u, v, w) in E:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break

    # detecção de ciclo negativo
    for (u, v, w) in E:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            return dist, parent, True  # ciclo negativo encontrado

    return dist, parent, False
