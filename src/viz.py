import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


# ============================================================
# UTIL
# ============================================================

def _ensure_out():
    os.makedirs("out", exist_ok=True)


# ============================================================
# VISUALIZAÇÕES – PARTE 1
# ============================================================

def gerar_distribuicao_graus():
    """
    Lê out/graus.csv e gera um histograma da distribuição dos graus.
    Salva em out/distribuicao_graus.png
    """
    _ensure_out()

    df = pd.read_csv("out/graus.csv", encoding="utf-8")

    plt.figure(figsize=(8, 6))
    max_grau = df["grau"].max()
    bins = range(0, max_grau + 2)

    plt.hist(df["grau"], bins=bins, edgecolor="black", align="left")
    plt.xlabel("Grau do bairro")
    plt.ylabel("Quantidade de bairros")
    plt.title("Distribuição dos Graus dos Bairros")
    plt.xticks(list(bins))

    plt.tight_layout()
    plt.savefig("out/distribuicao_graus.png", dpi=300)
    plt.close()

    print("Gerado: out/distribuicao_graus.png")


def gerar_top10_grau():
    """
    Gera gráfico de barras com os 10 bairros de maior grau.
    Salva em out/top10_grau.png
    """
    _ensure_out()

    df = pd.read_csv("out/graus.csv", encoding="utf-8")
    top10 = df.sort_values("grau", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(top10["bairro"], top10["grau"])
    plt.xlabel("Bairro")
    plt.ylabel("Grau")
    plt.title("Top 10 Bairros por Grau")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig("out/top10_grau.png", dpi=300)
    plt.close()

    print("Gerado: out/top10_grau.png")


def gerar_densidade_ego_microrregiao():
    """
    Calcula média da densidade_ego por microrregião e gera gráfico de barras.
    Salva em out/densidade_ego_microrregiao.png
    """
    _ensure_out()

    df_ego = pd.read_csv("out/ego_bairro.csv", encoding="utf-8")
    df_bairros = pd.read_csv("data/bairros_unique.csv", encoding="utf-8")

    df = df_ego.merge(df_bairros, on="bairro", how="left")

    medias = (
        df.groupby("microrregiao")["densidade_ego"]
        .mean()
        .reset_index()
        .sort_values("microrregiao")
    )

    plt.figure(figsize=(8, 6))
    plt.bar(medias["microrregiao"].astype(str), medias["densidade_ego"])
    plt.xlabel("Microrregião")
    plt.ylabel("Média da densidade_ego")
    plt.title("Densidade Média da Ego-Rede por Microrregião")

    plt.tight_layout()
    plt.savefig("out/densidade_ego_microrregiao.png", dpi=300)
    plt.close()

    print("Gerado: out/densidade_ego_microrregiao.png")


# ============================================================
# ÁRVORE DO PERCURSO — PNG
# ============================================================

def gerar_arvore_percurso_png():
    """
    Gera a árvore do percurso ND → Boa Viagem (Setúbal) em PNG estático,
    com layout orgânico (spring) e tamanho pensado para caber na tela.
    """
    _ensure_out()

    # Lê o caminho calculado pelo Dijkstra
    with open("out/percurso_nova_descoberta_setubal.json", encoding="utf-8") as f:
        dados = json.load(f)

    caminho = dados["caminho"]

    # Grafo caminho (árvore)
    G = nx.Graph()
    for b in caminho:
        G.add_node(b)

    for i in range(len(caminho) - 1):
        G.add_edge(caminho[i], caminho[i + 1])

    # Layout orgânico (spring), mas controlado
    # k controla o espaçamento entre os nós
    pos = nx.spring_layout(G, seed=42, k=0.6, iterations=100)

    # Figura mais larga que alta → boa para monitor
    plt.figure(figsize=(8, 4))  # antes era maior

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color="#ffcccc")
    nx.draw_networkx_edges(G, pos, width=3, edge_color="#ff0000")
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    plt.title("Árvore do Percurso: Nova Descoberta → Boa Viagem (Setúbal)")
    plt.axis("off")

    # Margens pequenas para não “esticar” demais a figura
    plt.margins(0.1)

    plt.tight_layout()
    plt.savefig("out/arvore_percurso.png", dpi=120)
    plt.close()

    print("Gerado: out/arvore_percurso.png")



# ============================================================
# GRAFO INTERATIVO (pyvis)
# ============================================================

def gerar_grafo_interativo():
    """
    Gera um HTML interativo completo em out/grafo_interativo.html
    """
    from pyvis.network import Network

    _ensure_out()

    df_bairros = pd.read_csv("data/bairros_unique.csv", encoding="utf-8")
    df_graus = pd.read_csv("out/graus.csv", encoding="utf-8")
    df_ego = pd.read_csv("out/ego_bairro.csv", encoding="utf-8")
    df_adj = pd.read_csv("data/adjacencias_bairros.csv", encoding="utf-8")

    mic = dict(zip(df_bairros["bairro"], df_bairros["microrregiao"]))
    graus = dict(zip(df_graus["bairro"], df_graus["grau"]))
    dens = dict(zip(df_ego["bairro"], df_ego["densidade_ego"]))

    with open("out/percurso_nova_descoberta_setubal.json", encoding="utf-8") as f:
        caminho = json.load(f)["caminho"]

    caminho_set = set(caminho)
    caminho_edges = set()

    for i in range(len(caminho) - 1):
        caminho_edges.add(frozenset({caminho[i], caminho[i+1]}))

    net = Network(height="800px", width="100%", bgcolor="#ffffff", directed=False)
    net.show_buttons(filter_=["nodes"])

    for bairro in sorted(df_bairros["bairro"].unique()):
        g = graus.get(bairro, 0)
        d = dens.get(bairro, 0)

        title = (
            f"<b>{bairro}</b><br>Grau: {g}<br>"
            f"Microrregião: {mic.get(bairro)}<br>"
            f"Densidade ego: {d:.3f}"
        )

        cor = "#ff6666" if bairro in caminho_set else "#97c2fc"

        net.add_node(
            bairro,
            label=bairro,
            size=20 if bairro in caminho_set else 12,
            title=title,
            color=cor
        )

    for _, row in df_adj.iterrows():
        u, v = row["bairro_origem"], row["bairro_destino"]
        par = frozenset({u, v})

        cor = "#ff0000" if par in caminho_edges else "#888888"
        width = 4 if par in caminho_edges else 1

        net.add_edge(u, v, color=cor, width=width)

    net.write_html("out/grafo_interativo.html")
    print("Gerado: out/grafo_interativo.html")

def gerar_grau_distribuicao_parte2(dataset_path="data/dataset_parte2/voos.csv"):
    import matplotlib.pyplot as plt
    from collections import defaultdict
    from .graphs.io import load_large_dataset
    from pathlib import Path

    print("Gerando visualização: distribuição de graus (Parte 2)...")

    g = load_large_dataset(dataset_path)

    # -----------------------------
    # CÁLCULO DO GRAU TOTAL (IN + OUT)
    # -----------------------------
    grau = defaultdict(int)

    for u, v, _ in g.edges():
        grau[u] += 1   # grau de saída
        grau[v] += 1   # grau de entrada

    graus = list(grau.values())

    # -----------------------------
    # PLOT DO HISTOGRAMA
    # -----------------------------
    plt.figure()
    plt.hist(graus, bins=15)
    plt.title("Distribuição dos Graus - Rede de Voos (Parte 2)")
    plt.xlabel("Grau (in + out)")
    plt.ylabel("Frequência")

    Path("out").mkdir(exist_ok=True)
    plt.savefig("out/grau_distribuicao.png")
    plt.close()

    print("Arquivo gerado: out/grau_distribuicao.png ✅")
