import re
import textwrap
from dataclasses import dataclass
from itertools import product
from pprint import pprint
from typing import List, Optional, Tuple, Union

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
    while x <= target.x1 + 50 and y >= target.y1 - 50:
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
        n = 200
        for x, y in product(range(0, n), range(-n, n)):
            r = throw(target, x, y)
            if r is not None:
                res = max(res, r)

        return res

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        target = self.parse_input(inp)

        res = set()
        n = 1000
        for x, y in product(range(0, n), range(-n, n)):
            r = throw(target, x, y)
            if r is not None:
                res.add((x, y))

        x = textwrap.dedent("""
        23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7
        """).strip().split()
        x = set(x)
        r = {f"{x},{y}" for x, y in res}
        print("missing", x - r)
        print("!missing", r - x)
        return len(res)


if __name__ == '__main__':
    Puzzle().solve()
