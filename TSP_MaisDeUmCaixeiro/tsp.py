import numpy as np
import os
import sys
import random
from abc import ABC, abstractmethod
current_directory = os.path.dirname(os.path.abspath(__file__))
project_root_directory = os.path.dirname(current_directory)
sys.path.append(project_root_directory)
from RKO import RKO
from Environment import RKOEnvAbstract, check_env
import matplotlib.pyplot as plt

class TSPProblem(RKOEnvAbstract):
    """
    An implementation of the Traveling Salesperson Problem (TSP) environment for the RKO solver.
    This class generates a random instance upon initialization.
    """
    def __init__(self, num_cities: int = 20, num_salesman: int = 1):
        super().__init__()
        print(f"Generating a random TSP instance with {num_cities} cities and {num_salesman} salesman.")

        self.num_cities = num_cities
        self.num_salesman = num_salesman

        self.instance_name = f"TSP_{num_cities}_cities_{num_salesman}_salesman"
        self.LS_type: str = 'Best'
        self.dict_best: dict = {}

        # Generate city coordinates and the distance matrix
        self.cities = self._generate_cities(num_cities)
        self.distance_matrix = self._calculate_distance_matrix()

        self.save_q_learning_report = False

        # IMPORTANTE: tam_solution agora inclui cidades + caixeiros
        self.tam_solution = self.num_cities + self.num_salesman

        # Parâmetros dos metaheurísticos
        self.BRKGA_parameters = {
            'p': [100, 50],          
            'pe': [0.20, 0.15],      
            'pm': [0.05],        
            'rhoe': [0.70]       
        }

        self.SA_parameters = {
            'SAmax': [10, 5],     
            'alphaSA': [0.5, 0.7],  
            'betaMin': [0.01, 0.03],   
            'betaMax': [0.05, 0.1],   
            'T0': [10]      
        }

        self.ILS_parameters = {
            'betaMin': [0.10, 0.5],   
            'betaMax': [0.20, 0.15]    
        }

        self.VNS_parameters = {
            'kMax': [5, 3],         
            'betaMin': [0.05, 0.1]    
        }

        self.PSO_parameters = {
            'PSize': [100, 50],     
            'c1': [2.05],     
            'c2': [2.05],        
            'w': [0.73]         
        }

        self.GA_parameters = {
            'sizePop': [100, 50],    
            'probCros': [0.98],  
            'probMut': [0.005, 0.01]   
        }

        self.LNS_parameters = {
            'betaMin': [0.10],   
            'betaMax': [0.30],  
            'TO': [100],       
            'alphaLNS': [0.95, 0.9] 
        }

    def _generate_cities(self, num_cities: int) -> np.ndarray:
        """Generates random (x, y) coordinates for each city."""
        return np.random.rand(num_cities, 2) * 100

    def _calculate_distance_matrix(self) -> np.ndarray:
        """Computes the Euclidean distance between every pair of cities."""
        num_cities = len(self.cities)
        dist_matrix = np.zeros((num_cities, num_cities))
        for i in range(num_cities):
            for j in range(i, num_cities):
                dist = np.linalg.norm(self.cities[i] - self.cities[j])
                dist_matrix[i, j] = dist_matrix[j, i] = dist
        return dist_matrix

    def decoder(self, keys: np.ndarray) -> dict[int, list[int]]:
        """
        Decodifica um vetor de random-keys em rotas para múltiplos caixeiros.
        
        Lógica:
        - Índices 0 a (num_cities-1) representam cidades
        - Índices num_cities a (num_cities+num_salesman-1) representam caixeiros
        - Os caixeiros atuam como separadores entre as rotas
        """
        n = self.num_cities
        m = self.num_salesman

        # Inicializa dicionário de rotas (chave = ID do caixeiro)
        salesman_routes = {sm_idx: [] for sm_idx in range(n, n + m)}

        # Lista temporária para construir a rota atual
        current_route = []

        # Ordena os índices pelas chaves
        vector_indices = np.argsort(keys)

        # Encontra o último caixeiro no vetor ordenado
        last_salesman_id = -1 
        for k in range(len(vector_indices) - 1, -1, -1):
            original_id = vector_indices[k] 
            if original_id >= n and original_id < n + m: 
                last_salesman_id = k 
                break

        # Se o último elemento não for um caixeiro, rotaciona o vetor
        # para garantir que termine com um caixeiro
        if last_salesman_id != -1:
            shift_amount = (len(vector_indices) - 1) - last_salesman_id
            vector_indices = np.roll(vector_indices, shift=shift_amount)

        # Percorre o vetor ordenado e distribui as cidades entre os caixeiros
        for k in vector_indices:
            if k >= n:  # É um caixeiro
                salesman_routes[int(k)] = [int(city) for city in current_route]
                current_route = []
            else:  # É uma cidade
                current_route.append(int(k))

        return salesman_routes

    def cost(self, solution: dict[int, list[int]], final_solution: bool = False) -> float:
        """
        Calcula o custo total (distância) para todas as rotas dos caixeiros.
        
        Args:
            solution: Dicionário com {salesman_id: [lista de cidades]}
            final_solution: Flag indicando se é a solução final
            
        Returns:
            Custo total (soma das distâncias de todas as rotas)
        """
        if solution is None:
            print("WARNING: cost function received None solution. Returning high penalty.")
            return float('inf')

        total_cost = 0.0

        # Itera sobre cada caixeiro e sua rota
        for salesman_id, city_route in solution.items():
            route_cost = 0.0

            # Calcula custo apenas se a rota tiver pelo menos 2 cidades
            if len(city_route) >= 2:
                for i in range(len(city_route) - 1):
                    from_city = city_route[i]
                    to_city = city_route[i + 1]
                    
                    # Verifica índices válidos
                    if from_city >= self.num_cities or to_city >= self.num_cities:
                        print(f"ERROR: Invalid city index. from_city={from_city}, to_city={to_city}")
                        return float('inf')
                    
                    route_cost += self.distance_matrix[from_city, to_city]

            total_cost += route_cost

        # Penaliza se nenhuma rota válida foi criada mas há cidades
        if total_cost == 0 and self.num_cities > 0:
            if not solution or not any(len(route) > 0 for route in solution.values()):
                return float('inf')

        return total_cost

    def plot_routes_simple(self, routes: dict[int, list[int]], cost: float):
        """
        Plota as cidades e as rotas de todos os caixeiros.
        """
        if routes is None:
            print("Cannot plot: routes is None")
            return

        fig, ax = plt.subplots(1, 1, figsize=(10, 10))

        # Plota todas as cidades
        ax.scatter(self.cities[:, 0], self.cities[:, 1], c='blue', s=100, 
                   label='Cities', zorder=5, alpha=0.6)
        
        # Adiciona labels nas cidades
        for i, city in enumerate(self.cities):
            ax.text(city[0], city[1] + 1.5, str(i), fontsize=8, ha='center')

        # Define cores diferentes para cada caixeiro
        colors = plt.cm.rainbow(np.linspace(0, 1, self.num_salesman))

        # Plota a rota de cada caixeiro
        for idx, (salesman_id, route) in enumerate(routes.items()):
            if len(route) > 0:
                # Cria a rota fechada (retorna ao início)
                plot_route = route + [route[0]]
                
                try:
                    ordered_cities = self.cities[plot_route, :]
                    color = colors[idx % len(colors)]
                    ax.plot(ordered_cities[:, 0], ordered_cities[:, 1], 
                            '-o', color=color, linewidth=2, markersize=4,
                            label=f'Salesman {salesman_id} ({len(route)} cities)')
                except IndexError as e:
                    print(f"Error plotting route for salesman {salesman_id}: {e}")
                    print(f"Route: {route}")

        ax.set_title(f'Multi-Salesman TSP Solution (Total Cost: {cost:.2f})', fontsize=14, fontweight='bold')
        ax.set_xlabel('X Coordinate', fontsize=12)
        ax.set_ylabel('Y Coordinate', fontsize=12)
        ax.legend(fontsize=10, loc='best')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # 1. Instancia o problema com múltiplos caixeiros
    env = TSPProblem(num_cities=30, num_salesman=3)
    check_env(env)
    
    # 2. Instancia o solver RKO
    solver = RKO(
        env=env, 
        print_best=True
    )
    
    # 3. Executa a otimização
    final_cost, final_solution, time_to_best = solver.solve(
        time_total=10, 
        runs=1,
        vns=1, 
        ils=1,
        sa=1
    )
    
    # 4. Decodifica a solução e plota
    solution = env.decoder(final_solution)
    env.plot_routes_simple(solution, final_cost)
    
    # 5. Mostra resultados finais
    print("\n" + "="*50)
    print("           FINAL RESULTS")
    print("="*50)
    print(f"Instance Name: {env.instance_name}")
    print(f"Number of Cities: {env.num_cities}")
    print(f"Number of Salesmen: {env.num_salesman}")
    print(f"Best Total Cost Found: {final_cost:.4f}")
    print(f"Time to Find Best Solution: {time_to_best}s")
    print(f"\nRoutes per Salesman:")
    for salesman_id, route in solution.items():
        print(f"  Salesman {salesman_id}: {len(route)} cities -> {route}")
    print("="*50)