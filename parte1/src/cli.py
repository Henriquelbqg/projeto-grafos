import argparse
import os
from pathlib import Path

from .solve import (
    run_metricas_globais,
    run_metricas_microrregioes,
    run_ego_bairros,
    run_graus,
    run_dist_enderecos,
    run_percurso_nova_descoberta_setubal,
    run_arvore_percurso,
    run_grafo_interativo,
    run_arvore_bfs,
)
from .graphs.io import build_graph, normalize_name, SETUBAL_LABEL
from .graphs.algorithms import bfs, dfs, dijkstra, bellman_ford


def main():
    parser = argparse.ArgumentParser(
        description="Projeto Grafos - Grafo dos Bairros do Recife",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  BFS a partir de um bairro
  python -m src.cli --dataset ./data/bairros_recife.csv --alg BFS --source "Boa Viagem" --out ./out/

  Dijkstra (Nova Descoberta → Boa Viagem (Setúbal))
  python -m src.cli --dataset ./data/bairros_recife.csv --alg DIJKSTRA --source "Nova Descoberta" --target "Boa Viagem" --out ./out/

        """
    )

    parser.add_argument(
        "--dataset",
        default="./data/bairros_recife.csv",
        help="Caminho para o dataset de bairros (padrão: ./data/bairros_recife.csv)"
    )

    parser.add_argument(
        "--alg",
        choices=["BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD"],
        help="Algoritmo a executar: BFS, DFS, DIJKSTRA, BELLMAN_FORD"
    )

    parser.add_argument(
        "--source",
        help="Bairro de origem (obrigatório para BFS, DFS, DIJKSTRA, BELLMAN_FORD)"
    )

    parser.add_argument(
        "--target",
        help="Bairro de destino (obrigatório para DIJKSTRA)"
    )

    parser.add_argument(
        "--out",
        default="./out/",
        help="Diretório de saída (padrão: ./out/)"
    )

    parser.add_argument(
        "--serve",
        action="store_true",
        help="Gerar todos os arquivos da Parte 1 e iniciar servidor HTTP para visualização"
    )

    args = parser.parse_args()
    source_display = args.source.strip() if args.source else None
    target_display = args.target.strip() if args.target else None
    source_norm = normalize_name(source_display) if source_display else None
    target_norm = normalize_name(target_display) if target_display else None


    if args.serve:

        print("Gerando todos os arquivos da Parte 1...")
        print("=" * 60)
        run_metricas_globais()
        run_metricas_microrregioes()
        run_ego_bairros()
        run_graus()
        run_dist_enderecos()
        run_percurso_nova_descoberta_setubal()
        run_arvore_percurso()
        run_arvore_bfs()
        run_grafo_interativo()

        from .viz import (
            gerar_distribuicao_graus,
            gerar_top10_grau,
            gerar_densidade_ego_microrregiao,
        )
        gerar_distribuicao_graus()
        gerar_top10_grau()
        gerar_densidade_ego_microrregiao()
        print("\nTodas as análises da Parte 1 foram concluídas!")
        print("\nArquivos HTML gerados:")
        print("   • http://localhost:8000/grafo_interativo.html")
        print("   • http://localhost:8000/arvore_percurso.html")
        print("   • http://localhost:8000/arvore_bfs_boa_vista.html")


        print("\n" + "=" * 60)
        print("Iniciando servidor HTTP...")
        print("=" * 60)
        import subprocess
        import sys

        servidor_path = Path(__file__).parent.parent / "servidor_html.py"
        subprocess.run([sys.executable, str(servidor_path)])
        return


    if args.alg and not source_norm:
        parser.error("--source é obrigatório quando --alg é especificado")

    if args.alg == "DIJKSTRA" and not target_norm:
        parser.error("--target é obrigatório para DIJKSTRA")


    out_dir = Path(args.out)
    if not out_dir.is_absolute():

        parte1_dir = Path(__file__).parent.parent.parent
        out_dir = parte1_dir / args.out
    out_dir.mkdir(parents=True, exist_ok=True)


    original_cwd = os.getcwd()
    parte1_dir = Path(__file__).parent.parent.parent
    os.chdir(parte1_dir)

    try:

        g = build_graph()


        os.chdir(out_dir)


        if args.alg == "BFS":
            resultado = bfs(g, source_norm)
            ordem = resultado.get("ordem", [])
            camadas = resultado.get("camadas", {})
            ciclos = resultado.get("ciclos", [])

            print(f"\nBFS a partir de '{source_display or source_norm}':")
            print(f"Ordem de visitação: {ordem[:20]}..." if len(ordem) > 20 else f"Ordem de visitação: {ordem}")
            print(f"Número de camadas: {len(set(camadas.values()))}")
            print(f"Ciclos encontrados: {len(ciclos)}")

        elif args.alg == "DFS":
            resultado = dfs(g, source_norm)
            ordem = resultado.get("ordem", [])
            ciclos = resultado.get("ciclos", [])
            arestas_class = resultado.get("arestas_class", [])

            print(f"\nDFS a partir de '{source_display or source_norm}':")
            print(f"Ordem de visitação: {ordem[:20]}..." if len(ordem) > 20 else f"Ordem de visitação: {ordem}")
            print(f"Ciclos encontrados: {len(ciclos)}")
            print(f"Arestas classificadas: {len(arestas_class)}")

        elif args.alg == "DIJKSTRA":
            dist, caminho = dijkstra(g, source_norm, target_norm)
            destino_print = target_display or (SETUBAL_LABEL if target_norm == "Boa Viagem" else target_norm)

            print(f"\nDijkstra de '{source_display or source_norm}' para '{destino_print}':")
            if dist == float('inf'):
                print("Não há caminho entre os bairros.")
            else:
                print(f"Distância: {dist}")
                print(f"Caminho: {' -> '.join(caminho)}")

        elif args.alg == "BELLMAN_FORD":
            dist, pai, ciclo_negativo = bellman_ford(g, source_norm)

            print(f"\nBellman-Ford a partir de '{source_display or source_norm}':")
            print(f"Ciclo negativo detectado: {ciclo_negativo}")
            print(f"Distâncias calculadas para {len([d for d in dist.values() if d != float('inf')])} vértices")

        else:

            print("Executando todas as análises da Parte 1...")
            run_metricas_globais()
            run_metricas_microrregioes()
            run_ego_bairros()
            run_graus()
            run_dist_enderecos()
            run_percurso_nova_descoberta_setubal()
            run_arvore_percurso()
            run_arvore_bfs()
            run_grafo_interativo()

            from .viz import (
                gerar_distribuicao_graus,
                gerar_top10_grau,
                gerar_densidade_ego_microrregiao,
            )
            gerar_distribuicao_graus()
            gerar_top10_grau()
            gerar_densidade_ego_microrregiao()
            print("\nTodas as análises foram concluídas!")
            print("\nArquivos HTML gerados:")
            print("   • http://localhost:8000/grafo_interativo.html")
            print("   • http://localhost:8000/arvore_percurso.html")
            print("   • http://localhost:8000/arvore_bfs_boa_vista.html")
            print("\nDica: Para visualizar os HTMLs, execute:")
            print("   python3 servidor_html.py")
            print("   Ou: cd out && python3 -m http.server 8000")
            print("   Depois acesse os links acima no navegador.")

    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
