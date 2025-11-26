import streamlit as st
import json
import pandas as pd
import os
import base64
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.solve import (
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

from src.viz import (
    gerar_distribuicao_graus,
    gerar_top10_grau,
    gerar_densidade_ego_microrregiao,
    gerar_grau_distribuicao_parte2
)

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="Grafos do Recife - Dashboard", layout="wide")

# =========================================================
# ESTADO GLOBAL (NAVEGAÇÃO)
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "view_file" not in st.session_state:
    st.session_state.view_file = None


# =========================================================
# ===================== HOME ===============================
# =========================================================
if st.session_state.page == "home":

    st.sidebar.title("📊 Dashboard")

    menu = st.sidebar.radio(
        "Menu",
        ["🏙 Recife", "✈️ Voos"]
    )

    # ---------- TOPO ----------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bairros", "94")
    c2.metric("Arestas", "180")
    c3.metric("Endereços", "5")
    c4.metric("Dataset Parte 2", "Voos")

    st.divider()

    # =========================================================
    # RECIFE
    # =========================================================
    if menu == "🏙 Recife":
        st.subheader("Grafo dos Bairros do Recife")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📦 Métricas Globais"):
                run_metricas_globais()
                st.session_state.view_file = "out/recife_global.json"
                st.session_state.page = "view"
                st.rerun()

            if st.button("📊 Graus"):
                run_graus()
                st.session_state.view_file = "out/graus.csv"
                st.session_state.page = "view"
                st.rerun()

            if st.button("🌳 Ego-Bairros"):
                run_ego_bairros()
                st.session_state.view_file = "out/ego_bairro.csv"
                st.session_state.page = "view"
                st.rerun()

        with col2:
            if st.button("🗂 Microrregiões"):
                run_metricas_microrregioes()
                st.session_state.view_file = "out/microrregioes.json"
                st.session_state.page = "view"
                st.rerun()

            if st.button("📍 Distâncias Endereços"):
                run_dist_enderecos()
                st.session_state.view_file = "out/distancias_enderecos.csv"
                st.session_state.page = "view"
                st.rerun()

            if st.button("🛣 Percurso ND → Setúbal"):
    
                # ✅ GERA O JSON NA HORA (IGUAL AO CLI)
                run_percurso_nova_descoberta_setubal()
                
                # ✅ GERA A ÁRVORE NA HORA (IGUAL AO CLI)
                run_arvore_percurso()

                # ✅ AGORA SIM, DEFINE O ARQUIVO PARA A VIEW
                st.session_state.view_file = "out/arvore_percurso.png"
                st.session_state.page = "view"
                st.rerun()


        with col3:
            if st.button("🌐 Grafo Interativo"):
                run_grafo_interativo()
                st.session_state.view_file = "out/grafo_interativo.html"
                st.session_state.page = "view"
                st.rerun()

            if st.button("📈 Distribuição de Graus"):
                gerar_distribuicao_graus()
                st.session_state.view_file = "out/distribuicao_graus.png"
                st.session_state.page = "view"
                st.rerun()

            if st.button("🏅 Top 10 Grau"):
                gerar_top10_grau()
                st.session_state.view_file = "out/top10_grau.png"
                st.session_state.page = "view"
                st.rerun()

    # =========================================================
    # VOOS
    # =========================================================
    elif menu == "✈️ Voos":
        st.subheader("Dataset Parte 2 — Voos")

        if st.button("📊 Gerar Análise"):
            run_parte2_analise()
            st.session_state.view_file = "out/parte2_report.json"
            st.session_state.page = "view"
            st.rerun()

        if st.button("📈 Grau de Voos"):
            gerar_grau_distribuicao_parte2()
            st.session_state.view_file = "out/grau_distribuicao.png"
            st.session_state.page = "view"
            st.rerun()


# =========================================================
# ===================== VIEW ===============================
# =========================================================
elif st.session_state.page == "view":

    if st.button("⬅️ Voltar"):
        st.session_state.page = "home"
        st.rerun()

    arquivo = st.session_state.view_file

    if not arquivo or not os.path.exists(arquivo):
        st.warning("Arquivo não encontrado.")
    else:
        st.subheader(f"📂 Visualizando: {arquivo}")

        # ---------- PNG ----------
        if arquivo.endswith(".png"):
            col_esq, col_dir = st.columns([1, 2])

            # =======================
            # COLUNA ESQUERDA
            # =======================
            with col_esq:
                st.subheader("📌 Análise")

                # ✅ CASO ESPECIAL → VIEW DO PERCURSO COM JSON
                if "arvore" in arquivo:

                    st.markdown("### 📦 JSON da Nova Descoberta")

                    with open("out/microrregioes.json", "r", encoding="utf-8") as f:
                        dados = json.load(f)

                    # Filtra somente a microrregião que contém Nova Descoberta
                    nova_descoberta = None
                    for item in dados:
                        if "Nova Descoberta" in item.get("bairros", []):
                            nova_descoberta = item
                            break

                    # ✅ CSS PARA SCROLL INTERNO DO JSON
                    st.markdown("""
                        <style>
                        div[data-testid="stJson"] {
                            max-height: 460px;
                            overflow-y: auto;
                            border-radius: 10px;
                            border: 1px solid #2a2f3a;
                            background-color: #0e1117;
                            padding: 12px;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    if nova_descoberta:
                        st.json(nova_descoberta)
                    else:
                        st.warning("Nova Descoberta não encontrada no JSON.")

                # ✅ TOP10 CONTINUA COM TEXTO NORMAL
                elif "top10" in arquivo:
                    st.markdown("""
                    **Top 10 Bairros por Grau**

                    Mostra os bairros mais conectados do Recife.  
                    Indica regiões com maior concentração de interligações.
                    """)

                # ✅ OUTROS PNGs CONTINUAM NORMAIS
                else:
                    st.markdown("Visualização gerada automaticamente pelo sistema.")

            # =======================
            # COLUNA DIREITA → IMAGEM SEMPRE APARECE
            # =======================
            with col_dir:

                st.markdown("""
                    <style>
                    .container-img {
                        height: 460px;                 /* ✅ MESMA ALTURA DO JSON */
                        overflow: auto;
                        border-radius: 10px;
                        border: 1px solid #2a2f3a;
                        padding: 10px;
                        background-color: #0e1117;
                        display: flex;
                        align-items: flex-start;      /* ✅ COLA NO TOPO */
                        justify-content: center;
                    }

                    .container-img img {
                        max-width: 100%;
                        height: auto;
                        object-fit: contain;
                    }
                    </style>
                """, unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="container-img">
                        <img src="data:image/png;base64,{base64.b64encode(open(arquivo, "rb").read()).decode()}" />
                    </div>
                    """,
                    unsafe_allow_html=True
                )




        # ---------- JSON ----------
        elif arquivo.endswith(".json"):

            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)

            # CSS para limitar altura e criar SCROLL INTERNO no st.json
            st.markdown("""
                <style>
                div[data-testid="stJson"] {
                    max-height: 500px;
                    overflow-y: auto;
                    border-radius: 10px;
                    border: 1px solid #2a2f3a;
                    background-color: #0e1117;
                    padding: 10px;
                }
                </style>
            """, unsafe_allow_html=True)

            # EXIBE COM AS CORES NATIVAS (IGUAL SUA IMAGEM)
            st.json(dados)



        # ---------- CSV ----------
        elif arquivo.endswith(".csv"):
            df = pd.read_csv(arquivo)
            st.dataframe(df, use_container_width=True)

        # ---------- HTML ----------
        elif arquivo.endswith(".html"):
            with open(arquivo, "r", encoding="utf-8") as f:
                html = f.read()

            st.components.v1.html(html, height=650, scrolling=True)
