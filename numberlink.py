import time
import sys
import search
from search import *
from copy import deepcopy




class State:

  def __init__(self, array, letra_conectando, cuantas_conectadas, pos_actual,
               last_pos):
    self.array = array  # matriz con el juego
    self.letra_conectando = letra_conectando  # cual se está buscando
    self.cuantas_conectadas = cuantas_conectadas  # cuantas conectadas
    if pos_actual == [-1, -1]:
      self.pos_actual = self.findFirst(letra_conectando, array)
    else:
      self.pos_actual = pos_actual
    if last_pos == [-1, -1]:
      self.last_pos = self.findLast(letra_conectando, array)
    else:
      self.last_pos = last_pos

  def __eq__(self, other):
    return (self.array == other.array
            and self.currentletter == other.currentletter)

  def __hash__(self):
    return hash(self.__str__() + self.currentletter)

  def __str__(self):
    string = ""
    for l in self.array:
      for c in l:
        string += c
      string += "\n"
    return string

  def findFirst(self, letter, array):  #primer ocurrencia de la letra en la mat
    i = 0
    j = 0
    while i < len(array):
      j = 0
      while j < len(array[i]):
        if array[i][j] == letter:
          return [i, j]
        j += 1
      i += 1
    return [-1, -1]

  def findLast(self, letter,
               array):  #ultima ocurrencia de una letra en la matriz
    i = 0
    j = 0
    buf = [-1, -1]
    while i < len(array):
      j = 0
      while j < len(array[i]):
        if array[i][j] == letter:
          buf = [i, j]
        j += 1
      i += 1
    return buf


class NumberLink(Problem):  # heredando de la clase problem de la libreria

  def __init__(self, initial):
    array = []
    with open(initial, "r") as file:
      for line in file:
        strippedLine = line.rstrip('\n')
        listedLine = list(strippedLine)
        array.append(listedLine)
    self.initial = State(
        array, 'A', 0, [-1, -1],
        [-1, -1])  # se inicializa todo en ceros, el primer State
    self.goal = self.cuantas_letras(
        array)  # contando cuantas letras diferentes hay

  def cuantas_letras(self, array):
    output = []
    for d in array:
      for n in d:
        if n not in output:
          output.append(n)
    return len(output) - 1

  def goal_test(
      self, state
  ):  # función objetivo: que la cantidad de letras conectadas del State sea el total de letras dif
    return state.cuantas_conectadas == self.goal

  def actions(self,
              state):  # acciones posibles desde un State a cualquier otro
    pos = state.pos_actual  # tomando la posición actual (fil, col actual)
    posibles_acciones = ['DOWN', 'UP', 'LEFT',
                         'RIGHT']  # y la serie de posibles acciones
    col_length = len(state.array)
    row_length = len(state.array[0])

    if pathExists(state.array, state.pos_actual, state.last_pos) == False:
      posibles_acciones = []  # no hay ruta valida hacia la ultima posición
      return posibles_acciones  # asi no exploramos soluciones invalidas

    # validamos los bordes para quitar las posibles opciones de mov. hacia otros estados
    if pos[0] == col_length - 1:
      posibles_acciones.remove('DOWN')
    if pos[0] == 0:
      posibles_acciones.remove('UP')
    if pos[1] == 0:
      posibles_acciones.remove('LEFT')
    if pos[1] == row_length - 1:
      posibles_acciones.remove('RIGHT')
    if verificarLimites(
        state.array, [pos[0] + 1, pos[1]]) == True and state.array[pos[0] + 1][
            pos[1]] != '.' and [pos[0] + 1, pos[1]] != state.last_pos:
      posibles_acciones.remove('DOWN')

    if verificarLimites(
        state.array, [pos[0] - 1, pos[1]]) == True and state.array[pos[0] - 1][
            pos[1]] != '.' and [pos[0] - 1, pos[1]] != state.last_pos:
      posibles_acciones.remove('UP')

    if verificarLimites(
        state.array, [pos[0], pos[1] - 1]) == True and state.array[pos[0]][
            pos[1] - 1] != '.' and [pos[0], pos[1] - 1] != state.last_pos:
      posibles_acciones.remove('LEFT')

    if verificarLimites(
        state.array, [pos[0], pos[1] + 1]) == True and state.array[pos[0]][
            pos[1] + 1] != '.' and [pos[0], pos[1] + 1] != state.last_pos:
      posibles_acciones.remove('RIGHT')

    pos_checkeando = [0, 0]

    for direction in directions:  # verificamos si hay ruta hacia cualquier estado en las direcciones
      if direction == [1, 0]:  # ver si hay ruta hacia abajo
        direccion = 'DOWN'
      if direction == [-1, 0]:  # ver si hay ruta hacia arriba
        direccion = 'UP'
      if direction == [0, -1]:
        direccion = 'LEFT'
      if direction == [0, 1]:
        direccion = 'RIGHT'

      pos_checkeando[0] = state.pos_actual[0] + direction[
          0]  # la posición en la que nos moveremos
      pos_checkeando[1] = state.pos_actual[1] + direction[
          1]  # en ambas coordenadas

      if verificarLimites(state.array, [
          pos_checkeando[0], pos_checkeando[1]
      ]) == True and [pos_checkeando[0], pos_checkeando[1]] == state.last_pos:
        posibles_acciones = []
        posibles_acciones.append(direccion)
        return posibles_acciones

      i = 0
      lado_checkeando = [0, 0]
      for side in directions:  #validando que no hayan dos seguidas
        lado_checkeando[0] = pos_checkeando[0] + side[0]
        lado_checkeando[1] = pos_checkeando[1] + side[1]

        if verificarLimites(state.array, [
            lado_checkeando[0], lado_checkeando[1]
        ]) and state.array[lado_checkeando[0]][lado_checkeando[
            1]] == state.letra_conectando and lado_checkeando != state.last_pos:
          i += 1

        if i == 2 and direccion in posibles_acciones:
          posibles_acciones.remove(direccion)

    return posibles_acciones

  def result_manual(self, state, action):
    nuevo_state = deepcopy(state)

    if action == "DOWN":
      nuevo_state.array[state.pos_actual[0] +
                      1][state.pos_actual[1]] = state.letra_conectando
      nuevo_state.pos_actual[0] = state.pos_actual[0] + 1

    if nuevo_state.pos_actual == state.last_pos:
      return State(nuevo_state.array, chr(ord(state.letra_conectando) + 1),
                   state.cuantas_conectadas + 1, [-1, -1], [-1, -1])
    else:
      return State(nuevo_state.array, state.letra_conectando,
                   state.cuantas_conectadas, nuevo_state.pos_actual,
                   state.last_pos)

  def result(
      self, state, action
  ):  # creando los nuevos estados para poder usar la libreria de arboles y la busqueda
    nuevo_state = deepcopy(state)  # copiando por valor

    if action == "DOWN":
      nuevo_state.array[state.pos_actual[0] +
                      1][state.pos_actual[1]] = state.letra_conectando
      nuevo_state.pos_actual[0] = state.pos_actual[0] + 1
    if action == "UP":
      nuevo_state.array[state.pos_actual[0] -
                      1][state.pos_actual[1]] = state.letra_conectando
      nuevo_state.pos_actual[0] = state.pos_actual[0] - 1
    if action == "LEFT":
      nuevo_state.array[state.pos_actual[0]][state.pos_actual[1] -
                                           1] = state.letra_conectando
      nuevo_state.pos_actual[1] = state.pos_actual[1] - 1
    if action == "RIGHT":
      nuevo_state.array[state.pos_actual[0]][state.pos_actual[1] +
                                           1] = state.letra_conectando
      nuevo_state.pos_actual[1] = state.pos_actual[1] + 1
    if nuevo_state.pos_actual == state.last_pos:  # si se conectó
      return State(nuevo_state.array, chr(ord(state.letra_conectando) + 1),
                   state.cuantas_conectadas + 1, [-1, -1], [-1, -1])
    else:
      return State(nuevo_state.array, state.letra_conectando,
                   state.cuantas_conectadas, nuevo_state.pos_actual,
                   state.last_pos)


directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]


def pathExists(array, start, end):
  visited = [[0 for j in range(0, len(array[0]))]
             for i in range(0, len(array))]
  ok = pathExistsDFS(array, start, end, visited)
  return ok


def pathExistsDFS(array, start, end, visited):
  for d in directions:
    i = start[0] + d[0]
    j = start[1] + d[1]
    next = [i, j]
    if i == end[0] and j == end[1]:
      return True
    if verificarLimites(array,
                        next) and array[i][j] == '.' and not visited[i][j]:
      visited[i][j] = 1
      exists = pathExistsDFS(array, next, end, visited)
      if exists:
        return True
  return False


def verificarLimites(array, pos):
  return 0 <= pos[0] and pos[0] < len(array) and 0 <= pos[1] and pos[1] < len(
      array[0])


problem = NumberLink(sys.argv[1])
solution = search.breadth_first_tree_search(problem)

for n in solution.path():
  print(n.state)


def play_game(file_path):
  problem = NumberLink(file_path)
  solution = search.breadth_first_tree_search(problem)

  print("solución:")
  for n in solution.path():
    print(n.state)


def play_game_manual(file_path):
  problem = NumberLink(file_path)
  current_state = problem.initial

  while not problem.goal_test(current_state):
    print("Estado actual:")
    print(current_state)

    print("Posibles acciones:")
    print(problem.actions(current_state))

    action = input(
        "Ingrese su movimiento (UP, DOWN, LEFT, RIGHT, X para salir): ")
    if action.upper() == 'X':
      #print("Game Over!")
      break

    if action in problem.actions(current_state):
      current_state = problem.result_manual(current_state, action)
    else:
      print("Invalid move. Please try again.")

  print("solucion:")
  print(current_state)


def main_menu():
  while True:
    print("\n=== Numberlink ===")
    print("1. Jugar Maquina")
    print("2. Exit")
    print("3. Manual")

    choice = input("Opcion: ")

    if choice == "1":
      file_path = input("Path (file.in): ")
      play_game(file_path)
    elif choice == "2":
      print("Adios!")
      break
    elif choice == "3":
      print("Escogiste manual!")
      file_path = input("Path (file.in): ")
      play_game_manual(file_path)
    else:
      print("Opcion invalida.")


if __name__ == "__main__":
  main_menu()
