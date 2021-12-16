from typing import List, Union

import aoc


class Puzzle(aoc.Puzzle):
    EXAMPLE = """---"""
    EXAMPLE_SOLUTION_PART1 = None
    EXAMPLE_SOLUTION_PART2 = None

    def parse_input(self, inp: str) -> List[str]:
        return inp.splitlines()

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        data = self.parse_input(inp)
        return 0

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        data = self.parse_input(inp)
        return 0


if __name__ == '__main__':
    Puzzle().solve()
