import matplotlib.pyplot as plt
import numpy as np

# Dados dos três andares
andares = ['Andar 0', 'Andar 1', 'Andar 2']
path_lengths = {
    'Andar 0': [177.0, 175.0, 173.0],
    'Andar 1': [163.0, 169.0, 191.0],
    'Andar 2': [139.0, 139.0, 143.0]
}
turns_fcpp = {
    'Andar 0': [21, 37, 29],
    'Andar 1': [22, 26, 19],
    'Andar 2': [37, 28, 25]
}
turns_totais = {
    'Andar 0': [54, 66, 55],
    'Andar 1': [36, 46, 60],
    'Andar 2': [39, 31, 29]
}
cpu_usage = [49.8, 2.0, 2.9]  # Uso de CPU por andar

# Plotando gráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# 1. Gráfico de Path Length Total
for andar in andares:
    axs[0, 0].plot(path_lengths[andar], label=andar)
axs[0, 0].set_title('Path Length Total em Células por Andar')
axs[0, 0].set_xlabel('Índice')
axs[0, 0].set_ylabel('Path Length')
axs[0, 0].legend()

# 2. Gráfico de Turns FCPP
for andar in andares:
    axs[0, 1].plot(turns_fcpp[andar], label=andar)
axs[0, 1].set_title('Turns FCPP por Andar')
axs[0, 1].set_xlabel('Índice')
axs[0, 1].set_ylabel('Número de Turns')
axs[0, 1].legend()

# 3. Gráfico de Turns Totais
for andar in andares:
    axs[1, 0].plot(turns_totais[andar], label=andar)
axs[1, 0].set_title('Turns Totais por Andar')
axs[1, 0].set_xlabel('Índice')
axs[1, 0].set_ylabel('Número de Turns')
axs[1, 0].legend()

# 4. Gráfico de Uso de CPU
axs[1, 1].bar(andares, cpu_usage)
axs[1, 1].set_title('Uso de CPU por Andar')
axs[1, 1].set_ylabel('Uso de CPU (%)')

plt.tight_layout()
plt.show()
