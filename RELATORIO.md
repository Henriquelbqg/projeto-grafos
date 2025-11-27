# Projeto Grafos - Relatório Técnico e Manual de Uso

Este relatório concentra instruções de uso, detalhes técnicos e resultados das duas etapas do projeto: **Parte 1** (Grafo dos bairros do Recife) e **Parte 2** (Dataset de voos dos EUA).

---

## Índice Geral

1. [Parte 1 - Grafo dos Bairros do Recife](#parte-1-grafo-dos-bairros-do-recife)
   - [Manual de Uso](#manual-de-uso)
   - [Documentação Técnica](#documentação-técnica)
   - [Algoritmos Implementados](#algoritmos-implementados)
   - [Arquivos de Entrada e Saída](#arquivos-de-entrada-e-saída)
2. [Parte 2 - Dataset de Voos](#parte-2-dataset-de-voos)
   - [Manual de Uso Parte 2](#manual-de-uso-parte-2)
   - [Arquitetura e Código](#arquitetura-e-código-parte-2)
   - [Algoritmos e Métricas](#algoritmos-e-métricas-parte-2)
   - [Dataset e Saídas](#dataset-e-saídas-parte-2)

---

## Parte 1: Grafo dos Bairros do Recife

## Manual de Uso

### Requisitos do Sistema

- **Python 3.11 ou superior**
- Bibliotecas Python (instalar via `pip install -r requirements.txt`):
  - pandas
  - matplotlib
  - pyvis

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Projetos_Grafos-main
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução

#### Opção 1: Gerar Todos os Arquivos da Parte 1

Para gerar todos os arquivos de saída e iniciar o servidor HTTP para visualização:

```bash
cd parte1
python3 -m src.cli --serve
```

Este comando:
- Gera todas as métricas (globais, microrregiões, ego-subrede)
- Calcula graus e rankings
- Calcula distâncias entre endereços
- Gera todas as visualizações (PNG e HTML)
- Inicia servidor HTTP na porta 8000

**Acesse os arquivos HTML em:**
- http://localhost:8000/grafo_interativo.html
- http://localhost:8000/arvore_percurso.html
- http://localhost:8000/arvore_bfs_boa_vista.html

#### Opção 2: Executar Algoritmo Específico

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
> O parâmetro `--target "Boa Viagem"` produz relatórios exibindo **Boa Viagem (Setúbal)**.

**Bellman-Ford:**
```bash
python3 -m src.cli --alg BELLMAN_FORD --source "Boa Vista" --out ./out/
```

### Estrutura de Diretórios

```
parte1/
├── data/                    # Arquivos de entrada
│   ├── bairros_recife.csv   # Dataset original
│   ├── bairros_unique.csv   # Bairros normalizados
│   ├── adjacencias_bairros.csv  # Arestas do grafo
│   └── enderecos.csv        # Pares de endereços para análise
├── out/                     # Arquivos de saída
│   ├── recife_global.json
│   ├── microrregioes.json
│   ├── ego_bairro.csv
│   ├── graus.csv
│   ├── distancias_enderecos.csv
│   ├── percurso_nova_descoberta_setubal.json
│   ├── *.png                # Visualizações estáticas
│   ├── *.html               # Visualizações interativas
│   └── notas_analiticas.md  # Explicações das visualizações
└── src/                     # Código-fonte
    ├── cli.py               # Interface de linha de comando
    ├── solve.py             # Orquestração das análises
    ├── viz.py               # Geração de visualizações
    └── graphs/
        ├── graph.py         # Classe Graph
        ├── algorithms.py    # Algoritmos (BFS, DFS, Dijkstra, Bellman-Ford)
        └── io.py            # Leitura de dados
```

---

## Documentação Técnica

### Estrutura do Código

#### 1. `graphs/graph.py` - Classe Graph

A classe `Graph` implementa uma estrutura de grafo usando lista de adjacências.

**Atributos:**
- `adj`: Dicionário onde cada chave é um vértice e o valor é uma lista de tuplas `(vizinho, peso)`
- `directed`: Boolean indicando se o grafo é direcionado (False para Parte 1)

**Métodos principais:**
- `add_vertex(v)`: Adiciona um vértice ao grafo
- `add_edge(u, v, weight, directed)`: Adiciona aresta entre u e v com peso
- `neighbors(v)`: Retorna lista de vizinhos de v com seus pesos
- `vertices()`: Retorna lista de todos os vértices
- `edges()`: Retorna lista de todas as arestas

**Características:**
- Para grafos não-direcionados (Parte 1), cada aresta é adicionada bidirecionalmente
- Suporta pesos nas arestas
- Implementação eficiente para grafos esparsos

#### 2. `graphs/io.py` - Leitura de Dados

**Funções principais:**
- `load_nodes(graph, path)`: Carrega nós do CSV `bairros_unique.csv`
- `load_edges(graph, path)`: Carrega arestas do CSV `adjacencias_bairros.csv`
- `build_graph()`: Constrói o grafo completo dos bairros do Recife

**Normalização:**
- Normaliza nomes de bairros (capitalização, remoção de espaços)
- Usa "Boa Viagem" como nó canônico para Setúbal e exibe "Boa Viagem (Setúbal)" nas saídas

#### 3. `graphs/algorithms.py` - Implementação dos Algoritmos

Todos os algoritmos foram implementados manualmente, sem usar bibliotecas externas.

#### 4. `solve.py` - Orquestração

Contém funções que orquestram as análises:
- `run_metricas_globais()`: Calcula métricas do grafo completo
- `run_metricas_microrregioes()`: Calcula métricas por microrregião
- `run_ego_bairros()`: Calcula ego-subrede para cada bairro
- `run_graus()`: Calcula grau de cada bairro
- `run_dist_enderecos()`: Calcula distâncias entre endereços usando Dijkstra
- `run_percurso_nova_descoberta_setubal()`: Calcula caminho específico
- `run_arvore_percurso()`: Gera visualizações da árvore do percurso
- `run_grafo_interativo()`: Gera grafo interativo HTML
- `run_arvore_bfs()`: Gera árvore BFS com camadas

#### 5. `viz.py` - Visualizações

Funções para gerar visualizações:
- `gerar_distribuicao_graus()`: Histograma de distribuição de graus
- `gerar_top10_grau()`: Gráfico de barras dos 10 bairros com maior grau
- `gerar_densidade_ego_microrregiao()`: Gráfico de densidade por microrregião
- `gerar_arvore_percurso_png()`: Árvore do percurso em PNG (matplotlib)
- `gerar_arvore_percurso_html()`: Árvore do percurso em HTML (pyvis)
- `gerar_grafo_interativo()`: Grafo completo interativo com busca
- `gerar_arvore_bfs()`: Árvore BFS com camadas (PNG e HTML)

---

## Algoritmos Implementados

### 1. BFS (Breadth-First Search) - Busca em Largura

**Localização:** `graphs/algorithms.py`, função `bfs()`

**Descrição:**
Algoritmo de busca em largura que explora o grafo nível por nível, começando de um vértice origem.

**Implementação:**
```python
def bfs(graph, source):
    visited = set()
    queue = [source]  # Fila FIFO
    ordem = []
    camadas = {source: 0}
    
    while queue:
        u = queue.pop(0)  # Remove primeiro elemento
        ordem.append(u)
        
        for v, _ in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                camadas[v] = camadas[u] + 1
                queue.append(v)
```

**Características:**
- Usa fila (lista Python) para manter ordem de visitação
- Calcula camadas (níveis) de cada vértice
- Detecta ciclos em grafos não-direcionados
- Complexidade: O(V + E) onde V = vértices, E = arestas

**Retorno:**
- `ordem`: Lista de vértices na ordem de visitação
- `camadas`: Dicionário vértice → nível
- `ciclos`: Lista de arestas que formam ciclos

### 2. DFS (Depth-First Search) - Busca em Profundidade

**Localização:** `graphs/algorithms.py`, função `dfs()`

**Descrição:**
Algoritmo de busca em profundidade que explora o grafo seguindo um caminho até o fim antes de retroceder.

**Implementação:**
```python
def dfs(graph, source):
    visited = set()
    ordem = []
    ciclos = []
    arestas_class = []  # (u, v, tipo)
    
    def dfs_visit(u, parent):
        visited.add(u)
        ordem.append(u)
        
        for v, _ in graph.neighbors(u):
            if v not in visited:
                arestas_class.append((u, v, "tree"))
                dfs_visit(v, u)  # Recursão
            else:
                if v != parent:
                    ciclos.append((u, v))
                    arestas_class.append((u, v, "back"))
    
    dfs_visit(source, None)
```

**Características:**
- Implementação recursiva
- Classifica arestas em "tree" (arestas da árvore) e "back" (arestas de retorno/ciclo)
- Detecta ciclos em grafos não-direcionados
- Complexidade: O(V + E)

**Retorno:**
- `ordem`: Lista de vértices na ordem de visitação
- `ciclos`: Lista de arestas que formam ciclos
- `arestas_class`: Lista de arestas classificadas

### 3. Dijkstra - Caminho Mínimo

**Localização:** `graphs/algorithms.py`, função `dijkstra()`

**Descrição:**
Algoritmo para encontrar o caminho de menor custo entre dois vértices em um grafo com pesos não-negativos.

**Implementação:**
```python
def dijkstra(graph, origem, destino):
    dist = {v: float('inf') for v in graph.vertices()}
    dist[origem] = 0
    parent = {v: None for v in graph.vertices()}
    nao_visitados = set(graph.vertices())
    
    while nao_visitados:
        # Busca linear do mínimo (sem heapq)
        u = None
        menor_dist = float('inf')
        for v in nao_visitados:
            if dist[v] < menor_dist:
                menor_dist = dist[v]
                u = v
        
        if u is None or menor_dist == float('inf'):
            break
        
        nao_visitados.remove(u)
        
        if u == destino:
            break
        
        # Relaxar arestas
        for (v, peso) in graph.neighbors(u):
            if v not in nao_visitados:
                continue
            novo_custo = dist[u] + peso
            if novo_custo < dist[v]:
                dist[v] = novo_custo
                parent[v] = u
    
    # Reconstruir caminho
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = parent[atual]
    caminho.reverse()
    
    return dist[destino], caminho
```

**Características:**
- **Implementação sem heapq**: Usa busca linear para encontrar o mínimo (conforme requisito)
- Funciona apenas com pesos não-negativos
- Para quando encontra o destino (otimização)
- Complexidade: O(V² + E) com busca linear (O(V log V + E) com heap)

**Retorno:**
- Tupla `(distancia, caminho)` onde:
  - `distancia`: Custo total do caminho mínimo
  - `caminho`: Lista de vértices do caminho

### 4. Bellman-Ford - Caminho Mínimo com Detecção de Ciclos Negativos

**Localização:** `graphs/algorithms.py`, função `bellman_ford()`

**Descrição:**
Algoritmo para encontrar caminhos mínimos que funciona com pesos negativos e detecta ciclos negativos.

**Implementação:**
```python
def bellman_ford(graph, origem):
    dist = {v: float("inf") for v in graph.vertices()}
    pai = {v: None for v in graph.vertices()}
    dist[origem] = 0.0
    
    # Montar lista de arestas
    edges = []
    for u in graph.vertices():
        for (v, peso) in graph.neighbors(u):
            edges.append((u, v, peso))
    
    # Relaxamento (|V|-1) vezes
    for _ in range(len(graph.vertices()) - 1):
        alterou = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pai[v] = u
                alterou = True
        if not alterou:
            break  # Otimização: para se não houve mudanças
    
    # Verificação de ciclo negativo
    ciclo_negativo = False
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            ciclo_negativo = True
            break
    
    return dist, pai, ciclo_negativo
```

**Características:**
- Funciona com pesos negativos
- Detecta ciclos negativos
- Relaxa arestas (|V|-1) vezes
- Complexidade: O(V × E)

**Retorno:**
- Tupla `(dist, pai, ciclo_negativo)` onde:
  - `dist`: Dicionário de distâncias mínimas
  - `pai`: Dicionário de predecessores (para reconstruir caminhos)
  - `ciclo_negativo`: Boolean indicando se há ciclo negativo

---

## Arquivos de Entrada e Saída

### Arquivos de Entrada (`data/`)

#### `bairros_recife.csv`
Dataset original com colunas "1.1" a "6.3" contendo bairros agrupados por microrregiões.

#### `bairros_unique.csv`
Bairros normalizados e únicos. Formato:
```
microrregiao,bairro
1,Boa Vista
1,Cabanga
...
```

#### `adjacencias_bairros.csv`
Arestas do grafo. Formato:
```
bairro_origem,bairro_destino,logradouro,observacao,peso
Boa Vista,Ilha Do Leite, R. Marques de Amorim,,1
Boa Vista,Derby, Av. Gov. Carlos de Lima Cavalcanti,,3
...
```

**Régua de Pesos:**
- 1 = Rua (vias locais)
- 2 = Ponte (travessias, viadutos)
- 3 = Avenida (vias arteriais principais)
- 4 = Rodovia (vias expressas)
- 5 = Estrada (estradas principais)

#### `enderecos.csv`
Pares de endereços para análise. Formato:
```
X,Y,bairro_X,bairro_Y
 Rua Nova Descoberta 500,Rua Baltazar Passos 50,Nova Descoberta,Boa Viagem (Setúbal)
...
```

### Arquivos de Saída (`out/`)

#### `recife_global.json`
Métricas globais do grafo:
```json
{
    "ordem": 94,
    "tamanho": 237,
    "densidade": 0.05422100205902539
}
```

#### `microrregioes.json`
Métricas por microrregião:
```json
[
    {
        "microrregiao": 1,
        "ordem": 11,
        "tamanho": 21,
        "densidade": 0.38181818181818183,
        "bairros": ["Boa Vista", "Cabanga", ...]
    },
    ...
]
```

#### `ego_bairro.csv`
Ego-subrede por bairro:
```
bairro,grau,ordem_ego,tamanho_ego,densidade_ego
Boa Vista,10,11,21,0.38181818181818183
...
```

#### `graus.csv`
Grau de cada bairro:
```
bairro,grau
Boa Vista,10
...
```

#### `distancias_enderecos.csv`
Distâncias e caminhos entre endereços:
```
X,Y,bairro_X,bairro_Y,custo,caminho
 Rua Nova Descoberta 500,Rua Baltazar Passos 50,Nova Descoberta,Boa Viagem (Setúbal),9.0,Nova Descoberta -> ... -> Boa Viagem (Setúbal)
...
```

#### `percurso_nova_descoberta_setubal.json`
Caminho específico Nova Descoberta → Boa Viagem (Setúbal):
```json
{
    "origem": "Nova Descoberta",
    "destino": "Boa Viagem (Setúbal)",
    "custo": 9.0,
    "caminho_display": ["Nova Descoberta", "Alto Do Mandu", ..., "Boa Viagem (Setúbal)"]
}
```

#### Visualizações

**PNG (matplotlib):**
- `distribuicao_graus.png`: Histograma da distribuição de graus
- `top10_grau.png`: Top 10 bairros por grau
- `densidade_ego_microrregiao.png`: Densidade média por microrregião
- `arvore_percurso.png`: Árvore do percurso estática
- `arvore_bfs_boa_vista.png`: Árvore BFS com camadas

**HTML (pyvis):**
- `grafo_interativo.html`: Grafo completo com:
  - Tooltip por bairro (grau, microrregião, densidade_ego)
  - Campo de busca por bairro
  - Caminho "Nova Descoberta → Boa Viagem (Setúbal)" destacado em vermelho
- `arvore_percurso.html`: Árvore do percurso interativa
- `arvore_bfs_boa_vista.html`: Árvore BFS interativa

#### `notas_analiticas.md`
Documento explicando o que cada visualização revela sobre o grafo.

---

## Parte 2: Dataset de Voos

### Manual de Uso Parte 2

1. **Preparação do ambiente**  
   ```bash
   cd parte2
   source ../.venv/bin/activate  # se ainda não estiver ativo
   ```

2. **Execução completa (relatório, métricas e gráficos):**
   ```bash
   python3 -m src.cli --out ./out/
   ```
   O comando carrega `data/voos.csv`, executa todas as análises, gera `out/parte2_report.json` e salva as visualizações PNG.

3. **Algoritmos específicos:**
   - BFS: `python3 -m src.cli --alg BFS --source EWR --out ./out/`
   - DFS: `python3 -m src.cli --alg DFS --source EWR --out ./out/`
   - Dijkstra: `python3 -m src.cli --alg DIJKSTRA --source EWR --target LAX --out ./out/`
   - Bellman-Ford: `python3 -m src.cli --alg BELLMAN_FORD --source EWR --out ./out/`

4. **Testes automatizados:**  
   ```bash
   pytest tests/
   ```
   Executa casos unitários cobrindo BFS, DFS, Dijkstra e Bellman-Ford em cenários direcionados.

### Arquitetura e Código Parte 2

- `src/cli.py`: Interface de linha de comando que valida argumentos, configura diretórios e delega execuções pontuais ou a análise completa.
- `src/algorithms2.py`:
  - `DiGraph`: especialização dirigida da classe `Graph` da Parte 1, reutilizando toda a infraestrutura.
  - `carregar_grafo_voos()`: lê `data/voos.csv` (colunas `ORIGIN`, `DEST`, `DISTANCE`) e monta o grafo dirigido ponderado.
  - `rodar_analise_parte2()`: orquestra BFS/DFS para `EWR`, `JFK`, `LGA`, roda Dijkstra para 5 pares, Bellman-Ford para múltiplas fontes, mede tempo/memória e gera `parte2_report.json`.
  - Funções auxiliares para gráficos (`gerar_distribuicao_grau_voos`, `gerar_top_hubs_voos`, `gerar_histograma_distancias_voos`, `gerar_disp_grau_in_out_voos`, `gerar_top_rotas_distantes`).
- `tests/`: suíte `pytest` que garante a corretude dos algoritmos com grafos de voo reduzidos e cenários sintéticos com ciclo negativo.

### Algoritmos e Métricas Parte 2

- **BFS/DFS**: reutilizam as implementações da Parte 1, agora explorando grafo direcionado; o relatório registra ordem de visitação, camadas e ciclos detectados por fonte.
- **Dijkstra**: calcula caminhos mínimos entre pares de hubs obrigatórios (`EWR`, `JFK`, `LGA`, `SFO`, `LAX`, `ATL`, `MIA`), registrando custo, caminho reconstruído, tempo e memória.
- **Bellman-Ford**: roda em duas configurações (grafo real e cenários artificiais com ciclo negativo) para validar estabilidade com pesos positivos e negativos.
- **Métricas globais**: número de vértices/arestas, pares direcionados únicos, estatísticas de grau (mínimo, máximo, média, mediana), top hubs e distribuição de distâncias.
- **Monitoramento de desempenho**: `rodar_analise_parte2()` usa `tracemalloc` e `time.perf_counter()` para anexar consumo de memória (KB) e tempo (s) por tarefa, facilitando comparações entre algoritmos.

### Dataset e Saídas Parte 2

- **Dataset `data/voos.csv`:**
  - Colunas principais: `ORIGIN`, `DEST`, `DISTANCE`.
  - Mais de 300 rotas direcionadas entre aeroportos norte-americanos, com pesos em milhas.
  - Durante a carga, pares inválidos são ignorados e distâncias são convertidas para `float`.

- **Arquivos gerados em `parte2/out/`:**
  - `parte2_report.json`: resumo completo das métricas, execuções e resultados dos algoritmos.
  - `grau_distribuicao.png`: histograma do grau total (entrada+saída).
  - `top_hubs_grau.png`: ranking de hubs com maior conectividade.
  - `histograma_distancias.png`: distribuição de distâncias das rotas.
  - `grau_in_out_scatter.png`: correlação entre graus de entrada e saída (tamanho proporcional ao grau total).
  - `top_rotas_distantes.png`: barras horizontais com as rotas mais longas.

---

## Considerações Técnicas

### Complexidade dos Algoritmos

| Algoritmo | Complexidade | Observação |
|-----------|--------------|------------|
| BFS | O(V + E) | Ótima para grafos esparsos |
| DFS | O(V + E) | Ótima para grafos esparsos |
| Dijkstra | O(V² + E) | Com busca linear (sem heap) |
| Bellman-Ford | O(V × E) | Funciona com pesos negativos |

### Estrutura de Dados

- **Lista de Adjacências**: Usada para representar o grafo
  - Vantagem: Eficiente para grafos esparsos
  - Espaço: O(V + E)
  - Acesso a vizinhos: O(grau do vértice)

### Normalização de Dados

- Nomes de bairros são normalizados (capitalização, remoção de espaços)
- "Setúbal" é tratado como "Boa Viagem" no grafo e rotulado como "Boa Viagem (Setúbal)" para o usuário
- Acentuação é preservada

### Tratamento de Casos Especiais

- Grafo vazio: Densidade = 0
- Vértice isolado: Densidade = 0
- Caminho inexistente: Dijkstra retorna `float('inf')`
- Ciclos negativos: Bellman-Ford detecta e retorna flag

---

## Conclusão

Este projeto implementa algoritmos fundamentais de grafos (BFS, DFS, Dijkstra, Bellman-Ford) do zero, sem usar bibliotecas que já os implementam. As aplicações práticas cobrem:

- **Parte 1:** análise do grafo dos bairros do Recife, com métricas globais/locais, caminhos mínimos e visualizações interativas/estáticas.
- **Parte 2:** exploração de um grafo dirigido de voos, avaliando hubs, rotas críticas, distribuição de distâncias e desempenho dos algoritmos em um dataset maior.

Ambas as etapas possuem documentação, relatórios e scripts reproduzíveis, permitindo replicar resultados e estender o trabalho para novas fontes de dados.

---

**Versão:** 1.0  
**Data:** 2025  
**Python:** 3.11+

