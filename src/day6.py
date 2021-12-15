import re
from dataclasses import dataclass
from functools import lru_cache
from pprint import pprint
from typing import List, Union

import numpy as np

import aoc


@lru_cache(maxsize=None)
def calc(dtt: int) -> int:
    res = 1

    if dtt <= 2:
        return res

    dtt -= 2
    while dtt >= 7:
        dtt -= 7
        res += calc(dtt)

    return res


def calc_list(its: List[int], days: int) -> int:
    return sum(calc((8 - it) + days) for it in its)


@dataclass
class Lanternfish:
    internal_timer: int


class Puzzle(aoc.Puzzle):
    DAY = 6
    EXAMPLE = """3,4,3,1,2"""
    EXAMPLE_SOLUTION_PART1 = 5934
    EXAMPLE_SOLUTION_PART2 = 26984457539

    def parse_input(self, inp: str) -> List[Lanternfish]:
        return [Lanternfish(int(x)) for x in inp.split(",")]

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        fishes = self.parse_input(inp)

        for i in range(80):
            new_fishes = []
            for fish in fishes:
                if fish.internal_timer == 0:
                    fish.internal_timer = 6
                    new_fishes.append(Lanternfish(8))
                else:
                    fish.internal_timer -= 1
            fishes.extend(new_fishes)

        return len(fishes)

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        it = [fish.internal_timer for fish in self.parse_input(inp)]
        return calc_list(it, 256)


if __name__ == '__main__':
    Puzzle().solve()

