from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import os
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
project_root_directory = os.path.dirname(current_directory)
sys.path.append(project_root_directory)
from RKO import RKO
from clusters import ClusterizadorLojas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

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

        self.cluster_id = cluster_id  #Região que este promotor atende
        self.cluster_designado = cluster_id is not None

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

        print(f"\n🔍 DEBUG - {nome_dia}:")
        print(f"   Número de lojas: {len(coords)}")
        print(f"   Primeira coord: {coords[0]} (tipo: {type(coords[0])})")
        print(f"   Última coord: {coords[-1]}")

        try:
            coords_lista = []

            for i, coord in enumerate(coords):
                if isinstance(coord, (tuple, list)) and len(coord) == 2:
                    x, y = coord
                    coords_lista.append([float(x), float(y)])
                else:
                    print(f"Coordenada {i} com formato inválido: {coord}")
                    return
            
            coords_array = np.array(coords_lista, dtype=float)

            if coords_array.shape[1] != 2:
                print(f"Erro: Array com formato inesperado: {coords_array.shape}")
                print(f"   Array: {coords_array}")
                return
            
            print(f"   Array shape: {coords_array.shape}")
            print(f"   Range X: [{coords_array[:, 0].min():.2f}, {coords_array[:, 0].max():.2f}]")
            print(f"   Range Y: [{coords_array[:, 1].min():.2f}, {coords_array[:, 1].max():.2f}]")

        except Exception as e:
            print(f"Erro ao converter coordenadas: {e}")
            print(f"   Coords originais: {coords}")
            return
        
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

def get_instancia_csv(num_lojas: int, num_instancia: int) -> pd.DataFrame:
    """
    Retorna o dataframe com os dados da instância especificada.

    Args:
        num_lojas (int): O número de lojas da categoria (ex: 10, 20, 50, 100)
        num_instancia (int): O número da instância desejada (ex: 1, 2, 10, 11).

    Returns:
        pd.Dataframe : Dataframe com os dados da instância.

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

    cols_lucro = [f'profitability_freq_{i}' for i in range(1, 7)]
    matrix_profitability = df_instancia[cols_lucro].values

    return list_coordinates, list_visit_duration, list_frequency, matrix_profitability

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

        list_coords, list_visits, list_frequency, _ = get_instancia_csv(lojas, inst) #Carregamento de dados da instância especificada

        self.num_lojas = len(list_coords)           # Número de lojas na instância
        self.frequencias = list_frequency       # Lista com as frequências de visitas de cada loja
        self.visit_durations = list_visits      # Lista com a duração das visitas
        self.visit_coords = list_coords         # Lista com as coordenadas das lojas

        #Clusterização
        self.clusterizador = ClusterizadorLojas(
            coords=self.visit_coords,
            frequencias=self.frequencias,
            metodo='kmeans',
            num_clusters='auto',  # ou especifique um número
            ponderar_por_frequencia=False  # False = mais equilibrado
        )
        #Executa clusterização
        self.cluster_labels = self.clusterizador.clusterizar()

        self.total_visit_duration = []
        self.total_coords = []
        
        #Mapeia cada VISITA ao seu cluster
        #IMPORTANTE: Múltiplas visitas da mesma loja têm o MESMO cluster
        self.cluster_por_visita = []

        for i in range(len(self.frequencias)):
            cluster_id = self.clusterizador.get_cluster_da_loja(i)
            for j in range(self.frequencias[i]):
                self.total_visit_duration.append(self.visit_durations[i])
                self.total_coords.append(self.visit_coords[i])
                self.cluster_por_visita.append(cluster_id)
        
        #Visualização (opcional)
        #self.clusterizador.visualizar()

        self.tam_solution = 3 * sum(list_frequency)

        """"""
        self.dict_best: dict = {}
        
        """
        Ex.:
            => ANTES (por loja):

                list_coords = [(10, 20), (30, 40), (50, 60)]
                list_visits = [60, 90, 120]
                list_frequency = [2, 1, 3]

            => DEPOIS (por visita):

                total_coords = [
                    (10, 20), (10, 20),           # Loja 0 visitada 2x
                    (30, 40),                     # Loja 1 visitada 1x
                    (50, 60), (50, 60), (50, 60)  # Loja 2 visitada 3x
                ]
                total_visit_duration = [60, 60, 90, 120, 120, 120]
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

    def decoder(self, keys):
        """
        => Recebe as chaves do RKO 
        => Divide em 3 partes 
        => Recebe os índices do vetor ordenado de order_keys 
        => Retorna a concatenação das listas

        Ex.:

            Chaves aleatórias: keys = [0.7, 0.2, 0.9, 0.5, 0.1, 0.8 | 0.3, 0.6, 0.4, 0.2, 0.9, 0.1 | 0.5, 0.8, 0.2, 0.7, 0.3, 0.6]
                                        └─────── order_keys ───────┘   └──── promotores_keys ────┘   └──────── visit_keys ──────┘

            => 1. Separação
                order_keys = [0.7, 0.2, 0.9, 0.5, 0.1, 0.8]
                promotores_keys = [0.3, 0.6, 0.4, 0.2, 0.9, 0.1]
                visit_keys = [0.5, 0.8, 0.2, 0.7, 0.3, 0.6]

            => 2. Ordenação
                np.argsort([0.7, 0.2, 0.9, 0.5, 0.1, 0.8])
                -> Valores:  0.1 < 0.2 < 0.5 < 0.7 < 0.8 < 0.9
                -> Índices:   4    1    3    0    5    2
                order = [4, 1, 3, 0, 5, 2]

            => 3. Saída
                solution = [4, 1, 3, 0, 5, 2,  # Ordem de processamento
                0.3, 0.6, 0.4, 0.2, 0.9, 0.1,  # Keys de alocação
                0.5, 0.8, 0.2, 0.7, 0.3, 0.6]  # Keys de sequência
        """

        tam = len(keys)
        tam_parts = tam // 3
        order_keys = keys[0:tam_parts]
        promoteres_keys = keys[tam_parts:2 * tam_parts]
        visit_keys = keys[2 * tam_parts:tam]

        order = np.argsort(order_keys)

        return list(order) + list(promoteres_keys) + list(visit_keys)
    
    def cost(self, solution, view_solution=False):

        # 1. Separação da solução
        tam = len(solution)
        tam_parts = tam // 3

        #order: Define qual visita processamos primeiro. Se a loja difícil for processada primeiro, ela pega os melhores horários.
        #Se for por último, ela pega o que sobrou.
        order = solution[0:tam_parts] 

        #promotores_keys: Define quem vai atender. É usada para escolher entre os promotores existentes ou criar um novo.
        promotores_keys = solution[tam_parts:2 * tam_parts]

        #visit_keys: É usada para escolher o dia da semana (caso seja um promotor novo) ou a posição na rota (manhã/tarde).
        visit_keys = solution[2 * tam_parts:tam] 
        #=======================================================

        # 2. Inicialização
        #Antigo: promotores_bin = [Promotores(self.velocidade)]
        promotores_bin = []

        donos_das_lojas = {}
        #=======================================================

        # 3. Processamento para cada visita

        """
        Aqui o algoritmo pega as visitas uma por uma.
        Se a Loja 50 tem o menor valor em order_keys, ela é a primeira a entrar no loop.
        O algoritmo tenta encaixar a Loja 50 no cenário vazio. Depois tenta encaixar a próxima, e assim por diante.
        """

        for idx, loja in enumerate(order):
            #Recupera as informações das lojas da iteração
            loja = int(loja)
            carga = self.total_visit_duration[loja]
            coords = self.total_coords[loja]

            # Chave aleatória do RKO (0.0 a 1.0) que vai decidir ONDE colocar a loja
            key = promotores_keys[idx]
            #=======================================================

            #Identifica o cluster da visita atual
            cluster_da_visita = self.cluster_por_visita[loja]

            # 4. Coleta de opções
            promotores_possiveis = []
            
            #Loja já possui promotor
            if coords in donos_das_lojas:
                #Recupera qual o promotor
                idx_dono = donos_das_lojas[coords]
                promotor_dono = promotores_bin[idx_dono]

                # VALIDAÇÃO: Confirma que o dono está no cluster correto
                assert promotor_dono.cluster_id == cluster_da_visita, \
                    f"Erro: Promotor {idx_dono} (Cluster {promotor_dono.cluster_id}) " \
                    f"não deveria ter a loja no Cluster {cluster_da_visita}"
                
                dias_validos = promotor_dono.dias_possiveis(carga)
                for dia in dias_validos:
                    promotores_possiveis.append((idx_dono, dia))

            #Loja ainda não possui promotor
            else:
                """
                O loop abaixo verifica para cada promotor existente se há espaço.
                Por conta de ser uma restrição não rígida, a resposta é sempre "Sim" (mesmo que gere Hora Extra).
                """

                #Opção A: Tenta alocar loja num promotor já existente
                for i in range(len(promotores_bin)):
                    promotor = promotores_bin[i]
            
                    # REGRA DE OURO: Promotor só pega loja do seu cluster
                    if promotor.cluster_id == cluster_da_visita:
                        if promotor.total_lojas_unicas() < 8:
                            dias_validos = promotor.dias_possiveis(carga)
                            for dia in dias_validos:
                                promotores_possiveis.append((i, dia))
                
                # Sempre permite criar novo promotor (designado ao cluster)
                promotores_possiveis.append((-1, -1)) 

            # Proteção contra lista vazia
            if len(promotores_possiveis) == 0:
                # Força criação de novo promotor
                promotores_possiveis.append((-1, -1))

                """
                Ex.:

                O código pergunta: "Quais são as jogadas possíveis agora?"

                Imagine que já existem 2 promotores (P0 e P1):

                -P0 diz: "Posso atender na Segunda ou na Terça". => Adiciona (0, 0) e (0, 1) na lista.
                -P1 diz: "Estou lotado, mas posso na Sexta com hora extra". => Adiciona (1, 4) na lista.
                -RH diz: "Sempre podemos contratar alguém novo". => Adiciona (-1, -1).
                
                A lista promotores_possiveis vira um Menu de Decisão: Index 0: (P0, 0) | Index 1: (P0, 1) | Index 2: (P1, 4) | Index 3: (-1, -1)
                """
            #=======================================================

            # 5. Escolha e alocação baseada na Chave Aleatória (O Sorteio)
            idx_escolhido = int(key * len(promotores_possiveis))

            """
            Aqui usa-se a chave aleatória (key) (um número entre 0.00 e 0.99) para escolher um item do menu.
            
            Matemáticamente: Se a lista tem 4 opções e o key é 0.80: 
                0.80 . 4 = 3.2
                int(3.2) = 3
                
            O algoritmo escolhe o item de índice 3 (Criar Novo Promotor).
            O Aprendizado: Se escolher o índice 3 for uma decisão ruim (custar muito caro), 
            o RKO vai evoluir para ter um key menor (ex: 0.20) nas próximas gerações, forçando a escolha do índice 0 ou 1 (Promotores existentes).
            """
            #=======================================================

            # 6. A Execução

            """
            Proteção contra erros de arredondamento:

            -Se a lista tem tamanho 5 e a chave for muito próxima de 1.0, a conta int(1.0 * 5) dá 5.

            -Mas os índices de uma lista de tamanho 5 são 0, 1, 2, 3, 4. O índice 5 daria erro (IndexError).

            -Essa linha garante que, se a matemática "passar do ponto", nós pegamos o último item da lista.
            """
            
            idx_escolhido = int(key * len(promotores_possiveis))
            if idx_escolhido >= len(promotores_possiveis):
                idx_escolhido = len(promotores_possiveis) - 1
            
            index_promotor_bin, dia_promotor_bin = promotores_possiveis[idx_escolhido]

            """
            Aqui pegamos a opção que ganhou o sorteio: 
            -Se a tupla for (-1, -1), as variáveis recebem -1 (Sinal de Novo Promotor).
            -Se a tupla for (0, 2), significa "Promotor 0, Dia 2 (Quarta)".
            """
            index_promotor_bin, dia_promotor_bin = promotores_possiveis[idx_escolhido]

            #Se o índice for de um novo promotor, adiciona-se um novo na lista de promotores
            if index_promotor_bin == -1:
                new_promotor = Promotores(self.velocidade, cluster_id=cluster_da_visita)
        
                dia_novo = int(visit_keys[idx] * 6)
                if dia_novo >= 6: dia_novo = 5
                
                new_promotor.adicionar_loja(dia_novo, coords, carga, visit_keys[idx])
                promotores_bin.append(new_promotor)
                donos_das_lojas[coords] = len(promotores_bin) - 1

            #Se o promotor já existe, adiciona-se a loja na sua rota com base na visit_keys    
            else:
                promotor = promotores_bin[index_promotor_bin]
                promotor.adicionar_loja(dia_promotor_bin, coords, carga, visit_keys[idx])

                #Registrando qual loja pertence a qual promotor
                donos_das_lojas[coords] = index_promotor_bin
                
        #=======================================================

        #6. Calculo da função objetivo

        """
        Função objetivo utilizada tenta maximizar: F0 = len(promotores_bin) + (menor_carga / 1000000000000)

        Termo principal: número de promotorese
            -> Minimiza o número de promotores pois é o custo principal.
            -> Peso é 1 por promotor
        
        Critério de desempate: Carga do promotor menos ocupado dividida por 1 mi
            -> Penaliza desbalanceamento (um promotor muito ocioso)
            -> Peso muito pequeno (apenas para desempate)

        Ex.: 
        # Solução A: 3 promotores balanceados       
            Prom_0: 2400 min
            Prom_1: 2380 min
            Prom_2: 2350 min
            menor_carga = 2350

            FO_A = 3 + (2350 / 1000000.0)
            FO_A = 3 + 0.002350
            FO_A = 3.002350
        
        # Solução B: 3 promotores desbalanceados
            Prom_0: 2800 min
            Prom_1: 2750 min
            Prom_2: 1200 min ← Muito ocioso!
            menor_carga = 1200

            FO_B = 3 + (1200 / 1000000.0)
            FO_B = 3 + 0.001200
            FO_B = 3.001200

        Portanto A é melhor que B pois B é penalizado no desbalanceamento. FO_A > FO_B
        """

        """
        Limitações da função objetivo atual:
            ⚠️ Penaliza apenas o promotor MENOS ocupado (não vê sobrecargas)
            ⚠️ Peso do desbalanceamento é muito baixo (~0.002 vs 1.0)
            ⚠️ Não considera rentabilidade das lojas (Fase 2)
            ⚠️ Não penaliza diretamente tempo de deslocamento
        """
        #=======================================================
        
        # --- Definição de Pesos (Custos) ---
        P_promotor = 750.0
        P_hr_extra = 0.3408 # (20.45 / 60)
        P_dist = 0.06 # R$/m
        P_hr_extra_abusiva = 10_000 # Custo Brutal

        """
        P_promotor = 750.0
        P_hr_extra = 0.3408 # (20.45 / 60)
        P_dist = 0.06 # R$/m
        P_hr_extra_abusiva = 10_000 # Custo Brutal
        """

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

            # Aplica a Lógica de Penalidade (Ponto de Ruptura)
            if he_minutos_semanal_promotor <= LIMITE_HE_SEMANAL:
                # Zona Segura: Penalidade Padrão
                Custo_3 += (he_minutos_semanal_promotor) * P_hr_extra
            else:
                # Zona Abusiva: Penalidade Severa (Simula custo de contratação)
                excesso = he_minutos_semanal_promotor - LIMITE_HE_SEMANAL
                
                penalidade_normal = (LIMITE_HE_SEMANAL) * P_hr_extra
                penalidade_abusiva = (excesso) * P_hr_extra_abusiva
                
                Custo_3 += penalidade_normal + penalidade_abusiva

        # --- Quarta Parcela : Distribuição de Carga ----

        TOLERANCIA_DIFERENCA = 10 * 60
        P_BALANCEAMENTO = 100_000

        Custo_4 = 0

        if len(promotores_bin) > 1:
            cargas_horarias = [p.carga_total() for p in promotores_bin]
            maior_carga = max(cargas_horarias)
            menor_carga = min(cargas_horarias)
            diferenca = maior_carga - menor_carga

            if diferenca > TOLERANCIA_DIFERENCA:
                excesso_desbalanceamento = diferenca - TOLERANCIA_DIFERENCA
                Custo_4 = excesso_desbalanceamento * P_BALANCEAMENTO

        # --- Quinta Parcela: Garantir frequência mínima das lojas ---
        P_FREQUENCIA = 1_000_000  # penalização grande

        # Conta quantas vezes cada coordenada foi visitada
        contador_visitas = {coord: 0 for coord in self.visit_coords}

        for promotor in promotores_bin:
            todas_coords = (
                promotor.coords_segunda +
                promotor.coords_terca +
                promotor.coords_quarta +
                promotor.coords_quinta +
                promotor.coords_sexta +
                promotor.coords_sabado
            )
            for coord in todas_coords:
                contador_visitas[coord] += 1

        # Penaliza lojas com visitas insuficientes
        Custo_5 = 0
        for i, coord in enumerate(self.visit_coords):
            visitas_realizadas = contador_visitas[coord]
            visitas_necessarias = self.frequencias[i]

            if visitas_realizadas < visitas_necessarias:
                deficit = visitas_necessarias - visitas_realizadas
                Custo_5 += deficit * P_FREQUENCIA

        #Opcional
        """
        P_VIOLACAO_CLUSTER = 1_000_000  # Penalidade severa
        Custo_6 = 0

        for promotor in promotores_bin:
            todas_coords = (promotor.coords_segunda + promotor.coords_terca + 
                        promotor.coords_quarta + promotor.coords_quinta + 
                        promotor.coords_sexta + promotor.coords_sabado)
            
            if len(todas_coords) > 0:
                clusters_atendidos = set()
                for coord in todas_coords:
                    idx_loja = self.visit_coords.index(coord)
                    cluster = self.clusterizador.get_cluster_da_loja(idx_loja)
                    clusters_atendidos.add(cluster)
                
                # Penaliza PESADAMENTE se atender múltiplos clusters
                if len(clusters_atendidos) > 1:
                    num_violacoes = len(clusters_atendidos) - 1
                    Custo_6 += num_violacoes * P_VIOLACAO_CLUSTER
                    
                    if view_solution:
                        print(f"AVISO: Promotor atende {len(clusters_atendidos)} clusters!")
        
        fitness_total = Custo_1 + Custo_2 + Custo_3 + Custo_4 + Custo_5 + Custo_6
        """

        # Cálculo Final
        fitness_total = Custo_1 + Custo_2 + Custo_3 + Custo_4 + Custo_5

        # =======================================================
        
        # Retorno Visualização (Objeto)
        if view_solution:
            print("\n" + "="*50)
            print("          RELATÓRIO FINANCEIRO DETALHADO          ")
            print("="*50)

            qtd_promotores = len(promotores_bin)
            
            # 1. Custo Equipe
            financeiro_equipe = qtd_promotores * P_promotor
            
            # 2. Custo Distância
            dist_total_frota = sum([p.dist_total() for p in promotores_bin])
            financeiro_distancia = dist_total_frota * P_dist
            
            # 3. Custo Hora Extra (Somando apenas o que excede, sem multa abusiva)
            total_minutos_he_reais = 0
            for p in promotores_bin:
                for d in range(6):
                    lim = 240 if d == 5 else 480
                    t = p.tempo_total_dia(d)
                    if t > lim:
                        total_minutos_he_reais += (t - lim)
            
            financeiro_he = total_minutos_he_reais * P_hr_extra
            
            financeiro_total = financeiro_equipe + financeiro_distancia + financeiro_he

            print(f"1. EQUIPE ({qtd_promotores} promotores):     R$ {financeiro_equipe:.2f}")
            print(f"2. COMBUSTÍVEL ({dist_total_frota:.1f} un): R$ {financeiro_distancia:.2f}")
            print(f"3. HORAS EXTRAS ({total_minutos_he_reais:.0f} min):  R$ {financeiro_he:.2f}")
            print("-" * 50)
            print(f"CUSTO OPERACIONAL TOTAL:      R$ {financeiro_total:.2f}")
            print(f"FITNESS OTIMIZADO (RKO):      {fitness_total:.2f}")

            #Validar exclusividade no cluster
            self.clusterizador.validar_exclusividade(promotores_bin, self.visit_coords)

            return promotores_bin

        # Log em Tempo Real (Console)
        if fitness_total < self.melhor_fitness_encontrado:
            self.melhor_fitness_encontrado = fitness_total
            
            qtd_promotores = len(promotores_bin)

            print(f" >>> [NOVO RECORD] Promotores: {qtd_promotores} | HE Total: {total_minutos_he_frota:.0f} min | (Fitness/Custo: R$ {fitness_total:.2f})")

            if view_solution:
                #Valida exclusividade
                self.clusterizador.validar_exclusividade(promotores_bin, self.visit_coords)

        return fitness_total
        
        #=======================================================

        """
        menor_carga = 1000000000000
        for promotor in promotores_bin:
            if promotor.carga_total() < menor_carga:
                menor_carga = promotor.carga_total()

        if view_solution:
            return promotores_bin
        return len(promotores_bin) + (menor_carga / 1000000.0)
        """

def verificar_clusters(env):
    """
    Plota os clusters
    """
    print("\n📊 Gerando visualização dos clusters...")
        
    # Chama o método _imprimir_estatisticas para mostrar dados
    env.clusterizador._imprimir_estatisticas()
        
    # Plota os clusters
    env.clusterizador.plot_clusters()
        
    print("✅ Visualização concluída!")

veloc_100_lojas = 18 #s/unidade
veloc_50_lojas = 15 #s/unidade
veloc_20_lojas = 12 #s/unidade
veloc_10_lojas = 10 #s/unidade

if __name__ == "__main__":

    #=========================
    n_lojas = 10
    inst = 1
    #=========================

    mapa_velocidades = {
        10: veloc_10_lojas,
        20: veloc_20_lojas,
        50: veloc_50_lojas,
        100: veloc_100_lojas
    }

    velocidade_atual = mapa_velocidades.get(n_lojas)

    list_coords, list_visits, list_frequency, matriz = get_instancia_csv(n_lojas, inst)
    
    env = RKO_Base(60, velocidade_atual, n_lojas, inst) #Alterar Velocidade da instância

    #Entender os clusters criados
    print("\n" + "="*80)
    print("                    ANÁLISE DE CLUSTERIZAÇÃO")
    print("="*80)

    verificar_clusters(env)

    solver = RKO(env, print_best=True)
    final_cost, final_solution, time_to_best = solver.solve(60, brkga=1, ils=1, lns=1)
    
    solucao_final = env.cost(env.decoder(final_solution), view_solution=True) 

    receita_bruta_fase1 = 0

    for id_loja in range(len(list_coords)):
        # 1. Pega a frequência fixa do arquivo
        freq_inicial = list_frequency[id_loja]
        
        # 2. Busca o valor na matriz de lucros
        # A matriz é base 0 (índice 0 = freq 1), então subtraímos 1 da frequência
        if freq_inicial > 0:
            lucro_loja = matriz[id_loja][freq_inicial - 1]
        else:
            lucro_loja = 0.0
            
        # 3. Acumula
        receita_bruta_fase1 += lucro_loja

    print("-" * 40)
    print(f"RECEITA BRUTA TOTAL (Fase 1): R$ {receita_bruta_fase1:,.2f}")
    print("="*50 + "\n")

    # --- RELATÓRIO DETALHADO E VERIFICAÇÃO ---
    print("\n" + "="*40)
    print("       ESTATÍSTICAS FINAIS DA FROTA       ")
    print("="*40)

    # Dicionário para rastrear conflitos: Coord -> Lista de Promotores
    mapa_visitas_global = {}
    
    total_lojas_atendidas = 0
    total_visitas_realizadas = 0

    for i, promotor in enumerate(solucao_final):
        # 1. Coleta todas as coordenadas visitadas
        todas_coords = (
            promotor.coords_segunda + promotor.coords_terca + 
            promotor.coords_quarta + promotor.coords_quinta + 
            promotor.coords_sexta + promotor.coords_sabado
        )
        
        # 2. Identifica lojas únicas (Set remove duplicatas do mesmo promotor)
        coords_unicas = set(todas_coords)
        
        # 3. Converte Coordenadas -> IDs de Loja para exibição legível
        ids_lojas = []
        for coord in coords_unicas:
            # Lógica de Conflito: Registra quem visitou essa coord
            if coord not in mapa_visitas_global:
                mapa_visitas_global[coord] = []
            mapa_visitas_global[coord].append(i)

            # Lógica de Exibição: Encontra o ID (index) na lista original
            try:
                id_real = list_coords.index(coord)
                ids_lojas.append(id_real)
            except ValueError:
                ids_lojas.append("?") # Caso não ache (improvável)

        # Ordena para ficar bonito: [0, 1, 5, 9]
        ids_lojas.sort()
        
        # Estatísticas individuais
        carga_h = promotor.carga_total() / 60.0
        num_visitas = len(todas_coords)
        
        # Acumuladores globais
        total_lojas_atendidas += len(coords_unicas)
        total_visitas_realizadas += num_visitas

        # --- IMPRESSÃO DO PROMOTOR ---

        cargas_dias = {"Segunda" : promotor.carga_segunda, 
                       "Terça" : promotor.carga_terca, 
                       "Quarta" : promotor.carga_quarta, 
                       "Quinta" : promotor.carga_quinta, 
                       "Sexta" : promotor.carga_sexta, 
                       "Sabado" : promotor.carga_sabado}

        print(f"PROMOTOR {i}")
        print(f"  > Carga Horária: {carga_h:.1f}h")
        print(f"  > Total Visitas: {num_visitas}")
        print(f"  > Carteira ({len(ids_lojas)} lojas): {ids_lojas}\n")

        for dia, minutos in cargas_dias.items():
            print(f"  > Carga {dia}: {minutos/60:.1f}h")

        print("-" * 60)

    # --- ESTATÍSTICAS GERAIS ---
    if len(solucao_final) > 0:
        media_lojas = total_lojas_atendidas / len(solucao_final)
        print(f"\nMÉDIAS DA EQUIPE:")
        print(f"  Lojas/Promotor: {media_lojas:.2f}")
    
    # --- RELATÓRIO DE CONFLITOS ---
    print("\n" + "="*60)
    print("          VERIFICAÇÃO DE EXCLUSIVIDADE          ")
    print("="*60)
    
    tem_conflito = False
    for coord, lista_promotores in mapa_visitas_global.items():
        if len(lista_promotores) > 1:
            tem_conflito = True
            # Recupera o ID para mostrar no erro
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

    #========================================

    # Loop de Plotagem
    while True:
        try:
            entrada = input("Digite o número do promotor para plotar a rota (ou -1 para sair): ")
            promotor = int(entrada)
            if promotor == -1:
                break
            
            dia = int(input("Digite o dia (0=Seg, 1=Ter, 2=Qua, 3=Qui, 4=Sex, 5=Sab): "))
            
            if 0 <= promotor < len(solucao_final):
                solucao_final[promotor].plot_rota(dia)
            else:
                print("Promotor inválido.")
        except ValueError:
            print("Entrada inválida.")
    
    print("\n" + "="*60)
    print("        VERIFICAÇÃO FINAL DA FREQUÊNCIA MÍNIMA        ")
    print("="*60)

    # Inicializa contador de visitas por loja (1 entrada por loja)
    contador_visitas = {coord: 0 for coord in list_coords}

    # Conta visitas reais da solução final
    for promotor in solucao_final:
        todas_coords = (
            promotor.coords_segunda +
            promotor.coords_terca +
            promotor.coords_quarta +
            promotor.coords_quinta +
            promotor.coords_sexta +
            promotor.coords_sabado
        )
        for coord in todas_coords:
            contador_visitas[coord] += 1

    # Verificação loja por loja
    violacoes = []
    for i, coord in enumerate(list_coords):
        visitas = contador_visitas[coord]
        minimo = list_frequency[i]

        if visitas < minimo:
            violacoes.append((i, visitas, minimo))

    # Impressão detalhada
    print("\nRelatório por loja:")
    for i, coord in enumerate(list_coords):
        visitas = contador_visitas[coord]
        minimo = list_frequency[i]
        status = "OK" if visitas >= minimo else "FALHA"
        print(f"Loja {i:3d} | Visitas = {visitas:2d} | Mínimo = {minimo:2d} | {status}")

    # Resultado final
    print("\n" + "="*60)
    if len(violacoes) == 0:
        print(" ✔️ SUCESSO: Todas as lojas atenderam a frequência mínima!")
    else:
        print(" ❌ FALHA: Existem lojas com visitas insuficientes!\n")
        print("Lojas problemáticas:")
        for loja, visitas, minimo in violacoes:
            print(f" - Loja {loja}: fez {visitas} visitas, mas precisava de {minimo}")
    print("="*60)