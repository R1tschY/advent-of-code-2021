from dataclasses import dataclass
from typing import List, Union

import aoc


@dataclass
class Pos:
    horizontal: float = 0
    depth: float = 0
    aim: float = 0


@dataclass
class Forward:
    value: float

    def apply1(self, pos: Pos):
        pos.horizontal += self.value

    def apply2(self, pos: Pos):
        pos.horizontal += self.value
        pos.depth += pos.aim * self.value


@dataclass
class Down:
    value: float

    def apply1(self, pos: Pos):
        pos.depth += self.value

    def apply2(self, pos: Pos):
        pos.aim += self.value


@dataclass
class Up:
    value: float

    def apply1(self, pos: Pos):
        pos.depth -= self.value

    def apply2(self, pos: Pos):
        pos.aim -= self.value


def parse(lines: str) -> List:
    lines = lines.split("\n")

    cmds = []
    for line in lines:
        if not line:
            continue

        (cmd, value) = line.split(" ", 1)
        value = int(value)
        if cmd == "forward":
            c = Forward(value)
        elif cmd == "down":
            c = Down(value)
        elif cmd == "up":
            c = Up(value)
        else:
            raise RuntimeError(cmd)
        cmds.append(c)
    return cmds


class Puzzle(aoc.Puzzle):
    DAY = 2
    EXAMPLE = """
        forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2"""
    EXAMPLE_SOLUTION_PART1 = 150
    EXAMPLE_SOLUTION_PART2 = 900

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        pos = Pos()
        x = parse(inp)
        for c in x:
            c.apply1(pos)
        return pos.horizontal * pos.depth

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        pos = Pos()
        x = parse(inp)
        for c in x:
            c.apply2(pos)
        return pos.horizontal * pos.depth


if __name__ == '__main__':
    Puzzle().solve()

