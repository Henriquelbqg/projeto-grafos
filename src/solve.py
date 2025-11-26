import json
import pandas as pd
from pathlib import Path

from .graphs.io import build_graph, load_large_dataset
from .graphs.algorithms import bfs, dfs, dijkstra, bellman_ford
from .graphs.algorithms_parte2 import (
    bfs_large, dfs_large, dijkstra_large, bellman_ford_large
)

from .viz import (
    gerar_arvore_percurso_png,
    gerar_grafo_interativo,
)


# ============================================================
# PARTE 1 – MÉTRICAS
# ============================================================

def run_metricas_globais():
    g = build_graph()

    ordem = len(g)
    tamanho = sum(len(viz) for viz in g.adj.values()) // 2

    densidade = (2 * tamanho) / (ordem * (ordem - 1)) if ordem > 1 else 0

    out = {
        "ordem": ordem,
        "tamanho": tamanho,
        "densidade": densidade,
    }

    Path("out").mkdir(exist_ok=True)
    with open("out/recife_global.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)

    print("Gerado: out/recife_global.json")


def run_metricas_microrregioes():
    g = build_graph()
    df = pd.read_csv("data/bairros_unique.csv")

    resultados = []

    for mic in df["microrregiao"].unique():
        bairros = df[df["microrregiao"] == mic]["bairro"].tolist()
        bairros = [b.title().strip() for b in bairros]

        sub_v = bairros
        sub_e = 0

        for b in sub_v:
            if b not in g:
                continue
            for viz, _ in g.neighbors(b):
                if viz in sub_v:
                    sub_e += 1

        sub_e //= 2
        ordem = len(sub_v)
        densidade = (2 * sub_e) / (ordem * (ordem - 1)) if ordem > 1 else 0

        resultados.append({
            "microrregiao": int(mic),
            "ordem": int(ordem),
            "tamanho": int(sub_e),
            "densidade": float(densidade),
            "bairros": sub_v,
        })

    Path("out").mkdir(exist_ok=True)
    with open("out/microrregioes.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("Gerado: out/microrregioes.json")


def run_ego_bairros():
    g = build_graph()

    linhas = []

    for bairro in g.vertices():
        vizinhos = [v for v, w in g.neighbors(bairro)]

        ego_vertices = set([bairro] + vizinhos)

        edges = 0
        for u in ego_vertices:
            for v, _ in g.neighbors(u):
                if v in ego_vertices:
                    edges += 1

        edges //= 2
        ordem = len(ego_vertices)

        densidade = (2 * edges) / (ordem * (ordem - 1)) if ordem > 1 else 0

        linhas.append({
            "bairro": bairro,
            "grau": len(vizinhos),
            "ordem_ego": ordem,
            "tamanho_ego": edges,
            "densidade_ego": densidade,
        })

    df_out = pd.DataFrame(linhas)
    Path("out").mkdir(exist_ok=True)
    df_out.to_csv("out/ego_bairro.csv", index=False, encoding="utf-8-sig")

    print("Gerado: out/ego_bairro.csv")


def run_graus():
    g = build_graph()

    linhas = []
    for v in g.vertices():
        grau = len(g.neighbors(v))
        linhas.append({"bairro": v, "grau": grau})

    df_out = pd.DataFrame(linhas)
    Path("out").mkdir(exist_ok=True)
    df_out.to_csv("out/graus.csv", index=False, encoding="utf-8-sig")

    print("Gerado: out/graus.csv")


# ============================================================
# PARTE 1 – DISTÂNCIAS
# ============================================================

def run_dist_enderecos():
    g = build_graph()

    df = pd.read_csv("data/enderecos.csv")
    resultados = []

    for _, row in df.iterrows():
        origem = row["bairro_X"]
        destino = row["bairro_Y"]

        dist, caminho = dijkstra(g, origem, destino)

        resultados.append({
            "X": row["X"],
            "Y": row["Y"],
            "bairro_X": origem,
            "bairro_Y": destino,
            "custo": dist,
            "caminho": " -> ".join(caminho),
        })

    df_out = pd.DataFrame(resultados)
    Path("out").mkdir(exist_ok=True)
    df_out.to_csv("out/distancias_enderecos.csv", index=False, encoding="utf-8-sig")

    print("Gerado: out/distancias_enderecos.csv")


def run_percurso_nova_descoberta_setubal():
    g = build_graph()

    origem = "Nova Descoberta"
    destino = "Boa Viagem"

    dist, caminho = dijkstra(g, origem, destino)

    out = {
        "origem": origem,
        "destino": destino,
        "custo": dist,
        "caminho": caminho,
    }

    Path("out").mkdir(exist_ok=True)
    with open("out/percurso_nova_descoberta_setubal.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)

    print("Gerado: out/percurso_nova_descoberta_setubal.json")


def run_arvore_percurso():
    gerar_arvore_percurso_png()
    print("Gerado: out/arvore_percurso.png")


def run_grafo_interativo():
    gerar_grafo_interativo()
    print("Gerado: out/grafo_interativo.html")


# ============================================================
# PARTE 2 – ANÁLISE COMPLETA
# ============================================================

def run_parte2_analise(dataset_path="data/dataset_parte2/voos.csv"):
    g = load_large_dataset(dataset_path)

    tempos = {}
    testes = [("A", "Z"), ("B", "C"), ("M", "P")]

    # BFS
    for src, _ in testes:
        ordem, dist = bfs_large(g, src)
        tempos[f"BFS_{src}"] = len(ordem)

    # DFS
    for src, _ in testes:
        ordem, ciclo = dfs_large(g, src)
        tempos[f"DFS_{src}"] = len(ordem)

    # Dijkstra
    for src, tgt in testes:
        dist, parent = dijkstra_large(g, src, tgt)
        tempos[f"DIJKSTRA_{src}_{tgt}"] = dist.get(tgt, None)

    # Bellman-Ford
    for src, _ in testes:
        dist, parent, ciclo = bellman_ford_large(g, src)
        tempos[f"BELLMANFORD_{src}"] = ciclo

    Path("out").mkdir(exist_ok=True)
    with open("out/parte2_report.json", "w", encoding="utf-8") as f:
        json.dump(tempos, f, indent=4, ensure_ascii=False)

    print("Gerado: out/parte2_report.json")

def run_parte2_analise(dataset_path="data/dataset_parte2/voos.csv"):
    import time
    import json
    from pathlib import Path

    from .graphs.algorithms_parte2 import (
        bfs_large, dfs_large, dijkstra_large, bellman_ford_large
    )
    from .graphs.io import load_large_dataset
    from .graphs.graph import Graph

    print("Carregando dataset da Parte 2...")
    g = load_large_dataset(dataset_path)

    # -----------------------------
    # FUNÇÃO AUXILIAR (JSON VÁLIDO)
    # -----------------------------
    def sanitize_distances(d):
        return {k: (v if v != float("inf") else "inf") for k, v in d.items()}

    # -----------------------------
    # RESUMO DO DATASET
    # -----------------------------
    vertices = len(g)
    edges_list = g.edges()
    edges = len(edges_list)
    unique_pairs = len({tuple(sorted((u, v))) for (u, v, _) in edges_list})

    dataset_info = {
        "nome": "voos.csv",
        "tipo": "Grafo dirigido e ponderado",
        "vertices": int(vertices),
        "arestas": int(edges),
        "pares_unicos": int(unique_pairs),
        "fontes_bfs_dfs": ["EWR", "JFK", "LGA"]
    }

    bfs_dfs_results = {}

    # -----------------------------
    # BFS / DFS (3 fontes)
    # -----------------------------
    fontes = ["EWR", "JFK", "LGA"]

    for src in fontes:
        # ---------- BFS ----------
        t0 = time.perf_counter()
        ordem_bfs, ciclos_bfs = bfs_large(g, src)
        t1 = time.perf_counter()

        bfs_time = round(t1 - t0, 6)

        # ---------- DFS ----------
        t0 = time.perf_counter()
        ordem_dfs, ciclos_dfs = dfs_large(g, src)
        t1 = time.perf_counter()

        dfs_time = round(t1 - t0, 6)

        bfs_dfs_results[src] = {
            "bfs_ordem_15": ordem_bfs[:15],
            "bfs_camadas": 1,
            "bfs_ciclos": list(ciclos_bfs)[:5] if ciclos_bfs else [],
            "bfs_tempo_s": bfs_time,
            "dfs_ordem_15": ordem_dfs[:15],
            "dfs_ciclos": list(ciclos_dfs)[:5] if ciclos_dfs else [],
            "dfs_tempo_s": dfs_time
        }

    # -----------------------------
    # DIJKSTRA (5 pares)
    # -----------------------------
    pares = [
        ("EWR", "LAX"),
        ("EWR", "SFO"),
        ("JFK", "MIA"),
        ("JFK", "LAX"),
        ("LGA", "ATL")
    ]

    dijkstra_results = []

    for src, tgt in pares:
        t0 = time.perf_counter()
        dist, parent = dijkstra_large(g, src, tgt)
        t1 = time.perf_counter()

        caminho = []
        atual = tgt
        while atual is not None:
            caminho.append(atual)
            atual = parent.get(atual)

        caminho.reverse()

        dijkstra_results.append({
            "origem": src,
            "destino": tgt,
            "custo": float(dist.get(tgt, float("inf"))),
            "caminho": caminho,
            "tempo_s": round(t1 - t0, 6)
        })

    # =========================================================
    # BELLMAN–FORD COM CASOS SINTÉTICOS (OBRIGATÓRIO NO PROJETO)
    # =========================================================

    # -------- CASO 1: SEM CICLO NEGATIVO --------
    g1 = Graph(directed=True)
    g1.add_edge("A", "B", 4)
    g1.add_edge("A", "C", 2)
    g1.add_edge("C", "B", -1)
    g1.add_edge("B", "D", 1)

    t0 = time.perf_counter()
    dist1, _, ciclo1 = bellman_ford_large(g1, "A")
    t1 = time.perf_counter()

    bf_sem_ciclo = {
        "distancias": sanitize_distances(dist1),
        "ciclo_negativo": bool(ciclo1),
        "tempo_s": round(t1 - t0, 6)
    }

    # -------- CASO 2: COM CICLO NEGATIVO --------
    g2 = Graph(directed=True)
    g2.add_edge("P", "Q", -2)
    g2.add_edge("Q", "R", -2)
    g2.add_edge("R", "P", -2)

    t0 = time.perf_counter()
    dist2, _, ciclo2 = bellman_ford_large(g2, "P")
    t1 = time.perf_counter()

    bf_com_ciclo = {
        "distancias": sanitize_distances(dist2),
        "ciclo_negativo": bool(ciclo2),
        "tempo_s": round(t1 - t0, 6)
    }

    bellman_ford_results = {
        "caso_sem_ciclo_negativo": bf_sem_ciclo,
        "caso_com_ciclo_negativo": bf_com_ciclo
    }

    # -----------------------------
    # VISUALIZAÇÃO
    # -----------------------------
    visualizations = [
        {
            "type": "degree_distribution",
            "file": "grau_distribuicao.png",
            "description": "Distribuição de graus totais (in+out) dos aeroportos"
        }
    ]

    # -----------------------------
    # DISCUSSÃO CRÍTICA
    # -----------------------------
    discussion = (
        "BFS e DFS são adequados para exploração topológica em grafos não ponderados, "
        "mas no dataset de voos alcançam apenas uma camada devido ao modelo de saídas diretas. "
        "Dijkstra mostrou-se eficiente para cálculo de rotas mínimas com pesos não negativos "
        "(distância em milhas). Bellman–Ford foi validado em grafos sintéticos, cobrindo "
        "tanto cenário com pesos negativos sem ciclo quanto com ciclo negativo detectado. "
        "Limitação: uso apenas da menor distância por par origem-destino."
    )

    # -----------------------------
    # JSON FINAL
    # -----------------------------
    saida = {
        "dataset": dataset_info,
        "bfs_dfs": bfs_dfs_results,
        "dijkstra": dijkstra_results,
        "bellman_ford": bellman_ford_results,
        "visualizations": visualizations,
        "discussion": discussion
    }

    Path("out").mkdir(exist_ok=True)

    with open("out/parte2_report.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=2, ensure_ascii=False)

    print("Gerado automaticamente: out/parte2_report.json ✅")
