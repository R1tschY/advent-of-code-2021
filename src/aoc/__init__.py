import inspect
import os.path
import textwrap
import time
from datetime import timedelta
from pathlib import Path
from typing import ClassVar, List, Optional, Union

import requests

YEAR = 2021


class Puzzle:
    DAY: ClassVar[int]
    EXAMPLE: ClassVar[str]
    EXAMPLE_SOLUTION_PART1: ClassVar[Union[int, str, float]]
    EXAMPLE_SOLUTION_PART2: ClassVar[Optional[Union[int, str, float]]]

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        raise NotImplementedError

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        raise NotImplementedError

    def solve(self, inp: str = None):
        if inp is None:
            pyfile = Path(inspect.getfile(self.__class__))
            inp = (pyfile.parent / f"{pyfile.stem}.txt")\
                .read_text(encoding="utf-8")

        inp = textwrap.dedent(inp).strip()
        example = textwrap.dedent(self.EXAMPLE).strip()

        _assert_eq(
            self.EXAMPLE_SOLUTION_PART1, self.solve_part1(example),
            "part 1")

        start = time.perf_counter()
        solution1 = self.solve_part1(inp)
        end = time.perf_counter()

        print(f"Part 1 solution: {solution1} ({timedelta(seconds=end - start)})")

        if self.EXAMPLE_SOLUTION_PART2:
            _assert_eq(
                self.EXAMPLE_SOLUTION_PART2, self.solve_part2(example), "part 2")

            start = time.perf_counter()
            solution2 = self.solve_part2(inp)
            end = time.perf_counter()

            print(f"Part 2 solution: {solution2} ({timedelta(seconds=end - start)})")

    def lines_input(self, input: str) -> List[int]:
        return [int(line) for line in input.split("\n")]

    def ints_input(self, input: str) -> List[int]:
        return [int(line) for line in input.split("\n")]

    def _get_input(self, year: int, day: int) -> str:
        cache_home = Path(os.environ.get(
            "XDG_CACHE_HOME", os.path.expanduser("~/.cache")))

        cache_folder = cache_home / f"aoc" / str(year)
        cache_file = cache_folder / f"day{day:02}"

        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")

        response = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input")
        response.raise_for_status()

        cache_folder.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(response.text, encoding="utf-8")
        return response.text


def _assert_eq(expected, actual, message):
    if actual != expected:
        raise AssertionError(f"{message}: Expected {expected}, got {actual}")
