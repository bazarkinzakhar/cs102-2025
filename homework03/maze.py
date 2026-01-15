from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows, cols = len(grid), len(grid[0])

    direction = choice(["up", "right"])

    if direction == "up":
        if x - 2 < 0:
            direction = "right"
    else:
        if y + 2 >= cols:
            direction = "up"

    if direction == "up" and x - 2 >= 0:
        grid[x - 1][y] = " "
    elif direction == "right" and y + 2 < cols:
        grid[x][y + 1] = " "

    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        grid = remove_wall(grid, (x, y))

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = (
            randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
        )
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    rows, cols = len(grid), len(grid[0])

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == "X" and (
                x == 0 or x == rows - 1 or y == 0 or y == cols - 1
            ):
                exits.append((x, y))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows, cols = len(grid), len(grid[0])
    nk = k + 1

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                if i - 1 >= 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = nk
                if i + 1 < rows and grid[i + 1][j] == 0:
                    grid[i + 1][j] = nk
                if j - 1 >= 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = nk
                if j + 1 < cols and grid[i][j + 1] == 0:
                    grid[i][j + 1] = nk

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    rows, cols = len(grid), len(grid[0])

    start = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                start = (i, j)
                break
        if start is not None:
            break

    if start is None:
        return None

    ex, ey = exit_coord
    if not isinstance(grid[ex][ey], int) or grid[ex][ey] == 0:
        return None

    path = [exit_coord]
    curr = exit_coord

    while curr != start:
        x, y = curr
        k = grid[x][y]
        next_cell = None

        if x > 0 and grid[x - 1][y] == k - 1:
            next_cell = (x - 1, y)
        elif x < rows - 1 and grid[x + 1][y] == k - 1:
            next_cell = (x + 1, y)
        elif y > 0 and grid[x][y - 1] == k - 1:
            next_cell = (x, y - 1)
        elif y < cols - 1 and grid[x][y + 1] == k - 1:
            next_cell = (x, y + 1)

        if next_cell is None:
            return None

        path.append(next_cell)
        curr = next_cell

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    blocked = 0
    checked = 0

    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            checked += 1
            if grid[nx][ny] == "■":
                blocked += 1

    if checked == 2:
        return blocked == 2
    if checked == 3:
        return blocked == 3

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)

    if len(exits) < 2:
        if len(exits) == 1:
            return grid, exits[0]
        return grid, None

    start, finish = exits[1], exits[0]

    if encircled_exit(grid, start) or encircled_exit(grid, finish):
        return grid, None

    sx, sy = start
    fx, fy = finish

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == " " or grid[i][j] == "X":
                grid[i][j] = 0

    grid[sx][sy] = 1
    grid[fx][fy] = 0

    k = 1
    while grid[fx][fy] == 0:
        found = False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == k:
                    found = True
                    break
            if found:
                break

        if not found:
            return grid, None

        grid = make_step(grid, k)
        k += 1

    back_path = shortest_path(grid, finish)
    if not back_path:
        return grid, None

    path = list(reversed(back_path))

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if isinstance(grid[i][j], int):
                grid[i][j] = " "
    grid[sx][sy] = "X"
    grid[fx][fy] = "X"

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
