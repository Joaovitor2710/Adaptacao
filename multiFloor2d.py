import time
import random
from multiRobotPathPlanner import MultiRobotPathPlanner  
from aStar import AStar
from plot_paths import plot_paths_multiple_robots
from metricas import visualizar_metricas
import psutil
from numba import jit
from turns import turns
import math

class DARP_MultiAndares:
    def __init__(self, num_robos, num_andares, obstaculos_andar, posicoes_escadas, posicoes_escadas_entrada, grids_andar=None, deposito = None, vis = True):
        self.num_robos = num_robos
        self.num_andares = num_andares
        self.obstaculos_andar = obstaculos_andar
        self.posicoes_escadas = posicoes_escadas
        self.posicoes_escadas_entrada = posicoes_escadas_entrada
        self.grids_andar = grids_andar if grids_andar is not None else {}
        self.robos_ativos = list(range(num_robos))
        self.posicoes_atuais = {0: []}
        self.posicoes_iniciais = {}
        self.metricas_dados = {}
        self.custo_escada_distancia = 10  
        self.custo_escada_tempo =   0.2
        self.deposito = deposito
        self.vis = vis

    def esta_posicao_valida(self, andar, posicao):
        if posicao in self.obstaculos_andar.get(andar, []):
            return False
        if(andar == 0) and self.deposito is not None:
            if posicao in self.deposito:
                return False
        if posicao in self.posicoes_escadas.values():
            return False
        if posicao in self.posicoes_escadas_entrada.values():
            return False
        if posicao in self.posicoes_atuais.get(andar, []):
            return False
        return True
    def distancia(self, posicao, escada_x, escada_y, largura_grid):
        # Calcula a distância de Manhattan entre a posição e a escada de entrada
        x = posicao // largura_grid
        y = posicao % largura_grid
        return abs(x - escada_x) + abs(y - escada_y)

    def escolher_posicao_aleatoria(self, andar, escada_entrada=None):
        grid_size = self.grids_andar.get(andar, (10, 10))
        max_pos = grid_size[0] * grid_size[1]
        posicoes_disponiveis = [i for i in range(max_pos) if self.esta_posicao_valida(andar, i)]
        
        if escada_entrada is not None:
            # Se a escada de entrada estiver definida, escolher uma posição perto dela
            escada_x, escada_y = escada_entrada // grid_size[1], escada_entrada % grid_size[1]
            # Ordena as posições válidas com base na distância até a escada de entrada
            posicoes_disponiveis.sort(key=lambda pos: self.distancia(pos, escada_x, escada_y, grid_size[1]))

        if not posicoes_disponiveis:
            print(f"Nenhuma posição disponível no andar {andar}.")
            return None
        return random.choice(posicoes_disponiveis)

    def definir_posicoes_iniciais(self, andar):
        escada_entrada = self.posicoes_escadas_entrada.get(andar, None)
        if escada_entrada:
            # Se há escada de entrada, tente escolher posições perto dela
            self.posicoes_iniciais[andar] = [self.escolher_posicao_aleatoria(andar, escada_entrada) for _ in range(self.num_robos)]
        else:
            # Caso contrário, escolha posições aleatórias como antes
            self.posicoes_iniciais[andar] = [self.escolher_posicao_aleatoria(andar) for _ in range(self.num_robos)]
        
        self.posicoes_iniciais[andar] = self.garantir_posicoes_unicas(andar, [p for p in self.posicoes_iniciais[andar] if p is not None])

    def garantir_posicoes_unicas(self, andar, posicoes):
        posicoes_unicas = []
        for pos in posicoes:
            while pos in posicoes_unicas or not self.esta_posicao_valida(andar, pos):
                pos = self.escolher_posicao_aleatoria(andar)
            posicoes_unicas.append(pos)
        return posicoes_unicas

    def obter_melhores_caminhos(self, planner):
        return planner.get_best_paths()
    
    def metricas(self, planner):
        return planner.get_best_case_num_paths()
    
    def turns(self, planner):
        return planner.get_best_case()

    def executar_darp_no_andar(self, andar):
        # === Execução do método ===
        if not self.robos_ativos:
            print(f"Nenhum robô disponível para o andar {andar}")
            return []
        
        posicoes = self.posicoes_iniciais.get(andar)
        if not posicoes:
            return []

        grid = self.grids_andar.get(andar, (10, 10))
        obs_pos = self.obstaculos_andar.get(andar, [])
        vis = self.vis 
        
        portions = [1 / self.num_robos] * self.num_robos
        notEqualPortions = False  

        planner = MultiRobotPathPlanner(
            nx=grid[0],
            ny=grid[1],
            notEqualPortions=notEqualPortions,
            initial_positions=posicoes,
            portions=portions,
            obs_pos=obs_pos,
            visualization=vis
        )



        melhores_caminhos = self.obter_melhores_caminhos(planner)


      

        return tuple(melhores_caminhos)


    def obter_obstaculos_com_escadas(self, andar):
        obstaculos = self.obstaculos_andar.get(andar, [])
        escada_entrada = self.posicoes_escadas_entrada.get(andar, None)
        escada = self.posicoes_escadas.get(andar, None)
        deposito = self.deposito
        
    
        if escada_entrada is not None:
            obstaculos.append(escada_entrada)
        if escada is not None:
            obstaculos.append(escada)
        if andar == 0 and deposito is not None :
            for i, valor in enumerate(self.deposito):
                obstaculos.append(valor)

        
        return obstaculos

    def executar_darp_multiandares(self):
        lista_turns = []
        start_time = time.time()
        andares_processados = 0
        lista_path = []
        for andar in range(self.num_andares):
                
            self.definir_posicoes_iniciais(andar)

            grid_andar = self.grids_andar.get(andar, (10, 10))
            grid_normalizado = tuple(x * 2 for x in grid_andar)
            escada_entrada = self.posicoes_escadas_entrada.get(andar, None)
            escada = self.posicoes_escadas.get(andar, None)
            obstaculos = self.obter_obstaculos_com_escadas(andar)
            caminho_andares_final = []
            caminho_final = []
            posicao_inicial = []
            deposito = self.deposito
            escada_ponto_ent = 0
            a, b = grid_andar
            grid = [[0 for _ in range(a * 2)] for _ in range(b * 2)]

            obstaculos_expandidos = []
    


            for obstaculo in obstaculos:
                obstaculo_x = obstaculo // b
                obstaculo_y = obstaculo % b
                obstaculoss = (obstaculo_x, obstaculo_y)
                if obstaculo != escada_entrada and obstaculo != escada and obstaculo not in deposito:
                    obstaculos_expandidos.extend(expandir_obstaculo(obstaculoss))


            dep_expandidos = []
         
        
            for dep in deposito:
                dep_x = dep // b 
                dep_y = dep % b
                depo = (dep_x, dep_y)
                dep_expandidos.append(depo)
    

            path_planning_result1 = {}

            if andar > 0:
                escada_x_ent = escada_entrada // b
                escada_y_ent = escada_entrada % b
                escada_ent = (escada_x_ent, escada_y_ent)
                escada_expandida = expandir_escada(escada_ent)
                escada_ponto_ent = escada_expandida[-1]

            obstaculos_expandidos1 = obstaculos_expandidos.copy()

            posicoes_expandidas = []
            posicoes = self.posicoes_iniciais.get(andar)
            for pos in posicoes:
                linha = pos // b
                coluna = pos % b
                posicoes_expandidas.append((linha, coluna))



            for idx, j in enumerate(posicoes_expandidas):
             posicao_inicialx = expandir_obstaculo(j)
             posicao_inicial.append(posicao_inicialx[0])

            dep_ponto = []
            for idx, dep in enumerate(dep_expandidos):  # Desestruturando a tupla (índice, valor)
                # Agora 'dep' é o valor da lista na posição 'idx'
                dep_pontox = expandir_obstaculo(dep)
                dep_ponto.append(dep_pontox[0])
                



            for i in range(self.num_robos):
                if i > 0:
                    obstaculos_expandidos1.extend(expandir_obstaculo(posicoes_expandidas[i - 1]))

                posicao_inicial1 = expandir_obstaculo(posicoes_expandidas[i])
                posicao_inicial1 = posicao_inicial1[0]
                dep_ponto1 = expandir_obstaculo(dep_expandidos[i])

            
                if andar > 0:
                    pp1 = AStar(escada_ponto_ent, posicao_inicial1, "euclidean", grid, obstaculos_expandidos1)

                else:
                    pp1 = AStar(dep_ponto1[0], posicao_inicial1, "euclidean", grid, obstaculos_expandidos1)
                   
                pp, _ = pp1.searching()
                path_planning_result1[i] = pp
                
                

            caminhos_andares = self.executar_darp_no_andar(andar)
           

            if escada is not None:
                escada_x = escada // b
                escada_y = escada % b
                escada = (escada_x, escada_y)
                escada_expandida = expandir_escada(escada)
                escada_ponto = escada_expandida[-1]
                path_planning_result = {}

                for i, caminho in enumerate(caminhos_andares):
                    posicao_final = caminho[-1][-2:]
                    posicao_final = desexpandir(posicao_final)
                    obstaculos_expandidos.extend(expandir_obstaculo(posicao_final))

                for i, caminho in enumerate(caminhos_andares):
                    posicao_final = caminho[-1][-2:]
                    posicao = desexpandir(posicao_final)
                    posicoes_robo_atual = expandir_obstaculo(posicao)
                    obstaculos_expandidos2 = list(set(obstaculos_expandidos) - set(posicoes_robo_atual))
                    pathPlanning = AStar(posicao_final, escada_ponto, "euclidean", grid, obstaculos_expandidos2)
                    path, visited = pathPlanning.searching()
                    path_planning_result[i] = path

            caminho_andares_final = [[(x2, y2) for _, _, x2, y2 in caminho] for caminho in caminhos_andares]

            if andar == 0:
                if self.vis == True:
                    plot_paths_multiple_robots(self.num_robos, caminho_andares_final, grid_normalizado,dep_ponto,  posicao_inicial, path_planning_result1, list(path_planning_result.values()), None, escada_ponto)

                path_lenght1 = calcular_comprimento_caminho(path_planning_result.values())
                path_lenght2 = calcular_comprimento_caminho(caminho_andares_final)

                # Adicionar custo da escada ao comprimento do caminho
                path_lenght1 = [comprimento + self.custo_escada_distancia for comprimento in path_lenght1]
                path_lenght_final = [comprimento1 + comprimento2 for comprimento1, comprimento2 in zip(path_lenght1, path_lenght2)]

                caminho_final = [
                    lista1 + lista2
                    for lista1, lista2 in zip(caminho_andares_final, path_planning_result.values())]
   
                

            elif andar == self.num_andares - 1:
                if self.vis == True:
                    plot_paths_multiple_robots(self.num_robos, caminho_andares_final, grid_normalizado, None, posicao_inicial, list(path_planning_result1.values()), None, escada_ponto_ent, None)

                path_lenght1 = calcular_comprimento_caminho(path_planning_result1.values())
                path_lenght2 = calcular_comprimento_caminho(caminho_andares_final)

                # Adicionar custo da escada ao comprimento do caminho
                path_lenght1 = [comprimento for comprimento in path_lenght1]
                path_lenght_final = [comprimento1 + comprimento2 for comprimento1, comprimento2 in zip(path_lenght1, path_lenght2)]

                caminho_final = [
                    lista1 + lista2
                    for lista1, lista2 in zip(path_planning_result1.values(), caminho_andares_final)]

            else:
                if self.vis == True:
                    plot_paths_multiple_robots(self.num_robos, caminho_andares_final, grid_normalizado, None,  posicao_inicial, list(path_planning_result1.values()), list(path_planning_result.values()), escada_ponto_ent, escada_ponto)

                path_lenght1 = calcular_comprimento_caminho(path_planning_result.values())
                path_lenght2 = calcular_comprimento_caminho(caminho_andares_final)
                path_lenght3 = calcular_comprimento_caminho(path_planning_result1.values())

                # Adicionar custo da escada ao comprimento do caminho
                path_lenght1 = [comprimento + self.custo_escada_distancia for comprimento in path_lenght1]
                path_lenght3 = [comprimento for comprimento in path_lenght3]
                path_lenght_final = [comprimento1 + comprimento2 + caminho3 for comprimento1, comprimento2, caminho3 in zip(path_lenght1, path_lenght2, path_lenght3)]

                caminho_final = [
                    lista1 + lista2 + lista3
                    for lista1, lista2, lista3 in zip(path_planning_result1.values(), caminho_andares_final, path_planning_result.values())]
                

            x = turns(caminho_final)
            x.count_turns_2()
            lista_turns.append(x.turns)
            lista_path.append(path_lenght_final)        
            andares_processados += 1

        
        execution_time = time.time() - start_time
        self.metricas_dados = {
        "tempo_execucao": execution_time + self.custo_escada_tempo,
        "path_lenght_final": lista_path,
        "turns_totais": lista_turns,
        "cpu": psutil.cpu_percent()
        } 
        if andares_processados == self.num_andares:
            print("Todos os andares foram processados.")




def expandir_obstaculo(obstaculo):
        x, y = obstaculo
        return [(x * 2, y * 2), (x * 2 + 1, y * 2),
                (x * 2, y * 2 + 1), (x * 2 + 1, y * 2 + 1)]
def expandir_escada(escada):
        x, y = escada
        return [(x * 2, y * 2), (x * 2 + 1, y * 2),
                (x * 2, y * 2 + 1), (x * 2 + 1, y * 2 + 1)]
def desexpandir(posicao_expandidas):
    x, y = posicao_expandidas
    return (x // 2, y // 2)

def calcular_comprimento_caminho(caminhos):
    import math

def calcular_comprimento_caminho(caminhos):
    comprimentos = []
    for caminho in caminhos:
        # Cria pares consecutivos de pontos usando zip
        pares = zip(caminho[:-1], caminho[1:])
        # Calcula a distância entre cada par de pontos
        distancias = map(lambda pontos: math.sqrt((pontos[1][0] - pontos[0][0])**2 + (pontos[1][1] - pontos[0][1])**2), pares)
        # Soma as distâncias para obter o comprimento total do caminho
        comprimento_total = sum(distancias)
        comprimentos.append(comprimento_total)
    return comprimentos

if __name__ == '__main__':
    num_robos = 3
    num_andares = 3
    obstaculos_andar = {
        0: [35,59,78],
        1: [24,56,71],
        2: [13,26,35]
    }
    posicoes_escadas_saida = {
        0: 99,
        1: 5
    }

    posicoes_escadas_entrada = {
        1: 99,
        2: 5
    }
    
    grids_andar = { 
    }

    deposito_1_andar = [10,20,30]

    vis = True

    darp_multiandares = DARP_MultiAndares(num_robos, num_andares, obstaculos_andar, posicoes_escadas_saida,posicoes_escadas_entrada, grids_andar, deposito_1_andar, vis)
    darp_multiandares.executar_darp_multiandares()


    print(f"Tempo de execução: {darp_multiandares.metricas_dados['tempo_execucao']}")
    print(f"Comprimento do caminho final: {darp_multiandares.metricas_dados['path_lenght_final']}")
    print(f"Turnos totais: {darp_multiandares.metricas_dados['turns_totais']}")
    print(f"Uso de CPU: {darp_multiandares.metricas_dados['cpu']}%")