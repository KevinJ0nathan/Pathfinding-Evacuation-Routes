from constants import *
import pygame

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col
    
    def get_color(self):
         return self.color
    
    def is_closed(self):
        return self.color == RED
    
    def is_opened(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def is_path(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check the DOWN neighbor
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check the UP neighbor
        if (
            self.row > 0
            and not grid[self.row - 1][self.col].is_barrier()
        ):
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check the RIGHT neighbor
        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check the LEFT neighbor
        if (
            self.col > 0
            and not grid[self.row][self.col - 1].is_barrier()
        ):
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self,other):
        return False
    def __str__(self):
        return f"Node(row={self.row}, col={self.col})"
    
