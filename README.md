# Modelo Heuristico - Alocacao de Promotores de Vendas

Sistema de otimizacao para alocacao de promotores de vendas em lojas, combinando programacao linear inteira mista com metaheuristicas.

## Descricao do Problema

O modelo resolve o problema de:
- Alocar lojas a promotores de vendas
- Definir a frequencia de visitas semanais para cada loja
- Programar as visitas diarias
- Otimizar as rotas de deslocamento

## Estrutura do Codigo

### 1. Modelo AMPL

O modelo de otimizacao (`modelo_promotores_estendido.mod`) define:

**Conjuntos:**
- PROMOTORES: Promotores disponiveis
- LOJAS: Lojas a visitar
- DIAS: Dias da semana (1 a 6)
- FREQ_POSSIVEIS: Opcoes de frequencia de visita (1 a 6)

**Variaveis de Decisao:**
- `r[i]`: 1 se o promotor i for contratado
- `c[i,j]`: 1 se o promotor i atende a loja j
- `v[i,j,d]`: 1 se o promotor i visita a loja j no dia d
- `z[j,f]`: 1 se a loja j recebe frequencia f de visitas
- `h[i,d]`: Horas extras do promotor i no dia d

**Funcao Objetivo:**
Maximizar lucro total = Receita - Custos

Onde os custos incluem:
- Custo fixo por promotor (R$ 750)
- Custo de deslocamento (R$ 0.06/unidade)
- Custo de hora extra (R$ 20.45/minuto)
- Penalidade por desbalanceamento de carga (R$ 5.0/minuto de desvio)

**Restricoes:**
- Cada loja atribuida a exatamente um promotor
- Jornada diaria (480 min seg-sex, 240 min sabado)
- Limite de 8 lojas por promotor
- Frequencia minima de visitas respeitada
- Consistencia entre frequencia escolhida e visitas realizadas

### 2. Clusterizacao K-Means

Utiliza K-Means Constrained para agrupar lojas geograficamente:
- Tamanho minimo por cluster: 10 lojas
- Tamanho maximo por cluster: 15 lojas
- Gera arquivos `.dat` para cada cluster

### 3. Solucao Inicial (S0)

Resolve cada cluster independentemente com o solver Gurobi:
- MIP gap: 1%
- Tempo limite: 60 segundos por cluster
- Atribui IDs globais unicos aos promotores

### 4. LNS + Simulated Annealing

**Funcao Destroy:**
- Seleciona uma loja pivo aleatoria
- Libera as N lojas mais proximas geograficamente (padrao: 10 lojas)

**Funcao Repair:**
- Fixa as lojas nao liberadas aos seus promotores atuais
- Resolve o modelo AMPL para reotimizar as lojas liberadas

**Criterios de Aceitacao (SA):**
- Solucoes melhores: sempre aceitas
- Solucoes equivalentes: aceitas
- Solucoes piores: aceitas com probabilidade exp(delta/T)

**Criterios de Parada:**
- Maximo de iteracoes sem melhora: max(10, 25% do numero de lojas)
- Tempo maximo: 20 minutos
- Temperatura final atingida

**Parametros SA:**
- Temperatura inicial: 10% do lucro inicial
- Temperatura final: 0.1
- Taxa de resfriamento: calculada para atingir T_final em N iteracoes

### 5. TSP - Otimizacao de Rotas

Modelo de roteamento (`modelo_roteamento_tsp.mod`) para caminho aberto:
- Minimiza distancia total percorrida
- Sem retorno ao ponto inicial
- Eliminacao de subciclos via MTZ

Para cada promotor e cada dia:
- Extrai as lojas programadas
- Resolve TSP para ordenar a rota
- Calcula distancia otimizada

### 6. Relatorios de Saida

**Relatorio TXT (`relatorio_final_completo.txt`):**
- Resumo executivo com lucros
- Detalhamento de receitas e custos
- Indicadores operacionais
- Agenda semanal por promotor
- Detalhamento por loja
- Analise de frequencias

**Relatorio Excel (`resultado_otimizacao_heuristica.xlsx`):**
- Relatorio por loja
- Validacoes de restricoes:
  - Jornada diaria
  - Limite de carteira
  - Frequencia minima
  - Alocacao unica
  - Consistencia de visitas
  - Visita pelo promotor responsavel
  - Distancias TSP
- Detalhamento diario com distancias por loja

## Dependencias

```
k-means-constrained
amplpy
pandas
numpy
scipy
openpyxl
```

Solvers AMPL:
- Gurobi (principal)
- HiGHS, CBC, CPLEX (alternativos)

## Entrada de Dados

Arquivo CSV com as colunas:
- `x_coordinate`: Coordenada X da loja
- `y_coordinate`: Coordenada Y da loja
- `visit_duration_minutes`: Tempo de visita em minutos
- `initial_frequency`: Frequencia minima de visitas
- `type`: Tipo da loja (P, M, G)
- `profitability_freq_1` a `profitability_freq_6`: Lucro potencial por frequencia
- `baseline_profitability`: Lucratividade base

## Parametros Configuraveis

| Parametro | Valor Padrao | Descricao |
|-----------|--------------|-----------|
| max_lojas | 8 | Maximo de lojas por promotor |
| P_rep | 750 | Custo fixo por promotor |
| P_dist | 0.06 | Custo por unidade de distancia |
| P_he | 20.45 | Custo por minuto de hora extra |
| PB | 5.0 | Penalidade por desbalanceamento |
| N_LOJAS_PARA_LIBERAR | 10 | Lojas liberadas por iteracao LNS |
| TIMELIMIT_REPARO | 60 | Tempo limite do repair (segundos) |
| TEMPO_MAXIMO_LNS | 1200 | Tempo maximo total LNS (segundos) |
| MIP_GAP | 0.01 | Gap de otimalidade |

## Fluxo de Execucao

1. Carregar dados do CSV
2. Clusterizar lojas com K-Means
3. Gerar arquivos .dat por cluster
4. Resolver cada cluster (Solucao S0)
5. Executar loop LNS+SA para melhoria
6. Renumerar promotores sequencialmente
7. Extrair variaveis do modelo final
8. Resolver TSP para cada promotor/dia
9. Calcular lucro final com rotas otimizadas
10. Gerar relatorios TXT e Excel

## Saidas

- `modelo_promotores_estendido.mod`: Modelo AMPL de alocacao
- `modelo_roteamento_tsp.mod`: Modelo AMPL de roteamento
- `dados_cluster_*.dat`: Dados por cluster
- `dados_LNS_repair_temp.dat`: Dados temporarios do LNS
- `tsp_promotor*_dia*.dat`: Dados temporarios do TSP
- `relatorio_final_completo.txt`: Relatorio textual
- `resultado_otimizacao_heuristica.xlsx`: Relatorio Excel com validacoes
