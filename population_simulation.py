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
            if terrain_grid[y][x] == 2 or terrain_grid[y][x] == 5 or terrain_grid[y][x] == 6:  # Field tile
                population_neighbors, hunter_neighbors, farmer_neighbors = get_population_neighbors(population_grid, terrain_grid, x, y)
                sea_count = np.count_nonzero(terrain_grid[max(0, y - 1):min(size_y, y + 2), max(0, x - 1):min(size_x, x + 2)] == 1)
                farmland_count = np.count_nonzero(terrain_grid[max(0, y - 1):min(size_y, y + 2), max(0, x - 1):min(size_x, x + 2)] == 6)
                town_count = np.count_nonzero(terrain_grid[max(0, y - 1):min(size_y, y + 2), max(0, x - 1):min(size_x, x + 2)] == 5)
                
                # updated_population_caps[y][x] += 5 * sea_count + 5 * farmland_count - 10 * town_count
                updated_population_caps[y][x] -= 1 * hunter_neighbors
                if terrain_grid[y][x] == 2 or terrain_grid[y][x] == 5:
                    updated_population_caps[y][x] -= 1 * hunter_neighbors
                    updated_population_caps[y][x] += 0.5 * farmer_neighbors

                if terrain_grid[y][x] == 6:
                    updated_population_caps[y][x] += 0.5 * farmer_neighbors
                    updated_population_caps[y][x] += 1 * hunter_neighbors


                if updated_population_caps[y][x] < 0:
                    updated_population_caps[y][x] = 0
                # if updated_population_caps[y][x] < 3 and terrain_grid[y][x] == 2:
                #     updated_population_caps[y][x] = 3
    return updated_population_caps




# def simulate_population_growth(population_grid, initial_population_caps, terrain_grid):
#     population_caps = update_population_caps(initial_population_caps, terrain_grid)
#     sizey = len(terrain_grid)
#     sizex = len(terrain_grid[0])
    
#     for y in range(sizey):
#         for x in range(sizex):
#             if population_grid[y][x][1] > population_caps[y][x]:
#                 population_grid[y][x][1] -= 2
#                 if terrain_grid[y][x] == 2:
#                     population_grid[y][x][1] -= 2
#                 if terrain_grid[y][x] == 3:
#                     population_grid[y][x][1] -= 4
#                 if terrain_grid[y][x] == 4:
#                     population_grid[y][x][1] -= 4
#                 if terrain_grid[y][x] == 5:
#                     population_grid[y][x][1] -= 6
#                 if terrain_grid[y][x] == 6:
#                     population_grid[y][x][1] -= 2
#                 # Find neighboring tiles
#                 neighbors = []
#                 for dy in range(-1, 2):
#                     for dx in range(-1, 2):
#                         nx, ny = x + dx, y + dy
#                         if (dx != 0 or dy != 0) and 0 <= nx < sizex and 0 <= ny < sizey:
#                             neighbors.append((nx, ny))
#                 # Select a random neighboring tile
#                 selected_tile = random.choice(neighbors)
#                 # Increase population of selected tile by 2
#                 population_grid[selected_tile[1]][selected_tile[0]][1] += 2
                
#             if terrain_grid[y][x] == 2 or terrain_grid[y][x] == 6:  # Field tile
#                 if population_grid[y][x][1] > 0:
#                     population_grid[y][x][1] += 1
#                 if population_grid[y][x][1] < 1:
#                     terrain_grid[y][x] = 2  # Convert back to fields
#                 if population_grid[y][x][1] > 24:
#                     terrain_grid[y][x] = 5  # Convert to town
#                     for dy in range(-1, 2):
#                         for dx in range(-1, 2):
#                             nx, ny = x + dx, y + dy
#                             if (dx != 0 or dy != 0) and 0 <= nx < sizex and 0 <= ny < sizey:
#                                 if terrain_grid[ny][nx] == 2:  # Field tile
#                                     terrain_grid[ny][nx] = 6  # Convert to farmland
#                                     population_grid[ny][nx][1] +=1
#             elif population_grid[y][x][1] > 40:
#                 terrain_grid[y][x] = 7  # Convert to city
#             elif terrain_grid[y][x] == 5:  # Town tile
#                 if population_grid[y][x][1] < population_caps[y][x]:
#                     population_grid[y][x][1] += 1
#                 if population_grid[y][x][1] < 25:
#                     terrain_grid[y][x] = 6  # Convert back to fields

#     for y in range(sizey):
#         for x in range(sizex):
#             population_grid[y][x][0] = sum(population_grid[y][x][1:])


#     return population_grid, terrain_grid

import random

def simulate_population_growth(current_tribe_location, population_grid, updated_population_caps, terrain_grid):
    size_y, size_x, _ = population_grid.shape
    currentx, currenty = current_tribe_location
    if population_grid[currenty][currentx][0] == 0:
        population_grid[currenty][currentx][1] = 3

    for y in range(size_y):
        for x in range(size_x):
            if population_grid[y][x][0] < 0:
                population_grid[y][x][0] = 0
            if population_grid[y][x][1] < 0:
                population_grid[y][x][1] = 0
            if population_grid[y][x][2] < 0:
                population_grid[y][x][2] = 0
            if population_grid[y][x][3] < 0:
                population_grid[y][x][3] = 0
            if terrain_grid[y][x] < 5:
                # Calculate the population growth based on existing hunter-gatherers
                population_growth = int(round(0.5 * population_grid[y][x][1]))
                # Update the hunter-gatherer population in the tile
                population_grid[y][x][1] += population_growth
            elif terrain_grid[y][x] == 6:
                # Calculate the population growth based on existing farmers
                population_growth = int(round(0.5 * population_grid[y][x][2]))
                population_grid[y][x][2] += population_growth
                # Update the farmer population in the tile
                if population_grid[y][x][1] > 0:
                    population_grid[y][x][1] -= (population_growth/2 + 1)
                # Calculate the population growth based on existing farmers
                population_growth = int(round(0.5 * population_grid[y][x][2]))
                population_grid[y][x][3] += population_growth
                # Update the farmer population in the tile
                if population_grid[y][x][1] > 0:
                    population_grid[y][x][1] -= (population_growth/2 + 1)
                if population_grid[y][x][0] > 25:
                    terrain_grid[y][x] = 5
                    population_grid[y][x][2] -= 12
                    population_grid[y][x][3] += 12
        
    
    # Attrition mechanics
    for y in range(size_y):
        for x in range(size_x):
            total_population = int(sum(population_grid[y][x][1:]))
            population_cap = updated_population_caps[y][x]
            if total_population > population_cap:
                # Reduce population in the overpopulated tile
                over = math.ceil((total_population - population_cap) / 2)
                xcurrent, ycurrent = current_tribe_location
                if population_grid[y][x][1] > 0:
                    if y != ycurrent or x != xcurrent:
                        population_grid[y][x][1] -= over * 1.9 - 1
                    else:
                        population_grid[y][x][1] -= over
                    if over > 5:
                        over = 5
                    # Find neighboring tiles
                    neighbors = []
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if (dx != 0 or dy != 0) and 0 <= nx < size_x and 0 <= ny < size_y:
                                neighbors.append((nx, ny))
                    # Select a random neighboring tile
                    selected_tile = random.choice(neighbors)
                    # Increase population of selected tile by 2
                    population_grid[selected_tile[1]][selected_tile[0]][1] += over
                if total_population > population_cap:
                    if population_grid[y][x][2] > 0:
                        if y != ycurrent or x != xcurrent:
                            population_grid[y][x][2] -= over * 1.9 - 1
                        else:
                            population_grid[y][x][2] -= over
                        if over > 5:
                            over = 5
                        # Find neighboring tiles
                        neighbors = []
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                nx, ny = x + dx, y + dy
                                if (dx != 0 or dy != 0) and 0 <= nx < size_x and 0 <= ny < size_y:
                                    neighbors.append((nx, ny))
                        # Select a random neighboring tile
                        selected_tile = random.choice(neighbors)
                        # Increase population of selected tile by 2
                        population_grid[selected_tile[1]][selected_tile[0]][2] += over
                        if terrain_grid[selected_tile[1]][selected_tile[0]] == 2:
                            terrain_grid[selected_tile[1]][selected_tile[0]] = 6
    
    # Update the total population count for each tile
    for y in range(size_y):
        for x in range(size_x):
            population_grid[y][x][0] = int(sum(population_grid[y][x][1:]))
    
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