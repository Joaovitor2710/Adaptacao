# Adaptacao-DARP-Para-MultiAndares-Simulado

Este repositório contém instruções para baixar e executar os arquivos referentes à adaptação do DARP para um ambiente multi-andares, mantendo os grids em 2D.

## Requisitos

### Versão do Python
- **Python**: 3.9

### Dependências  
```bash
opencv-python==4.5.2.54
pygame==2.0.1
scipy==1.7.1
nose==1.3.7
scikit-learn==0.24.2 
numpy==1.20
numba==0.54.1
pillow==8.4.0
matplotlib==3.4
pandas==1.3.3 
psutil

```

Recomenda-se o uso do pyenv para gerenciar a versão do Python, garantindo a compatibilidade com a versão 3.9. O algoritmo original do DARP apresenta dependências
que não foram atualizadas para o Python 10, o que pode gerar conflitos durante a instalação.

## Passos de Configuração

### 1.1 Instalar o Pyenv se não tiver Python 3.9 (Fortemente Recomendado)

```bash
curl https://pyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
source ~/.bashrc
pyenv --version
```

##### 1.1.1 Instalando a versão 3.9
```bash
pyenv install 3.9
```

### 1.2 Instalar a aplicação
```bash
git clone
cd nome
chmod +x Dependencies.sh
./Dependencies.sh DARP
pip install -r requirements.txt
```

#### 1.2.1 Executar o multi Andares
```bash
python3 multiFloor2d.py
```

## 2 Testando Novos Valores

Atualmente, o algoritmo **não** permite a passagem de valores diretamente pela linha de comando. Para testar diferentes configurações, é necessário modificar o código manualmente.  

Isso pode ser feito dentro da função `main` no arquivo **`multiFloor2d.py`**.  

Inicialmente, o código estará configurado da seguinte forma:  

![Configuração Inicial](Imagens/config.png)  

Todos os dados podem ser modificados, incluindo a posição das escadas e o grid. Abaixo estão os principais parâmetros que podem ser ajustados:  

| Parâmetro                     | Tipo            | Descrição  |
|--------------------------------|----------------|------------|
| `num_robos`                   | **int**        | Número de robôs |
| `num_andares`                 | **int**        | Número total de andares |
| `obstaculos_andar`            | **dict[list]** | Dicionário contendo listas de obstáculos para cada andar (começa em `0`) |
| `posicoes_de_escada_saida`    | **dict[list]** | Dicionário contendo listas das escadas de saída (também consideradas obstáculos) |
| `posicoes_de_escada_entrada`  | **dict[list]** | Dicionário contendo listas das escadas de entrada (também consideradas obstáculos) |
| `grid_andar`                  | **dict[tuple]** | Dicionário com as dimensões `(x, y)` do grid de cada andar |
| `deposito_1_andar`            | **list**       | Lista com as posições iniciais dos robôs no depósito |
| `vis`                         | **bool**       | Define se as saídas gráficas devem ser exibidas (`True` ou `False`) |

> **Observação:** As posições dos elementos dependem do tamanho do grid.  
> Exemplo: Se o grid for `10x10`, a última posição (`(9,9)`) deve ser representada como `99` na lista de obstáculos.

---

### 2.1 Executando o DARP Convencional  

Caso queira testar o DARP original em um grid padrão, consulte a documentação no repositório oficial:  
🔗 [DARP Original](https://github.com/alice-st/DARP?tab=readme-ov-file)

---

## 3 Visualização dos Resultados  

Esta seção explica como interpretar os resultados gerados pelo código.  

### 3.1 Caminhos Gerados pelo DARP Convencional  

![Visualização DARP](Imagens/DARP.png)  

Na imagem acima, cada robô é representado por uma cor diferente, mostrando a melhor trajetória para cobertura do ambiente.  

---

### 3.2 Mapeamento Multi-Andares  

![Visualização MultiAndares](Imagens/multi.png)  

Aqui, vemos um andar sendo mapeado pelos robôs. O **coverage** (região azul) é equivalente ao DARP convencional, mas, ao somar os três andares, o algoritmo multi-andares adiciona o **planejamento de trajetória com A*** para a transição entre andares.  

---

### 3.3 Resultados Finais  

![Visualização Resultados](Imagens/results.png)  

Após a execução do algoritmo, são apresentados:  

- **Tempo total de execução**  
- **Soma das distâncias percorridas** por cada robô, desde o depósito até o ponto final no último andar  
- **Número total de turnos** para cada robô considerando todos os andares  
- **Porcentagem de uso da CPU** durante a simulação  

---

### 3.4 Simulação das Escadas  

![Visualização Escada](Imagens/escada.png)  

As escadas **não** são diretamente mapeadas no algoritmo, mas sua distância e tempo de processamento são considerados no início da execução. Esses valores podem ser ajustados conforme necessário.  








