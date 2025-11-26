import argparse

from .solve import (
    run_metricas_globais,
    run_metricas_microrregioes,
    run_ego_bairros,
    run_graus,
    run_dist_enderecos,
    run_percurso_nova_descoberta_setubal,
    run_arvore_percurso,
    run_grafo_interativo,
    run_parte2_analise,
)

from .viz import (
    gerar_distribuicao_graus,
    gerar_top10_grau,
    gerar_densidade_ego_microrregiao,
    gerar_grau_distribuicao_parte2,
)


def main():
    parser = argparse.ArgumentParser(description="Projeto Grafos Recife + Parte 2")
    subparsers = parser.add_subparsers(dest="command")

    # Parte 1
    subparsers.add_parser("metricas-globais")
    subparsers.add_parser("metricas-microrregioes")
    subparsers.add_parser("ego-bairros")
    subparsers.add_parser("graus")
    subparsers.add_parser("dist-enderecos")
    subparsers.add_parser("percurso-nova-descoberta-setubal")
    subparsers.add_parser("arvore-percurso")
    subparsers.add_parser("grafo-interativo")

    # Parte 1 — visualizações
    subparsers.add_parser("viz-distribuicao-graus")
    subparsers.add_parser("viz-top10-grau")
    subparsers.add_parser("viz-densidade-ego")
    subparsers.add_parser("viz-parte1")

    # Parte 2
    p2 = subparsers.add_parser("parte2-relatorio")
    p2.add_argument("--dataset", default="data/dataset_parte2/voos.csv")
    subparsers.add_parser("viz-parte2")


    args = parser.parse_args()

    # =============================
    # PARTE 1
    # =============================
    if args.command == "metricas-globais":
        run_metricas_globais()

    elif args.command == "metricas-microrregioes":
        run_metricas_microrregioes()

    elif args.command == "ego-bairros":
        run_ego_bairros()

    elif args.command == "graus":
        run_graus()

    elif args.command == "dist-enderecos":
        run_dist_enderecos()

    elif args.command == "percurso-nova-descoberta-setubal":
        run_percurso_nova_descoberta_setubal()

    elif args.command == "arvore-percurso":
        run_arvore_percurso()

    elif args.command == "grafo-interativo":
        run_grafo_interativo()

    # =============================
    # PARTE 1 — VISUALIZAÇÕES
    # =============================
    elif args.command == "viz-distribuicao-graus":
        gerar_distribuicao_graus()

    elif args.command == "viz-top10-grau":
        gerar_top10_grau()

    elif args.command == "viz-densidade-ego":
        gerar_densidade_ego_microrregiao()

    elif args.command == "viz-parte1":
        gerar_distribuicao_graus()
        gerar_top10_grau()
        gerar_densidade_ego_microrregiao()

    # =============================
    # PARTE 2
    # =============================
    elif args.command == "parte2-relatorio":
        run_parte2_analise(args.dataset)
    elif args.command == "viz-parte2":
        gerar_grau_distribuicao_parte2()


    else:
        parser.print_help()


if __name__ == "__main__":
    main()
