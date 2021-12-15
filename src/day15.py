import heapq
from typing import Optional, Union

import attr
import numpy as np

import aoc


@attr.dataclass(slots=True)
class Pos:
    x: int
    y: int


@attr.s(order=True, slots=True)
class State:
    cost: int = attr.ib()
    pos: Pos = attr.ib(order=False)


@attr.s(order=True, slots=True)
class AstarState:
    f: int = attr.ib()
    cost: int = attr.ib(order=False)
    pos: Pos = attr.ib(order=False)


def shortest_path(map: np.ndarray, start: Pos, end: Pos) -> Optional[int]:
    """
    Simple Dijkstra
    """
    h, w = map.shape
    dist = np.ones_like(map) * 9999
    heap = []
    dist[start.y, start.x] = 0
    heapq.heappush(heap, State(0, start))
    nodes = 0

    def push(edge_cost: int, pos: Pos):
        ncost = edge_cost + map[pos.y, pos.x]
        if ncost < dist[pos.y, pos.x]:
            heapq.heappush(heap, State(ncost, pos))
            dist[pos.y, pos.x] = ncost

    while heap:
        nodes += 1
        # print("\n ===")
        # print(dist)
        state = heapq.heappop(heap)
        cost = state.cost
        position = state.pos

        if position == end:
            #print(dist)
            print(nodes)
            print(np.sum(dist < 99999))
            return cost

        if cost > dist[position.y, position.x]:
            continue

        if position.y < h - 1:
            push(cost, Pos(position.x, position.y + 1))
        if position.x < w - 1:
            push(cost, Pos(position.x + 1, position.y))
        if position.y > 0:
            push(cost, Pos(position.x, position.y - 1))
        if position.x > 0:
            push(cost, Pos(position.x - 1, position.y))

    return None


def shortest_path_opt(map: np.ndarray, start: Pos, end: Pos) -> Optional[int]:
    """
    Simple A*
    """
    height, width = map.shape
    dist = np.ones_like(map) * 99999
    heap = []
    dist[start.y, start.x] = 0
    heapq.heappush(heap, AstarState(0, 0, start))
    nodes = 0

    def h(pos: Pos) -> int:
        return (end.x - pos.x) + (end.y - pos.y)

    def push(edge_cost: int, pos: Pos):
        ncost = edge_cost + map[pos.y, pos.x]
        if ncost < dist[pos.y, pos.x]:
            dist[pos.y, pos.x] = ncost
            heapq.heappush(heap, AstarState(ncost + h(pos), ncost, pos))

    while heap:
        nodes += 1
        #print("\n ===")
        #print(dist)
        state = heapq.heappop(heap)
        cost = state.cost
        position = state.pos

        if position == end:
            #print(dist)
            print(nodes)
            print(np.sum(dist < 99999))
            return cost

        if cost > dist[position.y, position.x]:
            continue

        if position.y < height - 1:
            push(cost, Pos(position.x, position.y + 1))
        if position.x < width - 1:
            push(cost, Pos(position.x + 1, position.y))
        if position.y > 0:
            push(cost, Pos(position.x, position.y - 1))
        if position.x > 0:
            push(cost, Pos(position.x - 1, position.y))

    return None


class Puzzle(aoc.Puzzle):
    DAY = 15
    EXAMPLE = """
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
        """
    EXAMPLE_SOLUTION_PART1 = 40
    EXAMPLE_SOLUTION_PART2 = None#315

    def parse_input(self, inp: str) -> np.ndarray:
        return np.array([
            [int(x) for x in row]
            for row in inp.split("\n")
        ])

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        map = self.parse_input(inp)
        return shortest_path_opt(
            map, Pos(0, 0), Pos(map.shape[0] - 1, map.shape[1] - 1))

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        map = self.parse_input(inp)

        bigmap = np.block([
            [map + (i + j) for j in range(5)]
            for i in range(5)
        ])
        bigmap %= 9
        bigmap[bigmap == 0] = 9

        return shortest_path_opt(
            bigmap, Pos(0, 0), Pos(bigmap.shape[0] - 1, bigmap.shape[1] - 1))


if __name__ == '__main__':
    Puzzle().solve()
