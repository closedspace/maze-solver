from __future__ import annotations
import time
from canvas_constructs.cell import Cell
from canvas_constructs.point import Point
import random
from collections import deque

class Maze:
    def __init__(
        self,
        top_left_corner: Point,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win,
    ):
        self.__top_left = top_left_corner
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.cell_list: list[list[Cell]]
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._bfs_solve()


    def _create_cells(self):
        self.cell_list:list[list[Cell]] = []
        for i in range(self.__num_rows):
            row = []
            for j in range(self.__num_cols):
                row.append(Cell(self.__win))
            self.cell_list.append(row)
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        cell = self.cell_list[i][j]
        margin = self.__top_left
        top_left = Point(
            margin.x  + j * self.__cell_size_x,
            margin.y  + i * self.__cell_size_y,
        )
        bottom_right = Point(
            top_left.x + self.__cell_size_x,
            top_left.y + self.__cell_size_y,
        )
        cell.draw("white", top_left, bottom_right)
        self._animate()

    def _break_entrance_and_exit(self):
        self.cell_list[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self.cell_list[self.__num_rows - 1][self.__num_cols - 1].has_bottom_wall = False
        self._draw_cell(self.__num_rows - 1, self.__num_cols - 1)

    def get_adjacent_cell_coords(self, i: int, j: int) -> list[tuple[int, int]]:
        adjacent_cell_coords: list[tuple[int, int]] = []
        if i > 0:
            adjacent_cell_coords = [(i - 1, j)]
        if i < self.__num_rows - 1:
            adjacent_cell_coords.append((i + 1, j))
        if j > 0:
            adjacent_cell_coords.append((i, j - 1))
        if j < self.__num_cols - 1:
            adjacent_cell_coords.append((i, j + 1))
        return adjacent_cell_coords

    def _reset_visited(self):
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                self.cell_list[i][j].visited = False

    def _break_walls_r(self, i, j):
        cell = self.cell_list[i][j]
        cell.visited = True
        while True:
            adjacent_coords = self.get_adjacent_cell_coords(i,j)
            random.shuffle(adjacent_coords)
            adjacent_cells = [self.cell_list[c[0]][c[1]] for c in adjacent_coords]
            not_visited = [c for c in adjacent_cells if not c.visited]
            if not not_visited:
                return
            next_cell = not_visited[0]
            next_cell_coords = adjacent_coords[adjacent_cells.index(next_cell)]
            if next_cell_coords[0] < i:
                cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif next_cell_coords[0] > i:
                cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            elif next_cell_coords[1] < j:
                cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif next_cell_coords[1] > j:
                cell.has_right_wall = False
                next_cell.has_left_wall = False
            self._draw_cell(i, j)
            self._draw_cell(next_cell_coords[0], next_cell_coords[1])
            self._break_walls_r(next_cell_coords[0], next_cell_coords[1])


    def _bfs_solve(self):
        self._reset_visited()
        queue: deque[tuple[int, int]]= deque([(int(0), int(0))])
        path: dict[tuple[int,int], tuple[int,int] | None] = {(0, 0): None }
        while len(queue) > 0:
            (i, j) = queue.popleft()
            cell = self.cell_list[i][j]
            cell.visited = True
            if i == self.__num_rows - 1 and j == self.__num_cols - 1:
                self.draw_path(path)
                return
            for (i2, j2) in self.get_adjacent_cell_coords(i, j):
                cell_2 = self.cell_list[i2][j2]
                if cell_2.visited is False:
                    if cell.has_right_wall is False and cell_2.has_left_wall is False and j < j2:
                        queue.append((i2, j2))
                        path[(i2, j2)] = (i, j)
                        # cell.draw_move(cell_2, undo=False)
                        # self._animate()
                    elif cell.has_left_wall is False and cell_2.has_right_wall is False and j > j2:
                        queue.append((i2, j2))
                        path[(i2, j2)] = (i, j)
                        # cell.draw_move(cell_2, undo=False)
                        # self._animate()
                    elif cell.has_top_wall is False and cell_2.has_bottom_wall is False and i > i2:
                        queue.append((i2, j2))
                        path[(i2, j2)] = (i, j)
                        # cell.draw_move(cell_2, undo=False)
                        # self._animate()
                    elif cell.has_bottom_wall is False and cell_2.has_top_wall is False and i < i2:
                        queue.append((i2, j2))
                        path[(i2, j2)] = (i, j)
                        # cell.draw_move(cell_2, undo=False)
                        # self._animate()






    def draw_path(self, path):
        current = (self.__num_rows - 1, self.__num_cols - 1)
        reconstruct_path = [current]
        while path[current] is not None:
            next_cell_coords = path[current]
            reconstruct_path.append(next_cell_coords)
            current = next_cell_coords

        real_path = reconstruct_path[::-1]
        print(real_path)
        prev = real_path[0]
        next = real_path[1]
        for i in range(1, len(real_path)):
            prev_cell = self.cell_list[prev[0]][prev[1]]
            next_cell = self.cell_list[next[0]][next[1]]
            prev_cell.draw_move(next_cell, undo=False)
            self._animate()
            prev = next
            next = real_path[i]

        next_cell = self.cell_list[next[0]][next[1]]
        last_cell = self.cell_list[self.__num_rows - 1][self.__num_cols - 1]
        last_cell.draw_move(next_cell, undo=False)




    def _animate(self):
        self.__win.redraw()
        time.sleep(0.0001)
