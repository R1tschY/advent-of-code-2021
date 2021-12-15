from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Set, Union

import aoc


# 2 seg -> 1
# 3 seg -> 7
# 4 seg -> 4
# 7 seg -> 8


@dataclass
class Digit:
    solved: bool
    segments: FrozenSet[str]
    as_str: str


@dataclass
class Input:
    digits: List[Digit]
    outputs: List[str]


class Solver:
    solved: Dict[int, Digit]
    digits: List[Digit]

    def __init__(self, digits: List[Digit]):
        self.digits = digits
        self.solved = {}

    def find_through_intersection(self, number: int, segments: int, through: int, intersection: int):
        partner_seg = self.solved[through].segments
        for digit in self.digits:
            if len(digit.segments) == segments \
                    and len(partner_seg & digit.segments) == intersection:
                digit.solved = True
                self.solved[number] = digit
                break
        else:
            raise RuntimeError(f"{number} not found")

    def find_last(self, number: int, segments: int):
        for digit in self.digits:
            if len(digit.segments) == segments and not digit.solved:
                digit.solved = True
                self.solved[number] = digit
                break
        else:
            raise RuntimeError()

    def get_number_mapping(self) -> Dict[FrozenSet[str], int]:
        return {
            digit.segments: number for number, digit in self.solved.items()
        }


class Puzzle(aoc.Puzzle):
    DAY = 8
    EXAMPLE = """
        be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
        edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
        fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
        fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
        aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
        fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
        dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
        bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
        egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
        gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    EXAMPLE_SOLUTION_PART1 = 26
    EXAMPLE_SOLUTION_PART2 = 61229

    def parse_input(self, inp: str) -> List[Input]:
        res = []
        for x in inp.split("\n"):
            (digits, outputs) = x.split("|")
            res.append(Input(
                digits=[Digit(solved=False, segments=frozenset(d), as_str=d) for d in digits.strip().split()],
                outputs=outputs.strip().split()))

        return res

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        inputs = self.parse_input(inp)
        return sum(
            1
            for input in inputs
            for output in input.outputs
            if len(output) in (2, 3, 4, 7)
        )

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        inputs = self.parse_input(inp)
        return sum(
            self.solve_for_input(input.digits, input.outputs)
            for input in inputs
        )

    def solve_for_input(self, digits: List[Digit], output: List[str]) -> int:
        solver = Solver(digits)

        solver.find_last(1, 2)
        solver.find_last(7, 3)
        solver.find_last(4, 4)
        solver.find_last(8, 7)

        # 6
        solver.find_through_intersection(6, 6, 1, 1)

        # 9
        solver.find_through_intersection(9, 6, 4, 4)

        # 0
        solver.find_last(0, 6)

        # 5
        solver.find_through_intersection(5, 5, 6, 5)

        # 3
        solver.find_through_intersection(3, 5, 1, 2)

        # 2
        solver.find_last(2, 5)

        mapping = solver.get_number_mapping()
        return int("".join([str(mapping[frozenset(o)]) for o in output]))


if __name__ == '__main__':
    Puzzle().solve()
