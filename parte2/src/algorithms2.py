

import csv
import os
import sys
import time
import tracemalloc
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "parte1" / "src"))

from graphs.graph import Graph
from graphs.algorithms import bfs, dfs, dijkstra, bellman_ford



DEFAULT_DATASET_PARTE2 = "data/voos.csv"
OUT_DIR = "out"


class DiGraph(Graph):
    """
    Grafo dirigido, reutilizando a estrutura de Graph (Parte 1),
    mas sem espelhar arestas.
    """

    def __init__(self):
        super().__init__(directed=True)

    def add_edge(self, u, v, peso=1.0):
        self.add_vertex(u)
        self.add_vertex(v)

        super().add_edge(u, v, peso, directed=True)


def carregar_grafo_voos(path: str = DEFAULT_DATASET_PARTE2) -> DiGraph:
    """
    Carrega o dataset de voos.
    Espera um CSV com pelo menos as colunas: ORIGIN, DEST, DISTANCE.
    """
    g = DiGraph()


    if not os.path.isabs(path):
        base_path = Path(__file__).parent.parent.parent / "parte2"
        path = str(base_path / path)

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

        out_deg = len(g.neighbors(v))

        in_deg = 0
        for u in g.vertices():
            for (viz, _) in g.neighbors(u):
                if viz == v:
                    in_deg += 1
        graus[v] = in_deg + out_deg
    return graus


def gerar_distribuicao_grau_voos(g: Graph, out_path: str | None = None):
    if out_path is None:
        base_path = Path(__file__).parent.parent.parent / "parte2"
        out_path = str(base_path / OUT_DIR / "grau_distribuicao.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

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


def gerar_top_hubs_voos(g: Graph, top_n: int = 15, out_path: str | None = None):
    """
    Cria um gráfico de barras horizontais com os aeroportos de maior grau total.
    """
    if out_path is None:
        base_path = Path(__file__).parent.parent.parent / "parte2"
        out_path = str(base_path / OUT_DIR / "top_hubs_grau.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    graus = calcular_grau_total(g)
    ranking = sorted(graus.items(), key=lambda item: item[1], reverse=True)[:top_n]

    labels = [item[0] for item in ranking][::-1]
    valores = [item[1] for item in ranking][::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, valores, color="#0077b6")
    plt.xlabel("Grau total (in+out)")
    plt.ylabel("Aeroporto")
    plt.title(f"Top {top_n} aeroportos com maior grau total")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return out_path


def gerar_histograma_distancias_voos(g: Graph, out_path: str | None = None):
    """
    Histograma da distribuição de distâncias (pesos) das arestas do grafo de voos.
    """
    if out_path is None:
        base_path = Path(__file__).parent.parent.parent / "parte2"
        out_path = str(base_path / OUT_DIR / "histograma_distancias.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    distancias = []
    vistos = set()
    for origem in g.vertices():
        for destino, peso in g.neighbors(origem):
            chave = (origem, destino, peso)
            if chave in vistos:
                continue
            vistos.add(chave)
            distancias.append(peso)

    if not distancias:
        return out_path

    plt.figure(figsize=(10, 5))
    plt.hist(distancias, bins=30, color="#ff7f0e", edgecolor="black")
    plt.xlabel("Distância (milhas)")
    plt.ylabel("Número de rotas")
    plt.title("Distribuição das distâncias entre aeroportos")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return out_path


def gerar_disp_grau_in_out_voos(g: Graph, out_path: str | None = None):
    """
    Gera um gráfico de dispersão mostrando grau de saída vs grau de entrada.
    """
    if out_path is None:
        base_path = Path(__file__).parent.parent.parent / "parte2"
        out_path = str(base_path / OUT_DIR / "grau_in_out_scatter.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    vertices = list(g.vertices())
    in_deg = {v: 0 for v in vertices}
    out_deg = {v: len(g.neighbors(v)) for v in vertices}

    for origem in vertices:
        for destino, _ in g.neighbors(origem):
            in_deg[destino] = in_deg.get(destino, 0) + 1

    xs = [out_deg[v] for v in vertices]
    ys = [in_deg[v] for v in vertices]
    tamanhos = [(in_deg[v] + out_deg[v]) * 5 for v in vertices]

    plt.figure(figsize=(8, 6))
    plt.scatter(xs, ys, s=tamanhos, alpha=0.7, color="#2a9d8f", edgecolors="black", linewidths=0.5)
    plt.xlabel("Grau de saída")
    plt.ylabel("Grau de entrada")
    plt.title("Correlação entre grau de saída e grau de entrada")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return out_path


def gerar_top_rotas_distantes(g: Graph, top_n: int = 10, out_path: str | None = None):
    """
    Gera gráfico com as rotas mais longas em milhas.
    """
    if out_path is None:
        base_path = Path(__file__).parent.parent.parent / "parte2"
        out_path = str(base_path / OUT_DIR / "top_rotas_distantes.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    rotas = []
    for origem in g.vertices():
        for destino, peso in g.neighbors(origem):
            rotas.append((origem, destino, peso))

    if not rotas:
        return out_path

    rotas = sorted(rotas, key=lambda item: item[2], reverse=True)[:top_n]
    labels = [f"{o} → {d}" for o, d, _ in rotas][::-1]
    valores = [peso for _, _, peso in rotas][::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, valores, color="#f94144")
    plt.xlabel("Distância (milhas)")
    plt.ylabel("Rota")
    plt.title(f"Top {top_n} rotas mais longas do dataset")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    return out_path


def rodar_analise_parte2(
    dataset_path: str = DEFAULT_DATASET_PARTE2,
    out_report: str | None = None,
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

    base_path = Path(__file__).parent.parent.parent / "parte2"

    if out_report is None:
        out_report = str(base_path / OUT_DIR / "parte2_report.json")
    else:
        if not os.path.isabs(out_report):
            out_report = str(base_path / out_report)

    os.makedirs(os.path.dirname(out_report), exist_ok=True)

    g = carregar_grafo_voos(dataset_path)


    graus = calcular_grau_total(g)
    graus_valores = list(graus.values())


    pares_unicos = set()
    for v in g.vertices():
        for viz, _ in g.neighbors(v):
            pares_unicos.add((v, viz))

    summary = {
        "nome": os.path.basename(dataset_path),
        "tipo": "Grafo dirigido e ponderado",
        "vertices": len(g.vertices()),
        "arestas": sum(len(g.neighbors(v)) for v in g.vertices()),
        "pares_unicos": len(pares_unicos),
        "fontes_bfs_dfs": ["EWR", "JFK", "LGA"],
        "distribuicao_graus": {
            "min": min(graus_valores) if graus_valores else 0,
            "max": max(graus_valores) if graus_valores else 0,
            "media": round(sum(graus_valores) / len(graus_valores), 2) if graus_valores else 0,
            "mediana": sorted(graus_valores)[len(graus_valores) // 2] if graus_valores else 0,
        }
    }


    fontes = ["EWR", "JFK", "LGA"]

    metrics = []
    bfs_dfs_data = {}

    for src in fontes:
        if src not in g.adj:
            continue


        resultado_bfs, t_bfs, mem_bfs = medir_tempo_memoria(bfs, g, src)
        ordem_bfs = resultado_bfs.get("ordem", [])
        niveis_bfs = resultado_bfs.get("camadas", {})
        ciclos_bfs = resultado_bfs.get("ciclos", [])


        if src not in bfs_dfs_data:
            bfs_dfs_data[src] = {}
        bfs_dfs_data[src]["bfs_ordem_15"] = ordem_bfs[:15]
        bfs_dfs_data[src]["bfs_camadas"] = len(set(niveis_bfs.values())) if niveis_bfs else 0
        bfs_dfs_data[src]["bfs_ciclos"] = ciclos_bfs[:5]
        bfs_dfs_data[src]["bfs_tempo_s"] = round(t_bfs, 6)

        metrics.append(
            {
                "task": f"BFS_{src}",
                "algorithm": "BFS",
                "source": src,
                "time_s": round(t_bfs, 6),
                "memory_kb": round(mem_bfs, 2),
                "nodes_explored": len(ordem_bfs),
                "layers": len(set(niveis_bfs.values())) if niveis_bfs else 0,
                "cycles_found": len(ciclos_bfs),
            }
        )


        resultado_dfs, t_dfs, mem_dfs = medir_tempo_memoria(dfs, g, src)
        ordem_dfs = resultado_dfs.get("ordem", [])
        ciclos_dfs = resultado_dfs.get("ciclos", [])


        bfs_dfs_data[src]["dfs_ordem_15"] = ordem_dfs[:15]
        bfs_dfs_data[src]["dfs_ciclos"] = ciclos_dfs
        bfs_dfs_data[src]["dfs_tempo_s"] = round(t_dfs, 6)

        metrics.append(
            {
                "task": f"DFS_{src}",
                "algorithm": "DFS",
                "source": src,
                "time_s": round(t_dfs, 6),
                "memory_kb": round(mem_dfs, 2),
                "nodes_explored": len(ordem_dfs),
                "cycles_found": len(ciclos_dfs),
            }
        )


    pares_dijkstra = [
        ("EWR", "LAX"),
        ("EWR", "SFO"),
        ("JFK", "MIA"),
        ("JFK", "LAX"),
        ("LGA", "ATL"),
    ]

    dijkstra_data = []

    for s, t in pares_dijkstra:
        if s not in g.adj or t not in g.adj:
            continue


        resultado_dijkstra, td, mem_dijkstra = medir_tempo_memoria(dijkstra, g, s, t)
        dist, caminho = resultado_dijkstra


        dijkstra_data.append({
            "origem": s,
            "destino": t,
            "custo": dist if dist != float('inf') else None,
            "caminho": caminho,
            "tempo_s": round(td, 6),
            "memoria_kb": round(mem_dijkstra, 2)
        })

        metrics.append(
            {
                "task": f"Dijkstra_{s}_{t}",
                "algorithm": "Dijkstra",
                "source": s,
                "target": t,
                "time_s": round(td, 6),
                "memory_kb": round(mem_dijkstra, 2),
                "distance": dist if dist != float('inf') else None,
                "path_len": len(caminho),
            }
        )



    def bf_caso_sem_ciclo():
        g1 = Graph(directed=True)
        g1.add_edge("A", "B", 4, directed=True)
        g1.add_edge("A", "C", 5, directed=True)
        g1.add_edge("C", "D", -1, directed=True)
        g1.add_edge("B", "D", 1, directed=True)
        return bellman_ford(g1, "A")

    def bf_caso_com_ciclo():
        g2 = Graph(directed=True)
        g2.add_edge("P", "Q", 1, directed=True)
        g2.add_edge("Q", "R", -3, directed=True)
        g2.add_edge("R", "P", 1, directed=True)
        return bellman_ford(g2, "P")

    dist1, pai1, neg_cycle1 = bf_caso_sem_ciclo()
    t0 = time.perf_counter()
    bf_caso_sem_ciclo()
    t1 = time.perf_counter()

    bellman_ford_data = {}
    bellman_ford_data["caso_sem_ciclo_negativo"] = {
        "distancias": {k: (v if v != float("inf") else "inf") for k, v in dist1.items()},
        "ciclo_negativo": neg_cycle1,
        "tempo_s": round(t1 - t0, 6)
    }

    metrics.append(
        {
            "task": "BellmanFord_sem_ciclo",
            "algorithm": "Bellman-Ford",
            "case": "sem_ciclo_negativo",
            "time_s": round(t1 - t0, 6),
            "memory_kb": 0,
            "negative_cycle": neg_cycle1,
            "distances": {k: (v if v != float("inf") else "inf") for k, v in dist1.items()},
        }
    )

    dist2, pai2, neg_cycle2 = bf_caso_com_ciclo()
    t0 = time.perf_counter()
    bf_caso_com_ciclo()
    t1 = time.perf_counter()

    bellman_ford_data["caso_com_ciclo_negativo"] = {
        "distancias": {k: (v if v != float("inf") else "inf") for k, v in dist2.items()},
        "ciclo_negativo": neg_cycle2,
        "tempo_s": round(t1 - t0, 6)
    }

    metrics.append(
        {
            "task": "BellmanFord_com_ciclo",
            "algorithm": "Bellman-Ford",
            "case": "com_ciclo_negativo",
            "time_s": round(t1 - t0, 6),
            "memory_kb": 0,
            "negative_cycle": neg_cycle2,
            "distances": {k: (v if v != float("inf") else "inf") for k, v in dist2.items()},
        }
    )


    vis_distribuicao = gerar_distribuicao_grau_voos(g)
    vis_top_hubs = gerar_top_hubs_voos(g)
    vis_hist_dist = gerar_histograma_distancias_voos(g)
    vis_scatter = gerar_disp_grau_in_out_voos(g)
    vis_rotas = gerar_top_rotas_distantes(g)

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
        "dataset": summary,
        "bfs_dfs": bfs_dfs_data,
        "dijkstra": dijkstra_data,
        "bellman_ford": bellman_ford_data,
        "metricas_desempenho": metrics,
        "visualizations": [
            {
                "type": "degree_distribution",
                "file": os.path.basename(vis_distribuicao),
                "description": "Distribuição de graus totais (in+out) dos aeroportos"
            },
            {
                "type": "top_hubs",
                "file": os.path.basename(vis_top_hubs),
                "description": "Top aeroportos com maior grau total"
            },
            {
                "type": "distance_histogram",
                "file": os.path.basename(vis_hist_dist),
                "description": "Histograma das distâncias (pesos) das rotas"
            },
            {
                "type": "in_out_scatter",
                "file": os.path.basename(vis_scatter),
                "description": "Dispersão grau de saída vs grau de entrada"
            },
            {
                "type": "longest_routes",
                "file": os.path.basename(vis_rotas),
                "description": "Top rotas mais longas em milhas"
            },
        ],
        "discussion": discussion,
    }

    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Relatório da Parte 2 salvo em {out_report}")

    return {
        "report_path": out_report,
        "visualizations": [
            vis_distribuicao,
            vis_top_hubs,
            vis_hist_dist,
            vis_scatter,
            vis_rotas,
        ],
    }
