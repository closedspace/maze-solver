from __future__ import annotations
from canvas_constructs.point import Point
from canvas_constructs.line import Line

WALL_COLOR = "black"
EMPTY_WALL_COLOR = "white"

class Cell:
    def __init__(self, win) -> None:
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.__top_left: Point | None = None
        self.__bottom_right: Point | None = None
        self.__win = win
        self.visited = False

    def get_cell_center(self) -> Point:
        return Point((self.__top_left.x + self.__bottom_right.x) // 2, (self.__top_left.y + self.__bottom_right.y) // 2)

    def draw(self, fill_color: str, top_left: Point, bottom_right: Point) -> None:
        self.__top_left = top_left
        self.__bottom_right = bottom_right
        self.__win.canvas.create_rectangle(self.__top_left.x, self.__top_left.y, self.__bottom_right.x, self.__bottom_right.y, fill=fill_color)
        draw_line = self.__win.draw_line
        top_left = self.__top_left
        top_right = Point(self.__bottom_right.x, self.__top_left.y)
        bottom_left = Point(self.__top_left.x, self.__bottom_right.y)
        bottom_right = self.__bottom_right

        top_wall = Line(top_left, top_right)
        draw_line(top_wall, WALL_COLOR if self.has_top_wall else EMPTY_WALL_COLOR)
        left_wall = Line(top_left, bottom_left)
        draw_line(left_wall, WALL_COLOR if self.has_left_wall else EMPTY_WALL_COLOR)
        right_wall = Line(top_right, bottom_right)
        draw_line(right_wall, WALL_COLOR if self.has_right_wall else EMPTY_WALL_COLOR)
        bottom_wall = Line(bottom_left, bottom_right)
        draw_line(bottom_wall, WALL_COLOR if self.has_bottom_wall else EMPTY_WALL_COLOR)

    def draw_move(self, to_cell: Cell, undo=False):
        self_center = self.get_cell_center()
        target_cell_center = to_cell.get_cell_center()
        connecting_line = Line(self_center, target_cell_center)
        if undo:
            self.__win.draw_line(connecting_line, "green")
        else:
            self.__win.draw_line(connecting_line, "red")
