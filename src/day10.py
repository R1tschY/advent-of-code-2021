import operator
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
from pprint import pprint
from typing import Dict, FrozenSet, List, Optional, Set, Union

import numpy as np
import numpy.ma as ma

import aoc


class Puzzle(aoc.Puzzle):
    DAY = 10
    EXAMPLE = """
        [({(<(())[]>[[{[]{<()<>>
        [(()[<>])]({[<{<<[]>>(
        {([(<{}[<>[]}>{[]{[(<()>
        (((({<>}<{<{<>}{[]{[]{}
        [[<[([]))<([[{}[[()]]]
        [{[{({}]{}}([{[{{{}}([]
        {<[[]]>}<{[{[{[]{()[[[]
        [<(<(<(<{}))><([]([]()
        <{([([[(<>()){}]>(<<{{
        <{([{{}}[<[[[<>{}]]]>[]]"""
    EXAMPLE_SOLUTION_PART1 = 26397
    EXAMPLE_SOLUTION_PART2 = 288957

    def parse_input(self, inp: str) -> List[str]:
        return inp.split("\n")

    def syntax_error_score(self, line: str) -> int:
        stack = []

        CLOSING = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
        }
        POINTS = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137,
        }

        for c in line:
            if c in "([{<":
                stack.append(c)
            else:
                top = stack.pop()
                if c != CLOSING[top]:
                    return POINTS[c]

        return 0

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        lines = self.parse_input(inp)
        return sum(
            self.syntax_error_score(line)
            for line in lines
        )

    def autocomplete_score(self, line: str) -> Optional[int]:
        stack = []

        CLOSING = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
        }
        POINTS = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4,
        }

        for c in line:
            if c in "([{<":
                stack.append(c)
            else:
                top = stack.pop()
                if c != CLOSING[top]:
                    return None

        acc = 0
        for s in reversed(stack):
            acc = acc * 5 + POINTS[CLOSING[s]]
        return acc

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        lines = self.parse_input(inp)

        list = [
            self.autocomplete_score(line)
            for line in lines
        ]
        list = [
            score for score in list if score is not None
        ]
        list.sort()
        return list[len(list) // 2]


if __name__ == '__main__':
    Puzzle().solve()
