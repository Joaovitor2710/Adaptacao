"""
A_star 2D
@author: huiming zhou
"""


import math
import heapq

class AStar:
    def __init__(self, s_start, s_goal, heuristic_type, grid, obstacles):
        self.s_start = s_start
        self.s_goal = s_goal
        self.heuristic_type = heuristic_type
        self.grid = grid  # Matriz de mapa (10x10 ou qualquer tamanho)
        self.obstacles = obstacles  # Lista de obstáculos (coordenadas)

        self.u_set = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimentos possíveis (cima, baixo, esquerda, direita)

        self.OPEN = []  # Fila de prioridade (OPEN set)
        self.CLOSED = []  # Conjunto de nós visitados (CLOSED set)
        self.PARENT = dict()  # Registra o nó pai
        self.g = dict()  # Custo para chegar a cada nó

    def searching(self):
        """
        A* Searching.
        :return: path, visited order
        """
        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN, (self.f_value(self.s_start), self.s_start))

        while self.OPEN:
            _, s = heapq.heappop(self.OPEN)
            self.CLOSED.append(s)

            if s == self.s_goal:  # Condição de parada
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]:  # Condição para atualizar o custo
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (self.f_value(s_n), s_n))

        return self.extract_path(self.PARENT), self.CLOSED

    def get_neighbor(self, s):
        """
        Encontrar vizinhos do estado s que não estão em obstáculos.
        :param s: estado
        :return: vizinhos
        """
        neighbors = []
        for u in self.u_set:
            new_pos = (s[0] + u[0], s[1] + u[1])
            if 0 <= new_pos[0] < len(self.grid) and 0 <= new_pos[1] < len(self.grid[0]):
                neighbors.append(new_pos)
        return neighbors

    def cost(self, s_start, s_goal):
        """
        Calcular o custo para mover de s_start para s_goal.
        :param s_start: nó de início
        :param s_goal: nó final
        :return: custo da movimentação
        """
        if self.is_collision(s_start, s_goal):
            return math.inf
        return math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])

    def is_collision(self, s_start, s_end):
        """
        Verificar se o segmento de linha (s_start, s_end) colide com obstáculos.
        :param s_start: nó de início
        :param s_end: nó final
        :return: True se houver colisão, False se não houver
        """
        # Verificando se a posição de início ou de fim tem obstáculo
        if s_start in self.obstacles or s_end in self.obstacles:
            return True
        return False

    def f_value(self, s):
        """
        Calcular f = g + h. (g: Custo para chegar ao nó, h: valor heurístico)
        :param s: estado atual
        :return: valor f
        """
        return self.g[s] + self.heuristic(s)

    def extract_path(self, PARENT):
        """
        Extrair o caminho a partir do conjunto de pais.
        :return: O caminho planejado
        """
        path = [self.s_goal]
        s = self.s_goal
        while True:
            s = PARENT[s]
            path.append(s)
            if s == self.s_start:
                break
        return list(path)

    def heuristic(self, s):
        """
        Calcular a heurística.
        :param s: nó atual (estado)
        :return: valor heurístico
        """
        goal = self.s_goal  # Nó objetivo

        if self.heuristic_type == "manhattan":
            return abs(goal[0] - s[0]) + abs(goal[1] - s[1])
        else:
            return math.hypot(goal[0] - s[0], goal[1] - s[1])


# Exemplo de uso no contexto de robôs em diferentes andares:
if __name__ == '__main__':
    # Definindo um grid 10x10 (0 para espaço livre, 1 para obstáculo)
    grid = [[0 for _ in range(10)] for _ in range(10)]
    print(grid)

    # Adicionando obstáculos no grid (exemplo)
    obstacles = [(3, 3), (3, 4), (4, 3)]  # Obstáculos em (3,3), (3,4), (4,3)
    
    # Definindo o ponto inicial e objetivo no grid
    s_start = (0, 0)
    s_goal = (9, 9)
    
    # Criando o objeto A* com o grid e os obstáculos
    astar = AStar(s_start, s_goal, "euclidean", grid, obstacles)
    
    # Executando a busca A* e imprimindo o caminho e os nós visitados
    path, visited = astar.searching()
    print(f"Caminho encontrado: {path}")
    print(f"Ordens de visita: {visited}")
