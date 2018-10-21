from time import sleep


class Problem(object):
    def __init__(self, number, N, Q, Ls, Rs, Ks):
        self.number = number
        self.N = N
        self.Q = Q
        self.Ls = Ls
        self.Rs = Rs
        self.Ks = Ks
        self.solution = 0

    def show(self):
        print(f'Number: {self.number}')
        print(f'N: {self.N} Q: {self.Q}')
        print(f'Ls: {self.Ls}')
        print(f'Rs: {self.Rs}')
        print(f'Ks: {self.Ks}')

    def solve(self):
        saved_Rs = self.Rs.copy()
        saved_Ls = self.Ls.copy()
        self.show()
        for i, K in enumerate(self.Ks):
            removed = 0
            self.Rs = saved_Rs.copy()
            self.Ls = saved_Ls.copy()
            while removed < K and self.Rs:
                m = max(self.Rs)
                print(m)
                max_indeces = [i for i, j in enumerate(self.Rs) if j == m]
                try:
                    second_m = max([R for i, R in enumerate(self.Rs) if i not in max_indeces])
                except ValueError:
                    second_m = 0
                print(second_m)
                second_max_indeces = [i for i, j in enumerate(self.Rs) if j == second_m]
                print(max_indeces)
                max_lowest = max([self.Ls[i] for i in max_indeces])
                print(max_lowest)
                max_lowest_indeces = [i for i in max_indeces if self.Ls[i] == max_lowest]
                # print(Ls[max_lowest_indeces])
                bottom = max(max_lowest, second_m)
                diff = m - bottom
                if len(max_indeces) * diff >= K - removed:
                    diff = 1
                print('Diff:', diff)
                indeces_to_decrease = max_indeces
                for i in indeces_to_decrease:
                    self.Rs[i] -= diff
                    removed += diff
                for i in reversed(range(len(self.Rs))):
                    if self.Rs[i] == self.Ls[i]:
                        self.Rs.pop(i)
                        self.Ls.pop(i)
                        removed += 1
                print('Removed', removed)
                self.show()       
            try:
                self.solution += max(self.Rs) * (i + 1)
            except ValueError:
                self.solution += 0
            print('Partial solution', self.solution)
            # sleep(5)
        return self.solution


class Loader(object):
    problem_number = 0
    def __init__(self, input_file):
        with open(input_file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def get_problems(self):
        for problem_data in (zip(self.lines[1::4], self.lines[2::4], self.lines[3::4], self.lines[4::4])):
            Loader.problem_number += 1
            N, Q = [int(n) for n in problem_data[0].split()]
            X1, X2, A1, B1, C1, M1 = [int(n) for n in problem_data[1].split()]
            Y1, Y2, A2, B2, C2, M2 = [int(n) for n in problem_data[2].split()]
            Z1, Z2, A3, B3, C3, M3 = [int(n) for n in problem_data[3].split()]
            Xs = [X1, X2]
            Ys = [Y1, Y2]
            Zs = [Z1, Z2]
            for i in range(3, N + 1):
                Xs.append((A1 * Xs[i-2] + B1 * Xs[i-3] + C1) % M1)
                Ys.append((A2 * Ys[i-2] + B2 * Ys[i-3] + C2) % M2)
                Zs.append((A3 * Zs[i-2] + B3 * Zs[i-3] + C3) % M3)
            Ls = []
            Rs = []
            Ks = []
            for i in range(1, N + 1):
                Ls.append(min(Xs[i-1], Ys[i-1]) + 1)
                Rs.append(max(Xs[i-1], Ys[i-1]) + 1)
            for i in range(1, Q + 1):
                Ks.append(Zs[i-1] + 1)
            yield Problem(Loader.problem_number, N, Q, Ls, Rs, Ks)

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
