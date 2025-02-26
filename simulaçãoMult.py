from multiFloor2d import DARP_MultiAndares  

# Função para simulação com parâmetros definidos manualmente
def executar_simulacao(num_robos, num_andares, obstaculos_andar, posicoes_escadas, posicoes_escadas_entrada, grids_andar, deposito):
    # Executando a simulação com os parâmetros fornecidos
    darp_multiandares = DARP_MultiAndares(num_robos, num_andares, obstaculos_andar, posicoes_escadas, posicoes_escadas_entrada, grids_andar, deposito)
    darp_multiandares.executar_darp_multiandares()
    
    # Coletando os resultados
    return darp_multiandares.metricas_dados

# Parâmetros fixos
grid_size = None  # Tamanho do grid dos andares

# Definir as simulações manualmente
simulacoes = [
    {
        "num_robos": 3,
        "num_andares": 3,
        "obstaculos_andar": {0: [35, 59, 78], 1: [24, 56, 71], 2: [13, 26, 35]},
        "posicoes_escadas": {0: 99, 1: 5},
        "posicoes_escadas_entrada": {1: 99, 2: 5},
        "grids_andar": {0: [1] * 100, 1: [1] * 100, 2: [1] * 100},
        "deposito": [10, 20, 30]
    },
    {
        "num_robos": 2,
        "num_andares": 4,
        "obstaculos_andar": {0: [60, 76, 30], 1: [40, 50, 60], 2: [70, 80, 90], 3: [10, 30, 90]},
        "posicoes_escadas": {0: 99, 1: 5, 2: 50},
        "posicoes_escadas_entrada": {1: 99, 2: 5, 3: 50},
        "grids_andar": {0: [1] * 100, 1: [1] * 100, 2: [1] * 100, 3: [1] * 100},
        "deposito": [10, 20]
    },
    {
        "num_robos": 4,
        "num_andares": 2,
        "obstaculos_andar": {0: [15, 25, 35], 1: [45, 55, 65]},
        "posicoes_escadas": {0: 50},
        "posicoes_escadas_entrada": {1: 50},
        "grids_andar": {0: [1] * 100, 1: [1] * 100},
        "deposito": [10, 20, 30, 40]
    },
    {
        "num_robos": 5,
        "num_andares": 3,
        "obstaculos_andar": {0: [11, 22, 33], 1: [44, 55, 66], 2: [77, 88, 99]},
        "posicoes_escadas": {0: 90, 1: 60},
        "posicoes_escadas_entrada": {1: 90, 2: 60},
        "grids_andar": {0: [1] * 100, 1: [1] * 100, 2: [1] * 100},
        "deposito": [10, 20, 30, 40, 50]
    }
]

# Solicitar ao usuário para escolher qual simulação executar
print("Escolha a simulação que deseja executar (0 a 3):")
for i, simulacao in enumerate(simulacoes):
    print(f"{i}: Simulação {i + 1} - {simulacao['num_robos']} robôs, {simulacao['num_andares']} andares")

# Leitura do número da simulação escolhida
simulacao_escolhida = int(input("Digite o número da simulação (0 a 3): "))

# Verificar se a escolha é válida
if 0 <= simulacao_escolhida < len(simulacoes):
    simulacao = simulacoes[simulacao_escolhida]
    print(f"\nSimulação {simulacao_escolhida + 1} escolhida:")
    
    # Executar a simulação
    resultados = executar_simulacao(
        simulacao["num_robos"],
        simulacao["num_andares"],
        simulacao["obstaculos_andar"],
        simulacao["posicoes_escadas"],
        simulacao["posicoes_escadas_entrada"],
        grid_size,
        simulacao["deposito"]
    )
    
    # Inicializando as somas
    path_lenght_final_total = [0] * simulacao["num_robos"]
    turns_totais_total = [0] * simulacao["num_robos"]

    # Somando os valores dentro de cada andar
    for andar in range(simulacao["num_andares"]):
        path_lenght_final_total = [sum(x) for x in zip(path_lenght_final_total, resultados["path_lenght_final"][andar])]
        turns_totais_total = [sum(x) for x in zip(turns_totais_total, resultados["turns_totais"][andar])]
    
    # Exibindo as métricas da simulação
    print(f"Tempo de execução: {resultados['tempo_execucao']}")
    print(f"Comprimento do caminho final (somado): {path_lenght_final_total}")
    print(f"Turnos totais (somado): {turns_totais_total}")
    print(f"Uso de CPU: {resultados['cpu']}%")
else:
    print("Número de simulação inválido. Por favor, escolha um número entre 0 e 3.")
