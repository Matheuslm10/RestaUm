#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# TODO - DESCRIÇÃO DO MOTIVO DE IMPLEMENTAÇÃO DESTE ARQUIVO
"""

__author__ = "Aryslene Sobrenome"
__author__ = "Felipe Caggi"
__author__ = "Matheus Sobrenome"

import numpy

"""
# TODO - DESCRIÇÃO DO MÉTODO
"""


def buscarMovimentosPossiveis(state):
    r_mvmt = [1, 1, 0]  # Requisito de posicionamento horizontal no tabuleiro para movimentar a peça para direita
    l_mvmt = [0, 1, 1]  # Requisito de posicionamento horizontal no tabuleiro para movimentar a peça para esquerda
    d_mvmt = [1, 1, 0]  # Requisito de posicionamento vertical no tabuleiro para movimentar a peça para baixo
    u_mvmt = [0, 1, 1]  # Requisito de posicionamento vertical no tabuleiro para movimentar a peça para cima

    movements_list = [[], [], [],
                      []]  # Lista de movimentos possíveis no estado atual - [[r_mvmt], [l_mvmt], [d_mvmt], [u_mvmt]]

    # Varredura horizontal
    for row in range(0, len(state)):
        for col in range(0, len(state[0]) - 2):

            # A área de busca corresponde a 3 peças vizinhas posicionadas horizontalmente (peça da coluna atual mais os dois vizinhos à direita dessa)
            search_area = [state[row, col], state[row, col + 1], state[row, col + 2]]

            if (search_area == r_mvmt):
                movements_list[0].append([[row, col], [row, col + 1], [row,
                                                                       col + 2]])  # movements_list[0] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para direita

            if (search_area == l_mvmt):
                movements_list[1].append([[row, col], [row, col + 1], [row,
                                                                       col + 2]])  # movements_list[1] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para esquerda

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


def gerarFilhos(father):
    list_of_sons = []  # Lista para armazenamento dos filhos do pai atual

    movements_list = buscarMovimentosPossiveis(father)  # Verificação das movimentações possíveis

    # print(movements_list) <- SE PRECISAREM VISUALIZAR A LISTA DE MOVIMENTOS

    # Estruturas de repetição para percorrer a lista de movimentos
    for row in movements_list:
        for mvmt in row:  # 'mvmt' corresponde à lista das 3 coordenadas das peças que estarão sendo movimentadas/alteradas
            father_copy = father.copy()
            son = move(father_copy, mvmt)  # Realizando movimento
            list_of_sons.append(son)

    print('\nFather\n', father)  # Exibindo pai atual

    count = 1
    for son in list_of_sons:  # Exibindo cada filho do pai atual
        print('\nFilho', count, '\n', son)
        count += 1

    return list_of_sons


"""
# TODO - DESCRIÇÃO DO MÉTODO
"""


def aEstrela(tabuleiro):
    # Armazenamento de informações
    parents = dict()
    candidates = [tabuleiro]  # Lista dos nós candidatos a serem visitados
    visited = [tabuleiro]  # Lista dos nós já visitados

    while len(candidates) > 0:  # Percorre a lista de candidatos enquanto houver candidatos
        father = candidates[0]
        del candidates[0]

        list_of_sons = gerarFilhos(father)  # Gerando os filhos do pai atual

        # ... To Be Continued ...
        # Verificações de custos
        # Adicionar filhos na lista de candidatos de acordo com os requisitos do algoritmo A*
        # .
        # .
        # .
        # Foi tudi lembrei... tem que olhar no A* e ver oque mais pede


"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
if __name__ == '__main__':
    posicao_inicial = numpy.matrix([[0, 0, 1, 1, 1, 0, 0],
                                    [0, 0, 1, 1, 1, 0, 0],
                                    [1, 1, 1, 1, 1, 1, 1],
                                    [1, 1, 1, 0, 1, 1, 1],
                                    [1, 1, 1, 1, 1, 1, 1],
                                    [0, 0, 1, 1, 1, 0, 0],
                                    [0, 0, 1, 1, 1, 0, 0]])  # Posição inicial da peças no tabuleiro

    posicao_inicial = numpy.where(posicao_inicial == 0, -1,
                                  posicao_inicial)  # Alterando posições com valores igual a 0 para -1
    posicao_inicial[3][3] = 0  # Retornando valor da peça central para 0

    # print(posicao_inicial)

    aEstrela(posicao_inicial)