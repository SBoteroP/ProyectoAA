import time
import sys
import search
from search import *
from copy import deepcopy
from search import astar_search

import heapq


class State:

    def __init__(self, array, curr_letter, curr_ok, curr_pos, last_pos):
        self.array = array
        self.curr_letter = curr_letter
        self.curr_ok = curr_ok
        if curr_pos == [-1, -1]:
            self.curr_pos = self.findFirst(curr_letter, array)
        else:
            self.curr_pos = curr_pos
        if last_pos == [-1, -1]:
            self.last_pos = self.findLast(curr_letter, array)
        else:
            self.last_pos = last_pos

    def __eq__(self, other):
        return (self.array == other.array
                and self.currentletter == other.currentletter)

    def __hash__(self):
        return hash(self.__str__() + self.curr_letter)

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
        self.tic = time.perf_counter()
        self.initial = State(array, 'A', 0, [-1, -1], [-1, -1])
        self.goal = self.lasty(array)

    def lasty(self, array):
        output = []
        for d in array:
            for n in d:
                if n not in output:
                    output.append(n)
        return len(output) - 1

    def goal_test(self, state):
        return state.curr_ok == self.goal

    def actions(self, state):
        position = state.curr_pos
        possible_actions = ['DOWN', 'UP', 'LEFT', 'RIGHT']
        column_length = len(state.array)
        row_length = len(state.array[0])

        if pathExists(state.array, state.curr_pos, state.last_pos) == False:
            possible_actions = []
            return possible_actions

        if position[0] == column_length - 1:
            possible_actions.remove('DOWN')
        if position[0] == 0:
            possible_actions.remove('UP')
        if position[1] == 0:
            possible_actions.remove('LEFT')
        if position[1] == row_length - 1:
            possible_actions.remove('RIGHT')
        if inBounds(state.array, [
            position[0] + 1, position[1]
        ]) == True and state.array[position[0] + 1][position[1]] != '.' and [
            position[0] + 1, position[1]
        ] != state.last_pos:
            possible_actions.remove('DOWN')

        if inBounds(state.array, [
            position[0] - 1, position[1]
        ]) == True and state.array[position[0] - 1][position[1]] != '.' and [
            position[0] - 1, position[1]
        ] != state.last_pos:
            possible_actions.remove('UP')

        if inBounds(state.array, [
            position[0], position[1] - 1
        ]) == True and state.array[position[0]][position[1] - 1] != '.' and [
            position[0], position[1] - 1
        ] != state.last_pos:
            possible_actions.remove('LEFT')

        if inBounds(state.array, [
            position[0], position[1] + 1
        ]) == True and state.array[position[0]][position[1] + 1] != '.' and [
            position[0], position[1] + 1
        ] != state.last_pos:
            possible_actions.remove('RIGHT')

        pos_being_checked = [0, 0]

        for direction in directions:
            if direction == [1, 0]:
                direction_letters = 'DOWN'
            if direction == [-1, 0]:
                direction_letters = 'UP'
            if direction == [0, -1]:
                direction_letters = 'LEFT'
            if direction == [0, 1]:
                direction_letters = 'RIGHT'

            pos_being_checked[0] = state.curr_pos[0] + direction[0]
            pos_being_checked[1] = state.curr_pos[1] + direction[1]

            if inBounds(state.array,
                        [pos_being_checked[0], pos_being_checked[1]]) == True and [
                            pos_being_checked[0], pos_being_checked[1]
            ] == state.last_pos:
                possible_actions = []
                possible_actions.append(direction_letters)
                return possible_actions

            i = 0
            side_being_checked = [0, 0]
            for side in directions:
                side_being_checked[0] = pos_being_checked[0] + side[0]
                side_being_checked[1] = pos_being_checked[1] + side[1]

                if inBounds(state.array, [
                    side_being_checked[0], side_being_checked[1]
                ]) and state.array[side_being_checked[0]][side_being_checked[
                        1]] == state.curr_letter and side_being_checked != state.last_pos:
                    i += 1

                if i == 2 and direction_letters in possible_actions:
                    possible_actions.remove(direction_letters)

        return possible_actions

    def result_manual(self, state, action):
        new_state = deepcopy(state)

        if action == "DOWN":
            new_state.array[state.curr_pos[0] +
                            1][state.curr_pos[1]] = state.curr_letter
            new_state.curr_pos[0] = state.curr_pos[0] + 1
        # Similar logic for other directions...

        if new_state.curr_pos == state.last_pos:
            return State(new_state.array, chr(ord(state.curr_letter) + 1),
                         state.curr_ok + 1, [-1, -1], [-1, -1])
        else:
            return State(new_state.array, state.curr_letter, state.curr_ok,
                         new_state.curr_pos, state.last_pos)
            
        

    def result(self, state, action):
        new_state = deepcopy(state)

        if action == "DOWN":
            new_state.array[state.curr_pos[0] +
                            1][state.curr_pos[1]] = state.curr_letter
            new_state.curr_pos[0] = state.curr_pos[0] + 1
        if action == "UP":
            new_state.array[state.curr_pos[0] -
                            1][state.curr_pos[1]] = state.curr_letter
            new_state.curr_pos[0] = state.curr_pos[0] - 1
        if action == "LEFT":
            new_state.array[state.curr_pos[0]][state.curr_pos[1] -
                                               1] = state.curr_letter
            new_state.curr_pos[1] = state.curr_pos[1] - 1
        if action == "RIGHT":
            new_state.array[state.curr_pos[0]][state.curr_pos[1] +
                                               1] = state.curr_letter
            new_state.curr_pos[1] = state.curr_pos[1] + 1
        if new_state.curr_pos == state.last_pos:
            return State(new_state.array, chr(ord(state.curr_letter) + 1),
                         state.curr_ok + 1, [-1, -1], [-1, -1])
        else:
            return State(new_state.array, state.curr_letter, state.curr_ok,
                         new_state.curr_pos, state.last_pos)

        #########


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
        if inBounds(array, next) and array[i][j] == '.' and not visited[i][j]:
            visited[i][j] = 1
            exists = pathExistsDFS(array, next, end, visited)
            if exists:
                return True
    return False


def inBounds(array, pos):
    return 0 <= pos[0] and pos[0] < len(array) and 0 <= pos[1] and pos[1] < len(
        array[0])


# problem = NumberLink(sys.argv[1])
# solution = search.breadth_first_tree_search(problem)

# for n in solution.path():
#    print(n.state)

class FlowFreeSolver(Problem):
    def __init__(self, initial_state):
        super().__init__(initial_state)
    
    def goal_test(self, state):
        # Define your goal test logic here
        # This could be checking if all pairs are connected
        return state.curr_ok == self.lasty(state.array)


    def actions(self, state):
        # Define your actions logic here
        # This should return a list of valid actions from the current state
        position = state.curr_pos
        possible_actions = ['DOWN', 'UP', 'LEFT', 'RIGHT']
        column_length = len(state.array)
        row_length = len(state.array[0])

        if pathExists(state.array, state.curr_pos, state.last_pos) == False:
            possible_actions = []
            return possible_actions

        if position[0] == column_length - 1:
            possible_actions.remove('DOWN')
        if position[0] == 0:
            possible_actions.remove('UP')
        if position[1] == 0:
            possible_actions.remove('LEFT')
        if position[1] == row_length - 1:
            possible_actions.remove('RIGHT')
        if inBounds(state.array, [
            position[0] + 1, position[1]
        ]) == True and state.array[position[0] + 1][position[1]] != '.' and [
            position[0] + 1, position[1]
        ] != state.last_pos:
            possible_actions.remove('DOWN')

        # (Continue with similar logic for other directions)

        return possible_actions

    def result(self, state, action):
        # Define your result logic here
        # This should return the new state after applying the action
        new_state = deepcopy(state)

        if action == "DOWN":
            new_state.array[state.curr_pos[0] + 1][state.curr_pos[1]] = state.curr_letter
            new_state.curr_pos[0] = state.curr_pos[0] + 1
        elif action == "UP":
            # (Similar logic for other directions)
            pass

        if new_state.curr_pos == state.last_pos:
            return State(new_state.array, chr(ord(state.curr_letter) + 1),
                         state.curr_ok + 1, [-1, -1], [-1, -1])
        else:
            return State(new_state.array, state.curr_letter, state.curr_ok,
                         new_state.curr_pos, state.last_pos)

    def heuristic(self, state):
        # Define your heuristic logic here
        # This should be the Manhattan distance heuristic
        total_distance = 0
        for letter in state.array:
            if letter != '.':
                start = state.findFirst(letter, state.array)
                goal = state.findLast(letter, state.array)
                total_distance += abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        return total_distance

    def solve(self):
        start_node = Node(self.initial)
        frontier = PriorityQueue()
        frontier.put((self.heuristic(start_node.state), start_node))  # Include a priority when adding the item

        explored = set()

        while not frontier.empty():  # Use empty() to check if the queue is empty
            node = frontier.get()[1]  # Use get() to retrieve and remove the highest priority item and then get the item itself

            if self.goal_test(node.state):
                return node.solution()

            explored.add(node.state)

            for action in self.actions(node.state):
                child_state = self.result(node.state, action)

                if child_state not in explored and child_state not in frontier.queue:  # Use .queue to access the underlying list
                    child_node = Node(
                        child_state, node, action, node.path_cost + 1, self.heuristic(child_state)
                    )
                    frontier.put((child_node.path_cost, child_node))  # Include a priority when adding the item to the queue

        return None


    def solve_flow_free(self):
        solution = self.solve()
        if solution:
            for state in solution:
                print(state)
        else:
            print("No solution found.")


def play_game(file_path, use_astar=False):
    problem = NumberLink(file_path)
    solver = FlowFreeSolver(file_path)
    
    if use_astar:
        solver = FlowFreeSolver(file_path)
        solution = solver.solve_flow_free()
    else:
        solution = search.breadth_first_tree_search(problem)

    for n in solution.path():
        print(n.state)


def play_game_manual(file_path):
    problem = NumberLink(file_path)
    current_state = problem.initial

    while not problem.goal_test(current_state):
        print("Current State:")
        print(current_state)

        print("Possible Actions:")
        print(problem.actions(current_state))

        action = input("Enter your move (UP, DOWN, LEFT, RIGHT, X to exit): ")
        if action.upper() == 'X':
            print("Game Over!")
            break

        if action in problem.actions(current_state):
            current_state = problem.result_manual(current_state, action)
        else:
            print("Invalid move. Please try again.")

    print("Solution:")
    print(current_state)
    print("Game Over!")


# Menú
def main_menu():
    while True:
        print("\n=-=-= Number Link Game =-=-=")
        print("0. Exit")
        print("1. Jugar Exhaustivo")
        print("2. Jugar Heuristico")
        print("3. Manual")

        choice = input("Enter your choice (1, 2, 3, or 4): ")

        if choice == "1":
            file_path = input("Enter the path to the puzzle file: ")
            play_game(file_path)
        elif choice == "0":
            print("¡Adios!")
            break
        elif choice == "3":
            print("You chose Manual!")
            file_path = input("Enter the path to the puzzle file: ")
            play_game_manual(file_path)
        elif choice == "2":
            file_path = input("Enter the path to the puzzle file: ")
            play_game(file_path, use_astar=True)
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main_menu()
