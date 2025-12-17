# 🚚 Suzano Routing Challenge - Sistema de Otimização de Promotores

Este repositório contém as soluções desenvolvidas para o **Desafio UNIFESP - Bens de Consumo (Suzano)**. O projeto implementa um sistema robusto para a alocação e roteamento de promotores de vendas, combinando **Meta-heurísticas (Framework RKO)** e **Programação Linear Inteira Mista (AMPL/Gurobi)**.

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Method](https://img.shields.io/badge/Optimization-Metaheuristics%20%26%20MILP-orange)

## 📌 Descrição do Problema

A empresa possui um conjunto de lojas distribuídas geograficamente que precisam ser visitadas por promotores. O desafio central é maximizar o **Lucro Líquido** (Receita das visitas - Custos Operacionais), resolvendo os seguintes subproblemas:

1.  **Alocação:** Atribuir cada loja a um único promotor.
2.  **Nível de Serviço:** Definir a frequência de visitas semanais (1 a 6 vezes) baseando-se na curva de rentabilidade de cada loja (Fase 2).
3.  **Agendamento:** Programar em quais dias da semana as visitas ocorrem.
4.  **Roteamento:** Otimizar as rotas diárias para minimizar deslocamento (TSP).

### Fases do Desafio
* **Fase 1 (Frequência Fixa):** As lojas possuem uma frequência de visita pré-definida. O foco é minimizar custos (número de promotores, distância e horas extras) respeitando a jornada de trabalho.
* **Fase 2 (Frequência Ótima):** O modelo decide a frequência ideal de visitas para equilibrar o lucro gerado versus o custo operacional da visita.

---

## 🚀 Arquitetura da Solução

Este projeto explora duas abordagens distintas para resolver o problema:

### Abordagem A: Framework RKO (Meta-heurísticas)
Utiliza o *Random-Key Optimizer* para explorar o espaço de soluções através de algoritmos evolutivos.

* **Arquivos Principais:**
    * `RKO_Base.py`: Solve para a Fase 1.
    * `RKO_freq.py`: Solve para a Fase 2 (Otimização estocástica pura).
    * `RKO_Freq_clusters.py` 🏆: Solução final híbrida que aplica **K-Means** antes da otimização para garantir regiões geográficas coesas.
* **Algoritmos:** BRKGA, SA (Simulated Annealing), ILS, LNS, PSO, GA e VNS rodando em paralelo.

### Abordagem B: Modelo Matemático & Heurística (AMPL + LNS)
Combina a precisão de solvers matemáticos com a velocidade de busca local.

* **Arquivos Principais:** `modelo_promotores_estendido.mod`, `modelo_roteamento_tsp.mod`.
* **Mecânica:**
    1.  **Clusterização:** K-Means Constrained (10-15 lojas/cluster).
    2.  **Solução Inicial (S0):** Resolve cada cluster via Gurobi (MIP).
    3.  **Melhoria (LNS+SA):** Aplica lógica *Destroy & Repair* para reotimizar grupos de lojas e vizinhos.
    4.  **Roteamento Final:** Aplica TSP (Traveling Salesperson Problem) para ordenar as visitas.



---

## 🛠️ Detalhes Técnicos: Abordagem AMPL (Modelo Matemático)

### 1. Modelo de Alocação (`modelo_promotores_estendido.mod`)

**Função Objetivo:**
Maximizar `Lucro Total = Receita - (Custo Fixo + Custo Deslocamento + Custo HE + Penalidades)`

**Parâmetros de Custo:**
* Custo fixo por promotor: R$ 750,00
* Custo de deslocamento: R$ 0,06/unidade
* Custo de hora extra: R$ 20,45/minuto
* Penalidade desbalanceamento: R$ 5,00/minuto de desvio

**Variáveis de Decisão:**
* `r[i]`: Binária. 1 se o promotor *i* for contratado.
* `c[i,j]`: Binária. 1 se o promotor *i* atende a loja *j*.
* `v[i,j,d]`: Binária. 1 se o promotor *i* visita a loja *j* no dia *d*.
* `z[j,f]`: Binária. 1 se a loja *j* recebe a frequência *f*.
* `h[i,d]`: Contínua. Horas extras do promotor *i* no dia *d*.

**Restrições Principais:**
* Atribuição única de loja por promotor.
* Jornada diária (480 min seg-sex, 240 min sábado).
* Limite de carteira (máx. 8 lojas/promotor).
* Consistência entre frequência escolhida e total de visitas.

### 2. Otimização LNS + Simulated Annealing
Para refinar a solução do solver:
* **Destroy:** Seleciona uma loja pivô e libera as $N$ lojas mais próximas.
* **Repair:** Fixa as demais e resolve o modelo AMPL apenas para as lojas liberadas.
* **Critério de Aceite (SA):** Aceita soluções piores com probabilidade baseada na temperatura $T$ e no $\Delta$ do lucro, evitando ótimos locais.

### 3. Otimização de Rotas (TSP)
Modelo `modelo_roteamento_tsp.mod` implementa o problema do caixeiro viajante com caminho aberto (sem retorno obrigatório ao início) e eliminação de subciclos via MTZ, garantindo a menor distância percorrida por dia.

---

## 📊 Visualização dos Resultados

### Comparativo Visual (RKO)
O impacto da clusterização na organização das rotas na Abordagem A:

| Sem Clusterização (`RKO_freq.py`) | Com Clusterização (`RKO_freq_clusters.py`) |
|:---:|:---:|
|  |  |
| *Rotas cruzadas e dispersas* | *Regiões definidas e rotas locais* |

### Exemplo de Saída Financeira
```text
============================================================
             DEMONSTRATIVO FINANCEIRO          
============================================================
RECEITAS:
   - Frequências definidas (Fase 1):   R$ 22,150.00
   - Frequências otimizadas (Fase 2):  R$ 29,819.64
------------------------------------------------------------
CUSTOS OPERACIONAIS:
   - Equipe (22 pessoas):              R$ 16,500.00
   - Combustível (1240 un):            R$ 74.40
   - Horas Extras (120 min):           R$ 40.90
   ---------------------------------------------
   TOTAL CUSTOS:                       R$ 16,615.30
------------------------------------------------------------
LUCRO LÍQUIDO (FASE 2):                R$ 13,204.34
