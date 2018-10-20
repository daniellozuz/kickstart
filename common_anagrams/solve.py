from collections import Counter


class Problem(object):
    def __init__(self, number, length, A, B):
        self.number = number
        self.length = int(length)
        self.A = A
        self.B = B
        self.solution = 0

    def solve(self):
        A_substrings, B_substrings = self.get_substrings()
        for A_substring in A_substrings:
            if self.has_anagram(A_substring, B_substrings):
                self.solution += 1
        return self.solution

    def get_substrings(self):
        A_substrings, B_substrings = [], []
        for substring_length in range(1, self.length + 1):
            for first in range(self.length - substring_length + 1):
                A_substrings.append(self.A[first:first+substring_length])
                B_substrings.append(self.B[first:first+substring_length])
        return A_substrings, B_substrings

    def has_anagram(self, string, substrings):
        for substring in substrings:
            if len(substring) == len(string):
                if Counter(string) == Counter(substring):
                    return True
        return False


class Loader(object):
    problem_number = 0
    def __init__(self, input_file):
        with open(input_file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def get_problems(self):
        for problem_data in (zip(self.lines[1::3], self.lines[2::3], self.lines[3::3])):
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
    FILENAME = 'A-small-practice'
    loader = Loader(f'{FILENAME}.in')
    saver = Saver(f'{FILENAME}.out')
    for problem in loader.get_problems():
        print(f'Solving problem: {problem.number}')
        solution = problem.solve()
        print(f'Solution: {solution}')
        saver.save(solution)
