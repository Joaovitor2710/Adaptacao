import matplotlib.pyplot as plt
import numpy as np

def plot_paths_multiple_robots(num_robots, caminhos_andares_final, grid_size, dep_ponto=None, 
                               posicao_inicial=None,
                               path_planning_result1=None, path_planning_result=None,
                               escada_ponto_ent=None, escada_ponto=None,
                               titulo_base="Caminho do Robô"):

    x_size, y_size = grid_size
    cores = ['orange', 'blue', 'red']  # Laranja: início, Azul: cobertura, Vermelho: final
    
    # Cores específicas para os depósitos
    cores_deposito = ['brown', 'yellow', 'pink', 'purple', 'green']  # exemplo de cores para depósitos
    cores_robos = ['cyan', 'magenta', 'lime', 'gold', 'deepskyblue']

    # Criar subgráficos com 1 linha e num_robots colunas
    fig, axes = plt.subplots(1, num_robots, figsize=(15, 5))

    # Verificar se há apenas um robô (caso em que axes não é um array)
    if num_robots == 1:
        axes = [axes]

    for i in range(num_robots):
        ax = axes[i]  # Selecionar o eixo para o robô atual

        pontos_inicio = path_planning_result1[i] if path_planning_result1 else []
        pontos_coverage = caminhos_andares_final[i]
        pontos_final = path_planning_result[i] if path_planning_result else []

        # Deslocamento para centralizar os pontos
        x_inicio = [ponto[0] + 0.5 for ponto in pontos_inicio]
        y_inicio = [ponto[1] + 0.5 for ponto in pontos_inicio]

        x_coverage = [ponto[0] + 0.5 for ponto in pontos_coverage]
        y_coverage = [ponto[1] + 0.5 for ponto in pontos_coverage]

        x_final = [ponto[0] + 0.5 for ponto in pontos_final]
        y_final = [ponto[1] + 0.5 for ponto in pontos_final]

        # Plotando as trajetórias para cada robô no gráfico específico
        ax.plot(y_inicio, x_inicio, marker='o', linestyle='-', color=cores[0], label=f'Inicial', zorder=3)
        ax.plot(y_final, x_final, marker='o', linestyle='-', color=cores[2], label=f'Final', zorder=4)

        # Plotando os pontos da escada
        if escada_ponto:
            x_escada = escada_ponto[0] + 0.5
            y_escada = escada_ponto[1] + 0.5
            ax.scatter(y_escada, x_escada, color='green', label='Escada', zorder=5)

        if escada_ponto_ent:
            x_escada = escada_ponto_ent[0] + 0.5
            y_escada = escada_ponto_ent[1] + 0.5
            ax.scatter(y_escada, x_escada, color='purple', label='Escada_ent', zorder=5)

        # Plotando a cobertura (depois das outras linhas)
        ax.plot(y_coverage, x_coverage, marker='o', linestyle='-', color=cores[1], label=f'Cobertura', zorder=2)

        # Plotando apenas o depósito correspondente ao robô
        if dep_ponto and i < len(dep_ponto):
            x_dep = dep_ponto[i][0] + 0.5
            y_dep = dep_ponto[i][1] + 0.5
            cor_dep = cores_deposito[i % len(cores_deposito)]
            ax.scatter(y_dep, x_dep, color=cor_dep, label=f'Depósito {i+1}', zorder=6)

        # Plotando apenas a posição inicial correspondente ao robô
        if posicao_inicial and i < len(posicao_inicial):
            x_pos_ini = posicao_inicial[i][0] + 0.5
            y_pos_ini = posicao_inicial[i][1] + 0.5
            cor_robo = cores_robos[i % len(cores_robos)]
            ax.scatter(y_pos_ini, x_pos_ini, color=cor_robo, label=f'Robô {i+1} (Inicial)', zorder=7)

        # Ajustes do gráfico para cada subgráfico
        ax.set_xlim(0, x_size)
        ax.set_ylim(0, y_size)
        ax.set_xticks(np.arange(0, x_size + 1, 1))
        ax.set_yticks(np.arange(0, y_size + 1, 1))

        # Invertendo o eixo y para ir de cima para baixo
        ax.invert_yaxis()

        ax.set_title(f"{titulo_base} Robô {i+1}")
        ax.set_xlabel('Y')
        ax.set_ylabel('X')
        ax.grid(True, which='both')

        # Adicionando legenda
        ax.legend(loc='lower left')

    # Ajustando o layout para não sobrepor os subgráficos
    plt.tight_layout()

    # Mostrando o gráfico
    plt.show()