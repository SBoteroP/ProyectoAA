#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import sys
import search
from search import *
from copy import deepcopy
import winsound

#Author: Jonathan Miel 16013 et Charles Vandermies 15123

#################
# Problem class #
#################

class State:
    def __init__(self, array, curr_letter, curr_ok, curr_pos, last_pos):
        self.array=array
        self.curr_letter=curr_letter
        self.curr_ok=curr_ok
        if curr_pos == [-1, -1]:
            self.curr_pos = self.findFirst(curr_letter, array)
        else:
            self.curr_pos=curr_pos
        if last_pos == [-1, -1]:
            self.last_pos = self.findLast(curr_letter, array)
        else:
            self.last_pos=last_pos 

    def __eq__(self, other):
        return (self.array == other.array and self.currentletter == other.currentletter)

    def __hash__(self):
        return hash(self.__str__() + self.currentletter)

    def __str__(self):
        string = ""
        for l in self.array:
            for c in l:
                string += c
            string += "\n"
        return string

    def findFirst(self, letter, array):
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

    def findLast(self, letter, array):
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

class NumberLink(Problem):
    def __init__(self, initial):
        array = []
        with open(initial, "r") as file:
            for line in file:
                strippedLine = line.rstrip('\n')
                listedLine = list(strippedLine)       
                array.append(listedLine)
        self.tic= time.perf_counter()
        self.initial = State(array, 'A', 0, [-1, -1], [-1, -1])
        self.goal=self.lasty(array)

    def lasty(self, array):
        output = []
        for d in array:
            for n in d:
                if n not in output:
                    output.append(n)
        return len(output) - 1

    def goal_test(self, state):
        if state.curr_ok == self.goal:
            print("solution trouvée")
            self.toc=time.perf_counter()
            print(f"Temps de calcul: {self.toc - self.tic:0.4f} secondes")
        return state.curr_ok == self.goal
    
    def actions(self, state):
        possible_actions = ['DOWN', 'UP', 'LEFT', 'RIGHT']
        column_length=len(state.array)
        row_length=len(state.array[0])

        if pathExists(state.array, state.curr_pos, state.last_pos) == False:
            possible_actions = []
            return possible_actions

        

        #removing actions only considering an empty state.array

        if state.curr_pos[0]==column_length-1: #if at the last row
            possible_actions.remove('DOWN')
        if state.curr_pos[0]==0: #if at the first row
            possible_actions.remove('UP')
        if state.curr_pos[1]==0: #if at the first column
            possible_actions.remove('LEFT')
        if state.curr_pos[1]==row_length-1: #if at the last column
            possible_actions.remove('RIGHT')

        #removing actions considering letters  
        
        if inBounds(state.array, [state.curr_pos[0]+1,state.curr_pos[1]])==True and state.array[state.curr_pos[0]+1][state.curr_pos[1]] != '.' and [state.curr_pos[0]+1,state.curr_pos[1]] != state.last_pos:
            possible_actions.remove('DOWN')

        if inBounds(state.array, [state.curr_pos[0]-1,state.curr_pos[1]])==True and state.array[state.curr_pos[0]-1][state.curr_pos[1]] != '.' and [state.curr_pos[0]-1,state.curr_pos[1]] != state.last_pos: #si on est toujours dans le bounds, si c'est autre chose qu'un point et si la state.curr_pos est différente que la derenière state.curr_pos (la ou on veut aller pour la lettre courant), alors on enlève la possiiblité d'y aller
            possible_actions.remove('UP')

        if inBounds(state.array, [state.curr_pos[0],state.curr_pos[1]-1])==True and state.array[state.curr_pos[0]][state.curr_pos[1]-1] != '.' and [state.curr_pos[0],state.curr_pos[1]-1] != state.last_pos:
            possible_actions.remove('LEFT')

        if inBounds(state.array, [state.curr_pos[0],state.curr_pos[1]+1])==True and state.array[state.curr_pos[0]][state.curr_pos[1]+1] != '.' and [state.curr_pos[0],state.curr_pos[1]+1] != state.last_pos:
            possible_actions.remove('RIGHT')

        directions=[[1, 0], [-1, 0], [0, -1], [0, 1]]
        pos_being_checked=[0,0]

        for direction in directions: #on check dans chaque direction si il y a des problèmes aux cases adjacentes
            
            if direction == [1, 0]:
                direction_letters='DOWN'
            if direction == [-1, 0]:
                direction_letters='UP'
            if direction == [0, -1]:
                direction_letters='LEFT'
            if direction == [0, 1]:
                direction_letters='RIGHT'

            pos_being_checked[0]=state.curr_pos[0]+direction[0]
            pos_being_checked[1]=state.curr_pos[1]+direction[1]

            if inBounds(state.array, [pos_being_checked[0], pos_being_checked[1]])==True and [pos_being_checked[0], pos_being_checked[1]]== state.last_pos:
                possible_actions = []
                possible_actions.append(direction_letters) #met dans le possible action que la direction qui correspond à la case finale
                return possible_actions

            i=0

            side_being_checked=[0,0]
            for side in directions: #pour chaque direction on regarde autour pour compter le nombre de Lettre en cours de traitement
                
                side_being_checked[0]=pos_being_checked[0]+side[0]
                side_being_checked[1]=pos_being_checked[1]+side[1]
                
                if inBounds(state.array, [side_being_checked[0], side_being_checked[1]]) and state.array[side_being_checked[0]][side_being_checked[1]]==state.curr_letter and side_being_checked != state.last_pos:
                    i+=1

                if i==2 and direction_letters in possible_actions: #si il y a deux lettres adjacente et que la direction n'a pas encore été enlevée
                    possible_actions.remove(direction_letters)

        return possible_actions
    
    def result(self, state, action): #action ne prend que un à la fois
        new_state = deepcopy(state)

        if action == "DOWN":
            new_state.array[state.curr_pos[0]+1][state.curr_pos[1]] = state.curr_letter
            new_state.curr_pos[0]=state.curr_pos[0]+1
        if action == "UP":
            new_state.array[state.curr_pos[0]-1][state.curr_pos[1]] = state.curr_letter
            new_state.curr_pos[0]=state.curr_pos[0]-1
        if action == "LEFT":
            new_state.array[state.curr_pos[0]][state.curr_pos[1]-1] = state.curr_letter
            new_state.curr_pos[1]=state.curr_pos[1]-1        
        if action == "RIGHT":
            new_state.array[state.curr_pos[0]][state.curr_pos[1]+1] = state.curr_letter
            new_state.curr_pos[1]=state.curr_pos[1]+1

            
        # for row in new_state.array:
        #     print(row)
        if new_state.curr_pos == state.last_pos:
            return State(new_state.array, chr(ord(state.curr_letter) + 1), state.curr_ok+1, [-1, -1], [-1, -1])
        else:
            return State(new_state.array, state.curr_letter, state.curr_ok, new_state.curr_pos, state.last_pos)


######################
# Auxiliary function #
######################


def pathExists(array, start, end):
    visited = [ [0 for j in range(0, len(array[0]))] for i in range(0, len(array)) ]
    ok = pathExistsDFS(array, start, end, visited)
    return ok

def pathExistsDFS(array, start, end, visited):
    for d in directions:
        i = start[0] + d[0]
        j = start[1] + d[1]
        next = [i, j]
        if i == end[0] and j == end[1]:
            return True
        if inBounds(array, next) and array[i][j] == '.' and not visited[i][j]:
            visited[i][j] = 1
            exists = pathExistsDFS(array, next, end, visited)
            if exists:
                return True
    return False

def inBounds(array, pos): #renvoie si on est toujours dans le state.array
    return 0 <= pos[0] and pos[0] < len(array) and 0 <= pos[1] and pos[1] < len(array[0])


#####################
# Launch the search #
#####################
tic = time.process_time()
problem = NumberLink(sys.argv[1])
solution = search.breadth_first_tree_search(problem)
for n in solution.path():
    print(n.state)
toc = time.process_time()
print("Le programme s'est exécuté en "+str(toc-tic)+" secondes.")