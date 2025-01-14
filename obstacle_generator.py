import random

# Generate all positions in a 50x50 grid
all_positions = [(x, y) for x in range(50) for y in range(50)]

# Shuffle the positions to randomize
random.shuffle(all_positions)

# Use the randomized list of positions
predefined_obstacles = all_positions

# Example: Print the first 250 for visualization
print(predefined_obstacles)
