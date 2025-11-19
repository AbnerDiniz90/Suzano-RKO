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

class Promotores:
    def __init__(self, velocidade):
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
            1. Tenta encontrar dias onde a loja cabe SEM hora extra (Hard Constraint).
            2. Se não houver nenhum, retorna o dia que gera a MENOR hora extra (Soft Constraint).
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


veloc_100_lojas = 18 #s/unidade
veloc_50_lojas = 15 #s/unidade
veloc_20_lojas = 12 #s/unidade
veloc_10_lojas = 10 #s/unidade

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

    if num_lojas <= 0 or num_lojas > 50 or num_instancia <= 0 or num_instancia > 50:
        raise ValueError("Número de lojas ou número da instância não compatível.")

    pasta_tamanho = f"{num_lojas}_stores"

    pasta_instancia = f"instance_{str(num_instancia).zfill(3)}" 

    nome_arquivo = "stores.csv"

    caminho_completo = os.path.join(base_path, pasta_tamanho, pasta_instancia, nome_arquivo)

    df_instancia = pd.read_csv(caminho_completo)

    list_coordinates = list(df_instancia[['x_coordinate', 'y_coordinate']].itertuples(index=False, name=None))
    list_visit_duration = df_instancia['visit_duration_minutes'].tolist()
    list_frequency = df_instancia['initial_frequency'].tolist()

    return list_coordinates, list_visit_duration, list_frequency

class RKO_Base():
    """
    Classe base abstrata para o problema RKO
    """

    def __init__(self, tempo, velocidade):
        """
        Definição de atributos para o problema.
        """

        #--------------------------
        self.melhor_fitness_encontrado = float('inf')
        #--------------------------
        

        self.velocidade = velocidade    # Velocidade de deslocamento
        self.max_time = tempo           # Tempo máximo de execução para cada metaheurística (em segundos)
        self.instance_name = "Suzano_RKO_Problem"
        list_coords, list_visits, list_frequency = get_instancia_csv(50,1) #Carregamento de dados da instância especificada

        self.dict_best: dict = {}

        self.num_lojas = len(list_coords)           # Número de lojas na instância
        self.tam_solution = 3 * sum(list_frequency) # Tamanho do vetor RKO é a soma das frequências de visitas. É 3n pois tem as partes:
                                                    # 1. Ordem de inserção das visitas 
                                                    # 2. Alocação de promotor/dia para cada visita
                                                    # 3. Sequência na rota de cada visita
        
        self.frequencias = list_frequency       # Lista com as frequências de visitas de cada loja
        self.visit_durations = list_visits      # Lista com a duração das visitas
        self.visit_coords = list_coords         # Lista com as coordenadas das lojas

        self.total_visit_duration = []
        self.total_coords = []

        # Transforma dados de lojas únicas em dados de visitas individuais.
        for i in range(len(self.frequencias)):
            for j in range(self.frequencias[i]):
                self.total_visit_duration.append(self.visit_durations[i])
                self.total_coords.append(self.visit_coords[i])
        
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
        order = solution[0:tam_parts]
        promotores_keys = solution[tam_parts:2 * tam_parts]
        visit_keys = solution[2 * tam_parts:tam]
        #=======================================================

        # 2. Inicialização
        promotores_bin = [Promotores(self.velocidade)]
        #=======================================================

        # 3. Processamento para cada visita
        for idx, loja in enumerate(order):
            loja = int(loja)
            carga = self.total_visit_duration[loja]
            coords = self.total_coords[loja]

            # Chave aleatória do RKO (0.0 a 1.0) que vai decidir ONDE colocar a loja
            key = promotores_keys[idx]
            #=======================================================

            # 4. Coleta de opções
            promotores_possiveis = []

            """
            O loop abaixo verifica para cada promotor existente se há espaço.
            Por conta de ser uma restrição não rígida, a resposta é sempre "Sim" (mesmo que gere Hora Extra).
            """

            for i in range(len(promotores_bin)):
                #Sempre haverá dias disponíveis, contudo ou será com hr extra ou será tempo livre de um novo promotor
                dias_validos = promotores_bin[i].dias_possiveis(carga)
                for dia in dias_validos:
                    promotores_possiveis.append((i, dia))
            
            promotores_possiveis.append((-1, -1)) 

            # 5. Escolha e alocação baseada na Chave Aleatória
            idx_escolhido = int(key * len(promotores_possiveis))
            
            if idx_escolhido >= len(promotores_possiveis):
                idx_escolhido = len(promotores_possiveis) - 1

            index_promotor_bin, dia_promotor_bin = promotores_possiveis[idx_escolhido]

            if index_promotor_bin == -1:
                new_promotor = Promotores(self.velocidade)
                
                dia_novo = int(visit_keys[idx] * 6)
                if dia_novo >= 6: dia_novo = 5
                
                new_promotor.adicionar_loja(dia_novo, coords, carga, visit_keys[idx])
                promotores_bin.append(new_promotor)
            else:
                promotor = promotores_bin[index_promotor_bin]
                promotor.adicionar_loja(dia_promotor_bin, coords, carga, visit_keys[idx])
                
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
        
        # --- Definição de Valores (Ordem Corrigida) ---
        Custo_km = 0.06
        Valor_he = 0.3408  # (20.45 / 60)
        Salario = 750.0

        # --- Definição de Pesos (Fitness) ---
        P_promotor = 1_000_000
        P_hr_extra = 100
        P_dist = 100
        P_hr_extra_abusiva = 10_000_000 # Penalidade Brutal

        # O Limite é calculado APÓS definir Salario e Valor_he
        LIMITE_HE_SEMANAL = Salario / Valor_he 

        # --- Primeira Parcela: Contratação ---
        Custo_1 = P_promotor * len(promotores_bin) * Salario

        # --- Segunda Parcela: Distância ---
        Custo_dist_total = 0
        for promotor in promotores_bin:
            dist = promotor.dist_total()
            Custo_dist_total += dist * Custo_km # Assumindo Fator=1.0 implícito
        
        Custo_2 = Custo_dist_total * P_dist

        # --- Terceira Parcela: Hora Extra (Com Lógica de Break-even) ---
        Custo_3 = 0 # Fitness (Pontos)
        custo_he_financeiro_total = 0 # Dinheiro Real (R$)

        for promotor in promotores_bin:
            # Reinicia contagem para CADA promotor
            he_minutos_semanal_promotor = 0 
            
            for dia in range(6):
                limite = 240 if dia == 5 else 480
                tempo_total = promotor.tempo_total_dia(dia)

                if tempo_total > limite:
                    he_minutos_semanal_promotor += (tempo_total - limite)
            
            # Acumula o custo financeiro real
            custo_he_financeiro_total += he_minutos_semanal_promotor * Valor_he

            # Aplica a Lógica de Penalidade (Ponto de Ruptura)
            if he_minutos_semanal_promotor <= LIMITE_HE_SEMANAL:
                # Zona Segura: Penalidade Padrão
                Custo_3 += (he_minutos_semanal_promotor * Valor_he) * P_hr_extra
            else:
                # Zona Abusiva: Penalidade Severa (Simula custo de contratação)
                excesso = he_minutos_semanal_promotor - LIMITE_HE_SEMANAL
                
                penalidade_normal = (LIMITE_HE_SEMANAL * Valor_he) * P_hr_extra
                penalidade_abusiva = (excesso * Valor_he) * P_hr_extra_abusiva
                
                Custo_3 += penalidade_normal + penalidade_abusiva

        # =======================================================
        
        # Retorno Visualização (Objeto)
        if view_solution:
            return promotores_bin
        
        # Cálculo Final
        fitness_total = Custo_1 + Custo_2 + Custo_3

        # Log em Tempo Real (Console)
        if fitness_total < self.melhor_fitness_encontrado:
            self.melhor_fitness_encontrado = fitness_total
            
            qtd_promotores = len(promotores_bin)
            
            # Custo Real para o chefe ver
            custo_financeiro_estimado = (
                (qtd_promotores * Salario) + 
                Custo_dist_total + # Já está multiplicado por Custo_km lá em cima
                custo_he_financeiro_total
            )

            print(f" >>> [NOVO RECORD] Promotores: {qtd_promotores} | HE Total: {custo_he_financeiro_total/Valor_he:.0f} min | Custo Real: R$ {custo_financeiro_estimado:.2f} | (Fitness: {fitness_total:.0f})")

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


if __name__ == "__main__":
    list_coords, list_visits, list_frequency = get_instancia_csv(20, 1)
    
    # Configuração do Ambiente e Solver
    env = RKO_Base(60, veloc_50_lojas)
    solver = RKO(env, print_best=True)
    
    # Execução
    final_cost, final_solution, time_to_best = solver.solve(60, brkga=1, ils=1, lns=1)
    
    # Decodificação da Melhor Solução
    solucao_final = env.cost(env.decoder(final_solution), view_solution=True)  

    # --- ESTATÍSTICAS DA SOLUÇÃO ---
    print("\n" + "="*40)
    print("       ESTATÍSTICAS FINAIS DA FROTA       ")
    print("="*40)
    
    total_lojas_atendidas = 0
    total_visitas_realizadas = 0
    qtd_promotores = len(solucao_final)
    
    for i, promotor in enumerate(solucao_final):
        qtd_lojas = promotor.total_lojas_unicas()
        qtd_visitas = promotor.total_visitas()
        carga = promotor.carga_total()
        
        total_lojas_atendidas += qtd_lojas
        total_visitas_realizadas += qtd_visitas
        
        print(f"Promotor {i}: {qtd_lojas} lojas únicas | {qtd_visitas} visitas | Carga: {carga/60:.1f}h")

    if qtd_promotores > 0:
        media_lojas = total_lojas_atendidas / qtd_promotores
        media_visitas = total_visitas_realizadas / qtd_promotores
        
        print("-" * 40)
        print(f"Média de Lojas Únicas por Promotor: {media_lojas:.2f}")
        print(f"Média de Visitas por Promotor:      {media_visitas:.2f}")
        print("="*40 + "\n")

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