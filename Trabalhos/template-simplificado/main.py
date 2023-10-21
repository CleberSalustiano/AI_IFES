# 

import time
import random

from collections import deque
from viewer import MazeViewer
from math import inf, sqrt

def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 50% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.50 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
        linha = random.randint(0, n_linhas-1)
        coluna = random.randint(0, n_colunas-1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto


class Celula:
    def __init__(self, y, x, anterior):
        self.y = y
        self.x = x
        self.anterior = anterior
        self.f = 0
        self.g = 0
        self.h = 0


def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto):
    # generate neighbors of the current state
    vizinhos = [
        Celula(y=celula_atual.y-1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+1, anterior=celula_atual),
    ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


def depth_first_search(labirinto, inicio, goal, viewer):
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    objetivo_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (objetivo_encontrado is None):

        # seleciona o no mais novo para ser expandido
        no_atual = fronteira.pop()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for vizinho in vizinhos:
            if vizinho.y == goal.y and vizinho.x == goal.x:
                objetivo_encontrado = vizinho
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, vizinho)) and (not esta_contido(fronteira, vizinho)):
                    fronteira.append(vizinho)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        # viewer.pause()


    caminho = obtem_caminho(objetivo_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos


    # remova o comando abaixo e coloque o codigo DFS aqui
    #pass


def a_star_search(labirinto, inicio, goal, viewer):
    # Nós na fronteira que podem ser expandidos (vermelhos)
    fronteira = deque()
    # Nós já expandidos (amarelos)
    expandidos = set()

    # Adiciona o nó inicial à fronteira
    fronteira.append(inicio)

    # Variável para armazenar o objetivo quando for encontrado.
    objetivo_encontrado = None
    
    # Início do loop principal: Encontra o caminho usando o algoritmo A*
    while (len(fronteira) > 0) and (objetivo_encontrado is None):
    
        # Encontra o no com menor valor de f
        no_atual = fronteira[0]
        for item in fronteira:
            if item.f < no_atual.f:
                no_atual = item
        
        # Remove o nó atual da fronteira e adiciona aos expandidos
        fronteira.remove(no_atual)

        # Busca os vizinhos do nó
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)
        
        # Para cada vizinho, verifica se é o objetivo e adiciona à fronteira
        # se ainda não foi expandido e não está na fronteira
        for vizinho in vizinhos:
            if vizinho.y == goal.y and vizinho.x == goal.x:
                objetivo_encontrado = vizinho
                # Sai do loop interno
                break
            else:
                # Se o vizinho não foi expandido, calcula f = g + h
                if (not esta_contido(expandidos, vizinho)):
                    vizinho.g = no_atual.g + 1
                    vizinho.h = distancia(vizinho, goal)
                    vizinho.f = vizinho.g + vizinho.h

                    # Se estiver na fronteira e tiver um valor menor de g,
                    # atualiza o valor de g e do nó anterior na fronteira
                    if esta_contido(fronteira, vizinho):
                        for elemento in fronteira:
                            if (elemento.y == vizinho.y) and (elemento.x == vizinho.x):
                                if vizinho.g < elemento.g:
                                    continue
                    # Se não estiver na fronteira, adiciona-o
                    else:
                        fronteira.append(vizinho)
        expandidos.add(no_atual)
                    
        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        # viewer.pause()
                    
    caminho = obtem_caminho(objetivo_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos


def uniform_cost_search(labirinto, inicio, goal, viewer):
    # Nós gerados e passíveis de expansão (marcados em vermelho)
    fronteira = deque()
    # Nós já expandidos (marcados em amarelo)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # Inicializa uma lista de vizinhos do nó inicial
    vizinhos = celulas_vizinhas_livres(inicio, labirinto)

    # Variável para armazenar o objetivo quando encontrado
    objetivo_encontrado = None    
    
    while (len(fronteira) > 0) and (objetivo_encontrado is None):
        # Continua enquanto houver nós na fronteira e o objetivo não foi encontrado

        # Seleciona o nó mais recente para expansão
        no_atual = fronteira[0]
        for item in fronteira:
            if item.f < no_atual.f:
                no_atual = item
        
        # Remove o nó atual da fronteira e o adiciona aos expandidos
        fronteira.remove(no_atual)
        expandidos.add(no_atual)

        # Busca os vizinhos do nó atual
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)
        
        # Para cada vizinho, verifica se é o objetivo e o adiciona à
        # fronteira se ainda não foi expandido e não está na fronteira
        for vizinho in vizinhos:
            if vizinho.y == goal.y and vizinho.x == goal.x:
                objetivo_encontrado = vizinho
                # Encerra o loop interno, pois o objetivo foi encontrado
                break
            else:
                # Caso o vizinho não tenha sido expandido, calcula f = g + h
                if (not esta_contido(expandidos, vizinho)):
                    vizinho.g = no_atual.g + 1

                    # Se o vizinho já está na fronteira e com valor de g maior,
                    # atualiza o valor de g e o nó anterior na fronteira
                    if esta_contido(fronteira, vizinho):
                        for elemento in fronteira:
                            if (elemento.y == vizinho.y) and (elemento.x == vizinho.x):
                                if vizinho.g < elemento.g:
                                    elemento.g = vizinho.g
                                    elemento.anterior = vizinho.anterior
                    else:
                        fronteira.append(vizinho)
               
        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        # viewer.pause()
                    
    caminho = obtem_caminho(objetivo_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos



#-------------------------------


def main():
    for _ in range(1000):
        SEED = 0  # coloque None no lugar do 42 para deixar aleatorio
        random.seed(SEED)
        N_LINHAS  = 100
        N_COLUNAS = 100
        INICIO = Celula(y=0, x=0, anterior=None)
        GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None)


        """
        O labirinto sera representado por uma matriz (lista de listas)
        em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
        """
        labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL)

        viewer = MazeViewer(labirinto, INICIO, GOAL,
                            step_time_miliseconds=20, zoom=10)
        
        #----------------------------------------
        # DFS Search
        #----------------------------------------
        viewer._figname = "DFS"
        tempo_inicial = time.time()
        caminho, custo_total, expandidos = \
                depth_first_search(labirinto, INICIO, GOAL, viewer)
        tempo_final = time.time()

        if len(caminho) == 0:
            print("Goal is unreachable for this maze.")

        print(
            f"DFS:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tTempo de execucao: {tempo_final-tempo_inicial}.\n\n"
        )

        # viewer.update(path=caminho)
        # viewer.pause()
        
        #----------------------------------------
        # A-Star Search
        #----------------------------------------
        
        viewer._figname = "A-Star"
        tempo_inicial = time.time()
        caminho, custo_total, expandidos = \
                a_star_search(labirinto, INICIO, GOAL, viewer)
        tempo_final = time.time()

        if len(caminho) == 0:
            print("Goal is unreachable for this maze.")

        print(
            f"A-Star:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tTempo de execucao: {tempo_final-tempo_inicial}.\n\n"
        )

        # viewer.update(path=caminho)
        # viewer.pause()

        #----------------------------------------
        # Uniform Cost Search (Obs: opcional)
        #----------------------------------------

        viewer._figname = "Uniform Cost Search"
        tempo_inicial = time.time()
        caminho, custo_total, expandidos = \
                uniform_cost_search(labirinto, INICIO, GOAL, viewer)
        tempo_final = time.time()

        if len(caminho) == 0:
            print("Goal is unreachable for this maze.")

        print(
            f"Uniform Cost Search:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tTempo de execucao: {tempo_final-tempo_inicial}.\n\n"
        )

        # viewer.update(path=caminho)
        # viewer.pause()


    print("OK! Pressione alguma tecla pra finalizar...")
    input()


if __name__ == "__main__":
    main()