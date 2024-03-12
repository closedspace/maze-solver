
from tkinter import BOTH, YES, Canvas, Tk
from canvas_constructs.line import Line
from canvas_constructs.maze import Maze
from canvas_constructs.point import Point
from canvas_constructs.cell import Cell


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.width = width
        self.height = height
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.configure(background="white")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)

def main():
    win = Window(1000, 1000)
    num_cols = 30
    num_rows = 30
    margin = 50
    maze_point = Point(margin, margin)
    cell_size_x = (win.width - 2 * margin) // num_cols
    cell_Size_y = (win.height - 2 * margin) // num_rows
    maze = Maze(maze_point, num_rows, num_cols, cell_size_x, cell_Size_y, win)

    win.wait_for_close()

if __name__ == "__main__":
    main()
