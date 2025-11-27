import pandas as pd
from pathlib import Path
import csv
from .graph import Graph

SETUBAL_CANONICAL = "Boa Viagem"
SETUBAL_LABEL = "Boa Viagem (Setúbal)"


def _clean_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    cleaned = name.strip()
    cleaned = " ".join(cleaned.split())
    return cleaned.title()


def is_setubal(name: str) -> bool:
    if not isinstance(name, str):
        return False
    return "setubal" in name.lower() or "setúbal" in name.lower()


def normalize_name(name: str) -> str:
    cleaned = _clean_name(name)
    if is_setubal(cleaned):
        return SETUBAL_CANONICAL
    return cleaned





def load_nodes(graph: Graph, path="data/bairros_unique.csv"):

    path_obj = Path(path)
    if not path_obj.is_absolute():
        if not path_obj.exists():

            parte1_dir = Path(__file__).parent.parent.parent
            path_obj = parte1_dir / path
        else:
            path_obj = path_obj.resolve()

    if not path_obj.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_obj}")
    df = pd.read_csv(path_obj)

    for bairro in df["bairro"]:
        nome = normalize_name(bairro)

        if "Setubal" in nome or "Setúbal" in nome:
            nome = "Boa Viagem"

        graph.add_vertex(nome)

    return graph





def load_edges(graph: Graph, path="data/adjacencias_bairros.csv"):

    path_obj = Path(path)
    if not path_obj.is_absolute():
        if not path_obj.exists():

            parte1_dir = Path(__file__).parent.parent.parent
            path_obj = parte1_dir / path
        else:
            path_obj = path_obj.resolve()

    if not path_obj.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path_obj}")
    df = pd.read_csv(path_obj)

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





def build_graph(
    nodes_path="data/bairros_unique.csv",
    edges_path="data/adjacencias_bairros.csv"
):
    graph = Graph(directed=False)
    load_nodes(graph, nodes_path)
    load_edges(graph, edges_path)
    return graph








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

                continue


            g.add_edge(origem, destino, peso, directed=True)

    return g