"""Given a 2D matrix of 1s and 0s, we must find the area of the largest island of 1s."""

from collections import deque
from itertools import product

import numpy as np
from numpy.typing import NDArray

type Cell = tuple[int, int]


def get_largest_area(m: NDArray[np.float64]) -> int:
    """Find the largest area of a matrix of 1s and 0s."""
    h, w = m.shape

    def in_bounds(c: Cell) -> bool:
        y, x = c
        return (0 <= y < h) and (0 <= x < w)

    def get_neighbors(c: Cell) -> list[Cell]:
        y, x = c
        return [
            (y + d_y, x + d_x)
            for d_y, d_x in product([-1, 1], [-1, 1])
            if in_bounds((y + d_y, x + d_x))
        ]

    not_visited = {(y, x) for y, x in product(range(h), range(w)) if m[y, x]}
    max_area = 0
    to_visit = deque[Cell]()

    while not_visited:
        area = 0
        to_visit.append(not_visited.pop())

        while to_visit:
            c = to_visit.popleft()
            not_visited.discard(c)
            area += 1

            for n in get_neighbors(c):
                if n in not_visited:
                    to_visit.append(n)
        max_area = max(area, max_area)
    return max_area
