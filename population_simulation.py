import numpy as np
import random

def simulate_population_growth(population_grid, population_caps, terrain_grid):
    excess_population = np.zeros_like(population_grid)
    farmland_generated = np.zeros_like(terrain_grid)
    for y in range(len(population_grid)):
        for x in range(len(population_grid[y])):
            if terrain_grid[y][x] == 2:  # Fields
                # Population growth
                population_grid[y][x] += 1
                if population_grid[y][x] > 25:
                    # Population cap adjustments
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < len(population_caps[0]) and 0 <= ny < len(population_caps):
                                if terrain_grid[ny][nx] == 2:
                                    population_caps[ny][nx] += 3
                                elif terrain_grid[ny][nx] == 3:  # If neighboring tile is mountain
                                    population_caps[ny][nx] -= 3
                                    if population_caps[ny][nx] < 0:
                                        excess_population[ny][nx] -= population_caps[ny][nx]
                                        population_caps[ny][nx] = 0
                                elif terrain_grid[ny][nx] == 5:  # If neighboring tile is town
                                    if terrain_grid[y][x] == 2:  # If current tile is a field
                                        farmland_generated[y][x] = 1
                    terrain_grid[y][x] = 5  # Change current tile to town
                    excess_population[y][x] += population_grid[y][x] - 25
                    population_grid[y][x] = 25
    # Generate farmlands
    for y in range(len(farmland_generated)):
        for x in range(len(farmland_generated[y])):
            if farmland_generated[y][x]:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid):
                            if terrain_grid[ny][nx] == 2:  # If neighboring tile is a field
                                terrain_grid[ny][nx] = 6  # Change to farmland
    population_grid += excess_population
    # Ensure population doesn't exceed population caps
    population_grid = np.minimum(population_grid, population_caps)

# Function to generate population grid and population caps
def generate_population_grid(size, terrain_grid):
    population_grid = np.zeros((size, size), dtype=int)
    population_caps = np.zeros((size, size), dtype=int)
    for y in range(size):
        for x in range(size):
            if terrain_grid[y][x] == 2:  # Fields
                max_population = random.randint(5, 15)
                coast_adjacency = count_coast_adjacency(terrain_grid, x, y)
                max_population += 3 * coast_adjacency
                population_grid[y][x] = random.randint(5, 10)  # Random initial population between 5 and 10
                population_caps[y][x] = max_population
    return population_grid, population_caps

# Function to count the number of coast tiles adjacent to a cell
def count_coast_adjacency(terrain_grid, x, y):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid):
                if terrain_grid[ny][nx] == 1:  # Coast
                    count += 1
    return count