import numpy as np
import random

def generate_terrain_grid(size_x, size_y, num_iterations=5):
    # Generate initial terrain grid separately for x and y axes
    terrain_grid = np.random.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4], size=(size_y, size_x))
    
    # Apply clustering algorithm
    for _ in range(num_iterations):
        terrain_grid = update_terrain_grid(terrain_grid)
    
    return terrain_grid


# Function to update terrain grid to favor clusters of the same terrain type
def update_terrain_grid(terrain_grid):
    new_terrain_grid = np.zeros_like(terrain_grid)
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            neighbors = get_neighbors(terrain_grid, x, y)
            most_common_neighbor = max(set(neighbors), key=neighbors.count)
            random_integer = random.randint(0, 10)
            if random_integer > 2:
                new_terrain_grid[y][x] = most_common_neighbor
            else:
                new_terrain_grid[y][x] = terrain_grid[y][x]
    return new_terrain_grid

# Function to get neighbors of a cell
def get_neighbors(grid, x, y):
    neighbors = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx != x or ny != y):
                neighbors.append(grid[ny][nx])
    return neighbors
