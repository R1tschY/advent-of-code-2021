import re
import textwrap
from dataclasses import dataclass
from itertools import product
from typing import Optional, Union

import aoc


@dataclass
class Target:
    x0: int
    x1: int
    y0: int
    y1: int


def throw(target: Target, v_x: int, v_y: int) -> Optional[int]:
    x, y = 0, 0
    y_max = 0
    while x <= target.x1 and y >= target.y0:
        x += v_x
        y += v_y
        if v_x > 0:
            v_x -= 1
        elif v_x < 0:
            v_x += 1
        v_y -= 1
        y_max = max(y, y_max)
        # print(x, y)

        if target.x0 <= x <= target.x1 and target.y0 <= y <= target.y1:
            return y_max

    return None


class Puzzle(aoc.Puzzle):
    EXAMPLE = "target area: x=20..30, y=-10..-5"
    EXAMPLE_SOLUTION_PART1 = 45
    EXAMPLE_SOLUTION_PART2 = 112

    def parse_input(self, inp: str) -> Target:
        x0, x1, y0, y1 = re.findall(
            r"target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)", inp)[0]
        return Target(int(x0), int(x1), int(y0), int(y1))

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        target = self.parse_input(inp)

        res = 0
        n = max(abs(target.y0), target.x1) + 1
        for x, y in product(range(0, n), range(-n, n)):
            r = throw(target, x, y)
            if r is not None:
                res = max(res, r)

        return res

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        target = self.parse_input(inp)

        res = set()
        n = max(abs(target.y0), target.x1) + 1
        for x, y in product(range(0, n), range(-n, n)):
            r = throw(target, x, y)
            if r is not None:
                res.add((x, y))

        return len(res)


if __name__ == '__main__':
    Puzzle().solve()
