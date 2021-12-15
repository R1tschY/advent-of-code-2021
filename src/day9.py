import operator
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
from pprint import pprint
from typing import Dict, FrozenSet, List, Set, Union

import numpy as np
import numpy.ma as ma

import aoc


@dataclass
class Pos:
    x: int
    y: int


@dataclass
class Map:
    m: np.ndarray

    def low_points(self) -> List[Pos]:
        w, h = self.m.shape

        res = []

        for ix, iy in np.ndindex(self.m.shape):
            left = (ix - 1, iy)
            up = (ix, iy + 1)
            down = (ix, iy - 1)
            right = (ix + 1, iy)
            value = self.m[ix][iy]

            if all(
                self.m[x][y] > value
                for (x, y) in (left, up, down, right)
                if 0 <= x < w and 0 <= y < h
            ):
                res.append(Pos(ix, iy))

        return res

    def fload_fill(self, pos: Pos, filter: np.ndarray, out: np.ndarray):
        w, h = self.m.shape
        poses = [pos]
        next = []

        assert filter[pos.x][pos.y]
        assert self.m.shape == out.shape
        assert self.m.shape == filter.shape
        out[pos.x][pos.y] = True

        while poses:
            for p in poses:
                left = (p.x - 1, p.y)
                up = (p.x, p.y + 1)
                down = (p.x, p.y - 1)
                right = (p.x + 1, p.y)

                for (x, y) in (left, up, down, right):
                    if 0 <= x < w and 0 <= y < h and filter[x][y] and not out[x][y]:
                        out[x][y] = True
                        next.append(Pos(x, y))

            poses = next
            next = []


class Puzzle(aoc.Puzzle):
    DAY = 9
    EXAMPLE = """
        2199943210
        3987894921
        9856789892
        8767896789
        9899965678"""
    EXAMPLE_SOLUTION_PART1 = 15
    EXAMPLE_SOLUTION_PART2 = 1134

    def parse_input(self, inp: str) -> Map:
        return Map(np.array([
            [int(cell) for cell in row]
            for row in inp.split("\n")
        ]))

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        map = self.parse_input(inp)
        return sum(
            map.m[pos.x][pos.y] + 1
            for pos in map.low_points()
        )

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        map = self.parse_input(inp)

        basins = []
        filter = map.m < 9
        for pos in map.low_points():
            mask = np.zeros(shape=map.m.shape, dtype=bool)
            map.fload_fill(pos, filter, out=mask)
            basins.append(int(np.sum(mask)))

        basins.sort()
        return reduce(operator.mul, basins[-3:])


if __name__ == '__main__':
    Puzzle().solve()
