from itertools import combinations


class Problem(object):
    def __init__(self, number, amount, numbers):
        self.number = number
        self.amount = int(amount)
        self.numbers = [int(n) for n in numbers.split()] 
        self.solution = 0

    def solve(self):
        triplets = self.get_triplets()
        for triplet in triplets:
            if self.is_ok(triplet):
                self.solution += 1
        return self.solution

    def get_triplets(self):
        triplets = []
        for indeces in combinations(range(len(self.numbers)), 3):
            triplet = (self.numbers[indeces[0]], self.numbers[indeces[1]], self.numbers[indeces[2]])
            triplets.append(triplet)
        return triplets

    def is_ok(self, triplet):
        condition1 = triplet[0] == triplet[1] * triplet[2]
        condition2 = triplet[1] == triplet[0] * triplet[2]
        condition3 = triplet[2] == triplet[0] * triplet[1]
        return condition1 or condition2 or condition3


class Loader(object):
    problem_number = 0
    def __init__(self, input_file):
        with open(input_file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def get_problems(self):
        for problem_data in (zip(self.lines[1::2], self.lines[2::2])):
            Loader.problem_number += 1
            yield Problem(Loader.problem_number, *problem_data)

    def get_header(self):
        return self.lines[0]


class Saver(object):
    problem_number = 0
    def __init__(self, output_file):
        self.f = open(output_file, 'w')

    def save(self, solution):
        Saver.problem_number += 1
        self.f.write(f'Case #{Saver.problem_number}: {solution}\n')

if __name__ == '__main__':
    FILENAME = 'A-large'
    loader = Loader(f'{FILENAME}.in')
    saver = Saver(f'{FILENAME}.out')
    for problem in loader.get_problems():
        print(f'Solving problem: {problem.number}')
        solution = problem.solve()
        print(f'Solution: {solution}')
        saver.save(solution)
