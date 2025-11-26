# src/parte2_voos.py

import csv
import os
import time
import tracemalloc
from collections import Counter

import matplotlib.pyplot as plt

from src.graphs.graph import Graph, Aresta
from src.graphs.algorithms import bfs, dfs, dijkstra, bellman_ford


# Ajuste o caminho / nome do arquivo se necessário
DEFAULT_DATASET_PARTE2 = "data/dataset_parte2/voos.csv"
OUT_DIR = "out"


class DiGraph(Graph):
    """
    Grafo dirigido, reutilizando a estrutura de Graph (Parte 1),
    mas sem espelhar arestas.
    """

    def add_edge(self, u, v, peso=1.0):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(Aresta(u, v, peso))


def carregar_grafo_voos(path: str = DEFAULT_DATASET_PARTE2) -> DiGraph:
    """
    Carrega o dataset de voos.
    Espera um CSV com pelo menos as colunas: ORIGIN, DEST, DISTANCE.
    """
    g = DiGraph()

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            origem = row.get("ORIGIN") or row.get("origin")
            destino = row.get("DEST") or row.get("dest")
            dist_str = row.get("DISTANCE") or row.get("distance")

            if not origem or not destino or not dist_str:
                continue

            try:
                dist = float(dist_str)
            except ValueError:
                continue

            g.add_edge(origem, destino, dist)

    return g


def medir_tempo_memoria(func, *args, **kwargs):
    """
    Executa func(*args, **kwargs) medindo tempo e memória.
    Retorna (resultado, tempo_segundos, memoria_kb).
    """
    tracemalloc.start()
    t0 = time.perf_counter()
    resultado = func(*args, **kwargs)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tempo = t1 - t0
    mem_kb = peak / 1024.0
    return resultado, tempo, mem_kb


def calcular_grau_total(g: Graph):
    graus = {}
    for v in g.vertices():
        out_deg = len(g.vizinhos(v))
        in_deg = 0
        for u in g.vertices():
            for e in g.vizinhos(u):
                if e.destino == v:
                    in_deg += 1
        graus[v] = in_deg + out_deg
    return graus


def gerar_distribuicao_grau_voos(g: Graph, out_path: str | None = None):
    if out_path is None:
        out_path = os.path.join(OUT_DIR, "grau_distribuicao_voos.png")

    graus = calcular_grau_total(g)
    contagem = Counter(graus.values())

    xs = sorted(contagem.keys())
    ys = [contagem[x] for x in xs]

    plt.figure(figsize=(12, 5))
    plt.bar(xs, ys)
    plt.xlabel("Grau total (in+out)")
    plt.ylabel("Número de aeroportos")
    plt.title("Distribuição de graus totais (dataset de voos)")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return out_path


def rodar_analise_parte2(
    dataset_path: str = DEFAULT_DATASET_PARTE2,
    out_report: str = os.path.join(OUT_DIR, "parte2_report.json"),
):
    """
    Executa toda a análise da Parte 2:
    - carrega o grafo de voos
    - roda BFS/DFS (3 fontes)
    - roda Dijkstra (5 pares)
    - roda Bellman-Ford (2 casos sintéticos)
    - mede tempo/memória
    - gera distribuição de graus
    - salva out/parte2_report.json
    """
    import json

    os.makedirs(OUT_DIR, exist_ok=True)

    g = carregar_grafo_voos(dataset_path)

    summary = {
        "vertices": len(g.vertices()),
        "edges": sum(len(g.vizinhos(v)) for v in g.vertices()),
    }

    # ---------------- BFS / DFS ----------------
    fontes = ["EWR", "JFK", "LGA"]  # ajuste se quiser

    metrics = []

    for src in fontes:
        if src not in g.adj:
            continue

        # BFS
        (ordem_bfs, niveis_bfs, ciclos_bfs), t_bfs, mem_bfs = medir_tempo_memoria(
            bfs, g, src
        )
        metrics.append(
            {
                "task": f"BFS_{src}",
                "algorithm": "BFS",
                "source": src,
                "time_s": t_bfs,
                "memory_kb": mem_bfs,
                "nodes_explored": len(ordem_bfs),
                "layers": len(set(niveis_bfs.values())) if niveis_bfs else 0,
                "cycles_found": len(ciclos_bfs),
            }
        )

        # DFS
        (ordem_dfs, ciclos_dfs), t_dfs, mem_dfs = medir_tempo_memoria(
            dfs, g, src
        )
        metrics.append(
            {
                "task": f"DFS_{src}",
                "algorithm": "DFS",
                "source": src,
                "time_s": t_dfs,
                "memory_kb": mem_dfs,
                "nodes_explored": len(ordem_dfs),
                "cycles_found": len(ciclos_dfs),
            }
        )

    # ---------------- Dijkstra ----------------
    pares_dijkstra = [
        ("EWR", "LAX"),
        ("EWR", "SFO"),
        ("JFK", "MIA"),
        ("JFK", "LAX"),
        ("LGA", "ATL"),
    ]

    for s, t in pares_dijkstra:
        if s not in g.adj or t not in g.adj:
            continue
        (dist, caminho), td, memd = medir_tempo_memoria(dijkstra, g, s, t)
        metrics.append(
            {
                "task": f"Dijkstra_{s}_{t}",
                "algorithm": "Dijkstra",
                "source": s,
                "target": t,
                "time_s": td,
                "memory_kb": memd,
                "distance": dist,
                "path_len": len(caminho),
            }
        )

    # ---------------- Bellman-Ford ----------------
    # Casos sintéticos (como o do seu amigo)
    def bf_caso_sem_ciclo():
        vertices = ["A", "B", "C", "D"]
        edges = [
            ("A", "B", 4),
            ("A", "C", 5),
            ("C", "D", -1),
            ("B", "D", 1),
        ]
        return bellman_ford(vertices, edges, "A")

    def bf_caso_com_ciclo():
        vertices = ["P", "Q", "R"]
        edges = [
            ("P", "Q", 1),
            ("Q", "R", -3),
            ("R", "P", 1),
        ]
        return bellman_ford(vertices, edges, "P")

    (dist1, neg_cycle1), t1, m1 = medir_tempo_memoria(bf_caso_sem_ciclo)
    metrics.append(
        {
            "task": "BellmanFord_sem_ciclo",
            "algorithm": "Bellman-Ford",
            "case": "sem_ciclo_negativo",
            "time_s": t1,
            "memory_kb": m1,
            "negative_cycle": neg_cycle1,
            "distances": dist1,
        }
    )

    (dist2, neg_cycle2), t2, m2 = medir_tempo_memoria(bf_caso_com_ciclo)
    metrics.append(
        {
            "task": "BellmanFord_com_ciclo",
            "algorithm": "Bellman-Ford",
            "case": "com_ciclo_negativo",
            "time_s": t2,
            "memory_kb": m2,
            "negative_cycle": neg_cycle2,
            "distances": dist2,
        }
    )

    # ---------------- Visualização ----------------
    vis_path = gerar_distribuicao_grau_voos(g)

    discussion = (
        "BFS/DFS são úteis para entender alcance e camadas a partir de aeroportos fonte "
        "(EWR, JFK, LGA). Dijkstra usa a distância como peso (sempre ≥ 0) para obter "
        "rotas mínimas entre pares de aeroportos. Bellman-Ford permite trabalhar com "
        "pesos negativos; aqui usamos grafos sintéticos para demonstrar um caso sem "
        "ciclo negativo (distâncias bem definidas) e um com ciclo negativo (flag de "
        "detecção). A modelagem usa apenas a menor distância por par origem-destino, "
        "ignorando frequência de voos, atrasos e horários, o que simplifica o grafo "
        "mas perde aspectos importantes da dinâmica real."
    )

    report = {
        "summary": summary,
        "metrics": metrics,
        "visualizations": [
            {
                "type": "degree_distribution",
                "file": os.path.basename(vis_path),
                "description": "Distribuição de graus totais (in+out) dos aeroportos.",
            }
        ],
        "discussion": discussion,
    }

    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Relatório da Parte 2 salvo em {out_report}")
