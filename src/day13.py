import operator
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
from pprint import pprint
from typing import Dict, FrozenSet, List, Optional, Set, Tuple, Union

import numpy as np
import numpy.ma as ma

import aoc


@dataclass
class Input:
    dots: np.ndarray
    folds: List[Tuple[str, int]]


@dataclass
class Pos:
    x: int
    y: int


def fold(map: np.ndarray, dir: str, pos: int) -> np.ndarray:
    if dir == "x":
        left = map[:, :pos]
        right = map[:, pos + 1:]
        for (y, x) in zip(*np.where(right)):
            left[y, -x - 1] = True
        return left

    elif dir == "y":
        top = map[:pos]
        bottom = map[pos + 1:]
        for (y, x) in zip(*np.where(bottom)):
            top[-y - 1, x] = True
        return top


def print_map(map: np.ndarray):
    print("\n".join([
        "".join(["#" if cell else "." for cell in row])
        for row in map
    ]))


class Puzzle(aoc.Puzzle):
    DAY = 13
    EXAMPLE = """
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0
        
        fold along y=7
        fold along x=5
        """
    EXAMPLE_SOLUTION_PART1 = 17
    EXAMPLE_SOLUTION_PART2 = 16

    def parse_input(self, inp: str) -> Input:

        indots, infolds = inp.split("\n\n", 1)
        dots = [Pos(*map(int, d.split(",", 1))) for d in indots.split("\n")]

        folds = []
        for g in re.finditer(r"fold along ([xy])=(\d+)", infolds):
            folds.append((g.group(1), int(g.group(2))))

        m = np.zeros(
            shape=(max([d.y for d in dots]) + 1, max([d.x for d in dots]) + 1),
            dtype=bool)

        for pos in dots:
            m[pos.y, pos.x] = True

        return Input(
            dots=m, folds=folds
        )

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        input = self.parse_input(inp)
        res = fold(input.dots, input.folds[0][0], input.folds[0][1])
        return int(np.sum(res))

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        input = self.parse_input(inp)

        res = input.dots
        for infold in input.folds:
            res = fold(res, infold[0], infold[1])

        print_map(res)
        return int(np.sum(res))


if __name__ == '__main__':
    Puzzle().solve()
