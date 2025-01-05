from queue import PriorityQueue
import pygame

# Getting the sum of the absolute difference in x and y coordinates
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

#came_from, dictionary used to map each node, current, keeps track of the end node
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
    # Counter for tie-breaking in the priority queue

    # Initialize priority queue to maintain nodes to be explored and sorted by f_score
    count = 0

    # Priority queue to store nodes to explore, ordered by their f_score
    open_set = PriorityQueue()

    # Add the starting node to the open set with an initial f_score of 0
    open_set.put((0, count, start))

    # Dictionary to keep track of the most efficient path
    came_from = {}

    # g_score is the actual cost, f_score is the estimated total cost
    # Initialize g_score for all nodes to infinity, except the start node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0  # Cost from start to start is 0
    
    # Initialize f_score for all nodes to infinity, except the start node
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_position(), end.get_position())  # Estimate cost to reach the end from the start

    # Set to keep track of nodes currently in the open set
    open_set_hash = {start}

    # Main loop to process nodes in the open set
    # Continues to run when there are nodes to explore
    while not open_set.empty():
        # Handle user events (e.g., quitting the application)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the node with the lowest f_score from the priority queue
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # If we have reached the goal, reconstruct the path
        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()  # Mark the end node visually
            return path

        # Explore neighbors of the current node
        for neighbor in current.neighbors:

            # Calculate tentative g_score for the neighbor
            temp_g_score = g_score[current] + 1  # Assume a uniform cost of 1 for each step

            # If current g_score is lower than its neighbour's g_score
            if temp_g_score < g_score[neighbor]:

                # Updates came_from to indicate the current node as best
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                # Update f_score with the heuristic estimate
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())

                # If neighbor is not already in the open set, add it, allowing further exploration
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Mark the neighbor as being considered

        # Redraw the grid to visually update the search progress
        draw()

        # Mark the current node as processed if it is not the start node
        if current != start:
            current.make_closed()

def dijkstra_algorithm(draw, grid, start, end):
    # Counter for tie-breaking in the priority queue
    count = 0

    # Priority queue to store nodes to explore, ordered by their g_score
    open_set = PriorityQueue()

    # Add the starting node to the open set with an initial g_score of 0
    open_set.put((0, count, start))

    # Dictionary to keep track of the most efficient path
    came_from = {}

    # g_score is the actual cost
    # Initialize g_score for all nodes to infinity, except the start node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0  # Cost from start to start is 0

    # Set to keep track of nodes currently in the open set
    open_set_hash = {start}

    # Main loop to process nodes in the open set
    while not open_set.empty():
        # Handle user events (e.g., quitting the application)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the node with the lowest g_score from the priority queue
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # If we have reached the goal, reconstruct the path
        if current == end:
            path = reconstruct_path(came_from, end, draw)
            end.make_end()  # Mark the end node visually
            return path

        # Explore neighbors of the current node
        for neighbor in current.neighbors:
            # Calculate tentative g_score for the neighbor
            temp_g_score = g_score[current] + 1  # Assume a uniform cost of 1 for each step

            # If current g_score is lower than its neighbour's g_score
            if temp_g_score < g_score[neighbor]:
                # Updates came_from to indicate the current node as best
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score

                # If neighbor is not already in the open set, add it, allowing further exploration
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Mark the neighbor as being considered

        # Redraw the grid to visually update the search progress
        draw()

        # Mark the current node as processed if it is not the start node
        if current != start:
            current.make_closed()
