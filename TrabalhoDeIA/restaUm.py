#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# TODO - DESCRIÇÃO DO MOTIVO DE IMPLEMENTAÇÃO DESTE ARQUIVO
"""

__author__ = "Aryslene Bitencourt"
__author__ = "Felipe Caggi"
__author__ = "Matheus Lima Machado"

import numpy

"""
Soma todos os valores das casas, o objetivo é -15. 
Já que existem 16 espaços que não fazem parte do tabuleiro, e o objetivo é ter somente uma peça no tabuleiro.
Então: (16*-1)+1 = -15
"""
def isFinalState(father):
    count = 0
    for row in range(0, len(father)):
        for col in range(0, len(father[0])):
            count = count + father[row, col]

    if(count == -15):
        return True
    else:
        return False

"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def verificaIndiceDoMelhorCandidato(candidates):
    if(len(candidates) == 1):
        print('vetor de avaliações: [88]')
        return candidates[0]

    matriz_manhattan = numpy.matrix([[100, 100,   4,   3,   4, 100, 100],
                                     [100, 100,   3,   2,   3, 100, 100],
                                     [   4,  3,   2,   1,   2,   3,   4],
                                     [   3,  2,   1,   0,   1,   2,   3],
                                     [   4,  3,   2,   1,   2,   3,   4],
                                     [100, 100,   3,   2,   3, 100, 100],
                                     [100, 100,   4,   3,   4, 100, 100]])

    #COMPARA A MATRIZ DE MANHATTAN COM CADA FILHO
    evaluations_array = numpy.arange(len(candidates))
    eval = 0
    son_index = 0
    for son in candidates:
        for row in range(0, len(son)):
            for col in range(0, len(son[0])):
                #se for igual a 1, eu somo o valor da posicao equivalente ao meu contador de FA
                if(son[row, col] == 1):
                    eval += matriz_manhattan[row, col]
        evaluations_array[son_index] = eval
        eval = 0
        son_index = son_index + 1

    result = numpy.where(evaluations_array == numpy.amin(evaluations_array))
    print('vetor de avaliações: ',evaluations_array)

    bests_sons_indexes = result[0]
    best_son_chosen_index = bests_sons_indexes[0] #caso tenha empate de minimos, vai sempre escolher o q estiver na posicao 0
    return best_son_chosen_index

"""
Este método alterna entre 1 e 0 os valores das peças localizadas na lista de coordenadas recebidas no parâmentro 'mvmt'

    Se a peça possui valor 1, será trocado para o valor 0
    Se a peça possui valor 0, será trocado para o valor 1

    Essa troca de valores corresponde à movimentação das peças de acordo com as análises realizadas
"""
def move(state, mvmt):
    for piece in mvmt:

        if state[piece[0]][
            piece[1]] == 0:  # Verifica se o valor da peça na coordenada atual(piece[0], piece[1]) possui valor '1'
            state[piece[0]][piece[1]] = 1

        elif state[piece[0]][
            piece[1]] == 1:  # Verifica se o valor da peça na coordenada atual(piece[0], piece[1]) possui valor '0'
            state[piece[0]][piece[1]] = 0

    return state;

"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def buscarMovimentosPossiveis(state):
    r_mvmt = [1, 1, 0]  # Requisito de posicionamento horizontal no tabuleiro para movimentar a peça para direita
    l_mvmt = [0, 1, 1]  # Requisito de posicionamento horizontal no tabuleiro para movimentar a peça para esquerda
    d_mvmt = [1, 1, 0]  # Requisito de posicionamento vertical no tabuleiro para movimentar a peça para baixo
    u_mvmt = [0, 1, 1]  # Requisito de posicionamento vertical no tabuleiro para movimentar a peça para cima

    movements_list = [[], [], [], []]  # Lista de movimentos possíveis no estado atual - [[r_mvmt], [l_mvmt], [d_mvmt], [u_mvmt]]

    # Varredura horizontal
    for row in range(0, len(state)):
        for col in range(0, len(state[0]) - 2):

            # A área de busca corresponde a 3 casas vizinhas posicionadas horizontalmente (peça da coluna atual mais os dois vizinhos à direita dessa)
            search_area = [state[row, col], state[row, col + 1], state[row, col + 2]]

            # movements_list[0] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para direita
            if (search_area == r_mvmt):
                movements_list[0].append([[row, col], [row, col + 1], [row, col + 2]])

            # movements_list[1] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para esquerda
            if (search_area == l_mvmt):
                movements_list[1].append([[row, col], [row, col + 1], [row, col + 2]])

    # Varredura vertical
    for row in range(0, len(state) - 2):
        for col in range(0, len(state[0])):

            # A área de busca corresponde a 3 peças vizinhas posicionadas verticalmente (peça da coluna atual mais os dois vizinhos à abaixo dessa)
            search_area = [state[row, col], state[row + 1, col], state[row + 2, col]]

            if (search_area == d_mvmt):
                movements_list[2].append([[row, col], [row + 1, col], [row + 2,
                                                                       col]])  # movements_list[2] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para baixo

            if (search_area == u_mvmt):
                movements_list[3].append([[row, col], [row + 1, col], [row + 2,
                                                                       col]])  # movements_list[3] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para cima

    movements_list = numpy.array(movements_list)

    return movements_list


"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def gerarFilhos(father):
    list_of_sons = []

    movements_list = buscarMovimentosPossiveis(father)

    #print(movements_list) #<- SE PRECISAREM VISUALIZAR A LISTA DE MOVIMENTOS

    # Estruturas de repetição para percorrer a lista de movimentos
    for row in movements_list:
        for mvmt in row:  # 'mvmt' corresponde à lista das 3 coordenadas das peças que estarão sendo movimentadas/alteradas
            father_copy = father.copy()
            son = move(father_copy, mvmt)  # Realizando movimento
            list_of_sons.append(son)

    count = 1
    for son in list_of_sons:  # Exibindo cada filho do pai atual
        print('Filho', count)
        print(son)
        print('\n')
        count += 1

    return list_of_sons


"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def aEstrela(estado):
    # Armazenamento de informações

    ######################3
    #parents = dict()
    candidates = [estado]  # Lista dos nós candidatos a serem visitados
    visited = []     # Lista dos nós já visitados

    numInteracoes = 3
    iteracoes = 3

    #while len(candidates) > 0:  # Percorre a lista de candidatos enquanto houver candidatos
    while iteracoes > 0:
        print('------------------------------------__')
        print('Candidatos: ')
        for son in candidates:
            print(son)
            print('\n')
        print('Visidatos: ')
        for son in visited:
            print(son)
            print('\n')
        print('____________________________________--')

        fatherIndex = verificaIndiceDoMelhorCandidato(candidates)

        if(isFinalState(candidates[fatherIndex])):
            break
        else:
            print("Father (Não é solução!)")
            print(candidates[fatherIndex])
            print('\n')

        visited.append(candidates[fatherIndex])
        candidates.pop(fatherIndex)

        list_of_sons = gerarFilhos(candidates[fatherIndex])  # Gerando os filhos do pai atual

        for son in list_of_sons:
            candidates.append(son)

        iteracoes = iteracoes - 1



"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def limparPosicoesVazias(tabuleiro_inicial):
    tabuleiro_inicial = numpy.where(tabuleiro_inicial == 0, -1, tabuleiro_inicial)  # Alterando posições com valores igual a 0 para -1
    tabuleiro_inicial[3][3] = 0  # Retornando valor da peça central para 0
    return tabuleiro_inicial

"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
if __name__ == '__main__':
    estado_inicial_recebido = numpy.matrix([[0, 0, 1, 1, 1, 0, 0],
                                            [0, 0, 1, 1, 1, 0, 0],
                                            [1, 1, 1, 1, 1, 1, 1],
                                            [1, 1, 1, 0, 1, 1, 1],
                                            [1, 1, 1, 1, 1, 1, 1],
                                            [0, 0, 1, 1, 1, 0, 0],
                                            [0, 0, 1, 1, 1, 0, 0]])

    estado_inicial_tratado = limparPosicoesVazias(estado_inicial_recebido)
    aEstrela(estado_inicial_tratado)