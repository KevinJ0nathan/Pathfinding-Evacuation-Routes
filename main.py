import pygame
import math
from constants import *
from astar import *
from node import Node
from survivor import Survivor

# Setting the width and caption of the window
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Evacuation Route Path Finding")

# Making the grid of the map
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
                node = Node(i, j, gap, rows)
                grid[i].append(node)
    
    return grid

# Draw the grid on the screen
def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE)
    # Color each node
    for row in grid:
        for node in row:
            node.draw(window)
    # Draw the grid over the screen
    draw_grid(window, rows, width)
    pygame.display.update()

# Get row and column of the position of the mouse when its clicked
def get_clicked_position(position, rows, width):
    gap = width // rows
    y, x = position
    row = y // gap
    col = x // gap

    return row, col

# Main loop
def main(window, width):
    # Constants for map
    ROWS = 50
    grid = make_grid(ROWS, width)

    # Constants for
    start = None
    end = None
    survivor = None
    
    run = True
    path = []
    dup_path = []
    survivors = 0
    while run:
        draw(window, grid, ROWS, width)

        # When the survivor is traversing the path
        if survivor and path:
            next_node = path.pop(0)
            survivor.move_to(next_node)
            survivor.draw(window)
            pygame.display.update()
            pygame.time.delay(30)

        # When the survivor reached the path
        elif survivor and not path:
            path = dup_path[:]
            survivors += 1
            print(survivors)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # If left mouse button get pressed
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                # If the start node is not created yet, create a start node
                if not start and node != end:
                    start = node
                    start.make_start()
                # If the end node is not created yet, create an end node
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            # If right mouse button get pressed, reset the nodes
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path = dijkstra_algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)
                    if path:
                        survivor = Survivor(start)
                        dup_path = path[:]

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    survivor = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WINDOW, WIDTH)