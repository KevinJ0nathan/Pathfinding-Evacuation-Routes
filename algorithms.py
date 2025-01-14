from queue import PriorityQueue
import pygame

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        current.make_path()
        draw()
    path.reverse()  # Reverse the path to start from the beginning
    return path

def a_star_algorithm(draw, grid, start, end):

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_position(), end.get_position())

    open_set_hash = {start}

    # Define possible movements (including diagonals)
    movements = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vertical and horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            return path

        for dx, dy in movements:
            neighbor_row = current.row + dx
            neighbor_col = current.col + dy

            if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):  # Stay within bounds
                neighbor = grid[neighbor_row][neighbor_col]

                if not neighbor.is_barrier():  # Skip barriers
                    # Cost is sqrt(2) for diagonal moves, 1 for straight moves
                    cost = 1 if dx == 0 or dy == 0 else 1.414
                    temp_g_score = g_score[current] + cost

                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())

                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return None


def refactored_a_star_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    # Store g_score and f_score only for nodes in open_set
    g_score = {start: 0}
    f_score = {start: h(start.get_position(), end.get_position())}

    open_set_hash = {start}

    # Define possible movements (including diagonals)
    movements = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vertical and horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            return path

        for dx, dy in movements:
            neighbor_row = current.row + dx
            neighbor_col = current.col + dy

            if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):  # Stay within bounds
                neighbor = grid[neighbor_row][neighbor_col]

                if not neighbor.is_barrier():  # Skip barriers
                    # Cost is sqrt(2) for diagonal moves, 1 for straight moves
                    cost = 1 if dx == 0 or dy == 0 else 1.414
                    temp_g_score = g_score.get(current, float("inf")) + cost

                    if temp_g_score < g_score.get(neighbor, float("inf")):  # Safely retrieve g_score
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())

                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    print("No path found!")  # Add a message if no path is found
    return None


def dijkstra_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}

    # Define possible movements (including diagonals)
    movements = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vertical and horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()
            return path

        for dx, dy in movements:
            neighbor_pos = (current.row + dx, current.col + dy)
            if 0 <= neighbor_pos[0] < len(grid) and 0 <= neighbor_pos[1] < len(grid[0]):  # Stay within bounds
                neighbor = grid[neighbor_pos[0]][neighbor_pos[1]]
                if not neighbor.is_barrier():  # Skip barriers
                    # Cost is sqrt(2) for diagonal moves, 1 for straight moves
                    cost = 1 if dx == 0 or dy == 0 else 1.414
                    temp_g_score = g_score[current] + cost

                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((g_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return None