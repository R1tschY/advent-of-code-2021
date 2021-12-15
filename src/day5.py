import re
from dataclasses import dataclass
from typing import List, Union

import numpy as np

import aoc


@dataclass
class Pos:
    x: int
    y: int


@dataclass
class Size:
    width: int
    height: int


@dataclass
class Line:
    start: Pos
    end: Pos

    def is_horizontal(self):
        return self.start.y == self.end.y

    def is_vertical(self):
        return self.start.x == self.end.x


class VentureMap:
    map: np.ndarray

    def __init__(self, size: Size):
        self.map = np.zeros((size.width, size.height))

    def mark_line(self, line: Line):
        x0 = line.start.x
        y0 = line.start.y
        x1 = line.end.x
        y1 = line.end.y

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            self.map[x0][y0] += 1
            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy


class Puzzle(aoc.Puzzle):
    DAY = 5
    EXAMPLE = """
        0,9 -> 5,9
        8,0 -> 0,8
        9,4 -> 3,4
        2,2 -> 2,1
        7,0 -> 7,4
        6,4 -> 2,0
        0,9 -> 2,9
        3,4 -> 1,4
        0,0 -> 8,8
        5,5 -> 8,2"""
    EXAMPLE_SOLUTION_PART1 = 5
    EXAMPLE_SOLUTION_PART2 = 12

    def parse_input(self, inp: str) -> List[Line]:
        return [
            Line(
                Pos(int(m.group(1)), int(m.group(2))),
                Pos(int(m.group(3)), int(m.group(4))))
            for m in re.finditer(r"(\d+),(\d+)\s+->\s+(\d+),(\d+)", inp)
        ]

    def get_board_size(self, lines: List[Line]) -> Size:
        width = 0
        height = 0
        for line in lines:
            width = max(width, line.start.x)
            width = max(width, line.end.x)
            height = max(height, line.start.y)
            height = max(height, line.end.y)
        return Size(width + 1, height + 1)

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        lines = self.parse_input(inp)
        map = VentureMap(self.get_board_size(lines))

        for line in lines:
            if line.is_horizontal() or line.is_vertical():
                map.mark_line(line)

        return int(np.sum(map.map >= 2))

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        lines = self.parse_input(inp)
        map = VentureMap(self.get_board_size(lines))

        for line in lines:
            map.mark_line(line)

        return int(np.sum(map.map >= 2))


if __name__ == '__main__':
    Puzzle().solve()

