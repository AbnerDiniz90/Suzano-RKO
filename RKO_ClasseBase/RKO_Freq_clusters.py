from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import os
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
project_root_directory = os.path.dirname(current_directory)
sys.path.append(project_root_directory)
from RKO import RKO
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from clusters import ClusterizadorLojas

class Promotores:
    def __init__(self, velocidade, cluster_id=None):
        """
        Definição inicial de um promotor e sua agenda inicial.

        Ex.: 
        -> self.coords_segunda = [] => Coordenadas das lojas visitadas na segunda
        -> self.carga_segunda = 0   => Tempo total usado na segunda (minutos)
        """
        
        self.nome_promotor = 'teste'
        self.nome_rota = 'teste'
        self.velocidade = velocidade

        self.cluster_id = cluster_id
        self.cluster_designado = cluster_id is not None

        self.coords_segunda = []
        self.carga_segunda = 0
        self.cargas_segunda = []

        self.coords_terca = []
        self.carga_terca = 0
        self.cargas_terca = []

        self.coords_quarta = []
        self.carga_quarta = 0
        self.cargas_quarta = []

        self.coords_quinta = []
        self.carga_quinta = 0
        self.cargas_quinta = []

        self.coords_sexta = []
        self.carga_sexta = 0
        self.cargas_sexta = []

        self.coords_sabado = []
        self.carga_sabado = 0
        self.cargas_sabado = []

    def dist_total(self):

        dias = [
            self.coords_segunda, 
            self.coords_terca, 
            self.coords_quarta, 
            self.coords_quinta, 
            self.coords_sexta, 
            self.coords_sabado
        ]

        trajeto_total = 0
        for coords_dia in dias:
            trajeto_total += self.distancia(coords_dia)
        
        return trajeto_total
    
    def total_lojas_unicas(self):
        """
        Conta quantas lojas ÚNICAS este promotor atende na semana.
        Usa um 'set' (conjunto) para remover duplicatas de coordenadas.
        """
        todas_coords = (
            self.coords_segunda + self.coords_terca + 
            self.coords_quarta + self.coords_quinta + 
            self.coords_sexta + self.coords_sabado
        )
        # Set remove duplicatas automaticamente
        lojas_unicas = set(todas_coords)
        return len(lojas_unicas)
    
    def total_visitas(self):
        """
        Conta o número total de VISITAS (incluindo repetidas) na semana.
        """
        todas_coords = (
            self.coords_segunda + self.coords_terca + 
            self.coords_quarta + self.coords_quinta + 
            self.coords_sexta + self.coords_sabado
        )
        return len(todas_coords)

    def carga_total(self):
        """
        Soma das cargas ao longo da semana.
        """

        return (self.carga_segunda + self.carga_terca + self.carga_quarta +
                self.carga_quinta + self.carga_sexta + self.carga_sabado)
    
    def tempo_total_dia(self, dia):
        if dia == 0:
            return self.carga_segunda
        
        elif dia == 1:
            return self.carga_terca
        
        elif dia == 2:
            return self.carga_quarta
        
        elif dia == 3:
            return self.carga_quinta
        
        elif dia == 4:
            return self.carga_sexta
        
        elif dia == 5:
            return self.carga_sabado
        
    def ja_visitou_no_dia(self, dia, coord_loja):
        """
        Verifica se o promotor já tem uma visita agendada para esta loja neste dia.
        Retorna True se já visitou.
        """
        if dia == 0: lista_dia = self.coords_segunda
        elif dia == 1: lista_dia = self.coords_terca
        elif dia == 2: lista_dia = self.coords_quarta
        elif dia == 3: lista_dia = self.coords_quinta
        elif dia == 4: lista_dia = self.coords_sexta
        elif dia == 5: lista_dia = self.coords_sabado
        else: return False

        return coord_loja in lista_dia

    def adicionar_loja(self, dia, coord, carga, ordem_loja):
        """
        Insere a loja em um dia específico, calculando o tempo de deslocamento.

        Parâmetros:
        ->dia: Qual dia será inserido.

        ->coord: Tupla de coordenadas (x,y) da loja específica.

        ->carga: Tempo de visia em minutos.

        ->ordem_loja: Chave aleatória do RKO. Define a posição da loja na rota.
            Ex.: ordem_loja = 0.35 significa inserir em 35% da rota.
        """

        """
        ----Exemplo de como funciona----
        
        Se na segunda feira temos: self.coords_segunda = [(10, 20), (30, 40), (50, 60)]

        Significa que temos 4 posições de inserção: 0 => (10,20), 1 => (30,40), 2 => (50,60) 3 => no final

        Ao adicionar uma loja com ordem_loja = 0.65, temos:
            => idx_loja = ordem_loja * (len(self.coords_segunda) + 1)
            => idx_loja = 0.65 * (3 + 1)
            => idx_loja = 0.65 * 4
            => idx_loja = 2.6
            => idx_loja = int(2.6) = 2 

        Portanto com a inserção da nova loja temos: self.coords_segunda = [(10, 20), (30, 40), NOVA_LOJA, (50, 60)]
        
        Depois é feito:
            1. Adiciona-se a coordenada de NOVA_LOJA
            2. Registra-se a carga da NOVA_LOJA
            3. Recalcula-se a carga total do dia
        """

        if dia == 0: #Segunda
            idx_loja = ordem_loja * (len(self.coords_segunda) + 1)
            idx_loja = int(idx_loja)

            self.coords_segunda.insert(idx_loja, coord)
            self.cargas_segunda.append(carga)
            self.carga_segunda = sum(self.cargas_segunda) + self.custo_viagem(self.coords_segunda)

        elif dia == 1: #Terça
            idx_loja = ordem_loja * (len(self.coords_terca) + 1)
            idx_loja = int(idx_loja)

            self.coords_terca.insert(idx_loja, coord)
            self.cargas_terca.append(carga)
            self.carga_terca = sum(self.cargas_terca) + self.custo_viagem(self.coords_terca)

        elif dia == 2: #Quarta
            idx_loja = ordem_loja * (len(self.coords_quarta) + 1)
            idx_loja = int(idx_loja)

            self.coords_quarta.insert(idx_loja, coord)
            self.cargas_quarta.append(carga)
            self.carga_quarta = sum(self.cargas_quarta) + self.custo_viagem(self.coords_quarta)

        elif dia == 3: #Quinta
            idx_loja = ordem_loja * (len(self.coords_quinta) + 1)
            idx_loja = int(idx_loja)

            self.coords_quinta.insert(idx_loja, coord)
            self.cargas_quinta.append(carga)
            self.carga_quinta = sum(self.cargas_quinta) + self.custo_viagem(self.coords_quinta)

        elif dia == 4: #Sexta
            idx_loja = ordem_loja * (len(self.coords_sexta) + 1)
            idx_loja = int(idx_loja)

            self.coords_sexta.insert(idx_loja, coord)
            self.cargas_sexta.append(carga)
            self.carga_sexta = sum(self.cargas_sexta) + self.custo_viagem(self.coords_sexta)

        elif dia == 5: #Sábado
            idx_loja = ordem_loja * (len(self.coords_sabado) + 1)
            idx_loja = int(idx_loja)

            self.coords_sabado.insert(idx_loja, coord)
            self.cargas_sabado.append(carga)
            self.carga_sabado = sum(self.cargas_sabado) + self.custo_viagem(self.coords_sabado)
            
    """
    def dias_possiveis(self, carga):
        index_possiveis = []
        if self.carga_segunda + carga + self.custo_viagem(self.coords_segunda) <= 480:
            index_possiveis.append(0)
        if self.carga_terca + carga + self.custo_viagem(self.coords_terca)<= 480:
            index_possiveis.append(1)
        
        if self.carga_quarta + carga + self.custo_viagem(self.coords_quarta)<= 480:
            index_possiveis.append(2)
        if self.carga_quinta + carga + self.custo_viagem(self.coords_quinta)<= 480:
            index_possiveis.append(3)
        if self.carga_sexta + carga + self.custo_viagem(self.coords_sexta)<= 480:
            index_possiveis.append(4)
        if self.carga_sabado + carga + self.custo_viagem(self.coords_sabado)<= 240:
            index_possiveis.append(5)

        return index_possiveis
    """
    
    def dias_possiveis(self, carga_visita):
            """
            1. Tenta encontrar dias onde a loja cabe SEM hora extra.
            2. Se não houver nenhum, retorna o dia que gera a MENOR hora extra.
            """
            
            index_possiveis = []
            
            #Definção dos dados utilizados: (carga atual, carga total)
            dados_dias = [
                (self.carga_segunda, 480), # 0
                (self.carga_terca,   480), # 1
                (self.carga_quarta,  480), # 2
                (self.carga_quinta,  480), # 3
                (self.carga_sexta,   480), # 4
                (self.carga_sabado,  240)  # 5
            ]

            for dia_idx, (carga_atual, limite) in enumerate(dados_dias):
                if carga_atual + carga_visita <= limite:
                    index_possiveis.append(dia_idx)

            if len(index_possiveis) > 0:
                return index_possiveis

            # Se chegou aqui, vai ter que pagar hora extra. Vamos escolher a mais barata.
            melhor_dia = -1
            menor_excedente = float('inf')

            for dia_idx, (carga_atual, limite) in enumerate(dados_dias):
                tempo_final_estimado = carga_atual + carga_visita
                excedente = tempo_final_estimado - limite
                
                # Armazena o dia com menor excedente
                if excedente < menor_excedente:
                    menor_excedente = excedente
                    melhor_dia = dia_idx
            
            # Retorna o "menos pior" como única opção
            return [melhor_dia]

    def plot_rota(self, dia):
        
        if dia == 0:
            coords = self.coords_segunda
            carga_dia = self.carga_segunda
            max_carga_dia = 480
            nome_dia = "Segunda-feira"
        elif dia == 1:
            coords = self.coords_terca
            carga_dia = self.carga_terca
            max_carga_dia = 480
            nome_dia = "Terça-feira"
        elif dia == 2:
            coords = self.coords_quarta
            carga_dia = self.carga_quarta
            max_carga_dia = 480
            nome_dia = "Quarta-feira"
        elif dia == 3:
            coords = self.coords_quinta
            carga_dia = self.carga_quinta
            max_carga_dia = 480
            nome_dia = "Quinta-feira"
        elif dia == 4:
            coords = self.coords_sexta
            carga_dia = self.carga_sexta
            max_carga_dia = 480
            nome_dia = "Sexta-feira"
        elif dia == 5:
            coords = self.coords_sabado
            carga_dia = self.carga_sabado
            max_carga_dia = 320
            nome_dia = "Sábado"
        else:
            print("Dia inválido para plotagem.")
            return

        if not coords:
            print(f"Sem lojas para plotar no dia {nome_dia}.")
            return


        coords_array = np.array(coords)
        
        # Ajusta o tamanho da figura
        plt.figure(figsize=(10, 8))

        # --- Plotar a Rota com Ordem ---
        # 'bo-' significa 'b' (blue), 'o' (círculos) e '-' (linha)
        plt.plot(coords_array[:, 0], coords_array[:, 1], 'bo-', label='Rota', markersize=8)

        # --- Adicionar Números da Ordem ---
        for i, (x, y) in enumerate(coords_array):
            plt.text(x + 0.05, y + 0.05, str(i + 1), color='red', fontsize=12, fontweight='bold')

        # --- Título (com Promotor, Rota e Dia) ---
        titulo = (f"Rota: {self.nome_rota} | Promotor: {self.nome_promotor}\n"
                  f"Dia: {nome_dia}")
        plt.title(titulo, fontsize=14)

        # --- Legenda de Tempo (em Horas) ---
        # Converte a carga (minutos) para horas
        carga_horas = carga_dia / 60.0
        max_carga_horas = max_carga_dia / 60.0
        
        # Formata o texto
        info_texto = f"Tempo: {carga_horas:.2f}h / {max_carga_horas:.1f}h"

        # Adiciona a caixa de texto no canto
        plt.text(0.95, 0.01, info_texto,
                 verticalalignment='bottom', horizontalalignment='right',
                 transform=plt.gca().transAxes,
                 fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.grid()
        plt.show()
    
    def custo_viagem(self, coords):
        """
        Calcula a distância da viagem utilizando a norma de um vetor direção (Inicio - Fim) 
        e depois multiplica a distância encontrada pela velocidade para encontrar o tempo.
        Após isso divide-se por 60 para encontrar os minutos.
        """
        custo = 0

        if len(coords) < 2:
            return custo
        
        for i in range(len(coords) - 1):
            cidade_atual = coords[i]
            proxima_cidade = coords[i + 1]
            distancia = np.linalg.norm(np.array(cidade_atual) - np.array(proxima_cidade))
            custo += distancia * self.velocidade
        return custo/60
    
    def distancia(self, coords):
        """
        Calcula a distância da viagem utilizando a norma de um vetor direção (Inicio - Fim).
        """

        if len(coords) < 2:
            return 0
        
        distancia = 0

        for i in range(len(coords) - 1):
            cidade_atual = coords[i]
            proxima_cidade = coords[i + 1]
            distancia += np.linalg.norm(np.array(cidade_atual) - np.array(proxima_cidade))

        return distancia
    
def plotar_rotas_unificadas(solucao, dia_idx):
    """
    Plota as rotas com correção para números sobrepostos.
    """
    
    mapa_dias = {
        0: ('coords_segunda', 'Segunda-feira'),
        1: ('coords_terca', 'Terça-feira'),
        2: ('coords_quarta', 'Quarta-feira'),
        3: ('coords_quinta', 'Quinta-feira'),
        4: ('coords_sexta', 'Sexta-feira'),
        5: ('coords_sabado', 'Sábado')
    }
    
    if dia_idx not in mapa_dias:
        print("Dia inválido.")
        return

    attr_name, nome_dia = mapa_dias[dia_idx]
    
    plt.figure(figsize=(12, 10))
    plt.title(f"Visão Geral da Frota - {nome_dia}", fontsize=16)
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True, linestyle='--', alpha=0.6)

    cmap = plt.get_cmap('tab20')
    promotores_ativos = 0

    # Dicionário para controlar sobreposição de texto
    # Chave: (x, y) -> Valor: Quantidade de vezes que plotamos ali
    posicoes_ocupadas = {}

    for i, promotor in enumerate(solucao):
        coords = getattr(promotor, attr_name)
        
        if not coords:
            continue 
        
        promotores_ativos += 1
        
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        
        cor = cmap(i % 20)
        
        # Plota a linha (Rota)
        plt.plot(xs, ys, linestyle='-', color=cor, alpha=0.6, label=f'Promotor {i}')
        
        # Plota os pontos (Lojas) - Todos pretos conforme você pediu
        plt.scatter(xs, ys, color='black', zorder=10, s=30)

        # Adiciona os números com deslocamento inteligente
        for ordem, (x, y) in enumerate(coords):
            coord_chave = (x, y)
            
            # Verifica quantas vezes já escrevemos nessa coordenada
            deslocamento = posicoes_ocupadas.get(coord_chave, 0)
            posicoes_ocupadas[coord_chave] = deslocamento + 1
            
            # Calcula um offset baseado na quantidade de repetições
            # Vai empilhando os números verticalmente
            offset_y = 1.5 + (deslocamento * 3.0) 
            
            texto = str(ordem + 1)
            
            plt.text(x + 1.5, y + offset_y, texto, 
                     color=cor, fontsize=10, fontweight='bold', zorder=15)

    if promotores_ativos == 0:
        print(f"Nenhum promotor tem visitas agendadas para {nome_dia}.")
        plt.close()
        return

    plt.legend(loc='best', title="Equipe")
    plt.tight_layout()
    plt.show()

def get_instancia_csv(num_lojas: int, num_instancia: int) -> pd.DataFrame:
    """
    Retorna o dataframe com os dados da instância especificada.

    Args:
        num_lojas (int): O número de lojas da categoria (ex: 10, 20, 50, 100)
        num_instancia (int): O número da instância desejada (ex: 1, 2, 10, 11).

    Returns:
        list_coordinates : Lista com as coordenadas das lojas
        list_visit_duration : Lista com a duração das visitas
        matrix_profitability : Matriz Loja x Rentabilidade com base no aumento da frequência

    Raises:
        ValueError: Se os números fornecidos não forem válidos.
    """

    dir_atual = os.path.dirname(os.path.abspath(__file__))
    dir_root = os.path.dirname(dir_atual)
    base_path = os.path.join(dir_root, "Instancias_Unifesp_Suzano")

    if num_lojas <= 0 or num_lojas > 100 or num_instancia <= 0 or num_instancia > 100:
        raise ValueError("Número de lojas ou número da instância não compatível.")

    pasta_tamanho = f"{num_lojas}_stores"

    pasta_instancia = f"instance_{str(num_instancia).zfill(3)}" 

    nome_arquivo = "stores.csv"

    caminho_completo = os.path.join(base_path, pasta_tamanho, pasta_instancia, nome_arquivo)

    df_instancia = pd.read_csv(caminho_completo)

    list_coordinates = list(df_instancia[['x_coordinate', 'y_coordinate']].itertuples(index=False, name=None))
    list_visit_duration = df_instancia['visit_duration_minutes'].tolist()
    list_frequency = df_instancia['initial_frequency'].tolist()
    initial_freq = df_instancia['initial_frequency'].tolist()

    cols_lucro = [f'profitability_freq_{i}' for i in range(1, 7)]

    matrix_profitability = df_instancia[cols_lucro].values

    return list_coordinates, list_visit_duration, list_frequency, matrix_profitability, initial_freq

class RKO_Base():
    """
    Classe base abstrata para o problema RKO
    """

    def __init__(self, tempo, velocidade, lojas, inst):
        """
        Definição de atributos para o problema.
        """

        #--------------------------
        self.melhor_fitness_encontrado = float('inf')
        #--------------------------
        

        self.velocidade = velocidade    # Velocidade de deslocamento
        self.max_time = tempo           # Tempo máximo de execução para cada metaheurística (em segundos)
        self.instance_name = "Suzano_RKO_Problem"
        list_coords, list_visits, _, matrix_prof, initial_freq = get_instancia_csv(lojas, inst) #Carregamento de dados da instância especificada

        self.dict_best: dict = {}

        self.num_lojas = len(list_coords)           # Número de lojas na instância

        self.tam_solution = 9 * self.num_lojas # Tamanho do vetor RKO é 9 x o número de loja (M). É 9M pois tem as partes:
                                                    # 1. Chaves de Frequência [0 : M-1]
                                                    # 2. Ordem de inserção das visitas [M : 2M-1]
                                                    # 3. Alocação de promotor/dia para cada visita [2M : 3M-1]
                                                    # 4. Sequência na rota de cada visita [3M : 9M]
        
        #self.frequencias = list_frequency      # Lista com as frequências de visitas de cada loja (NÃO USADO MAIS)

        self.visit_durations = list_visits      # Lista com a duração das visitas
        self.visit_coords = list_coords         # Lista com as coordenadas das lojas
        self.matrix_prof = matrix_prof          # Matriz com as rentabilidades de cada frequência

        self.initial_freq = initial_freq        # Lista com as frequências iniciais de cada loja

        self.total_visit_duration = []
        self.total_coords = []

        #Definição do clusterizador de lojas
        self.clusterizador = ClusterizadorLojas(
            coords=self.visit_coords,
            frequencias=self.initial_freq,  # Usa as frequências iniciais
            metodo='kmeans',
            num_clusters='auto',
            ponderar_por_frequencia=False
        )
    
        # Executa clusterização
        self.cluster_labels = self.clusterizador.clusterizar()

        """
        # Transforma dados de lojas únicas em dados de visitas individuais. (NÃO USADO MAIS)
        for i in range(len(self.frequencias)):
            for j in range(self.frequencias[i]):
                self.total_visit_duration.append(self.visit_durations[i])
                self.total_coords.append(self.visit_coords[i])
        """

        self.LS_type: str = 'Best'  # Tipo de busca local

        self.save_q_learning_report = False

        """
        Definição dos parâmetros para cada metaheurística que o RKO irá utilizar para achar a solução. Escolhi essas três pois o Gemini disse serem as melhores
        para o problema de roteamento. Assim, se quiser adicionar mais metaheurísticas, basta criar o dicionário com os parâmetros necessários.

        Obs.: Os valores dos parâmetro foram retirados do 'Enviroment.py' e podem ser ajustados conforme necessário.
        """
        self.ILS_parameters: dict = {
            'betaMin': [0.10], # Mínimo da intensidade de perturbação aplicado para solução escapar do ótimo local. Valor maior significa mais perturbação.
            'betaMax': [0.20] # Máximo da intensidade de perturbação aplicado para solução escapar do ótimo local.
        }

        self.BRKGA_parameters: dict = {
            'p': [100],      # Tamanho total de soluções(chaves aleatórias) mantidas a cada geração.
            'pe': [0.20],    # Proporção das melhores soluções da população que serão copiadas para próxima geração.
            'pm': [0.10],    # Geração aleatória de novas soluçãos
            'rhoe': [0.70]   # Propbabilidade dos descendentes herdarem os genes dos pais elite.
        }

        self.LNS_parameters: dict = {
            'betaMin': [0.10], # Fração mínima de solução a serem removidas a cada iteração.
            'betaMax': [0.30], # Fração máxima de solução a serem removidas a cada iteração.
            'TO': [1000],      # Número de iterações sem melhora para o critério de parada.
            'alphaLNS': [0.95] # Fator de resfriamento para o LNS.
        }

        self.SA_parameters: dict = {
            'SAmax': [50],        # Número de iterações por temperatura
            'alphaSA': [0.99],    # Taxa de resfriamento (cooling rate)
            'betaMin': [0.05],    # Intensidade mínima de perturbação
            'betaMax': [0.25],    # Intensidade máxima de perturbação
            'T0': [10000]         # Temperatura inicial
        }

        # 2. VARIABLE NEIGHBORHOOD SEARCH (VNS)
        self.VNS_parameters: dict = {
            'kMax': [5],          # Número máximo de estruturas de vizinhança
            'betaMin': [0.05]     # Intensidade mínima de shake
        }

        # 3. PARTICLE SWARM OPTIMIZATION (PSO)
        self.PSO_parameters: dict = {
            'PSize': [100],       # Tamanho do enxame (número de partículas)
            'c1': [2.05],         # Coeficiente cognitivo (atração para melhor pessoal)
            'c2': [2.05],         # Coeficiente social (atração para melhor global)
            'w': [0.73]           # Peso de inércia (momentum)
        }

        # 4. GENETIC ALGORITHM (GA)
        self.GA_parameters: dict = {
            'sizePop': [100],     # Tamanho da população
            'probCros': [0.98],   # Probabilidade de crossover
            'probMut': [0.005]    # Probabilidade de mutação
        }

    def decoder(self, keys):
        """
        Ex de Funcionamento (N=2 Lojas)

        Vetor de Chaves (Input): 
        keys = [ 0.9, 0.1 | 0.8,  0.2 | 0.3,  0.9 | 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
               └─ Freq ──┘ └─ Order ─┘ └─ Prom ──┘ └─── Visit Block (Loja 0) ───┘ └── Visit Block (Loja 1) ──┘

        => 1. Separação e Decisão de Frequência
           -------------------------------------
           Freq Keys = [0.9, 0.1]
           
           > Loja 0 (Key 0.9):
             Freq = int(0.9 * 6) + 1 = 5 + 1 = 6 Visitas.
           
           > Loja 1 (Key 0.1):
             Freq = int(0.1 * 6) + 1 = 0 + 1 = 1 Visita.

        => 2. Expansão das Tarefas (Fabricação da Lista)
           ---------------------------------------------
           Aqui pegamos as chaves de Promotor e Visita baseadas na quantidade decidida acima.

           > Loja 0 (6 Visitas):
             - Chave Dono (Fixa): 0.3
             - Chaves Visita (Pega as 6 do bloco): [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
             - Gera 6 Tarefas:
               [ (Loja 0, Dono 0.3, Visita 0.1), (Loja 0, Dono 0.3, Visita 0.2) ... até Visita 0.6 ]

           > Loja 1 (1 Visita):
             - Chave Dono (Fixa): 0.9
             - Chaves Visita (Pega a 1ª do bloco): [0.9] -> Ignora [0.8, 0.7, 0.6, 0.5, 0.4]
             - Gera 1 Tarefa:
               [ (Loja 1, Dono 0.9, Visita 0.9) ]

           Total de Tarefas Geradas: 7

        => 3. Ordenação Global (Baseada em Order Keys)
           -------------------------------------------
           Order Keys = [0.8, 0.2]
           
           > Loja 0 tem prioridade 0.8 (Baixa prioridade na fila, vai para o fim).
           > Loja 1 tem prioridade 0.2 (Alta prioridade na fila, vai para o começo).

           A lista expandida é reordenada. A Loja 1 "fura a fila".

        => 4. Saída (Output para o Cost)
           -----------------------------
           Dicionário contendo:
           
           order (IDs):           [1,   0,   0,   0,   0,   0,   0]
                                   ^    ^----------------------------^
                                 Loja1  Loja 0 (6 vezes seguidas pois tem mesma prioridade)

           promotores_keys:       [0.9, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
                                   ^    ^--------------------------^
                                  Dono  Dono da Loja 0 (Repetido para garantir exclusividade)

           visit_keys:            [0.9, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
                                   ^    ^--------------------------^
                                  Dia   Dias variados para as visitas da Loja 0

           receita_total:         R$ (Soma do lucro da Freq 6 da Loja 0 + Freq 1 da Loja 1)
        """
        #=======================================================
        # 1.A. Separação do vetor de chaves

        num_lojas = self.num_lojas
        
        freq_keys_raw = keys[0 : num_lojas]
        order_keys_raw = keys[num_lojas : 2*num_lojas]
        promoter_keys_raw = keys[2*num_lojas : 3*num_lojas]

        # Offset para saber quando é o início do bloco de visitas
        offset_visit = 3 * num_lojas

        #-------------------------------------------------------
        # 1.B. Estruturas de Expansão 

        order_keys_list = []      
        promotor_keys_list = []     
        visit_keys_list = []       
        
        receita_total = 0
        mapa_ordem = {}

        #=======================================================
        # 2. Loop de Expansão 
        for i in range(num_lojas):
            # ----- A. Decide Frequência -----
            freq_keys = int(freq_keys_raw[i] * 6) 
            if freq_keys >= 6: freq_keys = 5

            # Decide número de visitas

            freq_idx = max(self.initial_freq[i] - 1, freq_keys)

            num_visitas = freq_idx + 1
            
            # ----- B. Calcula Receita -----
            receita_total += self.matrix_prof[i][freq_idx]
            
            # ----- C. Guarda a chave de ordem para ordenar -----
            mapa_ordem[i] = order_keys_raw[i]
            
            # ----- D. Pega a Chave do Promotor -----
            chave_promotor_loja = promoter_keys_raw[i]
            
            # ----- E. Define onde começa o bloco de visitas -----
            start_v = offset_visit + (i * 6)
            
            # ----- F. Expande as listas -----
            for k in range(num_visitas):
                order_keys_list.append(i)
                
                # REPETE a mesma chave de promotor N vezes
                promotor_keys_list.append(chave_promotor_loja)
                
                # Pega cada chave do bloco reservado
                visit_keys_list.append(keys[start_v + k])

        #=======================================================
        # 3. Ordenação Baseada na prioridade da loja
        indices_ordenados = sorted(
            range(len(order_keys_list)), 
            key=lambda k: mapa_ordem[order_keys_list[k]]
        )
        
        final_lojas = [order_keys_list[i] for i in indices_ordenados]
        final_promotores = [promotor_keys_list[i] for i in indices_ordenados]
        final_visitas = [visit_keys_list[i] for i in indices_ordenados]
        
        return {
            "order": final_lojas,
            "promotores_keys": final_promotores,
            "visit_keys": final_visitas,
            "receita_total": receita_total
        }
    
    def cost(self, solution, view_solution=False):
        # 1. Separação da solução
        order = solution["order"]
        promotores_keys = solution["promotores_keys"]
        visit_keys = solution["visit_keys"]
        receita_total = solution["receita_total"]

        # Inicialização dos clusters

        self.cluster_por_loja = {}
        for i in range(self.num_lojas):
            cluster_id = self.clusterizador.get_cluster_da_loja(i)
            self.cluster_por_loja[i] = cluster_id

        #=======================================================
        # 2. Inicialização com bin de promotores vazio
        promotores_bin = []

        # Inicialização da atribuição loja -> promotor
        donos_das_lojas = {}

        #=======================================================
        # 3. Processamento para cada visita

        """
        Aqui o algoritmo pega as visitas uma por uma.
        Se a Loja 50 tem o menor valor em order_keys, ela é a primeira a entrar no loop.
        O algoritmo tenta encaixar a Loja 50 no cenário vazio. Depois tenta encaixar a próxima, e assim por diante.
        """

        for idx, loja_id in enumerate(order):
            # Recupera as informações das lojas da iteração
            loja = int(loja_id)
            carga = self.visit_durations[loja]
            coords = self.visit_coords[loja]

            # Chave aleatória do RKO (0.0 a 1.0) que vai decidir ONDE colocar a loja
            key = promotores_keys[idx]

            #Identificar cluster
            cluster_da_loja = self.cluster_por_loja[loja]
            #=======================================================
            # 4. Coleta de opções (COM RESTRIÇÃO DE 1 VISITA/DIA E DONO ÚNICO)
            promotores_possiveis = []
            
            # Loja JÁ possui promotor (TODAS as visitas devem ir para o mesmo promotor)
            if coords in donos_das_lojas:
                # Recupera qual o promotor DONO
                idx_dono = donos_das_lojas[coords]
                promotor_dono = promotores_bin[idx_dono]

                #Verifica se o promotor dono pertence ao cluster correto
                assert promotor_dono.cluster_id == cluster_da_loja, \
                    f"Erro: Promotor {idx_dono} (Cluster {promotor_dono.cluster_id}) " \
                    f"não deveria ter a loja {loja} no Cluster {cluster_da_loja}"

                # Verifica quais dias estão disponíveis
                dias_validos = promotor_dono.dias_possiveis(carga)
                
                # Filtra apenas os dias onde a loja ainda NÃO foi visitada
                for dia in dias_validos:
                    if not promotor_dono.ja_visitou_no_dia(dia, coords):
                        promotores_possiveis.append((idx_dono, dia))
                
                # CRÍTICO: Se o dono não tem mais dias disponíveis, 
                # a solução é INVÁLIDA (penalidade será aplicada automaticamente)
                # Não criamos novo promotor aqui para manter a restrição de dono único
                
                if len(promotores_possiveis) == 0:
                    # Força alocar no melhor dia possível do dono, mesmo com hora extra
                    # Escolhe o dia com menor carga atual
                    cargas_dias_dono = [
                        (0, promotor_dono.carga_segunda),
                        (1, promotor_dono.carga_terca),
                        (2, promotor_dono.carga_quarta),
                        (3, promotor_dono.carga_quinta),
                        (4, promotor_dono.carga_sexta),
                        (5, promotor_dono.carga_sabado)
                    ]
                    
                    # Filtra apenas dias que ainda não têm esta loja
                    dias_sem_loja = [
                        (d, c) for d, c in cargas_dias_dono 
                        if not promotor_dono.ja_visitou_no_dia(d, coords)
                    ]
                    
                    if len(dias_sem_loja) > 0:
                        # Escolhe o dia com menor carga
                        dia_escolhido = min(dias_sem_loja, key=lambda x: x[1])[0]
                        promotores_possiveis.append((idx_dono, dia_escolhido))
                    else:
                        # Caso extremo: todos os 6 dias já têm a loja
                        # Isso só acontece se freq > 6 (impossível no seu modelo)
                        # Mas por segurança, coloca no primeiro dia
                        promotores_possiveis.append((idx_dono, 0))

            # Loja AINDA NÃO possui promotor (primeira visita)
            else:
                # Adicionar um novo promotor respeitando o cluster
                for i in range(len(promotores_bin)):
                    promotor = promotores_bin[i]
                    
                    # REGRA: Promotor só pega loja do seu cluster
                    if promotor.cluster_id == cluster_da_loja:
                        if promotor.total_lojas_unicas() < 8:
                            dias_validos = promotor.dias_possiveis(carga)
                            for dia in dias_validos:
                                if not promotor.ja_visitou_no_dia(dia, coords):
                                    promotores_possiveis.append((i, dia))

                # Opção B: Contratar novo promotor (SEMPRE disponível)
                promotores_possiveis.append((-1, -1))
            
            # Proteção
            if len(promotores_possiveis) == 0:
                promotores_possiveis.append((-1, -1))

            #=======================================================
            # 5. Escolha e alocação baseada na Chave Aleatória
            idx_escolhido = int(key * len(promotores_possiveis))
            
            if idx_escolhido >= len(promotores_possiveis):
                idx_escolhido = len(promotores_possiveis) - 1

            index_promotor_bin, dia_promotor_bin = promotores_possiveis[idx_escolhido]

            #=======================================================
            # 6. A Execução
            
            # Se o índice for de um novo promotor
            if index_promotor_bin == -1:
                new_promotor = Promotores(self.velocidade, cluster_id=cluster_da_loja)
                
                # Decisão do dia inicial
                dia_novo = int(visit_keys[idx] * 6)
                if dia_novo >= 6: 
                    dia_novo = 5
                
                # Adiciona a loja na rota do novo promotor
                new_promotor.adicionar_loja(dia_novo, coords, carga, visit_keys[idx])
                promotores_bin.append(new_promotor)

                # REGISTRA o dono da loja (PRIMEIRA VEZ)
                donos_das_lojas[coords] = len(promotores_bin) - 1

            # Se o promotor já existe, adiciona a loja
            else:
                promotor = promotores_bin[index_promotor_bin]
                promotor.adicionar_loja(dia_promotor_bin, coords, carga, visit_keys[idx])

                # Se for a primeira visita desta loja, registra o dono
                if coords not in donos_das_lojas:
                    donos_das_lojas[coords] = index_promotor_bin
                    
        #=======================================================
        #7. Calculo da função objetivo
        
        # Definição de Pesos (Custos)
        P_promotor = 750.0
        P_hr_extra = 0.95            
        P_dist = 0.06               # R$/m
        P_hr_extra_abusiva = 50_000 # Custo Brutal

        LIMITE_HE_SEMANAL = P_promotor / P_hr_extra 

        # --- Primeira Parcela: Contratação ---
        Custo_1 = P_promotor * len(promotores_bin)

        # --- Segunda Parcela: Distância ---
        Custo_dist_total = 0
        for promotor in promotores_bin:
            dist = promotor.dist_total()
            Custo_dist_total += dist
        
        Custo_2 = Custo_dist_total * P_dist

        # --- Terceira Parcela: Hora Extra ---
        Custo_3 = 0 
        total_minutos_he_frota = 0 # Dinheiro Real (R$)

        for promotor in promotores_bin:
            he_minutos_semanal_promotor = 0 
            
            for dia in range(6):
                limite = 240 if dia == 5 else 480
                tempo_total = promotor.tempo_total_dia(dia)

                if tempo_total > limite:
                    he_minutos_semanal_promotor += (tempo_total - limite)
            
            # Acumula as horas extras
            total_minutos_he_frota += he_minutos_semanal_promotor

            # Aplica a Lógica de Penalidade
            if he_minutos_semanal_promotor <= LIMITE_HE_SEMANAL:
                # Zona Segura: Penalidade Padrão
                Custo_3 += (he_minutos_semanal_promotor) * P_hr_extra
            else:
                # Zona Abusiva: Penalidade Severa
                excesso = he_minutos_semanal_promotor - LIMITE_HE_SEMANAL
                
                penalidade_normal = (LIMITE_HE_SEMANAL) * P_hr_extra
                penalidade_abusiva = (excesso) * P_hr_extra_abusiva
                
                Custo_3 += penalidade_normal + penalidade_abusiva

        # --- Quarta Parcela : Distribuição de Carga ----

        # Definição de Pesos (Custos)
        Tolerancia_dif = 3 * 60
        P_balanc = 1_000_000

        cargas_horarias = []

        for p in promotores_bin:
            cargas_horarias.append(p.carga_total())
            
            if len(cargas_horarias) > 1:
                maior_carga = max(cargas_horarias)
                menor_carga = min(cargas_horarias)
                diferenca = maior_carga - menor_carga

                if diferenca > Tolerancia_dif:
                    # Só penaliza o EXCEDENTE da diferença
                    # Ex: Se a diferença for 15h e a tolerância 10h, penaliza apenas 6h.
                    excesso_desbalanceamento = diferenca - Tolerancia_dif
                    Custo_4 = excesso_desbalanceamento * P_balanc
                else:
                    # Se a diferença for menor que 10h, o custo é zero
                    Custo_4 = 0
        # =======================================================
        # Penalidade de ociosidade

        # --- Quinta Parcela: Penalidade de Ociosidade Individual ---
        P_OCIOSIDADE = 50_000  # Custo por hora ociosa
        CARGA_MINIMA_DESEJADA = 18 * 60  # 18 horas semanais

        Penalidade_Ociosidade = 0
        for promotor in promotores_bin:
            carga_promotor = promotor.carga_total()
            
            if carga_promotor < CARGA_MINIMA_DESEJADA:
                deficit = CARGA_MINIMA_DESEJADA - carga_promotor
                Penalidade_Ociosidade += deficit * P_OCIOSIDADE

        # =======================================================
        # Cálculo Final
        fitness_total = Custo_1 + Custo_2 + Custo_3 + Custo_4 + Penalidade_Ociosidade
        
        # =======================================================
        # Retorno Visualização
        if view_solution:

            qtd_promotores = len(promotores_bin)
            
            # ----- Cálculo custos operacionais -----
            # A. Equipe
            financeiro_equipe = qtd_promotores * P_promotor
            
            # B. Combustível
            # Recalcula a distância total crua
            dist_total_frota = sum([p.dist_total() for p in promotores_bin])
            financeiro_dist = dist_total_frota * P_dist
            
            # C. Horas Extras
            total_min_he_reais = 0
            for p in promotores_bin:
                for d in range(6):
                    lim = 240 if d == 5 else 480
                    t = p.tempo_total_dia(d)
                    if t > lim:
                        total_min_he_reais += (t - lim)
            
            financeiro_he = total_min_he_reais * P_hr_extra
            
            custo_operacional_total = financeiro_equipe + financeiro_dist + financeiro_he

            # ----- Calculo da receita com base nas frequências -----

            """
            O cálulo da receita das duas fases é feito somando os valores correspondentes na 
            matrix_prof[id_loja][freq] que é uma matriz LOJA X Profitability_freq sendo 
            Profitability_freq as colunas dadas no .csv

            Logo, a diferença é que na fase 1 ela encontra a profitability_freq correspondente usando as frequências dadas
            e na fase 2 é usado as frequências encontradas pelo RKO.
            """

            #Acessa a matriz Loja x rentabilidade_freq e soma os valores
            receita_planejada = 0

            for id_loja in range(len(list_coords)):
                freq_planejada = list_freq[id_loja]
                if freq_planejada > 0:
                    receita_planejada += matrix_prof[id_loja][freq_planejada - 1]

            # ----- Impressão -----
            print("\n" + "="*60)
            print("             FINANCEIRO          ")
            print("="*60)

            print(f"RECEITAS:")
            print(f"   - Frequências definidas (Fase 1):   R$ {receita_planejada:,.2f}")
            print(f"   - Frequências otimizadas (Fase 2):  R$ {receita_total:,.2f}")

            print("-" * 60)
            print(f"CUSTOS OPERACIONAIS:")
            print(f"   - Equipe ({qtd_promotores} pessoas):         R$ {financeiro_equipe:,.2f}")
            print(f"   - Combustível ({dist_total_frota:.0f} un):       R$ {financeiro_dist:,.2f}")
            print(f"   - Horas Extras ({total_min_he_reais:.0f} min):     R$ {financeiro_he:,.2f}")
            print(f"   ---------------------------------------------")
            print(f"   TOTAL CUSTOS:                 R$ {custo_operacional_total:,.2f}")
            
            print("-" * 60)
            print(f"LUCRO (FASE 2):                  R$ {fitness_total - receita_total:,.2f}")

            return promotores_bin
            # =======================================================

        # Log em Tempo Real (Console)
        if fitness_total < self.melhor_fitness_encontrado:
            self.melhor_fitness_encontrado = fitness_total
            
            qtd_promotores = len(promotores_bin)

            print(f" >>> [NOVO RECORD] Promotores: {qtd_promotores} | HE Total: {total_minutos_he_frota:.0f} min | (Lucro: R$ {fitness_total - receita_total:.2f})")

        return fitness_total - receita_total
        

veloc_100_lojas = 18 #s/unidade
veloc_50_lojas = 15 #s/unidade
veloc_20_lojas = 12 #s/unidade
veloc_10_lojas = 10 #s/unidade

# =========================
#Definição do número de lojas e instância utilizada

n_lojas = 50
inst = 1
# =========================

if __name__ == "__main__":
    # =======================================================
    # Dados iniciais
    mapa_velocidades = {
        10: veloc_10_lojas,
        20: veloc_20_lojas,
        50: veloc_50_lojas,
        100: veloc_100_lojas
    }

    velocidade_atual = mapa_velocidades.get(n_lojas)
    list_coords, list_visits, list_freq, matrix_prof, initial_freq = get_instancia_csv(n_lojas, inst)

    # =======================================================
    # Solução RKO
    env = RKO_Base(60, velocidade_atual, n_lojas, inst) 
    solver = RKO(env, print_best=True)
    
    final_cost, final_solution, time_to_best = solver.solve(1200,     # 20 minutos
                                                            brkga=20,
                                                            ils=15,
                                                            lns=15,
                                                            sa=10,
                                                            vns=10,
                                                            pso=8,
                                                            ga=8)
    
    dados_decodificados = env.decoder(final_solution)
    solucao_final = env.cost(dados_decodificados, view_solution=True)  

    # ========== NOVO: VERIFICAÇÃO DE CLUSTERS ==========
    print("\n" + "="*60)
    print("          VERIFICAÇÃO DE CLUSTERS          ")
    print("="*60)
    
    env.clusterizador._imprimir_estatisticas()
    
    # Verifica exclusividade
    env.clusterizador.validar_exclusividade(solucao_final, env.visit_coords)
    
    # Opcional: Plotar clusters
    resposta = input("\nDeseja visualizar os clusters? (s/n): ")
    if resposta.lower() == 's':
        env.clusterizador.plot_clusters()

    # =======================================================
    # Impressão das frequências encontradas pelo RKO

    print("\n" + "="*60)
    print("          FREQUENCIAS E RECEITAS          ")
    print("="*60)
    print(f"{'ID LOJA':<10} | {'FREQ':<10} | {'RECEITA (R$)':<15}")
    print("-" * 60)

    lista_visitas = dados_decodificados["order"]
    contagem_freq = Counter(lista_visitas)
    
    receita_total_acumulada = 0
    total_visitas_geral = 0

    for id_loja in range(n_lojas):
        freq = contagem_freq.get(id_loja, 0)
        
        if freq > 0:
            # Matriz é base 0 (índice 0 = freq 1)
            receita = env.matrix_prof[id_loja][freq - 1]
        else:
            receita = 0.0
        
        receita_total_acumulada += receita
        total_visitas_geral += freq
        
        print(f"{id_loja:<10} | {freq:<10} | R$ {receita:<12.2f}")

    # =======================================================
    # Impressão dos dados dos promotores
    print("\n" + "="*60)
    print("          RELATÓRIO PROMOTORES          ")
    print("="*60)

    mapa_visitas_global = {}
    total_lojas_atendidas = 0
    
    for i, promotor in enumerate(solucao_final):
        todas_coords = (
            promotor.coords_segunda + promotor.coords_terca + 
            promotor.coords_quarta + promotor.coords_quinta + 
            promotor.coords_sexta + promotor.coords_sabado
        )
        
        coords_unicas = set(todas_coords)
        
        ids_lojas = []
        for coord in coords_unicas:
            if coord not in mapa_visitas_global:
                mapa_visitas_global[coord] = []
            mapa_visitas_global[coord].append(i)

            try:
                id_real = list_coords.index(coord)
                ids_lojas.append(id_real)
            except ValueError:
                ids_lojas.append("?")

        ids_lojas.sort()
        
        carga_h = promotor.carga_total() / 60.0
        num_visitas = len(todas_coords)
        total_lojas_atendidas += len(coords_unicas)

        cargas_dias = {
            "Segunda" : promotor.carga_segunda, 
            "Terça"   : promotor.carga_terca, 
            "Quarta"  : promotor.carga_quarta, 
            "Quinta"  : promotor.carga_quinta, 
            "Sexta"   : promotor.carga_sexta, 
            "Sábado"  : promotor.carga_sabado
        }

        print(f"PROMOTOR {i}")
        print(f"  > Carga Horária: {carga_h:.1f}h")
        print(f"  > Total Visitas: {num_visitas}")
        print(f"  > Carteira ({len(ids_lojas)} lojas): {ids_lojas}\n")

        for dia, minutos in cargas_dias.items():
            if minutos > 0:
                print(f"  > Carga {dia}: {minutos/60:.1f}h")

        print("-" * 60)

    # =======================================================
    # Impressão das estatísticas Gerais (Média Lojas e Conflito de distribuição)
    if len(solucao_final) > 0:
        media_lojas = total_lojas_atendidas / len(solucao_final)
        print(f"\nMÉDIAS DA EQUIPE:")
        print(f"  Lojas/Promotor: {media_lojas:.2f}")
    
    tem_conflito = False
    for coord, lista_promotores in mapa_visitas_global.items():
        if len(lista_promotores) > 1:
            tem_conflito = True
            try:
                id_loja = list_coords.index(coord)
                nome_loja = f"Loja ID {id_loja}"
            except:
                nome_loja = f"Coord {coord}"
            
            print(f" [ERRO] {nome_loja} disputada por promotores: {lista_promotores}")

    if not tem_conflito:
        print(" [SUCESSO] Distribuição Perfeita: Cada loja tem apenas 1 dono.\n")
    else:
        print(" [FALHA] Existem lojas com múltiplos donos.\n")

    # =======================================================
    # Loop de Plotagem
    print("\n--- Visualização de Rotas ---")
    while True:
        try:
            print("\nDigite o dia para visualizar a rota de TODOS os promotores:")
            entrada = input("(0=Seg, 1=Ter, 2=Qua, 3=Qui, 4=Sex, 5=Sab, -1=Sair): ")
            
            dia = int(entrada)
            
            if dia == -1:
                print("Encerrando...")
                break
            
            if 0 <= dia <= 5:
                # Chama a função nova passando a lista completa de soluções
                plotar_rotas_unificadas(solucao_final, dia)
            else:
                print("Dia inválido. Digite entre 0 e 5.")
                
        except ValueError:
            print("Entrada inválida. Digite um número.")