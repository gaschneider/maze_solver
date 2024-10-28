from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)


class Line():
    def __init__(self, pointA, pointB):
        self.__pA = pointA
        self.__pB = pointB

    def draw(self, canvas, fill_color):
        x1, y1 = self.__pA.x, self.__pA.y
        x2, y2 = self.__pB.x, self.__pB.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y