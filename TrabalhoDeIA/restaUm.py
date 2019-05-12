#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# TODO - DESCRIÇÃO DO MOTIVO DE IMPLEMENTAÇÃO DESTE ARQUIVOX
"""

__author__ = "Aryslene Santos Bitencourt [RGA: 201519060122]"
__author__ = "Felipe Alves Matos Caggi [RGA: 201719060061]"
__author__ = "Matheus Lima Machado [RGA: 201519060068]"

import numpy
import heapq
import winsound
import os
import time

#VARIÁVEIS GLOBAIS
idsDictionary = {}
smallerSoFar = 100

def isShyPeg(target, candidate):
    x = target[0]
    y = target[1]
    shypeg = False

    if (x, y) == (0, 2) or (x, y) == (2, 0):
        # verifica lateral direita e baixo
        if candidate[x, y + 1] == 0 and candidate[x + 1, y] == 0:
            shypeg = True
    elif (x, y) == (0, 4) or (x, y) == (2, 6):
        # verifica lateral esquerda e baixo
        if candidate[x, y - 1] == 0 and candidate[x + 1, y] == 0:
            shypeg = True
    elif (x, y) == (4, 0) or (x, y) == (6, 2):
        # verifica lateral direita e cima
        if candidate[x, (y + 1)] == 0 and candidate[(x - 1), y] == 0:
            shypeg = True
    elif (x, y) == (4, 6) or (x, y) == (6, 4):
        # verifica lateral esquerda e cima
        if candidate[x, y - 1] == 0 and candidate[x - 1, y] == 0:
            shypeg = True

    elif (x, y) == (0,3):
        # verifica lateral esquerda e cima
        if candidate[0,2] == 0 and candidate[1,3] == 0 and candidate[0,4] == 0:
            print("Disgraça!")
            shypeg = True
    elif (x, y) == (3,0):
        # verifica lateral esquerda e cima
        if candidate[2,0] == 0 and candidate[3,1] == 0 and candidate[4,0] == 0:
            shypeg = True
    elif (x, y) == (3,6):
        # verifica lateral esquerda e cima
        if candidate[2,6] == 0 and candidate[3,5] == 0 and candidate[4,6] == 0:
            shypeg = True
    elif (x, y) == (6,3):
        # verifica lateral esquerda e cima
        if candidate[6,2] == 0 and candidate[5,3] == 0 and candidate[6,4] == 0:
            shypeg = True

    return shypeg


def getCoordinates(state):
    coordinates_list = []
    for row in range(0, len(state)):
        for col in range(0, len(state[0])):
            if (state[row, col] == 1):
                coordinate = (row, col)
                coordinates_list.append(coordinate)

    return coordinates_list

def lookForGoodMovements(mvmts):
    goodMovements = 0
    for row in mvmts:
        for mvmt in row:
            origin_coordinate = mvmt[0]
            x = origin_coordinate[0]
            y = origin_coordinate[1]

            #se o movimento estiver no quadrante de cima
            if (x,y) == (0,2) or (x,y) == (0,3) or (x,y) == (0,4) or (x,y) == (1,2) or (x,y) == (1,3) or (x,y) == (1,4):
                goodMovements += 10
            # se o movimento estiver no quadrante da esquerda
            elif (x,y) == (2,0) or (x,y) == (2,1) or (x,y) == (3,0) or (x,y) == (3,1) or (x,y) == (4,0) or (x,y) == (4,1):
                goodMovements += 10
            # se o movimento estiver no quadrante da direita
            elif (x,y) == (2,5) or (x,y) == (2,6) or (x,y) == (3,5) or (x,y) == (3,6) or (x,y) == (4,5) or (x,y) == (4,6):
                goodMovements += 10
            # se o movimento estiver no quadrante de baixo
            elif (x,y) == (5,2) or (x,y) == (5,3) or (x,y) == (5,4) or (x,y) == (6,2) or (x,y) == (6,3) or (x,y) == (6,4):
                goodMovements += 10

    return goodMovements

def calculateSumOfManhattanBetweenPegs(target, coordinates_list):
    manhattan_sum = 0
    for another_coordinate in coordinates_list:
        manhattan = abs(target[0] - another_coordinate[0]) + abs(target[1] - another_coordinate[1])  # |X1-X2| + |Y1-Y2|
        manhattan_sum += manhattan
    return manhattan_sum
"""
DESCRIÇÃO: 'shypeg' siginifica peça tímida. Faz alusão às peças que ficam nas bordas isoladas das outras.
"""
def evaluate(candidate):
    coordinates_list = getCoordinates(candidate)
    possibleMovements = searchPossibleMovements(candidate)
    goodMovements = lookForGoodMovements(possibleMovements)

    manhattan_center = numpy.matrix([[0, 0, 4, 3, 4, 0, 0],
                                     [0, 0, 3, 2, 3, 0, 0],
                                     [4, 3, 2, 1, 2, 3, 4],
                                     [3, 2, 1, 0, 1, 2, 3],
                                     [4, 3, 2, 1, 2, 3, 4],
                                     [0, 0, 3, 2, 3, 0, 0],
                                     [0, 0, 4, 3, 4, 0, 0]])
    manhattan_eval = 0
    shypeg_penalty = 0
    farFromCenterPenalty = 0

    weight_FFCP = 1
    weight_GM = 0
    weight_M = 0
    weight_DF = 0
    weight_SPP = 0

    print("FILHO ANALISADO")
    print(candidate)
    total_of_pegs = len(coordinates_list)

    for target in coordinates_list:
        farFromCenterPenalty += manhattan_center[target]
        manhattan_sum = calculateSumOfManhattanBetweenPegs(target, coordinates_list)
        manhattan_eval += manhattan_sum

    print("SUA NOTA centro: ", farFromCenterPenalty)

    depth_factor = 1024 - ((32-total_of_pegs) ** 2)
    print("SUA NOTA profundidade: ", depth_factor)

    final_manhattan_eval = (manhattan_eval/total_of_pegs)
    print("SUA NOTA manhattan: ", final_manhattan_eval)

    total_shypeg_penalty = shypeg_penalty**(2**(shypeg_penalty))
    print("SUA NOTA shypeg: ", total_shypeg_penalty)

    final_eval = (final_manhattan_eval*weight_M) + (total_shypeg_penalty*weight_SPP) + (farFromCenterPenalty*weight_FFCP) + (depth_factor*weight_DF) - (goodMovements*weight_GM)
    print("SUA NOTA final: ", final_eval)

    return final_eval


"""
DESCRIÇÃO: Soma todos os valores das casas.
Como existem 16 espaços que não fazem parte do tabuleiro, e estão sendo representados por -1 na matriz.
Então: estado final (com os espaços vazios) = (-16)+1 = -15
"""
def calculateNumberOfPegs(state):
    count = 0
    for row in range(0, len(state)):
        for col in range(0, len(state[0])):
            count = count + state[row, col]

    total = count + 16 #16 posicões vazias

    return total


"""
DESCRIÇÃO: Este método realiza a movimentação das peças de acordo com as análises realizadas.
Na prática o método alterna entre 1 e 0 os valores das peças localizadas na lista de coordenadas 
recebidas no parâmentro 'mvmt'.
Se a peça possui valor 1, será trocado para o valor 0.
Se a peça possui valor 0, será trocado para o valor 1.
"""
def move(state, mvmt):

    for piece in mvmt:
        row = piece[0]
        col = piece[1]

        # Verifica se o valor da peça na coordenada atual(row, col) possui valor '1'
        if state[row][col] == 0:
            state[row][col] = 1

        # Verifica se o valor da peça na coordenada atual(row, col) possui valor '0'
        elif state[row][col] == 1:
            state[row][col] = 0

    return state


def searchPossibleMovements(state):
    right_mvmt = [1, 1, 0]  # Requisito de posicionamento horizontal no tabuleiro para movimentar a peça para direita
    left_mvmt  = [0, 1, 1]  # Requisito de posicionamento horizontal no tabuleiro para movimentar a peça para esquerda
    up_mvmt    = [1, 1, 0]  # Requisito de posicionamento vertical no tabuleiro para movimentar a peça para baixo
    down_mvmt  = [0, 1, 1]  # Requisito de posicionamento vertical no tabuleiro para movimentar a peça para cima

    movements_list = [[], [], [], []]  # Lista de movimentos possíveis no estado atual - [[right_mvmt], [left_mvmt], [up_mvmt], [down_mvmt]]

    # Varredura horizontal
    for row in range(0, len(state)):
        for col in range(0, len(state[0]) - 2):

            # A área de busca corresponde a 3 casas vizinhas posicionadas horizontalmente (peça da coluna atual mais os dois vizinhos à direita dessa)
            search_area = [state[row, col], state[row, col + 1], state[row, col + 2]]

            # movements_list[0] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para direita
            if (search_area == right_mvmt):
                movements_list[0].append([[row, col], [row, col + 1], [row, col + 2]])

            # movements_list[1] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para esquerda
            if (search_area == left_mvmt):
                movements_list[1].append([[row, col], [row, col + 1], [row, col + 2]])

    # Varredura vertical
    for row in range(0, len(state) - 2):
        for col in range(0, len(state[0])):

            # A área de busca corresponde a 3 peças vizinhas posicionadas verticalmente (peça da coluna atual mais os dois vizinhos à abaixo dessa)
            search_area = [state[row, col], state[row + 1, col], state[row + 2, col]]

            # movements_list[2] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para baixo
            if (search_area == up_mvmt):
                movements_list[2].append([[row, col], [row + 1, col], [row + 2, col]])

            # movements_list[3] armazena a coordenada(x,y) do trio de peças correspondentes ao padrão de movimentação para cima
            if (search_area == down_mvmt):
                movements_list[3].append([[row, col], [row + 1, col], [row + 2, col]])

    movements_list = numpy.array(movements_list)

    return movements_list


def generateSons(parent):
    global idsDictionary
    list_of_sons = []
    movements_list = searchPossibleMovements(parent)
    previous_id = 0

    # Para cada movimento possível, é gerado um filho. Porém se o filho gerado ter a mesma avaliação que um irmão, ele é descartado.
    for row in movements_list:
        for mvmt in row:  # 'mvmt' corresponde à lista das 3 coordenadas das peças que estarão sendo movimentadas/alteradas
            parent_copy = parent.copy()
            son = move(parent_copy, mvmt)
            list_of_sons.append(son)
            # current_id = calculateIdentifier(son)
            # if previous_id != current_id:
            #     list_of_sons.append(son)
            #     previous_id = current_id

    print('Gerei ',len(list_of_sons),' filhos a partir do melhor candidato!')

    return list_of_sons


def isFinalState(parent):
    global smallerSoFar
    number_of_pegs = calculateNumberOfPegs(parent)

    if (number_of_pegs == 1):
        return True
    else:
        print('A quantidade de peças no tabuleiro é: ', number_of_pegs)
        if (number_of_pegs < smallerSoFar):
            #print(parent)
            smallerSoFar = number_of_pegs
        print('O menor número de peças até agora é: ', smallerSoFar)

        return False


def calculateIdentifier(candidate):
    idString = ["","","","","","","",""]
    id = []

    oppositRow = len(candidate) - 1
    for row in range(0, len(candidate)):
        oppositeCol = len(candidate[0]) - 1

        for col in range(0, len(candidate[0])):
            #VARREDURA HORIZONTAL
            idString[0] += str(abs(candidate[row, col]))                #direção: diagonal pra baixo à direita
            idString[1] += str(abs(candidate[row, oppositeCol]))        #direção: diagonal pra baixo à esquerda

            idString[2] += str(abs(candidate[oppositRow, col]))         #direção: diagonal pra cima à direita
            idString[3] += str(abs(candidate[oppositRow, oppositeCol])) #direção: diagonal pra cima à esquerda

            #VARREDURA VERTICAL
            idString[4] += str(abs(candidate[col, row]))                #direção: diagonal pra baixo à direita
            idString[5] += str(abs(candidate[oppositeCol, row]))        #direção: diagonal pra baixo à esquerda

            idString[6] += str(abs(candidate[col, oppositRow]))         #direção: diagonal pra cima à direita
            idString[7] += str(abs(candidate[oppositeCol, oppositRow])) #direção: diagonal pra cima à esquerda

            oppositeCol = oppositeCol - 1
        oppositRow = oppositRow - 1

    #transforma cada string em binario, depois transforma pra decimal, e finalmente adiciona
    for string in idString:
        id.append(int(string, 2))

    identifier = min(id)

    return identifier


"""
DESCRIÇÃO: O método a seguir evita recalcular a avaliação de um estado, ao verificar se existe um estado equivalente em um
dicionário - que armazena {identificador(de estados equivalentes),avaliação}
"""
def searchTheIndexOfTheBestCandidate(candidates):
    evaluations_array = []
    heapq.heapify(evaluations_array)
    global idsDictionary

    for index_candidate in range (0, len(candidates)):

        candidate = candidates[index_candidate]

        id = calculateIdentifier(candidate)

        if id in idsDictionary:
            eval = idsDictionary[id]
        else:
            eval = evaluate(candidate)
            idsDictionary[id] = eval

        heapq.heappush(evaluations_array, (eval, index_candidate))


    print('A quantidade total de candidatos é: ', len(evaluations_array))
    best_eval,index_of_best = heapq.heappop(evaluations_array)

    print('A nota do melhor candidato é: ', round(best_eval, 2))
    print(candidates[index_of_best])

    return index_of_best

# class Tree:
#     def __init__(self, state):
#         self.parent = None
#         self.state = state
#         self.movement = None
#
#     def createSon(self, parent, state, movement=""):
#         self.parent = parent
#         self.state = state
#         self.movement = movement
#
#     def show(self, state):
#         if self.parent is not None:
#             print(state)
#             self.show(self.parent)

class Node:
   def __init__(self, state):
      self.state = state
      self.best_son = None
      self.parent = None


class doubly_linked_list:

   def __init__(self):
      self.head = None


   def push(self, NewVal):
      NewNode = Node(NewVal)
      NewNode.best_son = self.head
      if self.head is not None:
         self.head.parent = NewNode
      self.head = NewNode

# Print the Doubly Linked list
   def listprint(self, node):
      while (node is not None):
         print("\n")
         print(node.state),
         last = node
         node = node.best_son

def findSolutionPath(state, visited):
    if state in visited:
        print()



def aStar(state):
    linked_list = doubly_linked_list()
    candidates = [state]
    visited = []
    solutionNotFound = True

    while len(candidates) > 0:  # Percorre a lista de candidatos enquanto houver candidatos

        print("Já conheço ", len(idsDictionary), " estados equivalentes")

        parentIndex = searchTheIndexOfTheBestCandidate(candidates)
        parent = candidates[parentIndex]
        linked_list.push(parent)

        if(isFinalState(parent)):
            visited.append(parent)
            candidates.pop(parentIndex)
            solutionNotFound = False
            theEnd = time.time()
            print("TEMPO DE EXECUÇÃO: ",round(theEnd - start, 3), "segundos")
            print('Sucesso! Encontrei a solução!')
            print("Aqui está:")
            print(parent)
            #winsound.Beep(420, 4000)
            #findSolutionPath(parent, visited)
            linked_list.listprint(linked_list.head)

            # for x in range(0,3):
            #     os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 440))
            # os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 440))
            break
        else:
            print('Essa ainda não é a solução...')

        list_of_sons = generateSons(parent)

        if(len(list_of_sons)==0):
            visited.append(parent)
            print("Já visitei: ", len(visited), " estados")
            # print("O último visitado era um estéril!")
            print("\n")
            candidates.pop(parentIndex)
        else:
            visited.append(parent)
            print("Já visitei: ", len(visited), " estados")
            candidates.pop(parentIndex)
            for son in list_of_sons:
                candidates.append(son)
            print("\n")


"""
DESCRIÇÃO: Este método é responsável por substituir as posições vazias por -1.
"""
def cleanEmptyPositions(inicial_state_received):
    treated_inicial_state = numpy.where(inicial_state_received == 0, -1, inicial_state_received)
    treated_inicial_state[3][3] = 0
    return treated_inicial_state


"""
DESCRIÇÃO: Este método é responsável por executar o programa.
"""
if __name__ == '__main__':
    start = time.time()

    #DIFICULDADE: SUPERHARD -------------------------------------------------
    inicial_state_received = numpy.array([[0, 0, 1, 1, 1, 0, 0],
                                          [0, 0, 1, 1, 1, 0, 0],
                                          [1, 1, 1, 1, 1, 1, 1],
                                          [1, 1, 1, 0, 1, 1, 1],
                                          [1, 1, 1, 1, 1, 1, 1],
                                          [0, 0, 1, 1, 1, 0, 0],
                                          [0, 0, 1, 1, 1, 0, 0]])

    treated_inicial_state = cleanEmptyPositions(inicial_state_received)
    aStar(treated_inicial_state)

    # DIFICULDADE: DIFÍCIL -------------------------------------------------
    # treated_inicial_state = numpy.array([[-1, -1, 0, 1, 0, -1, -1],
    #                                        [-1, -1, 1, 1, 1, -1, -1],
    #                                        [ 0,  1, 1, 1, 1,  1,  0],
    #                                        [ 1,  1, 1, 1, 1,  1,  1],
    #                                        [ 0,  1, 1, 1, 1,  1,  0],
    #                                        [-1, -1, 1, 1, 1, -1, -1],
    #                                        [-1, -1, 0, 1, 0, -1, -1]])
    #
    #
    # aStar(treated_inicial_state)

    # DIFICULDADE: MODERADA  ------------------------------------------------
    # treated_inicial_state = numpy.array([[-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 1, 0, -1, -1],
    #                                        [ 0,  0, 1, 1, 1,  0,  0],
    #                                        [ 0,  1, 1, 1, 1,  1,  0],
    #                                        [ 1,  1, 1, 1, 1,  1,  1],
    #                                        [-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 0, 0, -1, -1]])
    #
    #
    # aStar(treated_inicial_state)

    # DIFICULDADE: FÁCIL ------------------------------------------------
    # treated_inicial_state = numpy.array([[-1, -1, 1, 1, 1, -1, -1],
    #                                        [-1, -1, 1, 1, 1, -1, -1],
    #                                        [ 0,  0, 1, 1, 1,  0,  0],
    #                                        [ 0,  0, 1, 0, 1,  0,  0],
    #                                        [ 0,  0, 0, 0, 0,  0,  0],
    #                                        [-1, -1, 0, 0, 0, -1, -1],
    #                                        [-1, -1, 0, 0, 0, -1, -1]])
    # aStar(treated_inicial_state)

    # DIFICULDADE: SUPEREASY ----------------------------------------------------
    # treated_inicial_state = numpy.array([[-1, -1, 0, 0, 0, -1, -1],
    #                                      [-1, -1, 0, 1, 0, -1, -1],
    #                                      [ 0,  0, 1, 1, 1,  0,  0],
    #                                      [ 0,  0, 0, 1, 0,  0,  0],
    #                                      [ 0,  0, 0, 1, 0,  0,  0],
    #                                      [-1, -1, 0, 0, 0, -1, -1],
    #                                      [-1, -1, 0, 0, 0, -1, -1]])
    # aStar(treated_inicial_state)