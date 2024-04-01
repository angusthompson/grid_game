import numpy as np
from terrain_generation import get_neighbors
import random

def generate_population_grid(size_y, size_x, terrain_grid):
    population_grid = np.zeros((size_y, size_x))
    initial_population_caps = np.zeros((size_y, size_x))

    # Randomly select one box for initial population
    initial_box_x = np.random.randint(size_x)
    initial_box_y = np.random.randint(size_y)

    # Ensure the selected box is a field (terrain type 2)
    while terrain_grid[initial_box_y][initial_box_x] != 2:
        initial_box_x = np.random.randint(size_x)
        initial_box_y = np.random.randint(size_y)

    for y in range(size_y):
        for x in range(size_x):
            if terrain_grid[y][x] == 2:  # Field tile
                random_integer = np.random.randint(5, 11)
                initial_population_caps[y][x] = random_integer

    # Allocate population between 1 and 5 in the selected box
    population_grid[initial_box_y][initial_box_x] = np.random.randint(1, 6)

    return population_grid, initial_population_caps


def initial_population_caps(terrain_grid):
    population_caps = np.zeros_like(terrain_grid)
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 2:  # Field tile
                population_caps[y][x] = np.random.randint(10, 21)
    return population_caps

def update_population_caps(initial_population_caps, terrain_grid):
    updated_population_caps = initial_population_caps.copy()
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 2 or terrain_grid[y][x] == 5 or terrain_grid[y][x] == 6:  # Field tile
                neighbor_types = get_neighbors(terrain_grid, x, y)
                sea_count = neighbor_types.count(1)  # Count adjacent sea tiles
                farmland_count = neighbor_types.count(6)  # Count adjacent farmland tiles
                town_count = neighbor_types.count(5) 
                updated_population_caps[y][x] += 5 * sea_count + 5 * farmland_count - 10 * town_count
    return updated_population_caps

def simulate_population_growth(population_grid, initial_population_caps, terrain_grid):
    population_caps = update_population_caps(initial_population_caps, terrain_grid)
    size = len(terrain_grid)
    
    for y in range(size):
        for x in range(size):
            if population_grid[y][x] > population_caps[y][x]:
                population_grid[y][x] -= 2
                if terrain_grid[y][x] == 2:
                    population_grid[y][x] -= 2
                if terrain_grid[y][x] == 3:
                    population_grid[y][x] -= 4
                if terrain_grid[y][x] == 4:
                    population_grid[y][x] -= 4
                if terrain_grid[y][x] == 5:
                    population_grid[y][x] -= 6
                if terrain_grid[y][x] == 6:
                    population_grid[y][x] -= 2
                # Find neighboring tiles
                neighbors = []
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if (dx != 0 or dy != 0) and 0 <= nx < size and 0 <= ny < size:
                            neighbors.append((nx, ny))
                # Select a random neighboring tile
                selected_tile = random.choice(neighbors)
                # Increase population of selected tile by 2
                population_grid[selected_tile[1]][selected_tile[0]] += 2
                
            if terrain_grid[y][x] == 2 or terrain_grid[y][x] == 6:  # Field tile
                if population_grid[y][x] > 0:
                    population_grid[y][x] += 1
                if population_grid[y][x] > 24:
                    terrain_grid[y][x] = 5  # Convert to town
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if (dx != 0 or dy != 0) and 0 <= nx < size and 0 <= ny < size:
                                if terrain_grid[ny][nx] == 2:  # Field tile
                                    terrain_grid[ny][nx] = 6  # Convert to farmland
            elif terrain_grid[y][x] == 5:  # Town tile
                if population_grid[y][x] < population_caps[y][x]:
                    population_grid[y][x] += 1
                if population_grid[y][x] < 25:
                    terrain_grid[y][x] = 6  # Convert back to fields


    return population_grid, terrain_grid




def generate_road_grid(size, terrain_grid, population_grid):
    # Initialize road grid with all zeros
    size = len(terrain_grid)
    road_grid = np.zeros((size, size), dtype=int)

    # Define terrain types where roads can be placed
    valid_terrain_types = [2, 3, 4, 5, 6]  # Assuming terrain types 2-6 represent valid terrain

    # Iterate through each tile in the grid
    for y in range(size):
        for x in range(size):
            # Check if the tile contains a town
            if terrain_grid[y][x] == 5:  # Assuming terrain type 5 represents towns
                # Find neighboring towns within a radius (e.g., five tiles)
                for ny in range(max(0, y - 5), min(size, y + 6)):
                    for nx in range(max(0, x - 5), min(size, x + 6)):
                        if terrain_grid[ny][nx] == 5 and (ny != y or nx != x):
                            # Determine the direction of the road between the current town and the neighboring town
                            dx, dy = nx - x, ny - y
                            steps = max(abs(dx), abs(dy))
                            dx //= steps
                            dy //= steps

                            # Trace a line of road tiles between the current town and the neighboring town
                            for i in range(1, steps):
                                tx, ty = x + dx * i, y + dy * i
                                if terrain_grid[ty][tx] not in valid_terrain_types:
                                    break # Stop tracing road if the tile is not a valid terrain type
                                else:
                                    road_grid[ty][tx] = 1  
                            break  # Stop searching for neighboring towns once one is found

    return road_grid
