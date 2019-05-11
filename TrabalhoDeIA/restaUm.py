#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# TODO - DESCRIÇÃO DO MOTIVO DE IMPLEMENTAÇÃO DESTE ARQUIVOX
"""

__author__ = "Aryslene Santos Bitencourt [RGA: 201519060122]"
__author__ = "Felipe Alves Matos Caggi [RGA: 201719060061]"
__author__ = "Matheus Lima Machado [RGA: 201519060068]"

import numpy
from random import randint
import heapq
import winsound
import os
import time

#VARIÁVEIS GLOBAIS
idsDictionary = {}
smallerSoFar = 100

#MATRIZ COM OS PESOS DE CADA POSIÇÃO UTILIZANDO A DISTÂNCIA DE MANHATTAN...
#...(EM RELAÇÃO AO CENTRO DO TABULEIRO) COMO CRITÉRIO.
matriz_manhattan = numpy.matrix([[100, 100,   4,   3,   4, 100, 100],
                                 [100, 100,   3,   2,   3, 100, 100],
                                 [   4,  3,   2,   1,   2,   3,   4],
                                 [   3,  2,   1,   0,   1,   2,   3],
                                 [   4,  3,   2,   1,   2,   3,   4],
                                 [100, 100,   3,   2,   3, 100, 100],
                                 [100, 100,   4,   3,   4, 100, 100]])

"""
DESCRIÇÃO: 
"""
def evaluate(coordinates_array):

    global matriz_manhattan

    manhattan_center = 0
    eval_manhattan_pegs = 0
    #para cada coordenada
    for target in coordinates_array:
        aux_array = coordinates_array.copy() #uso uma copia para não alterar o vetor de coordenadas original
        manhattan_pegs_sum = 0
        #manhattan_sum = matriz_manhattan[target[0], target[1]] #distancia em relação ao centro, quanto maior, pior a avaliação
        #print(matriz_manhattan[target[0], target[1]])
        #calculando a distancia de manhattan de cada peça em relação às outras no tabuleiro
        for another_coordinate in aux_array:
            manhattan_pegs = abs(target[0] - another_coordinate[0]) + abs(target[1] - another_coordinate[1])  #|X1-X2| + |Y1-Y2|
            manhattan_pegs_sum += manhattan_pegs

        manhattan_center += matriz_manhattan[target[0], target[1]]
        eval_manhattan_pegs += manhattan_pegs_sum

    print("sua nota de manhattan_center: ", manhattan_center)
    print("sua nota de manhattan_pegs: ", eval_manhattan_pegs)
    eval = manhattan_center + eval_manhattan_pegs
    total_of_pegs = len(coordinates_array)
    final_eval = eval/total_of_pegs
    return final_eval


"""
DESCRIÇÃO: Soma todos os valores das casas.
Para ser considerado estado final, soma deve dar -15. 
Já que existem 16 espaços que não fazem parte do tabuleiro, e o objetivo é ter somente uma peça no tabuleiro.
Então: (16*-1)+1 = -15
"""

def isFinalState(parent):
    global smallerSoFar
    count = 0
    for row in range(0, len(parent)):
        for col in range(0, len(parent[0])):
            count = count + parent[row, col]

    if (count == -15):
        return True
    else:
        print('A quantidade de peças no tabuleiro é: ', count+16)
        if ((count + 16) < smallerSoFar):
            smallerSoFar = count+16
        print('O menor número de peças até agora é: ', smallerSoFar)

        return False

"""
DESCRIÇÃO: 
"""
def verificaIndiceDoMelhorCandidato(candidates):

    coordinates_array = []
    evaluations_array = []
    heapq.heapify(evaluations_array)
    global idsDictionary

    #aqui to identidicando as peças e armazenando suas coordenadas
    for index_candidate in range (0, len(candidates)):

        candidate = candidates[index_candidate]

        id = calculateIdentifier(candidate)

        if id in idsDictionary:
            eval = idsDictionary[id]#retorna a avaliação que, anteriormente, foi calculada para outro estado equivalente a este passado no parametro
        else:
            for row in range(0, len(candidate)):
                for col in range(0, len(candidate[0])):
                    if(candidate[row, col] == 1):
                        coordinate = (row, col)
                        coordinates_array.append(coordinate)

            eval = evaluate(coordinates_array)
            idsDictionary[id] = eval

        #evaluations_array.append(eval)
        heapq.heappush(evaluations_array, (eval, index_candidate))

    print('A quantidade total de candidatos é: ', len(evaluations_array))
    # print('São eles: ')
    # for eval in evaluations_array:
    #     print(eval, " | ",end="")
    # print("")
    #print("qtd no heap: ", len(evaluations_array))
    #print(evaluations_array)
    best_eval,index_of_best = heapq.heappop(evaluations_array)

    print('A nota do melhor candidato é: ', round(best_eval, 2))
    #print('...e seu índice [no vetor de candidatos gerais] é: ', index_of_best)
    #print(candidates[index_of_best])

    return index_of_best


"""
DESCRIÇÃO: Este método realiza a movimentação das peças de acordo com as análises realizadas.
Na prática o método alterna entre 1 e 0 os valores das peças localizadas na lista de coordenadas 
recebidas no parâmentro 'mvmt'.
Se a peça possui valor 1, será trocado para o valor 0.
Se a peça possui valor 0, será trocado para o valor 1.
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
DESCRIÇÃO: Este método busca todos os movimentos que podem ser realizados 
a partir de um estado de um tabuleiro.
"""
def searchPossibleMovements(state):
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
DESCRIÇÃO: Este método analisa um estado (pai) e gera estados filhos a partir dele.
"""
def gerarFilhos(parent):
    global idsDictionary
    list_of_sons = []

    movements_list = searchPossibleMovements(parent)

    # Estruturas de repetição para percorrer a lista de movimentos
    for row in movements_list:
        for mvmt in row:  # 'mvmt' corresponde à lista das 3 coordenadas das peças que estarão sendo movimentadas/alteradas
            parent_copy = parent.copy()
            son = move(parent_copy, mvmt)  # Realizando movimento
            list_of_sons.append(son)

    print('Gerei ',len(list_of_sons),' filhos a partir do melhor candidato!')

    # if (len(list_of_sons) == 0):
    #     idsDictionary[calculateIdentifier(parent)] = 2147483647
    #     print('Encontrei um filho estéril! Vou continuar a partir do melhor candidato!')
    #     print("O estéril está aqui:")
    #     print(parent)
    #     print("\n")


    return list_of_sons


"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def aEstrela(estado):

    candidates = [estado]
    visited = []
    solutionNotFound = True



    while solutionNotFound:  # Percorre a lista de candidatos enquanto houver candidatos

        print("Já conheço ", len(idsDictionary), " estados equivalentes")

        parentIndex = verificaIndiceDoMelhorCandidato(candidates)
        parent = candidates[parentIndex]

        if(isFinalState(parent)):
            solutionNotFound = False
            theEnd = time.time()
            print("TEMPO DE EXECUÇÃO: ",round(theEnd - start, 3), "segundos")
            print('Sucesso! Encontrei a solução!')
            print("Aqui está:")
            print(parent)
            winsound.Beep(420, 4000)
            # for x in range(0,3):
            #     os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 440))
            # os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 440))
            break
        else:
            print('Essa ainda não é a solução...')


        list_of_sons = gerarFilhos(parent)  # Gerando os filhos do pai atual

        if(len(list_of_sons)!=0):
            visited.append(parent)
            print("Já visitei: ",len(visited)," estados")
            candidates.pop(parentIndex)
            for son in list_of_sons:
                candidates.append(son)
            print("\n")
        else:
            visited.append(parent)
            print("Já visitei: ", len(visited), " estados")
            #print("O último visitado era um estéril!")
            print("\n")
            candidates.pop(parentIndex)

"""
DESCRIÇÃO: 
"""
def calculateIdentifier(candidate):

    # aqui eu faço uma logica que se não estiver no grupo de identificadores, tem q chamar um metodo só pra calcular
    idString = ["","","","","","","",""]
    id = []

    #percorrer o candidato e gerar o identificador

    oppositRow = len(candidate) - 1
    for row in range(0, len(candidate)):
        oppositeCol = len(candidate[0]) - 1

        for col in range(0, len(candidate[0])):
            #VARREDURA HORIZONTAL
            idString[0] += str(abs(candidate[row, col]))                #direção: diagonal pra baixo à direita
            idString[1] += str(abs(candidate[row, oppositeCol]))        #direção: diagonal pra baixo à esquerda

            idString[2] += str(abs(candidate[oppositRow, col]))         #direção: diagonal pra cima à direita
            idString[3] += str(abs(candidate[oppositRow, oppositeCol])) #direção: diagonal pra cima à esquerda

            #VStringARREDURA VERTICAL
            idString[4] += str(abs(candidate[col, row]))                #direção: diagonal pra baixo à direita
            idString[5] += str(abs(candidate[oppositeCol, row]))        #direção: diagonal pra baixo à esquerda

            idString[6] += str(abs(candidate[col, oppositRow]))         #direção: diagonal pra cima à direita
            idString[7] += str(abs(candidate[oppositeCol, oppositRow])) #direção: diagonal pra cima à esquerda

            oppositeCol = oppositeCol - 1
        oppositRow = oppositRow - 1

    #para cada string de 0's e 1's, transforme-a para binario e depois adicione, em formato decimal, à lista
    for string in idString:
        id.append(int(string, 2))

    identifier = min(id)

    #print("ID: ", identifier)

    return identifier

"""
# TODO - DESCRIÇÃO DO MÉTODO
"""
def limparPosicoesVazias(tabuleiro_inicial):
    tabuleiro_inicial = numpy.where(tabuleiro_inicial == 0, -1, tabuleiro_inicial)  # Alterando posições com valores igual a 0 para -1
    tabuleiro_inicial[3][3] = 0  # Retornando valor da peça central para 0
    return tabuleiro_inicial

"""
DESCRIÇÃO: Este método é responsável por executar o programa.
"""
if __name__ == '__main__':
    start = time.time()
    # generateDictionaryEvaluations()
    #

    #DIFICULDADE: SUPERHARD -------------------------------------------------
    estado_inicial_recebido = numpy.array([[0, 0, 1, 1, 1, 0, 0],
                                           [0, 0, 1, 1, 1, 0, 0],
                                           [1, 1, 1, 1, 1, 1, 1],
                                           [1, 1, 1, 0, 1, 1, 1],
                                           [1, 1, 1, 1, 1, 1, 1],
                                           [0, 0, 1, 1, 1, 0, 0],
                                           [0, 0, 1, 1, 1, 0, 0]])

    estado_inicial_tratado = limparPosicoesVazias(estado_inicial_recebido)
    aEstrela(estado_inicial_tratado)

    # DIFICULDADE: DIFÍCIL -------------------------------------------------
    # estado_inicial_recebido = numpy.array([[-1, -1, 0, 1, 0, -1, -1],
    #                                        [-1, -1, 1, 1, 1, -1, -1],
    #                                        [ 0,  1, 1, 1, 1,  1,  0],
    #                                        [ 1,  1, 1, 1, 1,  1,  1],
    #                                        [ 0,  1, 1, 1, 1,  1,  0],
    #                                        [-1, -1, 1, 1, 1, -1, -1],
    #                                        [-1, -1, 0, 1, 0, -1, -1]])
    #
    #
    # aEstrela(estado_inicial_recebido)

    # DIFICULDADE: MODERADA  ------------------------------------------------
    # estado_inicial_recebido = numpy.array([[-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 1, 0, -1, -1],
    #                                        [ 0,  0, 1, 1, 1,  0,  0],
    #                                        [ 0,  1, 1, 1, 1,  1,  0],
    #                                        [ 1,  1, 1, 1, 1,  1,  1],
    #                                        [-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 0, 0, -1, -1]])
    #
    #
    # aEstrela(estado_inicial_recebido)

    # DIFICULDADE: FÁCIL ------------------------------------------------
    # estado_inicial_recebido = numpy.array([[-1, -1, 1, 1, 1, -1, -1],
    #                                        [-1, -1, 1, 1, 1, -1, -1],
    #                                        [ 0,  0, 1, 1, 1,  0,  0],
    #                                        [ 0,  0, 1, 0, 1,  0,  0],
    #                                        [ 0,  0, 0, 0, 0,  0,  0],
    #                                        [-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 0, 0, -1, -1]])
    # aEstrela(estado_inicial_recebido)

    # DIFICULDADE: SUPEREASY ----------------------------------------------------
    # estado_inicial_recebido = numpy.array([[-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 1, 0, -1, -1],
    #                                        [ 0,  0, 1, 1, 1,  0,  0],
    #                                        [ 0,  0, 0, 1, 0,  0,  0],
    #                                        [ 0,  0, 0, 1, 0,  0,  0],
    #                                        [-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 0, 0, -1, -1]])
    # aEstrela(estado_inicial_recebido)