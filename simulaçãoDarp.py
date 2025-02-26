import time
import psutil
from multiRobotPathPlanner import MultiRobotPathPlanner  


simulacoes = [
    {
        "num_robos": 3,
        "num_andares": 3,
        "obstaculos_andar": {0: [10,20,30, 35, 59, 78, 99], 1: [5,24, 56, 71, 99], 2: [13, 26, 35, 5]},
        "grid_size": (10, 10),
        "portions": [1/3] * 3 ,
        "nep": False ,
        "visualizar":  False ,
        "posicoes_iniciais" : [0,3,9] 
       
    },
    {
        "num_robos": 2,
        "num_andares": 4,
        "obstaculos_andar": {0: [10, 20, 60, 76, 30,99], 1: [40, 50, 60,99, 5], 2: [70, 80, 90,5, 50], 3: [10, 50, 90, 30]},
        "grid_size": (10, 10),
        "portions": [1/2] * 2 ,
        "nep": False ,
        "visualizar":  False,
        "posicoes_iniciais" : [0,3]   
    },
    {
        "num_robos": 4,
        "num_andares": 2,
        "obstaculos_andar": {0: [10,20,30,40, 15, 25, 35, 50], 1: [45, 55, 65, 50]},
        "grid_size": (10, 10),
        "portions": [1/4] * 4 ,
        "nep": False ,
        "visualizar":  False ,
        "posicoes_iniciais" : [0,3, 9, 18]   
    },
    {
        "num_robos": 5,
        "num_andares": 3,
        "obstaculos_andar": {0: [10, 20, 30, 40, 50,11, 22, 33, 90], 1: [44, 55, 66, 90, 60], 2: [77, 88, 99, 60]},
        "grid_size": (10, 10),
        "portions": [1/5] * 5,
        "nep": False ,
        "visualizar":  False, 
        "posicoes_iniciais" : [0,3, 9, 18, 24]    
    }
]


for simulacao in simulacoes:
    num_robos = simulacao["num_robos"]
    num_andares = simulacao["num_andares"]
    obstaculos_andar = simulacao["obstaculos_andar"]
    grid_size = simulacao["grid_size"]
    portions = simulacao["portions"]
    nep = simulacao["nep"]
    visualizar = simulacao["visualizar"]
    posicoes_iniciais = simulacao["posicoes_iniciais"]

    
   
    tempo_execucao_total = 0
    path_lenght_final_total = [0] * num_robos 
    turns_totais_total = [0] * num_robos  
    cpu_total = 0  
   

    for andar in range(num_andares):


        planner = MultiRobotPathPlanner(
            grid_size[0], grid_size[1], nep, posicoes_iniciais, portions, obstaculos_andar[andar], visualizar
        )
        tempo_execucao_total += planner.metricas_dados["tempo_execucao"]
        

        for i in range(num_robos):
            path_lenght_final_total[i] += planner.metricas_dados["path_lenght_final"][i]
        
        for i in range(num_robos):
            turns_totais_total[i] += planner.metricas_dados["turns_totais"][i]
        
        cpu_total += planner.metricas_dados["cpu"]
    

    num_andares_executados = num_andares  
    print(f"\nMétricas para a simulação com {num_andares} andares:")
    print(f"Tempo total de execução do DARP: {tempo_execucao_total:.4f} segundos")
    print(f"Comprimento total do caminho do Robô: {path_lenght_final_total}")
    print(f"Turnos totais do Robô:{turns_totais_total}")
    
    media_cpu = cpu_total / num_andares
    print(f"Média de uso de CPU: {media_cpu:.2f}%")

