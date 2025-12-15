# 🚚 Suzano Routing Challenge - Otimização de Promotores

Este repositório contém a solução desenvolvida para o **Desafio UNIFESP - Bens de Consumo (Suzano)**. O objetivo é otimizar a alocação e o roteamento de promotores de vendas, maximizando a rentabilidade das visitas e minimizando custos operacionais (deslocamento, horas extras e desbalanceamento de carga), utilizando o framework **RKO (Random-Key Optimizer)**.

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Method](https://img.shields.io/badge/Optimization-Metaheuristics-orange)

## 📌 O Problema

A empresa possui um conjunto de lojas distribuídas geograficamente que precisam ser visitadas por promotores. O desafio é dividido em duas fases:

1.  **Fase 1 (Frequência Fixa):** As lojas possuem uma frequência de visita semanal pré-definida. O objetivo é criar rotas que caibam na jornada de trabalho (Seg-Sáb) minimizando custos.
2.  **Fase 2 (Frequência Ótima):** O modelo deve **decidir** a frequência de visita (1 a 6 vezes/semana) baseando-se na curva de rentabilidade de cada loja. Deve-se encontrar o equilíbrio ótimo entre o lucro gerado pela visita e o custo operacional de realizá-la.

## 🚀 Abordagens e Arquivos

A solução evoluiu em três etapas principais, representadas pelos seguintes scripts:

### 1. `RKO_Fase1.py` (Fase 1)
Solução inicial para o problema de **Frequências Fixas**.
- **Foco:** Minimizar número de promotores, distância e horas extras.
- **Entrada:** Frequência de visitas é dada (imutável).
- **Mecânica:** O RKO define a ordem das visitas e a alocação dos promotores.

### 2. `RKO_Fase2.py` (Fase 2 - Pura)
Evolução para o problema de **Frequências Dinâmicas**.
- **Foco:** Maximizar o **Lucro Líquido** (Receita das visitas - Custos Operacionais).
- **Diferencial:** O algoritmo decide quantas vezes visitar cada loja. Lojas mais rentáveis recebem mais visitas, lojas periféricas recebem menos.
- **Limitação:** Como a otimização é puramente estocástica, as rotas podem ficar "bagunçadas" visualmente (cruzamentos longos no mapa), embora matematicamente válidas.

### 3. `RKO_Fase2_clusters.py` (Fase 2 - Híbrida com K-Means) 🏆 *Solução Final*
Aprimoramento da Fase 2 utilizando **Clusterização Geográfica**.
- **Metodologia:** Antes de rodar o otimizador, aplica-se o algoritmo **K-Means** para agrupar lojas próximas em "regiões".
- **Vantagem:** Cada promotor é restrito a trabalhar dentro de um cluster específico. Isso garante rotas visualmente limpas, reduz drasticamente o deslocamento e facilita a logística real.
- **Resultado:** Maior lucro líquido e rotas humanamente viáveis.

---

## 🛠️ Tecnologias e Algoritmos

A solução utiliza o framework **RKO (Random-Key Optimizer)**, que codifica a solução em vetores de chaves aleatórias e utiliza decodificadores para transformar essas chaves em rotas.

**Meta-heurísticas utilizadas em paralelo:**
* 🧬 **BRKGA** (Biased Random-Key Genetic Algorithm)
* 🔥 **SA** (Simulated Annealing)
* 🔄 **ILS** (Iterated Local Search)
* 💣 **LNS** (Large Neighborhood Search)
* 🐦 **PSO** (Particle Swarm Optimization)
* 🧬 **GA** (Genetic Algorithm Padrão)
* 🌐 **VNS** (Variable Neighborhood Search)

**Pré-processamento:**
* 📍 **K-Means Clustering** (Scikit-Learn) para regionalização.

## 📊 Visualização dos Resultados

### Comparativo Visual
O impacto da clusterização na organização das rotas:

| Sem Clusterização (`RKO_freq.py`) | Com Clusterização (`RKO_freq_clusters.py`) |
|:---:|:---:|
|  |  |
| *Rotas cruzadas e dispersas* | *Regiões definidas e rotas locais* |

*Nota: As imagens acima são exemplos gerados pelas ferramentas de plotagem integradas no código.*

### Exemplo de Saída (Terminal)
```text
============================================================
             FINANCEIRO          
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
LUCRO (FASE 2):                        R$ 13,204.34

