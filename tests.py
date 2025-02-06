import unittest
import time

from src.mazeclass import Maze
from src.artbox import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        window = Window(800, 600)
        num_cols = 11
        num_rows = 15
        m1 = Maze((20, 20), (num_rows, num_cols), (50, 50), window)
        m1._break_entrance_and_exit()
        m1._break_walls_r(0, 0)
        m1._reset_visited()
        m1.solve()
        window.wait_for_close()

        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertEqual(
            m1._cells[0][0].walls["N"],
            False,
        )
        self.assertEqual(
            m1._cells[-1][-1].walls["S"],
            False,
        )
        self.assertEqual(
            m1._cells[0][0].visited,
            True,
        )

if __name__ == "__main__":
    unittest.main()