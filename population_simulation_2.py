import numpy as np

def generate_population_grid(size, terrain_grid):
    population_grid = np.zeros_like(terrain_grid)
    initial_population_caps = np.zeros_like(terrain_grid)

    for y in range(size):
        for x in range(size):
            if terrain_grid[y][x] == 2:  # Field tile
                random_integer = np.random.randint(5, 11)
                initial_population_caps[y][x] = random_integer
                population_grid[y][x] = np.random.randint(1, random_integer + 1)

    return population_grid, initial_population_caps

def count_coast_adjacency(terrain_grid, x, y):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid):
                if terrain_grid[ny][nx] == 1:  # Sea tile
                    count += 1
    return count

def count_farmland_adjacency(terrain_grid, x, y):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid):
                if terrain_grid[ny][nx] == 6:  # Farmland tile
                    count += 1
    return count

def update_population_caps(initial_population_caps, terrain_grid, farmland_adjacency):
    population_caps = initial_population_caps.copy()
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 2:  # Town tile
                population_caps[y][x] += 3 * count_coast_adjacency(terrain_grid, x, y) + 5
            if terrain_grid[y][x] == 5:
                population_caps[y][x] += 3 * count_coast_adjacency(terrain_grid, x, y) + 5 * count_farmland_adjacency(terrain_grid, x, y)
    return population_caps

def simulate_population_growth(population_grid, initial_population_caps, terrain_grid, farmland_adjacency):
    population_caps = update_population_caps(initial_population_caps, terrain_grid, farmland_adjacency)
    
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 2:  # Field tile
                if population_grid[y][x] < population_caps[y][x]:
                    population_grid[y][x] += 1
                if population_grid[y][x] > 24:
                    terrain_grid[y][x] = 5  # Convert to town
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if (dx != 0 or dy != 0) and 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid):
                                if terrain_grid[ny][nx] == 2:  # Field tile
                                    terrain_grid[ny][nx] = 6  # Convert to farmland
            elif terrain_grid[y][x] == 5:  # Town tile
                if population_grid[y][x] < population_caps[y][x]:
                    population_grid[y][x] += 1

    return population_grid, terrain_grid


def update_farmland_adjacency(terrain_grid):
    farmland_adjacency = np.zeros_like(terrain_grid)
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 5:  # Town tile
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if (dx != 0 or dy != 0) and 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid):
                            if terrain_grid[ny][nx] == 6:  # Farmland tile
                                farmland_adjacency[ny][nx] += 1
    return farmland_adjacency