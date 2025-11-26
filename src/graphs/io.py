import pandas as pd
from pathlib import Path
from src.graphs.graph import Graph
import csv
from .graph import Graph


# ------------------------------
# Normalização Parte 1
# ------------------------------
def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    name = name.strip()
    name = " ".join(name.split())
    name = name.title()
    return name


# ------------------------------
# Parte 1 — Carrega nós
# ------------------------------
def load_nodes(graph: Graph, path="data/bairros_unique.csv"):
    df = pd.read_csv(path)

    for bairro in df["bairro"]:
        nome = normalize_name(bairro)

        if "Setubal" in nome or "Setúbal" in nome:
            nome = "Boa Viagem"

        graph.add_vertex(nome)

    return graph


# ------------------------------
# Parte 1 — Carrega arestas
# ------------------------------
def load_edges(graph: Graph, path="data/adjacencias_bairros.csv"):
    df = pd.read_csv(path)

    for _, row in df.iterrows():
        u = normalize_name(row["bairro_origem"])
        v = normalize_name(row["bairro_destino"])
        peso = float(row["peso"])

        if "Setubal" in u or "Setúbal" in u:
            u = "Boa Viagem"
        if "Setubal" in v or "Setúbal" in v:
            v = "Boa Viagem"

        graph.add_edge(u, v, peso)

    return graph


# ------------------------------
# Parte 1 — Build Recife Graph
# ------------------------------
def build_graph(
    nodes_path="data/bairros_unique.csv",
    edges_path="data/adjacencias_bairros.csv"
):
    graph = Graph(directed=False)
    load_nodes(graph, nodes_path)
    load_edges(graph, edges_path)
    return graph




# ============================================================
# Carregamento do dataset grande (Parte 2)
# ============================================================

def load_large_dataset(path: str) -> Graph:
    """
    Carrega o dataset de voos no formato NY-flights (voos.csv).

    Espera colunas:
      - origin  (código do aeroporto de origem, ex.: 'EWR')
      - dest    (código do aeroporto de destino, ex.: 'LAX')
      - distance (distância em milhas, usada como peso)

    Retorna um Graph dirigido (directed=True).
    """

    g = Graph(directed=True)

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            origem = (row.get("origin") or "").strip()
            destino = (row.get("dest") or "").strip()
            dist_str = (row.get("distance") or "").strip()

            if not origem or not destino or not dist_str:
                continue

            try:
                peso = float(dist_str)
            except ValueError:
                # pula linhas com distância inválida
                continue

            # grafo dirigido: voo origem -> destino
            g.add_edge(origem, destino, peso, directed=True)

    return g