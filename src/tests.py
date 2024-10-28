import unittest
from maze import Maze
from functools import reduce

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_2(self):
        num_cols = 15
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    
    def test_maze_entrance_exit(self):
        num_cols = 15
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(
            m1._cells[0][0].has_left_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols-1][num_rows-1].has_right_wall,
            False,
        )

    def test_maze_cell_visited_should_all_be_false(self):
        num_cols = 15
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)
        all_cells = reduce(lambda curr, col: curr + col, m1._cells)
        at_least_one_visited = reduce(lambda curr, cell: curr or cell.visited, all_cells, False)
        self.assertEqual(
            at_least_one_visited,
            False,
        )

    def test_maze_solution(self):
        num_cols = 15
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(
            m1.solve(),
            True,
        )

if __name__ == "__main__":
    unittest.main()