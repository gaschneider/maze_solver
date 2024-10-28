from cell import Cell
from graphics import Point
import time
import random
from functools import reduce

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self.win) for _ in range(self.num_rows)] for _ in range(self.num_cols)]
        
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        top = self.y1 + self.cell_size_y * j
        left = self.x1 + self.cell_size_x * i
        bottom = top + self.cell_size_y
        right = left + self.cell_size_x

        self._cells[i][j].draw(Point(left, top), Point(right, bottom))
        self._animate()

    def _animate(self, speed=0):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(speed)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0,0)

        last_cell_col, last_cell_row = self.num_cols - 1, self.num_rows - 1
        self._cells[last_cell_col][last_cell_row].has_right_wall = False
        self._draw_cell(last_cell_col,last_cell_row)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            # Cells to visit
            to_visit = []

            # All the possible directions
            possible_directions = [(i - 1, j),(i + 1, j),(i, j - 1),(i, j + 1)]
            for p in possible_directions:
                adj_i, adj_j = p[0], p[1]
                # Verify if the i,j is within bounds
                if adj_i < 0 or adj_i > (self.num_cols - 1) or adj_j < 0 or adj_j > (self.num_rows - 1):
                    continue
                if self._cells[adj_i][adj_j].visited:
                    continue
                to_visit.append(p)
            
            # Draw current cell if there is no other cell to visit around and exit
            if len(to_visit) == 0:
                self._draw_cell(i,j)
                return
            
            # Pick a random adjacent cell to go
            adj_i, adj_j = to_visit[random.randrange(0, len(to_visit), 1)]
            
            # Break wall between cells
            if adj_i < i:
                self._cells[adj_i][adj_j].has_right_wall = False
                self._cells[i][j].has_left_wall = False
            elif adj_i > i:
                self._cells[adj_i][adj_j].has_left_wall = False
                self._cells[i][j].has_right_wall = False
            elif adj_j < j:
                self._cells[adj_i][adj_j].has_bottom_wall = False
                self._cells[i][j].has_top_wall = False
            else:
                self._cells[adj_i][adj_j].has_top_wall = False
                self._cells[i][j].has_bottom_wall = False

            # Call chosen cell to break walls
            self._break_walls_r(adj_i, adj_j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate(0.05)
        self._cells[i][j].visited = True

        # Is the end cell, meaning the path was found
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        cell = self._cells[i][j]
        count_walls = reduce(lambda curr, w: curr + 1 if w else curr,[cell.has_left_wall, cell.has_right_wall, cell.has_top_wall, cell.has_bottom_wall], 0)
        # Loser cell = has 3 walls, meaning the only path free is the one it came
        if count_walls == 3:
            return False 

        # Checks left cell if has no wall between them
        if not cell.has_left_wall and i > 0 and not self._cells[i-1][j].visited:
            cell.draw_move(self._cells[i-1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                cell.draw_move(self._cells[i-1][j], True)

        # Checks right cell if has no wall between them
        if not cell.has_right_wall and i + 1 < self.num_cols and not self._cells[i+1][j].visited:
            cell.draw_move(self._cells[i+1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                cell.draw_move(self._cells[i+1][j], True)

        # Checks top cell if has no wall between them
        if not cell.has_top_wall and j > 0 and not self._cells[i][j-1].visited:
            cell.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                cell.draw_move(self._cells[i][j-1], True)

        # Checks bottom cell if has no wall between them
        if not cell.has_bottom_wall and j + 1 < self.num_rows and not self._cells[i][j+1].visited:
            cell.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                cell.draw_move(self._cells[i][j+1], True)

        return False
    
    def solve(self):
        return self._solve_r(0, 0)