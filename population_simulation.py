import numpy as np
from terrain_generation import get_neighbors, get_population_neighbors
import random
import math

def generate_population_grid(size_y, size_x, terrain_grid):
    # population_grid = np.zeros((size_y, size_x))
    population_grid = np.zeros((size_y, size_x, 8), dtype=int)

    initial_population_caps = np.zeros((size_y, size_x))

    # Randomly select one box for initial population
    initial_box_x = np.random.randint(20,size_x-20)
    initial_box_y = np.random.randint(15,size_y-15)

    # Ensure the selected box is a field (terrain type 2)
    while terrain_grid[initial_box_y][initial_box_x] != 2:
        initial_box_x = np.random.randint(20,size_x-20)
        initial_box_y = np.random.randint(15,size_y-15)

    for y in range(size_y):
        for x in range(size_x):
            if terrain_grid[y][x] == 2:  # Field tile
                random_integer = np.random.randint(5, 11)
                initial_population_caps[y][x] = random_integer

    # Allocate population between 1 and 5 in the selected box
    population_grid[initial_box_y][initial_box_x][1] = np.random.randint(2, 6)
    for y in range(size_y):
        for x in range(size_x):
            population_grid[y][x][0] = sum(population_grid[y][x][1:])

    return population_grid, initial_population_caps


def initial_population_caps(terrain_grid):
    population_caps = np.zeros_like(terrain_grid)
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 2:  # Field tile
                population_caps[y][x] = np.random.randint(10, 21)
    return population_caps








def update_population_caps(initial_population_caps, terrain_grid, population_grid):
    updated_population_caps = initial_population_caps.copy()
    size_y, size_x = terrain_grid.shape  # Get the shape of the terrain grid

    for y in range(size_y):
        for x in range(size_x):
            population_grid[y][x][0] = sum(population_grid[y][x][1:])
            population_neighbors, hunter_neighbors, farmer_neighbors, merchant_neighbors = get_population_neighbors(population_grid, terrain_grid, x, y)
            sea_count = np.count_nonzero(terrain_grid[max(0, y - 1):min(size_y, y + 2), max(0, x - 1):min(size_x, x + 2)] == 1)
            farmland_count = np.count_nonzero(terrain_grid[max(0, y - 1):min(size_y, y + 2), max(0, x - 1):min(size_x, x + 2)] == 6)
            town_count = np.count_nonzero(terrain_grid[max(0, y - 1):min(size_y, y + 2), max(0, x - 1):min(size_x, x + 2)] == 5)

            if terrain_grid[y][x] == 2 and hunter_neighbors > 1:  # Pop caps for fields
                updated_population_caps[y][x] -= 1 * hunter_neighbors
                updated_population_caps[y][x] -= 0.3 * farmer_neighbors
                updated_population_caps[y][x] -= 0.3 * merchant_neighbors

            if terrain_grid[y][x] == 5:  # Pop caps for towns
                updated_population_caps[y][x] -= 0.3 * hunter_neighbors
                updated_population_caps[y][x] += 0.5 * farmer_neighbors
                updated_population_caps[y][x] -= 0.3 * merchant_neighbors
                updated_population_caps[y][x] += 3 * sea_count
                updated_population_caps[y][x] -= 0.2 * population_grid[y][x][3]

            if terrain_grid[y][x] == 6:  # Pop caps for farmlands
                updated_population_caps[y][x] += 10
                updated_population_caps[y][x] -= 0.2 * hunter_neighbors
                updated_population_caps[y][x] += 0.1 * farmer_neighbors
                updated_population_caps[y][x] += 0.3 * merchant_neighbors
                updated_population_caps[y][x] -= 0.1 * population_grid[y][x][2]
                updated_population_caps[y][x] -= 0.2 * population_grid[y][x][3]

    
    population_grid[y][x][0] = sum(population_grid[y][x][1:])

    return updated_population_caps

def simulate_population_growth(current_tribe_location, population_grid, updated_population_caps, terrain_grid):
    size_y, size_x, _ = population_grid.shape
    currentx, currenty = current_tribe_location

    for y in range(size_y):
        for x in range(size_x):
            population_neighbors, hunter_neighbors, farmer_neighbors, merchant_neighbors = get_population_neighbors(population_grid, terrain_grid, x, y)
            if population_grid[y][x][0] > 0:
                population_grid[y][x][0] = sum(population_grid[y][x][1:])
                # for n in population_grid[y][x][n]:        # Check that no pops are negative
                #     if population_grid[y][x][n] < 0:
                #         population_grid[y][x][n] = 0

                pop_cap = updated_population_caps[y][x]

                if population_grid[y][x][0] > 0:    # Mechanics for pop growth
                    if terrain_grid[y][x] == 2:            # Growth in fields
                        population_grid[y][x][1] += population_grid[y][x][1]*0.5
                        if population_grid[y][x][0] < 5:
                            population_grid[y][x][1] += 1
                        population_grid[y][x][1] -= 0.2 * hunter_neighbors
                        population_grid[y][x][1] -= 0.3 * farmer_neighbors

                    elif terrain_grid[y][x] == 6:            # Growth in farmlands
                        population_grid[y][x][2] += population_grid[y][x][2]
                        population_grid[y][x][1] -= (population_grid[y][x][2]*0.5 + 1)
                        population_grid[y][x][2] -= 0.2 * hunter_neighbors
                        if population_grid[y][x][1] < 0:
                            population_grid[y][x][1] = 0
                        if population_grid[y][x][2] < 0:
                            population_grid[y][x][2] = 0

                    elif terrain_grid[y][x] == 5:            # Growth in towns
                        population_grid[y][x][2] -= population_grid[y][x][2]*0.5
                        population_grid[y][x][3] += population_grid[y][x][2]*0.3
                        population_grid[y][x][3] += population_grid[y][x][3]*0.3
                        population_grid[y][x][3] += 0.2 * farmer_neighbors
                        if population_grid[y][x][2] < 0:
                            population_grid[y][x][2] =0

    return population_grid, terrain_grid


def simulate_population_attrition(current_tribe_location, population_grid, updated_population_caps, terrain_grid):
    size_y, size_x, _ = population_grid.shape
    currentx, currenty = current_tribe_location

    for y in range(size_y):
        for x in range(size_x):
            population_neighbors, hunter_neighbors, farmer_neighbors, merchant_neighbors = get_population_neighbors(population_grid, terrain_grid, x, y)
            pop_cap = updated_population_caps[y][x]

            population_grid[y][x][0] = sum(population_grid[y][x][1:])
            if population_grid[y][x][0] > pop_cap and population_grid[y][x][0] > 0:    # Mechanics for pop attrition

                # Find neighboring tiles
                neighbors = []
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if (dx != 0 or dy != 0) and 0 <= nx < size_x and 0 <= ny < size_y:
                            neighbors.append((nx, ny))
                # Select a random neighboring tile
                selected_tile = random.choice(neighbors)

                over = population_grid[y][x][0] - pop_cap

                if terrain_grid[y][x] == 1 or terrain_grid[y][x] == 3 or terrain_grid[y][x] == 4:            # Attrition in sea, deser, mountain
                    population_grid[y][x][1] -= (over * 0.5 + 1)
                    population_grid[selected_tile[1]][selected_tile[0]][1] += (over * 0.5)      # Emigration
                    if population_grid[y][x][1] < 0:
                        over = -population_grid[y][x][1]
                        population_grid[y][x][1] = 0
                        population_grid[y][x][3] -= (over * 0.5 + 1)
                        if population_grid[y][x][3] < 0:
                            population_grid[y][x][3] = 0

                if terrain_grid[y][x] == 2:            # Attrition in fields
                    population_grid[y][x][1] -= (over * 0.5 + 1)
                    population_grid[selected_tile[1]][selected_tile[0]][1] += (over * 0.5)      # Emigration
                    if population_grid[y][x][1] < 0:
                        over = -population_grid[y][x][1]
                        population_grid[y][x][1] = 0
                        population_grid[y][x][3] -= (over * 0.5 + 1)
                        if population_grid[y][x][3] < 0:
                            population_grid[y][x][3] = 0

                elif terrain_grid[y][x] == 6:            # Attrition in farmlands
                    population_grid[y][x][1] -= (over + 1)
                    population_grid[selected_tile[1]][selected_tile[0]][1] += (over * 0.5)      # Emigration
                    if population_grid[y][x][1] < 0:
                        over = -population_grid[y][x][1]
                        population_grid[y][x][1] = 0
                        population_grid[y][x][2] -= (over * 0.5 + 1)
                        population_grid[selected_tile[1]][selected_tile[0]][2] += (over * 0.5)      # Emigration
                        if population_grid[y][x][2] < 0:
                            # over = -population_grid[y][x][2]
                            population_grid[y][x][2] = 0
                            # population_grid[y][x][3] -= (over * 0.5 + 1)
                            # population_grid[selected_tile[1]][selected_tile[0]][3] += (over * 0.5)      # Emigration
                            # if population_grid[y][x][3] < 0:
                            #     population_grid[y][x][3] = 0

                elif terrain_grid[y][x] == 5:            # Attrition in towns
                    population_grid[y][x][1] -= (over + 1)
                    population_grid[selected_tile[1]][selected_tile[0]][1] += (over * 0.5)      # Emigration
                    if population_grid[y][x][1] < 0:
                        over = -population_grid[y][x][1]
                        population_grid[y][x][1] = 0
                        population_grid[y][x][2] -= (over + 1)
                        population_grid[selected_tile[1]][selected_tile[0]][2] += (over * 0.5)      # Emigration
                        if population_grid[y][x][2] < 0:
                            over = -population_grid[y][x][2]
                            population_grid[y][x][2] = 0
                            population_grid[y][x][3] -= (over * 0.5 + 1)
                            population_grid[selected_tile[1]][selected_tile[0]][3] += (over * 0.5)      # Emigration
                            if population_grid[y][x][3] < 0:
                                population_grid[y][x][3] = 0
                
                if population_grid[y][x][0] > updated_population_caps[y][x]:
                    if terrain_grid[y][x] == 2:
                        population_grid[y][x][1] = pop_cap
                        population_grid[y][x][2] = 0
                        population_grid[y][x][3] = 0
                    if terrain_grid[y][x] == 6:
                        population_grid[y][x][1] = 0
                        population_grid[y][x][2] = pop_cap
                        population_grid[y][x][3] = 0
                    if terrain_grid[y][x] == 5:
                        population_grid[y][x][1] = 0
                        population_grid[y][x][2] = 0
                        population_grid[y][x][3] = pop_cap

                    

            population_grid[y][x][0] = int(sum(population_grid[y][x][1:]))      # Terrain development mechanics
            if terrain_grid[y][x] == 2 and population_grid[y][x][2] > 0:
                terrain_grid[y][x] = 6
            if terrain_grid[y][x] == 2 and population_grid[y][x][2] > 30:
                terrain_grid[y][x] = 5
            if terrain_grid[y][x] == 5 and population_grid[y][x][0] < 20:
                terrain_grid[y][x] = 2
            # if terrain_grid[y][x] == 1 and population_grid[y][x][0] > 2:
            #     population_grid[y][x][1] = 2    
    
    if population_grid[currenty][currentx][0] == 0:
        population_grid[currenty][currentx][1] = 3
    population_grid[y][x][0] = sum(population_grid[y][x][1:])

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