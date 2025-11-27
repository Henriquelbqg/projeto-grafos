import argparse
import os
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent / "parte1" / "src"))

from graphs.graph import Graph
from graphs.algorithms import bfs, dfs, dijkstra, bellman_ford


sys.path.insert(0, str(Path(__file__).parent))

from algorithms2 import (
    carregar_grafo_voos,
    rodar_analise_parte2,
    gerar_distribuicao_grau_voos
)


def main():
    parser = argparse.ArgumentParser(
        description="Projeto Grafos - Parte 2 (Dataset de Voos)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  Dijkstra entre dois aeroportos
  python -m src.cli --dataset ./data/voos.csv --alg DIJKSTRA --source EWR --target LAX --out ./out/

  BFS a partir de um aeroporto
  python -m src.cli --dataset ./data/voos.csv --alg BFS --source EWR --out ./out/

  Gerar relatório completo (sem --alg)
  python -m src.cli --dataset ./data/voos.csv --out ./out/
        """
    )

    parser.add_argument(
        "--dataset",
        default="./data/voos.csv",
        help="Caminho para o dataset de voos (padrão: ./data/voos.csv)"
    )

    parser.add_argument(
        "--alg",
        choices=["BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD"],
        help="Algoritmo a executar: BFS, DFS, DIJKSTRA, BELLMAN_FORD"
    )

    parser.add_argument(
        "--source",
        help="Aeroporto de origem (obrigatório para BFS, DFS, DIJKSTRA, BELLMAN_FORD)"
    )

    parser.add_argument(
        "--target",
        help="Aeroporto de destino (obrigatório para DIJKSTRA)"
    )

    parser.add_argument(
        "--out",
        default="./out/",
        help="Diretório de saída (padrão: ./out/)"
    )

    args = parser.parse_args()


    if args.alg and not args.source:
        parser.error("--source é obrigatório quando --alg é especificado")

    if args.alg == "DIJKSTRA" and not args.target:
        parser.error("--target é obrigatório para DIJKSTRA")


    out_dir = Path(args.out)
    if not out_dir.is_absolute():

        parte2_dir = Path(__file__).parent.parent.parent / "parte2"
        out_dir = parte2_dir / args.out
    out_dir.mkdir(parents=True, exist_ok=True)


    original_cwd = os.getcwd()
    parte2_dir = Path(__file__).parent.parent.parent / "parte2"
    os.chdir(parte2_dir)

    try:

        dataset_path = args.dataset
        if not os.path.isabs(dataset_path):
            dataset_path = str(parte2_dir / dataset_path)


        if args.alg:

            g = carregar_grafo_voos(dataset_path)

            if args.alg == "BFS":
                resultado = bfs(g, args.source)
                ordem = resultado.get("ordem", [])
                camadas = resultado.get("camadas", {})
                ciclos = resultado.get("ciclos", [])

                print(f"\nBFS a partir de '{args.source}':")
                print(f"Ordem de visitação: {ordem[:20]}..." if len(ordem) > 20 else f"Ordem de visitação: {ordem}")
                print(f"Número de camadas: {len(set(camadas.values()))}")
                print(f"Ciclos encontrados: {len(ciclos)}")

            elif args.alg == "DFS":
                resultado = dfs(g, args.source)
                ordem = resultado.get("ordem", [])
                ciclos = resultado.get("ciclos", [])
                arestas_class = resultado.get("arestas_class", [])

                print(f"\nDFS a partir de '{args.source}':")
                print(f"Ordem de visitação: {ordem[:20]}..." if len(ordem) > 20 else f"Ordem de visitação: {ordem}")
                print(f"Ciclos encontrados: {len(ciclos)}")
                print(f"Arestas classificadas: {len(arestas_class)}")

            elif args.alg == "DIJKSTRA":
                dist, caminho = dijkstra(g, args.source, args.target)

                print(f"\nDijkstra de '{args.source}' para '{args.target}':")
                if dist == float('inf'):
                    print("Não há caminho entre os aeroportos.")
                else:
                    print(f"Distância: {dist} milhas")
                    print(f"Caminho: {' -> '.join(caminho)}")

            elif args.alg == "BELLMAN_FORD":
                dist, pai, ciclo_negativo = bellman_ford(g, args.source)

                print(f"\nBellman-Ford a partir de '{args.source}':")
                print(f"Ciclo negativo detectado: {ciclo_negativo}")
                print(f"Distâncias calculadas para {len([d for d in dist.values() if d != float('inf')])} vértices")

        else:

            print("Executando análise completa da Parte 2...")


            os.chdir(parte2_dir)
            out_report = str(out_dir / "parte2_report.json")


            resultado = rodar_analise_parte2(dataset_path, out_report)

            print("\nAnálise completa da Parte 2 concluída!")
            print(f"   Relatório: {resultado.get('report_path', out_report)}")
            visualizacoes = resultado.get("visualizations", [])
            if visualizacoes:
                print("   Visualizações geradas:")
                for viz_path in visualizacoes:
                    print(f"     - {viz_path}")
            else:
                print("   (Nenhuma visualização registrada)")

    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
