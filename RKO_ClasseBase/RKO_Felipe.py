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
"""
Definições de velocidades (em segundos por unidade) para cada categoria de instância que foi especificada no pdf.
"""

import numpy as np
import matplotlib.pyplot as plt

class Promotores:
    # 1. ADICIONADO "nome_promotor" E "nome_rota" AO INIT
    def __init__(self, velocidade):
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


    def carga_total(self):
        return (self.carga_segunda + self.carga_terca + self.carga_quarta +
                self.carga_quinta + self.carga_sexta + self.carga_sabado)
    
    def adicionar_loja(self, dia, coord, carga, ordem_loja):
        if dia == 0:
            idx_loja = ordem_loja * (len(self.coords_segunda) + 1)
            idx_loja = int(idx_loja)
            self.coords_segunda.insert(idx_loja, coord)
            self.cargas_segunda.append(carga)
            self.carga_segunda = sum(self.cargas_segunda) + self.custo_viagem(self.coords_segunda)
        elif dia == 1:
            idx_loja = ordem_loja * (len(self.coords_terca) + 1)
            idx_loja = int(idx_loja)

            self.coords_terca.insert(idx_loja, coord)
            self.cargas_terca.append(carga)
            self.carga_terca = sum(self.cargas_terca) + self.custo_viagem(self.coords_terca)
        elif dia == 2:
            idx_loja = ordem_loja * (len(self.coords_quarta) + 1)
            idx_loja = int(idx_loja)

            self.coords_quarta.insert(idx_loja, coord)
            self.cargas_quarta.append(carga)
            self.carga_quarta = sum(self.cargas_quarta) + self.custo_viagem(self.coords_quarta)
        elif dia == 3:
            idx_loja = ordem_loja * (len(self.coords_quinta) + 1)
            idx_loja = int(idx_loja)

            self.coords_quinta.insert(idx_loja, coord)
            self.cargas_quinta.append(carga)
            self.carga_quinta = sum(self.cargas_quinta) + self.custo_viagem(self.coords_quinta)
        elif dia == 4:
            idx_loja = ordem_loja * (len(self.coords_sexta) + 1)
            idx_loja = int(idx_loja)

            self.coords_sexta.insert(idx_loja, coord)
            self.cargas_sexta.append(carga)
            self.carga_sexta = sum(self.cargas_sexta) + self.custo_viagem(self.coords_sexta)
        elif dia == 5:
            idx_loja = ordem_loja * (len(self.coords_sabado) + 1)
            idx_loja = int(idx_loja)

            self.coords_sabado.insert(idx_loja, coord)
            self.cargas_sabado.append(carga)
            self.carga_sabado = sum(self.cargas_sabado) + self.custo_viagem(self.coords_sabado)
            
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
        custo = 0
        if len(coords) < 2:
            return custo
        for i in range(len(coords) - 1):
            cidade_atual = coords[i]
            proxima_cidade = coords[i + 1]
            distancia = np.linalg.norm(np.array(cidade_atual) - np.array(proxima_cidade))
            custo += distancia * self.velocidade
        return custo/60


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
        self.velocidade = velocidade
        self.max_time = tempo  # Tempo máximo de execução para cada metaheurística (em segundos)
        self.instance_name = "Suzano_RKO_Problem"
        list_coords, list_visits, list_frequency = get_instancia_csv(50,1)

        self.dict_best: dict = {}

        self.num_lojas = len(list_coords) # Número de lojas na instância
        self.tam_solution = 3 * sum(list_frequency) # Tamanho do vetor RKO é a soma das frequências de visitas
        
        self.frequencias = list_frequency  # Lista com as frequências de visitas de cada loja
        self.visit_durations = list_visits
        self.visit_coords = list_coords

        self.total_visit_duration = []
        self.total_coords = []
        for i in range(len(self.frequencias)):
            for j in range(self.frequencias[i]):
                self.total_visit_duration.append(self.visit_durations[i])
                self.total_coords.append(self.visit_coords[i])


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
        # print("Keys:", keys)
        tam = len(keys)
        tam_parts = tam // 3
        order_keys = keys[0:tam_parts]
        promoteres_keys = keys[tam_parts:2 * tam_parts]
        visit_keys = keys[2 * tam_parts:tam]

        order = np.argsort(order_keys)

        # print("Order:", order)
        # print("Promotores keys:", promoteres_keys)
        return list(order) + list(promoteres_keys) + list(visit_keys)
    
    def cost(self, solution, view_solution=False):
        tam = len(solution)
        tam_parts = tam // 3
        order = solution[0:tam_parts]
        promotores_keys = solution[tam_parts:2 * tam_parts]
        visit_keys = solution[2 * tam_parts:tam]
        # print("Order:", order)
        # print("Promotores keys:", promotores_keys)

        promotores_bin = [Promotores(self.velocidade)]

        for idx, loja in enumerate(order):
            loja = int(loja)
            carga = self.total_visit_duration[loja]
            coords = self.total_coords[loja]
            key = promotores_keys[idx]
            # print( key , idx, loja)

            promotores_possiveis = []
            for i in range(len(promotores_bin)):
                dias_possiveis = promotores_bin[i].dias_possiveis(carga)
                for dia in dias_possiveis:
                    promotores_possiveis.append( (i, dia) )

            if len(promotores_possiveis) > 0:
                idx_promotor = int(key * len(promotores_possiveis))
                # print(key, idx_promotor, len(promotores_possiveis))

                index_promotor_bin , dia_promotor_bin = promotores_possiveis[idx_promotor]

                promotor = promotores_bin[index_promotor_bin]
                promotor.adicionar_loja(dia_promotor_bin, coords, carga, visit_keys[idx])

            else:
                new_promotor = Promotores(self.velocidade)
                dia = int(key * 6)  
                new_promotor.adicionar_loja(dia, coords, carga, visit_keys[idx])
                promotores_bin.append(new_promotor)


        menor_carga = 1000000000000
        for promotor in promotores_bin:
            if promotor.carga_total() < menor_carga:
                menor_carga = promotor.carga_total()

        if view_solution:
            return promotores_bin
        return len(promotores_bin) + (menor_carga / 1000000.0)

            

            
                

            



            
        

if __name__ == "__main__":
    list_coords, list_visits, list_frequency = get_instancia_csv(10,1)
    print(list_coords)
    print(list_visits)
    print(list_frequency)


    env = RKO_Base(60, veloc_50_lojas)
    solver = RKO(env, print_best=True)
    final_cost, final_solution, time_to_best = solver.solve(60, brkga=1, ils=1, lns=1)

    solucao_final = env.cost(env.decoder(final_solution), view_solution=True)  

    for promotor in solucao_final:
        print(f"Carga Total: {promotor.carga_total():.2f} minutos, Média por dia: {promotor.carga_total()/6:.2f} minutos")  

    while True:
        promotor = int(input("Digite o número do promotor para plotar a rota (ou -1 para sair): "))
        if promotor == -1:
            break
        dia = int(input("Digite o dia da semana (0=Segunda, 1=Terça, 2=Quarta, 3=Quinta, 4=Sexta, 5=Sábado): "))
        if 0 <= promotor < len(solucao_final):
            solucao_final[promotor].plot_rota(dia)