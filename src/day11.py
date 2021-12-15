import operator
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
from pprint import pprint
from typing import Dict, FrozenSet, List, Optional, Set, Union

import numpy as np
import numpy.ma as ma

import aoc


@dataclass
class Map:
    map: np.ndarray


def clamp(low: int, x: int, high: int) -> int:
    return max(min(x, high), low)


def print_map(map: np.ndarray):
    print("\n".join([
        "".join([str(x) if x < 10 else "*" for x in row])
        for row in map
    ]))
    print()


def simulate_step(map: np.ndarray) -> int:
    map += 1

    flashed = np.zeros(shape=map.shape, dtype=bool)
    while True:
        flashing = map > 9
        todo = np.where(flashing & ~flashed)
        if not todo[0].size:
            break

        flashed = flashing

        for (y, x) in zip(*todo):
            top = clamp(0, y - 1, 9)
            bottom = clamp(0, y + 1, 9)
            left = clamp(0, x - 1, 9)
            right = clamp(0, x + 1, 9)
            map[top:bottom + 1, left:right + 1] += 1

    flashes = flashed.sum()
    map[flashed] = 0
    return flashes


class Puzzle(aoc.Puzzle):
    DAY = 11
    EXAMPLE = """
        5483143223
        2745854711
        5264556173
        6141336146
        6357385478
        4167524645
        2176841721
        6882881134
        4846848554
        5283751526"""
    EXAMPLE_SOLUTION_PART1 = 1656
    EXAMPLE_SOLUTION_PART2 = 195

    def parse_input(self, inp: str) -> np.ndarray:
        return np.array([list(map(int, line)) for line in inp.split("\n")])

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        map = self.parse_input(inp)

        flashes = 0
        for i in range(100):
            flashes += simulate_step(map)

        return flashes

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        map = self.parse_input(inp)

        for i in range(10000):
            if simulate_step(map) == 100:
                return i + 1

        return -1


if __name__ == '__main__':
    Puzzle().solve()
