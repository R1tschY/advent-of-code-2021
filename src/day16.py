import binascii
from dataclasses import dataclass
from functools import reduce
from heapq import heappop, heappush
from operator import __mul__, methodcaller
from typing import List, Optional, Tuple, Union

import attr
import numpy as np

import aoc


@dataclass
class Package:
    version: int

    def sum_versions(self) -> int:
        pass

    def eval(self) -> int:
        pass


@dataclass
class Literal(Package):
    value: int

    def sum_versions(self) -> int:
        return self.version

    def eval(self) -> int:
        return self.value


@dataclass
class Operator(Package):
    type: int
    pkgs: List[Package]

    def sum_versions(self) -> int:
        return self.version + sum(pkg.sum_versions() for pkg in self.pkgs)

    def eval(self) -> int:
        if self.type == 0:
            return sum(map(methodcaller("eval"), self.pkgs))
        elif self.type == 1:
            return reduce(__mul__, map(methodcaller("eval"), self.pkgs))
        elif self.type == 2:
            return min(map(methodcaller("eval"), self.pkgs))
        elif self.type == 3:
            return max(map(methodcaller("eval"), self.pkgs))
        elif self.type == 5:
            return 1 if self.pkgs[0].eval() > self.pkgs[1].eval() else 0
        elif self.type == 6:
            return 1 if self.pkgs[0].eval() < self.pkgs[1].eval() else 0
        elif self.type == 7:
            return 1 if self.pkgs[0].eval() == self.pkgs[1].eval() else 0


def parse_pkg(b: str, i: int) -> Tuple[int, Package]:
    version = int(b[i:i+3], 2)
    type = int(b[i+3:i+6], 2)
    i += 6
    if type == 4:
        res: List[str] = []
        while True:
            res.append(b[i + 1:i + 5])
            if b[i] == "0":
                i += 5
                break
            i += 5
        value = int("".join(res), 2)
        # print("LIT", version, type, value)
        return i, Literal(version=version, value=value)
    else:
        if b[i] == "1":
            i += 1
            subpkgs = int(b[i:i+11], 2)
            i += 11
            # print(f"OP1", version, type, subpkgs)
            pkgs = []
            for j in range(subpkgs):
                i, pkg = parse_pkg(b, i)
                pkgs.append(pkg)
            return i, Operator(version=version, type=type, pkgs=pkgs)
        else:
            i += 1
            l = int(b[i:i+15], 2)
            i += 15
            # print(f"OP0", version, type, l)
            pkgs = []
            end = i + l
            while i < end:
                i, pkg = parse_pkg(b, i)
                pkgs.append(pkg)
            return i, Operator(version=version, type=type, pkgs=pkgs)


class Puzzle(aoc.Puzzle):
    EXAMPLES = [
        ("8A004A801A8002F478", 16, None),
        ("620080001611562C8802118E34", 12, None),
        ("C0015000016115A2E0802F182340", 23, None),
        ("A0016C880162017C3686B18A3D4780", 31, None),
        ("C200B40A82", None, 3),
        ("04005AC33890", None, 54),
        ("880086C3E88112", None, 7),
        ("CE00C43D881120", None, 9),
        ("D8005AC2A8F0", None, 1),
        ("F600BC2D8F", None, 0),
        ("9C005AC2F8F0", None, 0),
        ("9C0141080250320F1802104A08", None, 1),
    ]

    def parse_input(self, inp: str) -> str:
        return "".join([f"{i:08b}" for i in binascii.a2b_hex(inp)])

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        b = self.parse_input(inp)
        i, pkg = parse_pkg(b, 0)
        return pkg.sum_versions()

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        b = self.parse_input(inp)
        i, pkg = parse_pkg(b, 0)
        return pkg.eval()


if __name__ == '__main__':
    Puzzle().solve()
