import heapq

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.maze[row][col] != '#'

    def heuristic(self, current, goal):
        # Manhatten distance heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def solve(self, start, goal):
        pq = [(0, start)]
        came_from = {}
        cost_so_far = {start: 0}

        while pq:
            current_cost, current = heapq.heappop(pq)

            if current == goal:
                break

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = current[0] + dr, current[1] + dc

                if self.is_valid(new_row, new_col):
                    new_cost = cost_so_far[current] + 1
                    if (new_row, new_col) not in cost_so_far or new_cost < cost_so_far[(new_row, new_col)]:
                        cost_so_far[(new_row, new_col)] = new_cost
                        priority = new_cost + self.heuristic((new_row, new_col), goal)
                        heapq.heappush(pq, (priority, (new_row, new_col)))
                        came_from[(new_row, new_col)] = current

        # Reconstruct the path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()

        return path

def print_maze(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in path:
                print('P', end=' ')
            else:
                print(maze[i][j], end=' ')
        print()

maze = [
    "S#######",
    "#......#",
    "#.#####.#",
    "#.#...#.#",
    "#.#.#.#.#",
    "#...#...#",
    "#.#.#.#G#",
    "#######E"
]

start = (0, 1)
goal = (6, 7)

solver = MazeSolver(maze)
solution = solver.solve(start, goal)
print_maze(maze, solution)
