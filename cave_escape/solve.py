from time import sleep


class Raven(object):
    def __init__(self, energy, position):
        self.energy = energy
        self.position = position
    
    def __repr__(self):
        return f'Position: {self.position}, Energy: {self.energy}'


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'({self.x}, {self.y})'


class Maze(object):
    def __init__(self, maze):
        self.maze = maze

    def __getitem__(self, position):
        return self.maze[position.x-1][position.y-1]
    
    def get_copy(self):
        return self.maze.deepcopy()


class Problem(object):
    solution = 0
    
    def __init__(self, number, N, M, E, maze, Sr, Sc, Tr, Tc):
        self.number = number
        self.rows = N
        self.columns = M
        self.energy = E
        self.maze = Maze(maze)
        self.starting_position = Position(Sr, Sc)
        self.target = Position(Tr, Tc)
        self.raven = Raven(E, self.starting_position)

    def show(self):
        print(f'Number: {self.number}')
        print(f'Rows: {self.rows} Columns: {self.columns}')
        print(f'Start: {self.starting_position}')
        print(f'Target: {self.target}')
        print(f'Raven: {self.raven}')

    def solve(self):
        self.show()
        # self.flood()
        for trap in self.get_proximate_traps():
            maze = self.maze.get_copy()
        return self.solution

    def get_proximate_traps(self):
        return []


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
    FILENAME = 'A-small-practice'
    loader = Loader(f'{FILENAME}.in')
    saver = Saver(f'{FILENAME}.out')
    for problem in loader.get_problems():
        print(f'Solving problem: {problem.number}')
        solution = problem.solve()
        print(f'Solution: {solution}')
        saver.save(solution)
