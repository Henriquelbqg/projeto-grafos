import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from .graphs.io import SETUBAL_CANONICAL, SETUBAL_LABEL


def _get_parte1_path(relative_path: str) -> Path:
    """Resolve caminho relativo ao diretório parte1"""

    parte1_dir = Path(__file__).parent.parent
    return parte1_dir / relative_path






def _ensure_out():
    """Garante que o diretório out existe e copia lib/ se necessário"""
    parte1_dir = Path(__file__).parent.parent


    current_dir = Path.cwd()
    if current_dir.name == "out":

        out_dir = current_dir
    else:

        out_dir = parte1_dir / "out"
        os.makedirs(out_dir, exist_ok=True)


    lib_source = parte1_dir / "lib"
    lib_dest = out_dir / "lib"

    if lib_source.exists() and not lib_dest.exists():
        import shutil
        shutil.copytree(lib_source, lib_dest)
        print(f"Copiado lib/ para {lib_dest} para suporte aos HTMLs")






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
    df_bairros = pd.read_csv(_get_parte1_path("data/bairros_unique.csv"), encoding="utf-8")

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






def gerar_arvore_percurso_png():
    """
    Gera a árvore do percurso ND → Boa Viagem (Setúbal) em PNG estático,
    usando apenas matplotlib (sem networkx).
    """
    _ensure_out()


    with open("out/percurso_nova_descoberta_setubal.json", encoding="utf-8") as f:
        dados = json.load(f)

    caminho = dados.get("caminho_display", dados["caminho"])
    n = len(caminho)


    fig, ax = plt.subplots(figsize=(12, 4))


    x_positions = {}
    y_positions = {}
    y_base = 0.5

    for i, bairro in enumerate(caminho):
        x_positions[bairro] = i / max(1, n - 1)

        y_offset = 0.1 * (i % 2) if n > 1 else 0
        y_positions[bairro] = y_base + y_offset


    for i in range(len(caminho) - 1):
        x1 = x_positions[caminho[i]]
        y1 = y_positions[caminho[i]]
        x2 = x_positions[caminho[i + 1]]
        y2 = y_positions[caminho[i + 1]]
        ax.plot([x1, x2], [y1, y2], linewidth=3, color='#ff0000', zorder=1)


    for i, bairro in enumerate(caminho):
        x = x_positions[bairro]
        y = y_positions[bairro]


        if i == 0 or i == len(caminho) - 1:
            color = '#ff0000'
            size = 800
        else:
            color = '#ffcccc'
            size = 600

        ax.scatter(x, y, s=size, c=color, zorder=2, edgecolors='black', linewidths=1)


        ax.text(x, y - 0.15, bairro, ha='center', va='top',
                fontsize=9, fontweight='bold', rotation=45 if n > 5 else 0)

    ax.set_title("Árvore do Percurso: Nova Descoberta → Boa Viagem (Setúbal)",
                 fontsize=12, fontweight='bold')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig("out/arvore_percurso.png", dpi=120, bbox_inches='tight')
    plt.close()

    print("Gerado: out/arvore_percurso.png")


def gerar_arvore_percurso_html():
    """
    Gera a árvore do percurso ND → Boa Viagem (Setúbal) em HTML interativo (pyvis).
    """
    from pyvis.network import Network

    _ensure_out()


    with open("out/percurso_nova_descoberta_setubal.json", encoding="utf-8") as f:
        dados = json.load(f)

    caminho = dados.get("caminho_display", dados["caminho"])


    net = Network(height="600px", width="100%", bgcolor="#ffffff", directed=False)
    net.show_buttons(filter_=["physics"])


    for i, bairro in enumerate(caminho):

        if i == 0 or i == len(caminho) - 1:
            net.add_node(
                bairro,
                label=bairro,
                size=30,
                color="#ff0000",
                title=f"<b>{bairro}</b><br>Posição no caminho: {i+1}/{len(caminho)}"
            )
        else:
            net.add_node(
                bairro,
                label=bairro,
                size=20,
                color="#ff6666",
                title=f"<b>{bairro}</b><br>Posição no caminho: {i+1}/{len(caminho)}"
            )


    for i in range(len(caminho) - 1):
        net.add_edge(
            caminho[i],
            caminho[i + 1],
            width=5,
            color="#ff0000",
            title=f"{caminho[i]} → {caminho[i+1]}"
        )

    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "stabilization": {"iterations": 100}
      },
      "configure": {
        "enabled": false
      }
    }
    """)

    net.write_html("out/arvore_percurso.html")
    print("Gerado: out/arvore_percurso.html")







def gerar_grafo_interativo():
    """
    Gera um HTML interativo completo em out/grafo_interativo.html
    """
    from pyvis.network import Network

    _ensure_out()

    df_bairros = pd.read_csv(_get_parte1_path("data/bairros_unique.csv"), encoding="utf-8")
    df_graus = pd.read_csv("out/graus.csv", encoding="utf-8")
    df_ego = pd.read_csv("out/ego_bairro.csv", encoding="utf-8")
    df_adj = pd.read_csv(_get_parte1_path("data/adjacencias_bairros.csv"), encoding="utf-8")

    mic = dict(zip(df_bairros["bairro"], df_bairros["microrregiao"]))
    graus = dict(zip(df_graus["bairro"], df_graus["grau"]))
    dens = dict(zip(df_ego["bairro"], df_ego["densidade_ego"]))

    with open("out/percurso_nova_descoberta_setubal.json", encoding="utf-8") as f:
        dados = json.load(f)

    caminho = dados["caminho"]
    caminho_display = dados.get("caminho_display", caminho)
    caminho_set = set(caminho)
    caminho_edges = set()

    for i in range(len(caminho) - 1):
        caminho_edges.add(frozenset({caminho[i], caminho[i+1]}))

    net = Network(height="800px", width="100%", bgcolor="#ffffff", directed=False)

    net.show_buttons(filter_=["nodes", "edges", "layout", "interaction", "physics", "selection", "manipulation"])

    net.set_options("""
    {
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false
      },
      "configure": {
        "enabled": true
      }
    }
    """)

    for bairro in sorted(df_bairros["bairro"].unique()):
        g = graus.get(bairro, 0)
        d = dens.get(bairro, 0)
        label = SETUBAL_LABEL if bairro == SETUBAL_CANONICAL else bairro

        title = (
            f"<b>{label}</b><br>Grau: {g}<br>"
            f"Microrregião: {mic.get(bairro)}<br>"
            f"Densidade ego: {d:.3f}"
        )

        cor = "#ff6666" if bairro in caminho_set else "#97c2fc"

        net.add_node(
            bairro,
            label=label,
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


    temp_html = "out/grafo_interativo_temp.html"
    net.write_html(temp_html)


    with open(temp_html, "r", encoding="utf-8") as f:
        html_content = f.read()


    caminho_legenda = " → ".join([caminho_display[0], caminho_display[-1]]) if len(caminho_display) >= 2 else " → ".join(caminho_display)

    search_box = f"""
    <div style="padding: 15px; background-color: #f5f5f5; border-bottom: 2px solid #ddd;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <label for="searchBairro" style="font-weight: bold; margin-right: 10px; color: #333;">
                Buscar bairro:
            </label>
            <input
                type="text"
                id="searchBairro"
                placeholder="Digite o nome do bairro..."
                style="padding: 8px 12px; font-size: 14px; width: 300px; border: 2px solid #ccc; border-radius: 4px;"
                onkeyup="filtrarBairros()"
            />
            <button
                onclick="limparBusca()"
                style="padding: 8px 15px; margin-left: 10px; font-size: 14px; background-color: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;"
            >
                Limpar
            </button>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                Dica: digite o nome do bairro para destacá-lo no grafo. O caminho "{caminho_legenda}" está destacado em vermelho.
            </div>
        </div>
    </div>
    """


    html_content = html_content.replace(
        '<div id="mynetwork"',
        search_box + '\n    <div id="mynetwork"'
    )


    search_script = """
    <script type="text/javascript">
        var originalNodes = null;
        var originalEdges = null;

        function filtrarBairros() {
            var searchTerm = document.getElementById('searchBairro').value.toLowerCase().trim();

            if (!originalNodes) {
                originalNodes = nodes.get({ returnType: "Object" });
                originalEdges = edges.get({ returnType: "Object" });
            }

            if (searchTerm === '') {
                // Restaurar estilos originais
                var restore = [];
                for (var nodeId in originalNodes) {
                    var original = originalNodes[nodeId];
                    restore.push({
                        id: nodeId,
                        hidden: false,
                        color: original.color || undefined,
                        size: original.size || undefined,
                        borderWidth: original.borderWidth || undefined
                    });
                }
                nodes.update(restore);
            } else {
                var updates = [];
                var matchingNodes = [];

                for (var nodeId in originalNodes) {
                    var originalNode = originalNodes[nodeId];
                    var label = (originalNode.label || '').toLowerCase();
                    var isMatch = label.includes(searchTerm);

                    if (isMatch) {
                        matchingNodes.push(nodeId);
                        updates.push({
                            id: nodeId,
                            hidden: false,
                            color: { border: '#f43f5e', background: '#ffe4e6' },
                            size: (originalNode.size || 25) * 1.2,
                            borderWidth: 3
                        });
                    } else {
                        updates.push({
                            id: nodeId,
                            hidden: false,
                            color: originalNode.color || undefined,
                            size: originalNode.size || undefined,
                            borderWidth: originalNode.borderWidth || undefined
                        });
                    }
                }

                nodes.update(updates);

                if (matchingNodes.length > 0 && network) {
                    network.selectNodes(matchingNodes);
                    network.focus(matchingNodes[0], {
                        scale: 1.3,
                        animation: {
                            duration: 600,
                            easingFunction: "easeInOutQuad"
                        }
                    });
                }
            }
        }

        function limparBusca() {
            document.getElementById('searchBairro').value = '';
            filtrarBairros();
        }
    </script>
    """


    html_content = html_content.replace(
        '</body>',
        search_script + '\n    </body>'
    )


    with open("out/grafo_interativo.html", "w", encoding="utf-8") as f:
        f.write(html_content)


    import os
    if os.path.exists(temp_html):
        os.remove(temp_html)

    print("Gerado: out/grafo_interativo.html")






def gerar_arvore_bfs():
    """
    Gera a árvore BFS a partir de "Boa Vista" mostrando as camadas (níveis).
    Salva em out/arvore_bfs_boa_vista.png e out/arvore_bfs_boa_vista.html
    """
    from pyvis.network import Network
    from .graphs.io import build_graph
    from .graphs.algorithms import bfs

    _ensure_out()


    g = build_graph()
    resultado = bfs(g, "Boa Vista")
    camadas = resultado["camadas"]
    ordem = resultado["ordem"]


    bairros_por_camada = {}
    for bairro, camada in camadas.items():
        if camada not in bairros_por_camada:
            bairros_por_camada[camada] = []
        bairros_por_camada[camada].append(bairro)


    cores_camadas = {
        0: "#ff0000",
        1: "#ff6666",
        2: "#ff9999",
        3: "#ffcccc",
        4: "#ffe6e6",
    }


    fig, ax = plt.subplots(figsize=(16, 10))

    max_camada = max(camadas.values()) if camadas else 0
    num_camadas = max_camada + 1


    posicoes = {}
    max_bairros_por_camada = max(len(bairros_por_camada.get(i, [])) for i in range(num_camadas)) if num_camadas > 0 else 1
    y_spacing = 0.8 / max(1, max_bairros_por_camada + 1)

    for camada in range(num_camadas):
        bairros = bairros_por_camada.get(camada, [])
        x = 0.1 + (camada / max(1, max_camada)) * 0.8 if max_camada > 0 else 0.5

        for idx, bairro in enumerate(bairros):
            y = 0.9 - (idx + 1) * y_spacing
            posicoes[bairro] = (x, y)



    arestas_bfs = set()
    visitados_bfs = {"Boa Vista"}

    for bairro in ordem[1:]:

        for viz, _ in g.neighbors(bairro):
            if viz in visitados_bfs and camadas.get(viz, float('inf')) < camadas[bairro]:
                arestas_bfs.add((viz, bairro))
                break
        visitados_bfs.add(bairro)

    for u, v in arestas_bfs:
        if u in posicoes and v in posicoes:
            x1, y1 = posicoes[u]
            x2, y2 = posicoes[v]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.6, zorder=1)


    for camada in range(num_camadas):
        bairros = bairros_por_camada.get(camada, [])
        cor = cores_camadas.get(camada, "#cccccc")

        for bairro in bairros:
            if bairro in posicoes:
                x, y = posicoes[bairro]
                size = 1000 if camada == 0 else 600
                ax.scatter(x, y, s=size, c=cor, zorder=2, edgecolors='black', linewidths=2)
                ax.text(x, y - 0.03, bairro, ha='center', va='top',
                       fontsize=8, fontweight='bold', rotation=0)


    for camada in range(num_camadas):
        ax.text(camada / max(1, max_camada) if max_camada > 0 else 0.5, -0.05,
               f"Camada {camada}", ha='center', va='top',
               fontsize=12, fontweight='bold', color='blue')

    ax.set_title("Árvore BFS: Boa Vista (Camadas/Níveis)",
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.15, 1.05)
    ax.axis('off')

    plt.tight_layout()

    current_dir = Path.cwd()
    if current_dir.name == "out":
        output_path_png = "arvore_bfs_boa_vista.png"
    else:
        output_path_png = "out/arvore_bfs_boa_vista.png"
    plt.savefig(output_path_png, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Gerado: {output_path_png}")


    net = Network(height="800px", width="100%", bgcolor="#ffffff", directed=False)
    net.show_buttons(filter_=["physics"])


    for camada in range(num_camadas):
        bairros = bairros_por_camada.get(camada, [])
        cor = cores_camadas.get(camada, "#cccccc")

        for bairro in bairros:
            net.add_node(
                bairro,
                label=bairro,
                size=30 if camada == 0 else 20,
                color=cor,
                title=f"<b>{bairro}</b><br>Camada: {camada}"
            )


    for u, v in arestas_bfs:
        net.add_edge(u, v, width=3, color="#333333")


    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 200,
          "springConstant": 0.01,
          "nodeDistance": 150
        },
        "stabilization": {"iterations": 100}
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "LR",
          "sortMethod": "directed"
        }
      },
      "configure": {
        "enabled": false
      }
    }
    """)


    if current_dir.name == "out":
        output_path_html = "arvore_bfs_boa_vista.html"
    else:
        output_path_html = "out/arvore_bfs_boa_vista.html"
    net.write_html(output_path_html)
    print(f"Gerado: {output_path_html}")
