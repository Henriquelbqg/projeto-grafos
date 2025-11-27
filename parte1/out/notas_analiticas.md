# Notas Analíticas - Visualizações do Grafo dos Bairros do Recife

Este documento explica o que cada visualização revela sobre a estrutura e características do grafo dos bairros do Recife.

## 1. Distribuição dos Graus (`distribuicao_graus.png`)

**O que revela:**
- Mostra a distribuição do número de conexões (grau) que cada bairro possui no grafo.
- Permite identificar se o grafo segue uma distribuição homogênea ou se há bairros com muitas conexões (hubs) e outros com poucas conexões.
- Bairros com grau alto são pontos centrais na rede de interconexões, enquanto bairros com grau baixo são mais periféricos.

**Insights esperados:**
- Se a distribuição for assimétrica (poucos bairros com muitos graus, muitos com poucos), indica uma estrutura de "small-world" ou "scale-free".
- Bairros centrais (alto grau) são geralmente aqueles com melhor infraestrutura viária e localização estratégica.

## 2. Top 10 Bairros por Grau (`top10_grau.png`)

**O que revela:**
- Identifica os bairros mais conectados do Recife, ou seja, aqueles que têm o maior número de interconexões diretas com outros bairros.
- Esses bairros funcionam como "hubs" na rede urbana, sendo pontos de passagem importantes para deslocamentos.

**Insights esperados:**
- Bairros com maior grau são geralmente centrais, com boa infraestrutura viária e múltiplas opções de acesso.
- Esses bairros tendem a ter maior densidade de tráfego e são estratégicos para planejamento urbano.

## 3. Densidade Média da Ego-Rede por Microrregião (`densidade_ego_microrregiao.png`)

**O que revela:**
- Mostra o quão interconectados são os bairros dentro de cada microrregião.
- A densidade da ego-rede mede quantas conexões existem entre os vizinhos diretos de um bairro, indicando a "coesão" da região.

**Insights esperados:**
- Microrregiões com alta densidade ego indicam que os bairros dentro dela estão bem conectados entre si, formando uma rede mais coesa.
- Baixa densidade ego pode indicar que os bairros de uma microrregião dependem mais de conexões externas para se comunicar.

## 4. Árvore do Percurso: Nova Descoberta → Boa Viagem (`arvore_percurso.png` e `arvore_percurso.html`)

**O que revela:**
- Visualiza o caminho mínimo calculado pelo algoritmo de Dijkstra entre dois bairros específicos.
- Mostra a sequência de bairros que devem ser percorridos para ir de um ponto a outro com menor custo (considerando os pesos das arestas).

**Insights esperados:**
- Permite entender a rota mais eficiente entre dois pontos da cidade.
- O número de bairros no caminho e o custo total revelam a acessibilidade entre diferentes regiões.
- Caminhos longos podem indicar necessidade de melhorias na infraestrutura viária.

## 5. Árvore BFS: Boa Vista (`arvore_bfs_boa_vista.png` e `arvore_bfs_boa_vista.html`)

**O que revela:**
- Mostra a estrutura hierárquica de camadas (níveis) alcançáveis a partir do bairro "Boa Vista" usando busca em largura (BFS).
- Cada camada representa bairros que estão à mesma distância topológica (número de arestas) do bairro origem.

**Insights esperados:**
- Permite visualizar o "raio de influência" de um bairro central.
- Camadas próximas (1-2) indicam bairros facilmente acessíveis.
- A distribuição de bairros por camada revela a centralidade do bairro origem na rede.
- Bairros em camadas distantes podem ter dificuldades de acesso a partir do polo.

## 6. Grafo Interativo (`grafo_interativo.html`)

**O que revela:**
- Visualização completa e interativa de todo o grafo dos bairros do Recife.
- Permite explorar as conexões entre todos os bairros, visualizar métricas por bairro (grau, microrregião, densidade ego) e destacar caminhos específicos.

**Insights esperados:**
- Facilita a exploração visual da estrutura geral da rede.
- A busca por bairro permite análise focada em regiões específicas.
- O realce do caminho Nova Descoberta → Boa Viagem mostra como diferentes partes da cidade se conectam.
- A cor e tamanho dos nós revelam padrões de centralidade e importância na rede.

## Métricas Complementares

### Bairro com Maior Grau
- Indica o bairro mais central na rede, com maior número de conexões diretas.
- Geralmente corresponde a bairros com infraestrutura viária desenvolvida e localização estratégica.

### Bairro Mais Denso (maior densidade_ego)
- Indica o bairro cujos vizinhos estão mais interconectados entre si.
- Sugere uma região com alta coesão local, onde os bairros adjacentes formam uma rede bem integrada.

## Conclusão

As visualizações em conjunto revelam:
- **Estrutura da rede**: Se é centralizada (poucos hubs) ou distribuída (muitos nós com grau similar).
- **Acessibilidade**: Quais bairros são mais fáceis de alcançar a partir de pontos centrais.
- **Coesão regional**: Como os bairros se agrupam e se conectam dentro das microrregiões.
- **Rotas eficientes**: Caminhos mínimos entre pontos importantes da cidade.

Essas análises são úteis para:
- Planejamento urbano e de transporte
- Identificação de gargalos na rede viária
- Análise de centralidade e importância de bairros
- Planejamento de rotas e logística

