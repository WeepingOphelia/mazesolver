import time
import random

from .artbox import Cell, Point

class Maze():
    def __init__(self, origin, matrix_dim, cell_dim, window=None, seed=None):
        self.x = origin[0]
        self.y = origin[1]
        self.num_rows = matrix_dim[0]
        self.num_cols = matrix_dim[1]
        self.cell_x = cell_dim[0]
        self.cell_y = cell_dim[1]
        self.win = window
        if seed != None:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        self._cells = [[Cell(self.win) for i in range(self.num_rows)] for j in range(self.num_cols)]
        if self.win:
            for i in range(self.num_cols):
                for j in range(self.num_rows):
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        tl = Point(self.x + (j * self.cell_x), self.y + (i * self.cell_y))
        br = Point(tl.x + self.cell_x, tl.y + self.cell_y)
        self._cells[i][j].draw(tl, br)
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].walls["N"] = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].walls["S"] = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            neighbors = self._get_unvisited_neighbors(i, j)
            if not neighbors:
                self._draw_cell(i, j)
                return
            dir = random.choice(list(neighbors.keys()))
            self._remove_wall((i, j), neighbors[dir], dir)
            self._break_walls_r(*neighbors[dir])

    def _can_move(self, i, j, dir):
        if dir == "N" and i == 0:
            return False
        if dir == "E" and j == self.num_rows - 1:
            return False
        if dir == "S" and i == self.num_cols - 1:
            return False
        if dir == "W" and j == 0:
            return False
        x, y = self._get_cell(i, j, dir)
        return not self._cells[i][j].walls[dir] and not self._cells[x][y].visited

    def _get_cell(self, i, j, dir):
        if dir == "N":
            return (i - 1, j)
        elif dir == "E":
            return (i, j + 1)
        elif dir == "S":
            return (i + 1, j)
        elif dir == "W":
            return (i, j - 1)

    def _get_unvisited_neighbors(self, i, j):
        neighbors = {}
        if i > 0 and not self._cells[i - 1][j].visited:
            neighbors["N"] = (i - 1, j)
        if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
            neighbors["E"] = (i, j + 1)
        if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
            neighbors["S"] = (i + 1, j)
        if j > 0 and not self._cells[i][j - 1].visited:
            neighbors["W"] = (i, j - 1)
        return neighbors
    
    def _remove_wall(self, cell1, cell2, dir):
        if dir == "N":
            self._cells[cell1[0]][cell1[1]].walls["N"] = False
            self._cells[cell2[0]][cell2[1]].walls["S"] = False
        elif dir == "E":
            self._cells[cell1[0]][cell1[1]].walls["E"] = False
            self._cells[cell2[0]][cell2[1]].walls["W"] = False
        elif dir == "S":
            self._cells[cell1[0]][cell1[1]].walls["S"] = False
            self._cells[cell2[0]][cell2[1]].walls["N"] = False
        elif dir == "W":
            self._cells[cell1[0]][cell1[1]].walls["W"] = False
            self._cells[cell2[0]][cell2[1]].walls["E"] = False
        self._draw_cell(cell1[0], cell1[1])
        self._draw_cell(cell2[0], cell2[1])

    def _reset_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        for dir in ["N", "E", "S", "W"]:
            if self._can_move(i, j, dir):
                x, y = self._get_cell(i, j, dir)
                self._cells[i][j].draw_move(self._cells[x][y])
                if self._solve_r(x, y):
                    return True
                self._cells[i][j].draw_move(self._cells[x][y], undo=True)
        return False


    def solve(self):
        return self._solve_r(0, 0)