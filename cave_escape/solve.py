from copy import deepcopy
from time import sleep


class Raven(object):
    def __init__(self, energy, position):
        self.energy = energy
        self.position = position
    
    def __repr__(self):
        return f'Position: {self.position}, Energy: {self.energy}'


class Position(object):
    def __init__(self, r, c):
        self.r = r
        self.c = c
    
    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def __hash__(self):
        return hash((self.r, self.c))

    def __repr__(self):
        return f'({self.r}, {self.c})'


class Maze(object):
    def __init__(self, maze):
        self.maze = maze
        self.traps = self.get_traps()

    def __getitem__(self, position):
        return self.maze[position.r-1][position.c-1]
    
    def __setitem__(self, position, value):
        self.maze[position.r-1][position.c-1] = value

    def get_traps(self):
        traps = []
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if -10**5 < self.maze[row][col] < 0:
                    traps.append(Position(row + 1, col + 1))
        return traps


class Problem(object):
    solution = -1
    VISITED = -10**6
    
    def __init__(self, number, N, M, E, maze, Sr, Sc, Tr, Tc):
        self.number = number
        self.rows = N
        self.columns = M
        self.energy = E
        self.maze = Maze(maze)
        self.starting_position = Position(Sr, Sc)
        self.target = Position(Tr, Tc)
        self.raven = Raven(E, self.starting_position)

    def show(self, maze=None):
        print(f'Number: {self.number}')
        print(f'Rows: {self.rows} Columns: {self.columns}')
        print(f'Start: {self.starting_position}')
        print(f'Target: {self.target}')
        print(f'Raven: {self.raven}')
        if maze:
            print(f'{maze.maze}')

    def solve(self):
        if self.raven.energy < 0:
            return -1
        # self.show(self.maze)
        # print('Target',self.maze[self.target])
        self.visit_neutral(self.raven.position)
        # self.show(self.maze)
        if self.is_exit_reachable():
            return self.raven.energy
        # print('Reachable traps', self.get_reachable_traps())
        for trap in self.get_reachable_traps():
            problem = deepcopy(self)
            problem.visit_trap(trap)
            solution = problem.solve()
            if solution > self.solution:
                self.solution = solution
        return self.solution

    def is_exit_reachable(self):
        return self.maze[self.target] == Problem.VISITED 

    def visit_trap(self, position):
        self.raven.energy += self.maze[position]
        self.maze[position] = Problem.VISITED
        self.raven.position = position
        self.maze.traps.remove(position)

    def visit_neutral(self, position):
        if self.maze[position] > 0:
            self.raven.energy += self.maze[position]
        self.maze[position] = Problem.VISITED
        for next_position in self.get_neutral_moves(position):
            self.visit_neutral(next_position)

    def get_neutral_moves(self, position):
        return [p for p in self.get_moves(position) if self.maze[p] >= 0]

    def get_moves(self, position):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        moves = [Position(position.r + dr, position.c + dc) for dr, dc in directions]
        return [move for move in moves if 0 < move.r <= self.rows and 0 < move.c <= self.columns]

    def get_reachable_traps(self):
        traps = []
        for trap in self.maze.traps:
            for position in self.get_moves(trap):
                if self.maze[position] == Problem.VISITED:
                    traps.append(trap)
        return list(set(traps))


class Loader(object):
    problem_number = 0
    def __init__(self, input_file):
        with open(input_file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def get_problems(self):
        current_line_number = 1
        for problem in range(int(self.lines[0])):
            Loader.problem_number += 1
            N, M, E, Sr, Sc, Tr, Tc = [int(n) for n in self.lines[current_line_number].split()]
            current_line_number += 1
            maze = [[int(x) for x in self.lines[i].split()] for i in range(current_line_number, current_line_number + N)]
            current_line_number += N
            yield Problem(Loader.problem_number, N, M, E, maze, Sr, Sc, Tr, Tc)


class Saver(object):
    problem_number = 0
    def __init__(self, output_file):
        self.f = open(output_file, 'w')

    def save(self, solution):
        Saver.problem_number += 1
        self.f.write(f'Case #{Saver.problem_number}: {solution}\n')


if __name__ == '__main__':
    FILENAME = 'C-small-practice'
    loader = Loader(f'{FILENAME}.in')
    saver = Saver(f'{FILENAME}.out')
    for problem in loader.get_problems():
        print(f'Solving problem: {problem.number}')
        solution = problem.solve()
        print(f'Solution: {solution}')
        saver.save(solution)
