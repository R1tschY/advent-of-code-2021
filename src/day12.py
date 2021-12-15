import operator
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import itemgetter
from pprint import pprint
from typing import Dict, FrozenSet, List, Optional, Set, Tuple, Union

import numpy as np
import numpy.ma as ma

import aoc


def build_graph(edges: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    graph = defaultdict(list)
    for start, end in edges:
        graph[start].append(end)
        graph[end].append(start)
    return graph


class Solver1:
    def __init__(self, graph: Dict[str, List[str]]):
        self.stack = []
        self.solutions = []
        self.graph = graph

    def all_paths(self) -> List[List[str]]:
        self.stack = []
        self.solutions = []
        self._all_paths(node="start")
        return self.solutions

    def _all_paths(self, node: str):
        if node == "end":
            # print(",".join(stack))
            self.solutions.append(self.stack[:])
            return

        for edge in self.graph[node]:
            if edge.islower() and edge in self.stack:
                continue

            self.stack.append(node)
            self._all_paths(edge)
            self.stack.pop()


class Solver2:
    def __init__(self, graph: Dict[str, List[str]]):
        self.stack = []
        self.solutions = []
        self.graph = graph

    def all_paths(self) -> List[List[str]]:
        self.stack = []
        self.solutions = []
        self._all_paths(node="start", yssc=False)
        return self.solutions

    def _all_paths(self, node: str, yssc: bool):
        if node == "end":
            # print(",".join(stack))
            self.solutions.append(self.stack[:])
            return

        for edge in self.graph[node]:
            if edge == "start":
                continue
            next_yssc = yssc
            if edge.islower() and edge in self.stack:
                if yssc:
                    continue
                else:
                    next_yssc = True

            self.stack.append(node)
            self._all_paths(edge, next_yssc)
            self.stack.pop()


class Puzzle(aoc.Puzzle):
    DAY = 12
    EXAMPLE = """
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
        """
    EXAMPLE_SOLUTION_PART1 = 10
    EXAMPLE_SOLUTION_PART2 = 36

    def parse_input(self, inp: str) -> List[Tuple[str, str]]:
        return [tuple(line.split("-", 1)) for line in inp.split("\n")]

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        edges = self.parse_input(inp)
        graph = build_graph(edges)
        return len(Solver1(graph).all_paths())

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        edges = self.parse_input(inp)
        graph = build_graph(edges)
        return len(Solver2(graph).all_paths())


if __name__ == '__main__':
    Puzzle().solve()
