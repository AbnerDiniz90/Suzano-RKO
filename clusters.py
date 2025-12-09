from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class ClusterizadorLojas:
    """
    Agrupa lojas geograficamente para criar rotas regionalizadas.
    Cada promotor fica responsável por uma região específica
    """

    def __init__(self, coords, frequencias, metodo='kmeans', num_clusters='auto', ponderar_por_frequencia=False):
        """
        Parâmetros:
        - coords: lista de tuplas
            Lista de coordenadas (x,y) das lojas
        - frequencias: lista de ints
            Frequência de visita de cada loja
        - metodo: str
            Nesse caso é o KMeans
        - num_clusters: auto
            Número de clusters desejado
        - ponderar_por_frequencia: bool
            Se True, lojas com mais visitas influenciam mais o cluster
            Se False, todas as lojas têm peso igual
        """

        self.coords = np.array(coords)
        self.frequencias = frequencias
        self.metodo = metodo
        self.num_clusters = num_clusters
        self.ponderar_por_frequencia = ponderar_por_frequencia

        self.labels = None
        self.centroides = None
        self.clusters_lojas = {}

        #Cada loja pertence a exatamente 1 cluster
        #Cada promotor atende lojas do próprio cluster

    def calcular_num_clusters_otimo(self):
        """
        Calcula número ótimo de clusters baseado em:
        - Total de visitas necessárias
        - Capacidade semanal de um promotor
        """

        total_visitas = sum(self.frequencias)
        visitas_por_promotor = 2400 / 40

        num_promotores_estimado = int(np.ceil(total_visitas / visitas_por_promotor))

        num_clusters = max(2, int(num_promotores_estimado * 1.15))

        print("Estimativa Automática:")
        print(f"   - Total visitas necessárias: {total_visitas}")
        print(f"   - Promotores estimados: {num_promotores_estimado}")
        print(f"   - Clusters sugeridos: {num_clusters}")

        return num_clusters
    
    def clusterizar(self):
        if self.num_clusters == 'auto':
            self.num_clusters = self.calcular_num_clusters_otimo()

        self.num_clusters = min(self.num_clusters, len(self.coords))

        if self.metodo == 'kmeans':
            self._kmeans_clustering()
        else:
            raise NotImplementedError("Apenas K-Means implementado por enquanto")
        
        self._organizar_clusters()
        
        return self.labels
    
    def _kmeans_clustering(self):
        if self.ponderar_por_frequencia:
            coords_expandidas = []
            indices_originais = []

            for i, coord in enumerate(self.coords):
                freq = self.frequencias[i]

                for _ in range(freq):
                    coords_expandidas.append(coord)
                    indices_originais.append(i)

            coords_expandidas = np.array(coords_expandidas)

            kmeans = KMeans(
                n_clusters = self.num_clusters,
                random_state = 42,
                n_init = 20,
                max_iter = 500
            )

            labels_expandidos = kmeans.fit_predict(coords_expandidas)

            self.labels = np.zeros(len(self.coords), dtype=int)

            for i in range(len(self.coords)):
                labels_da_loja = [labels_expandidos[j] for j, idx in enumerate(indices_originais) if idx == i]
                self.labels[i] = max(set(labels_da_loja), key=labels_da_loja.count)

            self.centroides = kmeans.cluster_centers_

        else:
            # Modo 2: Cada loja conta como 1 ponto, independente da frequência
            kmeans = KMeans(
                n_clusters = self.num_clusters,
                random_state = 42,
                n_init = 20,
                max_iter = 500
            )

            self.labels = kmeans.fit_predict(self.coords)
            self.centroides = kmeans.cluster_centers_

        #VALIDAÇÃO: Garante que cada loja tem exatamente 1 cluster
        assert len(self.labels) == len(self.coords), "Erro: Número de labels diferente de lojas!"
        assert len(set(self.labels)) <= self.num_clusters, "Erro: Mais clusters que o esperado!"

        print(f"Clusterização concluída: {len(self.coords)} lojas em {len(set(self.labels))} clusters")
        print(f"Garantia: Cada loja pertence a EXATAMENTE 1 cluster")

    def _organizar_clusters(self):
        """
        Cria dicionário mapeando cluster_id
        """
        self.clusters_lojas = {i: [] for i in range(self.num_clusters)}

        for idx_loja, cluster_id in enumerate(self.labels):
            self.clusters_lojas[cluster_id].append(idx_loja)

    def _imprimir_estatisticas(self):
        """
        Mostra estatísticas de cada cluster
        """
        print("\n" + "="*60)
        print("              ESTATÍSTICAS DOS CLUSTERS              ")
        print("="*60)

        for cluster_id in range(self.num_clusters):
            lojas = self.clusters_lojas[cluster_id]
            total_visitas = sum([self.frequencias[i] for i in lojas])
            
            # Calcula diâmetro do cluster (maior distância interna)
            if len(lojas) > 1:
                coords_cluster = self.coords[lojas]
                distancias = []
                for i in range(len(coords_cluster)):
                    for j in range(i+1, len(coords_cluster)):
                        dist = np.linalg.norm(coords_cluster[i] - coords_cluster[j])
                        distancias.append(dist)
                diametro = max(distancias)
            else:
                diametro = 0
            
            print(f"Cluster {cluster_id}:")
            print(f"  Lojas: {len(lojas)}")
            print(f"  Visitas semanais: {total_visitas}")
            print(f"  Diâmetro: {diametro:.1f} unidades")
            print(f"  IDs: {lojas}")
            print("-"*60)

    def get_cluster_da_loja(self, idx_loja):
        """
        Retorna ID de uma loja específica
        """
        return int(self.labels[idx_loja])
    
    def get_lojas_do_cluster(self, cluster_id):
        """
        Retorna lista de índices das lojsa em um cluster
        """
        return self.clusters_lojas[cluster_id]
    
    def validar_exclusividade(self, promotores_bin, visit_coords):
        """
        Valida se a solução final respeita a regra: 
        1 loja = 1 cluster = 1 promotor único
        
        Parâmetros:
        promotores_bin : list
            Lista de objetos Promotores da solução
        visit_coords : list
            Lista de coordenadas das lojas (do RKO_Base)
        
        Retorna:
        bool : True se válido, False se houver violações
        """

        print("\n" + "="*70)
        print("           VALIDAÇÃO DE EXCLUSIVIDADE LOJA-PROMOTOR           ")
        print("="*70)

        mapa_lojas = {}

        for idx_promotor, promotor in enumerate(promotores_bin):
            todas_coords = (
                promotor.coords_segunda + promotor.coords_terca + 
                promotor.coords_quarta + promotor.coords_quinta + 
                promotor.coords_sexta + promotor.coords_sabado
            )

            # Pega coordenadas únicas (remove visitas repetidas do mesmo promotor)
            coords_unicas = set(todas_coords)
            
            for coord in coords_unicas:
                if coord not in mapa_lojas:
                    mapa_lojas[coord] = []
                mapa_lojas[coord].append(idx_promotor)

        #Verifica violações
        violacoes = []
        for coord, promotores in mapa_lojas.items():
            if len(promotores) > 1:
                # Encontra ID da loja
                try:
                    id_loja = visit_coords.index(coord)
                except ValueError:
                    id_loja = "?"
                
                violacoes.append((id_loja, coord, promotores))

        # Relatório
        if len(violacoes) == 0:
            print("SUCESSO: Todas as lojas têm EXATAMENTE 1 promotor!")
            print(f"   - {len(mapa_lojas)} lojas verificadas")
            print(f"   - {len(promotores_bin)} promotores ativos")
            print("="*70 + "\n")
            return True
        else:
            print(f"FALHA: {len(violacoes)} lojas têm múltiplos promotores!\n")
            for id_loja, coord, proms in violacoes:
                print(f"   Loja {id_loja} {coord}")
                print(f"   → Disputada por promotores: {proms}")
                
                # Mostra clusters dos promotores envolvidos
                for p_idx in proms:
                    p_cluster = promotores_bin[p_idx].cluster_id
                    print(f"      • Promotor {p_idx} (Cluster {p_cluster})")
                print()
            
            print("DICA: Verifique se o método cost() está filtrando corretamente")
            print("       promotores pelo cluster_id antes de alocar lojas.")
            print("="*70 + "\n")
            return False
    
    def plot_clusters(self, salvar_arquivo=None):
        plt.figure(figsize=(12, 10))

        cores = plt.cm.tab20(np.linspace(0, 1, self.num_clusters))

        for cluster_id in range(self.num_clusters):
            lojas = self.clusters_lojas[cluster_id]
            coords_cluster = self.coords[lojas]

            # Usa o nome correto: self.frequencias
            tamanhos = [self.frequencias[i] * 100 for i in lojas]

            plt.scatter(
                coords_cluster[:, 0],
                coords_cluster[:, 1],
                c=[cores[cluster_id]],
                s=tamanhos,
                alpha=0.6,
                edgecolors='black',
                linewidths=1.5,
                label=f'Região {cluster_id}'
            )

            # Adiciona o número da loja
            for idx_loja in lojas:
                coord = self.coords[idx_loja]
                plt.text(
                    coord[0], coord[1], str(idx_loja),
                    fontsize=8, ha='center', va='center', fontweight='bold'
                )

        # Plota centroides
        if self.centroides is not None:
            plt.scatter(
                self.centroides[:, 0],
                self.centroides[:, 1],
                c='red',
                s=500,
                marker='X',
                edgecolors='black',
                linewidths=2,
                label='Centroides',
                zorder=10
            )

        plt.title('Clusterização de Lojas por Região', fontsize=16, fontweight='bold')
        plt.xlabel('Coordenada X', fontsize=12)
        plt.ylabel('Coordenada Y', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        """
        if salvar_arquivo:
            plt.savefig(salvar_arquivo, dpi=300, bbox_inches='tight')
            print(f"Gráfico salvo em: {salvar_arquivo}")
        """

        plt.show()