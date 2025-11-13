from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import os

"""
Definições de velocidades (em segundos por unidade) para cada categoria de instância que foi especificada no pdf.
"""

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

class RKO_Base(ABC):
    """
    Classe base abstrata para o problema RKO
    """

    def __init__(self, df_instancia: pd.DataFrame):
        super.__init__()

        """
        Definição de atributos para o problema.
        """

        self.instance_name = "Suzano_RKO_Problem"

        self.num_lojas = len(df_instancia) # Número de lojas na instância
        self.tam_solution = sum(df_instancia['initial_frequency']) # Tamanho do vetor RKO é a soma das frequências de visitas

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

if __name__ == "__main__":
    list_coords, list_visits, list_frequency = get_instancia_csv(10,1)
    print(list_coords)

    