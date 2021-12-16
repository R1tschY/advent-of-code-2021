import inspect
import re
import textwrap
import time
from datetime import timedelta
from pathlib import Path
from typing import ClassVar, List, Optional, Tuple, Union

import requests

YEAR = 2021


class Puzzle:
    EXAMPLE: ClassVar[str] = None
    EXAMPLE_SOLUTION_PART1: ClassVar[int] = None
    EXAMPLE_SOLUTION_PART2: ClassVar[int] = None

    EXAMPLES: ClassVar[List[Tuple[str, Optional[int], Optional[int]]]] = None

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        raise NotImplementedError

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        raise NotImplementedError

    def solve(self):
        examples = self._check_examples()

        inp = textwrap.dedent(self._get_input()).strip()
        start = time.perf_counter()
        solution1 = self.solve_part1(inp)
        end = time.perf_counter()

        print(f"Part 1 solution: {solution1} ({timedelta(seconds=end - start)})")

        if any(value2 is not None for _, _, value2 in examples):
            start = time.perf_counter()
            solution2 = self.solve_part2(inp)
            end = time.perf_counter()

            print(f"Part 2 solution: {solution2} ({timedelta(seconds=end - start)})")

    def lines_input(self, input: str) -> List[int]:
        return [int(line) for line in input.split("\n")]

    def ints_input(self, input: str) -> List[int]:
        return [int(line) for line in input.split("\n")]

    def _check_examples(self):
        examples = []

        if self.EXAMPLES:
            examples.extend(self.EXAMPLES)

        if self.EXAMPLE:
            examples.append((
                self.EXAMPLE,
                self.EXAMPLE_SOLUTION_PART1,
                self.EXAMPLE_SOLUTION_PART2))

        for example, value1, value2 in examples:
            self._check_example(example, value1, value2)

        return examples

    def _check_example(
            self, example: str, value1: Optional[int], value2: Optional[int]):
        example = textwrap.dedent(example).strip()

        if value1 is not None:
            _assert_eq(value1, self.solve_part1(example), "example part 1")
        if value2 is not None:
            _assert_eq(value2, self.solve_part2(example), "example part 2")

    def _get_input(self) -> str:
        puzzle_file = Path(inspect.getfile(self.__class__))
        day = re.findall(r"day(\d+)", puzzle_file.stem)[0]

        cache_file = puzzle_file.with_suffix(".txt")
        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")

        session_cookie = self._read_session_cookie(puzzle_file)
        response = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{day}/input",
            cookies={"session": session_cookie})
        response.raise_for_status()

        cache_file.write_text(response.text, encoding="utf-8")
        return response.text

    def _read_session_cookie(self, puzzle_file: Path):
        path = puzzle_file.parent
        while str(path) != path.root:
            if (path / ".aocsession").exists():
                return (path / ".aocsession").read_text().strip()
            path = path.parent

        raise RuntimeError("did not found .aocsession file")


def _assert_eq(expected, actual, message):
    if actual != expected:
        raise AssertionError(f"{message}: Expected {expected}, got {actual}")
