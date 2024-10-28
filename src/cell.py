from graphics import Line, Point

class Cell():
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.center = None
        self.__win = window


    def draw(self, top_left, bottom_right):
        if self.__win is None:
            return
        
        self.__top_left = top_left
        self.__bottom_right = bottom_right

        x1, y1 = self.__top_left.x, self.__top_left.y
        x2, y2 = self.__bottom_right.x, self.__bottom_right.y
        half_len = (x2 - x1) / 2
        self.center = Point(x1 + half_len, y1 + half_len)

        x1, y1 = self.__top_left.x, self.__top_left.y
        x2, y2 = self.__bottom_right.x, self.__bottom_right.y

        wall = Line(self.__top_left, Point(x1,y2))
        self.__win.draw_line(wall, "black" if self.has_left_wall else "white")
        
        wall = Line(Point(x2,y1), self.__bottom_right)
        self.__win.draw_line(wall, "black" if self.has_right_wall else "white")
        
        wall = Line(self.__top_left, Point(x2,y1))
        self.__win.draw_line(wall, "black" if self.has_top_wall else "white")
        
        wall = Line(Point(x1,y2), self.__bottom_right)
        self.__win.draw_line(wall, "black" if self.has_bottom_wall else "white")

    def draw_move(self, to_cell, undo=False):
        line = Line(self.center, to_cell.center)

        if self.__win is None:
            return
        self.__win.draw_line(line, "gray" if undo else "red")
        