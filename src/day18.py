import ast
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce as fnreduce
from itertools import permutations
from typing import Generic, List, Optional, TypeVar, Union

import aoc

NoneType = type(None)

T = TypeVar("T")


class BaseNode:
    def visit(self, visitor: "NodeVisitor[T]") -> T:
        pass

    def magnitude(self) -> int:
        pass


@dataclass
class Node(BaseNode):
    left: "BaseNode"
    right: "BaseNode"

    def get_sub(self, left: bool) -> "BaseNode":
        return self.left if left else self.right

    def set_sub(self, left: bool, value: BaseNode) -> None:
        if left:
            self.left = value
        else:
            self.right = value

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def visit(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_node(self)

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


@dataclass
class Literal(BaseNode):
    value: int

    def __str__(self):
        return str(self.value)

    def visit(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_literal(self)

    def magnitude(self) -> int:
        return self.value


class NodeVisitor(Generic[T]):
    def visit_literal(self, literal: Literal) -> T:
        raise NotImplementedError

    def visit_node(self, node: Node) -> T:
        raise NotImplementedError


class NodeStackVisitor(NodeVisitor[bool]):
    def __init__(self):
        self.stack = []
        self.path = []

    def visit(self, data: BaseNode) -> bool:
        self.stack = [data]
        self.path = []
        return data.visit(self)

    def visit_literal(self, literal: Literal) -> bool:
        return False

    def visit_node(self, node: Node) -> bool:
        # left
        self.path.append(True)
        self.stack.append(node.left)
        l = node.left.visit(self)

        # right
        if not l:
            self.path[-1] = False
            self.stack[-1] = node.right
            r = node.right.visit(self)
            self.stack.pop()
            self.path.pop()
            return r
        else:
            return l


def create_tree(x) -> BaseNode:
    if isinstance(x, list):
        return Node(create_tree(x[0]), create_tree(x[1]))
    elif isinstance(x, int):
        return Literal(x)
    else:
        raise RuntimeError


def next_left_literal(path: List[bool], stack: List[BaseNode]) -> Optional[Literal]:
    while path:
        if path[-1]:
            path.pop()
            stack.pop()
        else:
            path[-1] = True
            stack[-1] = stack[-2].left

            while True:
                if isinstance(stack[-1], Literal):
                    return stack[-1]
                elif isinstance(stack[-1], Node):
                    path.append(False)
                    stack.append(stack[-1].right)
    return None


def next_right_literal(path: List[bool], stack: List[BaseNode]) -> Optional[Literal]:
    while path:
        if not path[-1]:
            path.pop()
            stack.pop()
        else:
            path[-1] = False
            stack[-1] = stack[-2].right

            while True:
                if isinstance(stack[-1], Literal):
                    return stack[-1]
                elif isinstance(stack[-1], Node):
                    path.append(True)
                    stack.append(stack[-1].left)
    return None


def expand(path: List[bool], stack: List[BaseNode]):
    target = stack[-1]
    assert isinstance(target, Node)
    assert isinstance(target.left, Literal)
    assert isinstance(target.right, Literal)

    left = target.left.value
    right = target.right.value
    stack[-1] = Literal(0)
    stack[-2].set_sub(path[-1], stack[-1])

    # left
    left_lit = next_left_literal(path[:], stack[:])
    if left_lit:
        left_lit.value += left

    # right
    right_lit = next_right_literal(path[:], stack[:])
    if right_lit:
        right_lit.value += right


def split(path: List[bool], stack: List[BaseNode]):
    target = stack[-1]
    assert isinstance(target, Literal)
    l = target.value // 2
    r = l + target.value % 2
    stack[-1] = Node(Literal(l), Literal(r))
    stack[-2].set_sub(path[-1], stack[-1])


def reduce(data: BaseNode) -> BaseNode:
    class ReduceVisitor(NodeStackVisitor):
        def visit_literal(self, literal: Literal) -> bool:
            return False

        def visit_node(self, node: Node) -> bool:
            if len(self.stack) > 4 \
                    and isinstance(node.left, Literal) \
                    and isinstance(node.right, Literal):
                expand(self.path, self.stack)
                return True

            return super().visit_node(node)

    class SplitVisitor(NodeStackVisitor):
        def visit_literal(self, literal: Literal) -> bool:
            if literal.value > 9:
                split(self.path, self.stack)
                return True

            return False

    while ReduceVisitor().visit(data) or SplitVisitor().visit(data):
        pass

    return data


class Puzzle(aoc.Puzzle):
    EXAMPLE = """
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """
    EXAMPLE_SOLUTION_PART1 = 4140
    EXAMPLE_SOLUTION_PART2 = 3993

    def parse_input(self, inp: str) -> List[BaseNode]:
        return [create_tree(ast.literal_eval(line)) for line in inp.splitlines()]

    def solve_part1(self, inp: str) -> Union[int, str, float]:
        lines = self.parse_input(inp)

        def add(acc: BaseNode, right: BaseNode) -> BaseNode:
            return reduce(Node(acc, right))

        data = fnreduce(add, lines)
        return data.magnitude()

    def solve_part2(self, inp: str) -> Union[int, str, float]:
        lines = self.parse_input(inp)

        def magnitude(left: BaseNode, right: BaseNode) -> int:
            return reduce(Node(deepcopy(left), deepcopy(right))).magnitude()

        return max(
            magnitude(left, right)
            for left, right in permutations(lines, 2)
        )


if __name__ == '__main__':
    Puzzle().solve()

