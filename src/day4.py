import itertools
from dataclasses import dataclass
from typing import Iterator, List, Tuple, Union

import numpy as np
import numpy.ma as ma

import aoc


@dataclass
class BingoBoard:
    numbers: np.array
    mask: np.array

    @classmethod
    def parse(cls, lines: List[str]):
        board = np.zeros((5, 5))

        for (row, line) in enumerate(lines):
            for (column, cell) in enumerate(line.split()):
                board[row][column] = int(cell)

        return BingoBoard(board, np.zeros((5, 5), dtype=bool))

    def mark(self, number: int) -> None:
        np.logical_or(self.mask, np.equal(number, self.numbers), out=self.mask)

    def has_bingo(self) -> bool:
        a = np.any(np.equal(5, np.sum(self.mask, axis=0)))
        b = np.any(np.equal(5, np.sum(self.mask, axis=1)))
        return a or b

    def sum_of_unmarked(self) -> int:
        return int(np.sum(ma.masked_array(self.numbers, mask=self.mask)))


class Puzzle(aoc.Puzzle):
    DAY = 4
    EXAMPLE = """
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        22 13 17 11  0
         8  2 23  4 24
        21  9 14 16  7
         6 10  3 18  5
         1 12 20 15 19
        
         3 15  0  2 22
         9 18 13 17  5
        19  8  7 25 23
        20 11 10 24  4
        14 21 16 12  6
        
        14 21 17 24  4
        10 16 15  9 19
        18  8 23 26 20
        22 11 13  6  5
         2  0 12  3  7"""
    EXAMPLE_SOLUTION_PART1 = 4512
    EXAMPLE_SOLUTION_PART2 = 1924

    def parse_input(self, inp: str) -> Tuple[List[int], List[BingoBoard]]:
        lines = inp.split("\n")

        numbers = [int(i) for i in lines[0].split(",")]

        boards = []
        for (_, board) in itertools.groupby(lines[1:], lambda line: len(line)):
            board = list(board)
            if len(board) == 5:
                boards.append(BingoBoard.parse(board))

        return numbers, boards

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        numbers, boards = self.parse_input(inp)

        for number in numbers:
            for (i, board) in enumerate(boards):
                board.mark(number)

            for board in boards:
                if board.has_bingo():
                    return number * board.sum_of_unmarked()

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        numbers, boards = self.parse_input(inp)

        for number in numbers:
            for (i, board) in enumerate(boards):
                board.mark(number)

            new_boards = [
                board
                for board in boards
                if not board.has_bingo()
            ]

            if len(new_boards) == 0:
                return number * boards[0].sum_of_unmarked()

            boards = new_boards


if __name__ == '__main__':
    Puzzle().solve()

