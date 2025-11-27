import json
import pandas as pd
from pathlib import Path
import os

from .graphs.io import (
    build_graph,
    normalize_name,
    SETUBAL_CANONICAL,
    SETUBAL_LABEL,
    is_setubal,
)
from .graphs.algorithms import bfs, dfs, dijkstra, bellman_ford

from .viz import (
    gerar_arvore_percurso_png,
    gerar_arvore_percurso_html,
    gerar_grafo_interativo,
    gerar_arvore_bfs,
)


def _get_parte1_path(relative_path: str) -> Path:
    """Resolve caminho relativo ao diretório parte1"""

    parte1_dir = Path(__file__).parent.parent
    return parte1_dir / relative_path


def _aplicar_rotulo_setubal(caminho: list[str], usar_rotulo_final: bool) -> list[str]:
    if usar_rotulo_final and caminho and caminho[-1] == SETUBAL_CANONICAL:
        return caminho[:-1] + [SETUBAL_LABEL]
    return caminho






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
    df = pd.read_csv(_get_parte1_path("data/bairros_unique.csv"))

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


    maior_densidade_row = df_out.loc[df_out["densidade_ego"].idxmax()]
    maior_densidade_bairro = maior_densidade_row["bairro"]
    maior_densidade_valor = maior_densidade_row["densidade_ego"]

    print("Gerado: out/ego_bairro.csv")
    print(f"Bairro mais denso: {maior_densidade_bairro} (densidade_ego = {maior_densidade_valor:.4f})")


def run_graus():
    g = build_graph()

    linhas = []
    for v in g.vertices():
        grau = len(g.neighbors(v))
        linhas.append({"bairro": v, "grau": grau})

    df_out = pd.DataFrame(linhas)
    Path("out").mkdir(exist_ok=True)
    df_out.to_csv("out/graus.csv", index=False, encoding="utf-8-sig")


    maior_grau_row = df_out.loc[df_out["grau"].idxmax()]
    maior_grau_bairro = maior_grau_row["bairro"]
    maior_grau_valor = int(maior_grau_row["grau"])

    print("Gerado: out/graus.csv")
    print(f"Bairro com maior grau: {maior_grau_bairro} (grau = {maior_grau_valor})")






def run_dist_enderecos():
    g = build_graph()

    df = pd.read_csv(_get_parte1_path("data/enderecos.csv"))
    resultados = []

    for _, row in df.iterrows():
        origem_label = row["bairro_X"]
        destino_label = row["bairro_Y"]
        origem = normalize_name(origem_label)
        destino = normalize_name(destino_label)

        dist, caminho = dijkstra(g, origem, destino)
        caminho_display = _aplicar_rotulo_setubal(caminho, is_setubal(destino_label))

        resultados.append({
            "X": row["X"],
            "Y": row["Y"],
            "bairro_X": origem_label,
            "bairro_Y": destino_label,
            "custo": dist,
            "caminho": " -> ".join(caminho_display),
        })

    df_out = pd.DataFrame(resultados)
    Path("out").mkdir(exist_ok=True)
    df_out.to_csv("out/distancias_enderecos.csv", index=False, encoding="utf-8-sig")

    print("Gerado: out/distancias_enderecos.csv")


def run_percurso_nova_descoberta_setubal():
    g = build_graph()

    origem = "Nova Descoberta"
    destino = SETUBAL_CANONICAL

    dist, caminho = dijkstra(g, origem, destino)
    caminho_display = _aplicar_rotulo_setubal(caminho, True)

    out = {
        "origem": origem,
        "destino": SETUBAL_LABEL,
        "destino_canon": destino,
        "custo": dist,
        "caminho": caminho,
        "caminho_display": caminho_display,
    }

    Path("out").mkdir(exist_ok=True)
    with open("out/percurso_nova_descoberta_setubal.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)

    print("Gerado: out/percurso_nova_descoberta_setubal.json")


def run_arvore_percurso():
    gerar_arvore_percurso_png()
    gerar_arvore_percurso_html()
    print("Gerados: out/arvore_percurso.png e out/arvore_percurso.html")


def run_grafo_interativo():
    gerar_grafo_interativo()
    print("Gerado: out/grafo_interativo.html")


def run_arvore_bfs():
    gerar_arvore_bfs()
    print("Gerados: out/arvore_bfs_boa_vista.png e out/arvore_bfs_boa_vista.html")
