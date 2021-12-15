import operator
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
from pprint import pprint
from typing import Dict, FrozenSet, List, Optional, Set, Tuple, Union

import numpy as np
import numpy.ma as ma

import aoc


class Solver:
    def __init__(self, template: str, inserts: Dict[str, str]):
        self.inserts = inserts
        self.template = template

        self.state = Counter()
        for i in range(len(template) - 1):
            self.state[template[i:i+2]] += 1

    def step(self):
        clone = Counter()
        for seq, count in self.state.items():
            next = self.inserts.get(seq)
            if next:
                clone[seq[0] + next] += count
                clone[next + seq[1]] += count
            else:
                clone[seq] += count
        self.state = clone

    def print(self):
        print("======")
        pprint(self.state)

    def common(self):
        res = Counter()
        for seq, count in self.state.items():
            res[seq[0]] += count
            res[seq[1]] += count

        res[self.template[0]] += 1
        res[self.template[-1]] += 1
        return [(e, c / 2) for e, c in res.items()]


class Puzzle(aoc.Puzzle):
    DAY = 14
    EXAMPLE = """
        NNCB
        
        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C
        """
    EXAMPLE_SOLUTION_PART1 = 1588
    EXAMPLE_SOLUTION_PART2 = 2188189693529

    def parse_input(self, inp: str) -> Tuple[str, Dict[str, str]]:
        template, insertions = inp.split("\n\n")
        inserts = dict([
            row.split(" -> ")
            for row in insertions.split("\n")
        ])
        return template, inserts

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        solver = Solver(*self.parse_input(inp))

        for i in range(10):
            solver.step()

        c = solver.common()
        c.sort(key=lambda x: x[1])
        return c[-1][1] - c[0][1]

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        solver = Solver(*self.parse_input(inp))

        for i in range(40):
            solver.step()

        c = solver.common()
        c.sort(key=lambda x: x[1])
        return c[-1][1] - c[0][1]


if __name__ == '__main__':
    Puzzle().solve()
