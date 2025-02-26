import pandas as pd
import numpy as np

def visualizar_metricas(metricas_dados):
    # Criar listas para armazenar as métricas gerais
    dados = []
    todas_metricas = []
    todos_turns = []
    todas_medias = []
    todos_desvios = []
    todos_tempos_execucao = []
    todos_tempos_cpu = []
    todos_usos_cpu = []
    todos_memorias = []
    
    path_lenght_final = [0] * len(next(iter(metricas_dados.values()))['path_lenght_final'])

    # Somando as listas de path_lenght_final dos andares
    for andar in metricas_dados.values():
        for i in range(len(path_lenght_final)):
            path_lenght_final[i] += andar['path_lenght_final'][i]


    for andar, metricas in metricas_dados.items():
        custo = metricas["custo_computacional"]

        # Adicionar os dados na lista
        dados.append({
            "andar": andar,
            "path_lenght em células": metricas["path_lenght_final"],
            "células por robô": metricas["metricas"], 
            "minimo numero de celulas": {min(metricas["metricas"])},
            "maximo numero de celulas": {max(metricas["metricas"])},
            "número médio de células nos caminhos dos robos": {np.mean(np.array(metricas["metricas"]))},
            "turns": metricas["turns"], 
            "average": metricas["average"],
            "desvio_padrão": metricas["std_dev"],
            "tempo_execucao": custo["tempo_execucao"],
            "tempo_cpu": custo["tempo_cpu"],
            "uso_cpu": custo["uso_cpu"],
            "memoria_usada": custo["memoria_usada"]
        })

    
        for metricas_robo in metricas["metricas"]:
            todas_metricas.append(np.mean(metricas_robo))  # Média de cada lista de métricas
        for turn_robo in metricas["turns"]:
            todos_turns.append(np.mean(turn_robo)) 
        todas_medias.append(metricas["average"])
        todos_desvios.append(metricas["std_dev"])
        todos_tempos_execucao.append(custo["tempo_execucao"])
        todos_tempos_cpu.append(custo["tempo_cpu"])
        todos_usos_cpu.append(custo["uso_cpu"])
        todos_memorias.append(custo["memoria_usada"])

    # Exibir os dados formatados como dicionário
    for item in dados:
        print(f"\nAndar {item['andar']}:")
        for chave, valor in item.items():
            if chave != "andar":
                print(f"  {chave.replace('_', ' ').capitalize()}: {valor}")
    
    # Exibir média geral
    print("path_lenght_final em células para cada robô:", path_lenght_final)
    print("\n📊 **Médias Gerais**")
    print(f"Média Geral das células: {sum(todas_metricas) / len(todas_metricas):.4f}")
    print(f"Média Geral dos Turns: {sum(todos_turns) / len(todos_turns):.4f}")
    print(f"Média Geral dos averages dos turns: {sum(todas_medias) / len(todas_medias):.4f}")
    print(f"Média Geral dos Desvios Padrão dos turns: {sum(todos_desvios) / len(todos_desvios):.4f}")
    print(f"Tempo Médio de Execução: {sum(todos_tempos_execucao) / len(todos_tempos_execucao):.4f} s")
    print(f"Tempo Médio de CPU: {sum(todos_tempos_cpu) / len(todos_tempos_cpu):.4f} s")
    print(f"Uso Médio de CPU: {sum(todos_usos_cpu) / len(todos_usos_cpu):.2f} %")
    print(f"Memória Média Usada: {sum(todos_memorias) / len(todos_memorias):.2f} MB")

