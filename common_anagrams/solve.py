from collections import Counter


class Problem(object):
    current_problem_number = 0
    def __init__(self, length, A, B):
        Problem.current_problem_number += 1
        self.number = Problem.current_problem_number
        self.length = int(length)
        self.A = A
        self.B = B
        self.solution = 0

    def solve(self):
        print(f'Solving problem {self.number}')
        A_substrings, B_substrings = self.get_substrings()
        for A_substring in A_substrings:
            if self.has_anagram(A_substring, B_substrings):
                self.solution += 1
        print(self.solution)

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
    def __init__(self, input_file):
        with open(input_file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def get_problems(self):
        for problem in (zip(self.lines[1::3], self.lines[2::3], self.lines[3::3])):
            yield Problem(*problem)

    def get_header(self):
        return self.lines[0]


if __name__ == '__main__':
    loader = Loader('A-small-practice.in')
    for problem in loader.get_problems():
        problem.solve()
