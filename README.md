# Projeto Grafos - Grafos do Recife + Comparação de Algoritmos

Projeto da cadeira de Teoria dos Grafos implementando algoritmos de grafos (BFS, DFS, Dijkstra, Bellman-Ford) e análise do grafo dos bairros do Recife.

## 📋 Requisitos

- Python 3.11+
- Bibliotecas listadas em `requirements.txt`

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Ebn0511/Projetos_Grafos.git
cd Projetos_Grafos
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências dentro do ambiente:
```bash
pip install -r requirements.txt
```

> Dica: ao finalizar o uso, execute `deactivate` para sair do ambiente virtual.

## 📁 Estrutura do Projeto

```
Projetos_Grafos/
├── README.md
├── RELATORIO.md           # Documentação técnica completa
├── requirements.txt
├── .gitignore
├── interface_grafica/         # Landing page interativa (bonus UX)
│   ├── index.html
│   ├── parte1.html
│   ├── parte2.html
│   └── style.css
├── parte1/                    # Parte 1: Grafo dos Bairros do Recife
│   ├── data/
│   │   ├── bairros_recife.csv
│   │   ├── adjacencias_bairros.csv
│   │   ├── bairros_unique.csv
│   │   └── enderecos.csv
│   ├── out/                   # Arquivos de saída
│   ├── lib/                   # Recursos para visualizações HTML
│   ├── servidor_html.py       # Servidor HTTP para visualizar HTMLs
│   ├── visualizar.py          # Script simplificado para gerar tudo
│   └── src/
│       ├── cli.py             # Interface de linha de comando
│       ├── solve.py            # Orquestração das análises
│       ├── viz.py             # Geração de visualizações
│       └── graphs/
│           ├── graph.py       # Classe Graph
│           ├── algorithms.py  # Algoritmos (BFS, DFS, Dijkstra, Bellman-Ford)
│           └── io.py          # Leitura de dados
├── parte2/                    # Parte 2: Dataset Maior (Voos)
│   ├── data/
│   │   └── voos.csv
│   ├── out/
│   ├── tests/                 # Testes unitários
│   └── src/
│       ├── cli.py
│       └── algorithms2.py
```

## 🎯 Como Executar

### Parte 1: Grafo dos Bairros do Recife

#### ⚡ Forma Mais Rápida: Gerar Tudo e Visualizar

**Comando único para gerar todos os arquivos e iniciar servidor HTTP:**

```bash
cd parte1
python3 -m src.cli --serve
```

Este comando:
- ✅ Gera todas as métricas (globais, microrregiões, ego-subrede)
- ✅ Calcula graus e rankings
- ✅ Calcula distâncias entre endereços
- ✅ Gera todas as visualizações (PNG e HTML)
- ✅ Inicia servidor HTTP na porta 8000

**Acesse os arquivos HTML em:**
- http://localhost:8000/grafo_interativo.html
- http://localhost:8000/arvore_percurso.html
- http://localhost:8000/arvore_bfs_boa_vista.html

**Alternativa usando script auxiliar:**
```bash
cd parte1
python3 visualizar.py
```

#### Executar algoritmo específico

**BFS (Busca em Largura):**
```bash
cd parte1
python3 -m src.cli --alg BFS --source "Boa Vista" --out ./out/
```

**DFS (Busca em Profundidade):**
```bash
python3 -m src.cli --alg DFS --source "Boa Vista" --out ./out/
```

**Dijkstra (Caminho Mínimo):**
```bash
python3 -m src.cli --alg DIJKSTRA --source "Nova Descoberta" --target "Boa Viagem" --out ./out/
```
> O destino Setúbal é representado como `Boa Viagem` na linha de comando; a saída exibe `Boa Viagem (Setúbal)`.

**Bellman-Ford:**
```bash
python3 -m src.cli --alg BELLMAN_FORD --source "Boa Vista" --out ./out/
```

#### Executar todas as análises (sem servidor)

```bash
cd parte1
python3 -m src.cli --out ./out/
```

Isso gera todos os arquivos de saída obrigatórios:
- `out/recife_global.json`
- `out/microrregioes.json`
- `out/ego_bairro.csv`
- `out/graus.csv`
- `out/distancias_enderecos.csv`
- `out/percurso_nova_descoberta_setubal.json`
- `out/arvore_percurso.png` e `.html`
- `out/arvore_bfs_boa_vista.png` e `.html`
- `out/grafo_interativo.html`
- `out/distribuicao_graus.png`
- `out/top10_grau.png`
- `out/densidade_ego_microrregiao.png`
- `out/notas_analiticas.md`

### Parte 2: Dataset de Voos

#### ⚡ Forma Mais Rápida: Rodar toda a Parte 2

```bash
cd parte2
python3 -m src.cli --out ./out/
pytest tests/
```

Este comando:
- ✅ Executa BFS/DFS a partir de `EWR`, `JFK` e `LGA`
- ✅ Roda Dijkstra para os 5 pares obrigatórios
- ✅ Executa Bellman-Ford nos cenários com e sem ciclo negativo
- ✅ Mede tempo e memória de todas as tarefas
- ✅ Gera `out/parte2_report.json` e os gráficos:
  - `grau_distribuicao.png`
  - `top_hubs_grau.png`
  - `histograma_distancias.png`
  - `grau_in_out_scatter.png`
  - `top_rotas_distantes.png`
- ✅ Roda `pytest tests/` para validar BFS, DFS, Dijkstra e Bellman-Ford

#### Executar algoritmo específico

**Dijkstra (Caminho Mínimo):**
```bash
cd parte2
python3 -m src.cli --dataset ./data/voos.csv --alg DIJKSTRA --source EWR --target LAX --out ./out/
```

**BFS (Busca em Largura):**
```bash
python3 -m src.cli --dataset ./data/voos.csv --alg BFS --source EWR --out ./out/
```

**DFS (Busca em Profundidade):**
```bash
python3 -m src.cli --dataset ./data/voos.csv --alg DFS --source EWR --out ./out/
```

**Bellman-Ford:**
```bash
python3 -m src.cli --dataset ./data/voos.csv --alg BELLMAN_FORD --source EWR --out ./out/
```

## 📊 Arquivos de Saída

### Parte 1

| Arquivo | Descrição |
|---------|-----------|
| `recife_global.json` | Métricas globais do grafo (ordem, tamanho, densidade) |
| `microrregioes.json` | Métricas por microrregião |
| `ego_bairro.csv` | Ego-subrede por bairro (grau, ordem_ego, tamanho_ego, densidade_ego) |
| `graus.csv` | Lista de graus por bairro |
| `distancias_enderecos.csv` | Distâncias e caminhos entre pares de endereços |
| `percurso_nova_descoberta_setubal.json` | Caminho de Nova Descoberta para Boa Viagem (Setúbal) |
| `arvore_percurso.png` | Visualização estática da árvore do percurso |
| `arvore_percurso.html` | Visualização interativa da árvore do percurso |
| `grafo_interativo.html` | Grafo completo interativo com tooltips, busca por bairro e caminho destacado |
| `distribuicao_graus.png` | Histograma da distribuição de graus |
| `top10_grau.png` | Top 10 bairros por grau |
| `densidade_ego_microrregiao.png` | Densidade média de ego-rede por microrregião |
| `arvore_bfs_boa_vista.png` | Árvore BFS mostrando camadas a partir de Boa Vista (PNG) |
| `arvore_bfs_boa_vista.html` | Árvore BFS mostrando camadas a partir de Boa Vista (HTML interativo) |
| `notas_analiticas.md` | Documento explicando o que cada visualização revela |

### Parte 2

| Arquivo | Descrição |
|---------|-----------|
| `parte2_report.json` | Relatório completo com métricas de desempenho dos algoritmos |
| `grau_distribuicao.png` | Distribuição de graus do dataset de voos |
| `top_hubs_grau.png` | Top aeroportos com maior grau total |
| `histograma_distancias.png` | Histograma das distâncias das rotas |
| `grau_in_out_scatter.png` | Dispersão grau de saída vs grau de entrada |
| `top_rotas_distantes.png` | Top rotas mais longas em milhas |

## 🌐 Interface Gráfica (Bônus UX)

- Local: `interface_grafica/`
- Arquivos: `index.html`, `parte1.html`, `parte2.html`, `style.css`
- Como visualizar rapidamente:
  ```bash
  cd interface_grafica
  python3 serve.py
  ```
  O script sobe o servidor na raiz do projeto e abre automaticamente `http://localhost:8080/interface_grafica/`.

Principais recursos:
- Hero com métricas do projeto e CTA direto para cada parte
- Timeline de apresentação guiada
- Links rápidos para gráficos, relatórios e documentação técnica
| `top_hubs_grau.png` | Ranking dos aeroportos com maior grau total |
| `histograma_distancias.png` | Histograma das distâncias (pesos) entre aeroportos |

## 🧪 Testes

Execute os testes da Parte 2:

```bash
cd parte2
pytest tests/
```

Os testes verificam:
- **BFS**: Níveis corretos em grafo pequeno
- **DFS**: Detecção de ciclo e classificação de arestas
- **Dijkstra**: Caminhos corretos com pesos ≥ 0
- **Bellman-Ford**: Detecção de ciclos negativos e distâncias corretas

## 🔧 Algoritmos Implementados

Todos os algoritmos foram implementados do zero, sem usar bibliotecas que já os implementam:

- **BFS (Breadth-First Search)**: Busca em largura
- **DFS (Depth-First Search)**: Busca em profundidade com classificação de arestas
- **Dijkstra**: Caminho mínimo com pesos não-negativos
- **Bellman-Ford**: Caminho mínimo com detecção de ciclos negativos

## 📝 Notas Técnicas

### Pesos das Arestas (Parte 1)

Os pesos das arestas no grafo dos bairros do Recife são definidos em `adjacencias_bairros.csv` (coluna `peso`) e seguem a seguinte régua:

| Peso | Tipo de Via | Descrição |
|------|-------------|-----------|
| 1 | Rua | Vias locais, ruas de bairro |
| 2 | Ponte | Travessias sobre rios/canais, viadutos |
| 3 | Avenida | Vias arteriais principais |
| 4 | Rodovia | Rodovias e vias expressas |
| 5 | Estrada | Estradas principais de ligação |

**Fórmula de cálculo**: O peso representa o custo de travessia entre bairros, onde valores menores indicam conexões mais diretas e rápidas. O algoritmo de Dijkstra utiliza esses pesos para encontrar o caminho de menor custo entre dois bairros.

- **Grafo não-direcionado**: Parte 1 usa grafo não-direcionado
- **Grafo dirigido**: Parte 2 usa grafo dirigido (voos)

### Implementação dos Algoritmos

- **BFS/DFS**: Implementados com estruturas de dados básicas (listas, sets)
- **Dijkstra**: Caminho mínimo com pesos não-negativos
- **Bellman-Ford**: Implementado com relaxamento de arestas e detecção de ciclos negativos
- Todos os algoritmos foram implementados do zero, sem usar bibliotecas como networkx, igraph ou graph-tool

### Funcionalidades do Grafo Interativo

O arquivo `grafo_interativo.html` inclui:
- **Tooltip por bairro**: Mostra grau, microrregião e densidade_ego ao passar o mouse
- **Campo de busca**: Permite buscar bairros por nome e destacá-los no grafo
- **Caminho destacado**: O caminho "Nova Descoberta → Boa Viagem (Setúbal)" está destacado em vermelho
- **Controles interativos**: Zoom, arrastar, ajustar física do grafo

## 📚 Documentação

### Documentação Técnica Completa

Consulte `RELATORIO.md` para:
- Manual de uso detalhado
- Documentação técnica dos algoritmos
- Explicação da estrutura do código
- Complexidade dos algoritmos
- Descrição completa dos arquivos de entrada e saída

### Notas Analíticas

O arquivo `parte1/out/notas_analiticas.md` explica o que cada visualização revela sobre o grafo dos bairros do Recife.

## 👥 Autores

- Enzo Nunes: ebn@cesar.school
- Lucas Souto: lsmc2@cesar.school
- Gabriel Antônio: gaor@cesar.school
- Henrique Lobo: hlqg@cesar.school
