from typing import Union

import aoc


class Puzzle(aoc.Puzzle):
    DAY = 3
    EXAMPLE = """
        00100
        11110
        10110
        10111
        10101
        01111
        00111
        11100
        10000
        11001
        00010
        01010"""
    EXAMPLE_SOLUTION_PART1 = 198
    EXAMPLE_SOLUTION_PART2 = 230

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        numbers = [int(x, 2) for x in inp.split("\n")]
        bits = len(inp.split("\n", 1)[0])

        gamma = 0
        for i in reversed(range(bits)):
            c = 0
            for n in numbers:
                if n & (1 << i):
                    c += 1

            if c > len(numbers) / 2:
                gamma |= 1

            gamma <<= 1
        gamma >>= 1

        epsilon = ~gamma & ((1 << bits) - 1)
        return epsilon * gamma

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        numbers = [int(x, 2) for x in inp.split("\n")]
        bits = len(inp.split("\n", 1)[0])

        init = numbers
        for i in reversed(range(bits)):
            c = ([], [])
            for n in init:
                c[int((n & (1 << i)) != 0)].append(n)

            if len(c[0]) > len(c[1]):
                init = c[0]
            else:
                init = c[1]

            if len(init) == 1:
                oxygen = init[0]
                break

        init = numbers
        for i in reversed(range(bits)):
            c = ([], [])
            for n in init:
                c[int((n & (1 << i)) != 0)].append(n)

            if len(c[0]) > len(c[1]):
                init = c[1]
            else:
                init = c[0]

            if len(init) == 1:
                co2 = init[0]
                break

        return oxygen * co2


if __name__ == '__main__':
    Puzzle().solve()

