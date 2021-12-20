from dataclasses import dataclass
from typing import List, Union

import numpy as np

import aoc


@dataclass
class Input:
    arr: np.ndarray
    map: np.ndarray


def expand(map: np.ndarray, val: bool) -> np.ndarray:
    h, w = map.shape
    if val:
        res = np.ones((h + 2, w + 2), dtype=map.dtype)
    else:
        res = np.zeros((h + 2, w + 2), dtype=map.dtype)
    res[1:-1, 1:-1] = map
    return res


def arr_to_int(arr: np.ndarray) -> int:
    res = 0
    for bit in arr.flat:
        if bit:
            res = (res << 1) | 1
        else:
            res <<= 1
    return res


def eval(arr: np.ndarray, map: np.ndarray, outer_val: bool) -> np.ndarray:
    map = expand(map, outer_val)
    h, w = map.shape
    res = np.zeros((h, w), dtype=map.dtype)

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            res[y, x] = arr[arr_to_int(map[y - 1:y + 2, x - 1:x + 2])]

    if arr[0]:
        res[0, 0:w] = not outer_val
        res[0:h, 0] = not outer_val
        res[-1, 0:w] = not outer_val
        res[0:h, -1] = not outer_val

    return res


def print_map(map: np.ndarray):
    print("\n".join([
        "".join(["#" if x else "." for x in y])
        for y in map
    ]))


class Puzzle(aoc.Puzzle):
    EXAMPLE = """
        ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
        #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
        .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
        .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
        .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
        ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
        ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
        
        #..#.
        #....
        ##..#
        ..#..
        ..###
    """
    EXAMPLE_SOLUTION_PART1 = 35
    EXAMPLE_SOLUTION_PART2 = 3351

    def parse_input(self, inp: str) -> Input:
        top, bottom = inp.split("\n\n")
        return Input(
            arr=np.array([x == "#" for x in top if x in ".#"], dtype=bool),
            map=np.array([
                [x == "#" for x in line]
                for line in bottom.splitlines()
            ], dtype=bool))

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        input = self.parse_input(inp)
        map = input.map
        arr = input.arr
        assert arr.shape == (512,)

        outer_val = False
        map = expand(map, outer_val)
        for i in range(2):
            map = eval(arr, map, outer_val)
            if arr[0]:
                outer_val = not outer_val
        return np.sum(map)

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        input = self.parse_input(inp)
        map = input.map
        arr = input.arr
        assert arr.shape == (512,)

        outer_val = False
        map = expand(map, outer_val)
        for i in range(50):
            map = eval(arr, map, outer_val)
            if arr[0]:
                outer_val = not outer_val
        return np.sum(map)


if __name__ == '__main__':
    Puzzle().solve()
