from tkinter import BOTH, YES, Canvas
from canvas_constructs.point import Point


class Line:
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas: Canvas, fill_color, width=2):
        canvas.create_line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y, fill=fill_color, width=width)