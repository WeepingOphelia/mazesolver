from artbox import Window, Point
from mazeclass import Maze


def main():
    matrix_dims = (12, 16)
    margin = 50
    origin = Point(margin, margin)
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / matrix_dims[1]
    cell_size_y = (screen_y - 2 * margin) / matrix_dims[0]
    win = Window(screen_x, screen_y)

    maze = Maze(origin, matrix_dims, (cell_size_x, cell_size_y), win)

    win.wait_for_close()

main()