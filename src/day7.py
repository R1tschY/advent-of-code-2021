from typing import List, Union

import aoc


class Puzzle(aoc.Puzzle):
    DAY = 7
    EXAMPLE = """16,1,2,0,4,2,7,1,2,14"""
    EXAMPLE_SOLUTION_PART1 = 37
    EXAMPLE_SOLUTION_PART2 = 168

    def parse_input(self, inp: str) -> List[int]:
        return [int(x) for x in inp.split(",")]

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        poses = self.parse_input(inp)
        min_pos = min(poses)
        max_pos = max(poses)

        return min([
            sum([abs(pos - x) for pos in poses])
            for x in range(min_pos, max_pos + 1)
        ])

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        poses = self.parse_input(inp)
        min_pos = min(poses)
        max_pos = max(poses)

        return min([
            sum([sum(range(abs(pos - x) + 1)) for pos in poses])
            for x in range(min_pos, max_pos + 1)
        ])


if __name__ == '__main__':
    Puzzle().solve()

