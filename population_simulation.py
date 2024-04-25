import numpy as np
from terrain_generation import get_neighbors, get_population_neighbors, get_name
from economy import generate_state, add_to_state
import random
import math
from parameters import WHITE
import time

def find_towns(population_grid, towns, states, territories, terrain_grid):
    z = 0
    for i in towns:
        town = towns[z]
        x = town['position_x']
        y = town['position_y']
        if territories[y][x] == 0:
            states, territories, town = generate_state(z, town, x, y, states, territories, terrain_grid)
            towns[z] = town
        else:
            n = territories[y][x]
            add_to_state(z, n, town, x, y, states, territories, terrain_grid)
        z += 1
    return towns

def generate_population_grid(size_y, size_x, terrain_grid):
    population_grid = np.zeros((size_y, size_x, 8), dtype=int)
    territories = np.zeros((size_y, size_x), dtype=int)
    print("empty population and territories grids initialised")
    towns = []
    states = []

    # Create a placeholder for initial_population_caps_grid
    initial_population_caps_grid = None

    # Add a placeholder state
    states.append({"name": 'blank', "state": 0, "colour": WHITE, "towns": ('none'), "commodities": 0,
                   "tax_rev": 0, "population_counts": (0, 0, 0, 0, 0, 0, 0, 0), "expansionism": 0, "military_power": 0,
                   "noble_growth": 0, "unrest": 0, "status": 'Primitive Accumulation', "index": 0, "capital": 'none'})
    print("states initialised")
    # Populate initial_population_caps_grid lazily when needed
    def get_initial_population_caps_grid():
        nonlocal initial_population_caps_grid
        if initial_population_caps_grid is None:
            initial_population_caps_grid = np.zeros((size_y, size_x))
            for y in range(size_y):
                for x in range(size_x):
                    if terrain_grid[y][x] == 2:  # Field tile
                        random_integer = np.random.randint(5, 11)
                        initial_population_caps_grid[y][x] = random_integer
        return initial_population_caps_grid

    print("initial pop caps grid function written")
    time.sleep(0.5)
    # Randomly select one box for initial population
    initial_box_x = np.random.randint(20, size_x - 20)
    initial_box_y = np.random.randint(15, size_y - 15)
    print("initial position selected")
    time.sleep(0.5)

    # Ensure the selected box is a field (terrain type 2)
    count = 0
    while terrain_grid[initial_box_y][initial_box_x] != 2 and count < 6:
        initial_box_x = np.random.randint(20, size_x - 20)
        initial_box_y = np.random.randint(15, size_y - 15)
        time.sleep(0.05)
        count += 1
    else: terrain_grid[initial_box_y][initial_box_x] = 2
    
    print("initial position confirmed")
    time.sleep(0.5)

    # Allocate population between 3 and 5 in the selected box
    population_grid[initial_box_y][initial_box_x][1] = np.random.randint(2, 6)
    print("initial population allocated")
    time.sleep(0.5)
    for y in range(size_y):
        for x in range(size_x):
            population_grid[y][x][0] = sum(population_grid[y][x][1:])

    print("eve's tribe created")
    return population_grid, get_initial_population_caps_grid(), towns, states, territories

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
                if updated_population_caps[y][x] < 0: updated_population_caps[y][x] = 5

            if terrain_grid[y][x] == 5:  # Pop caps for towns
                updated_population_caps[y][x] = 20
                updated_population_caps[y][x] += 0.15 * farmer_neighbors
                updated_population_caps[y][x] -= 0.2 * merchant_neighbors
                updated_population_caps[y][x] -= 0.2 * hunter_neighbors
                updated_population_caps[y][x] += 4 * sea_count
                # updated_population_caps[y][x] -= 0.1 * population_grid[y][x][3]

            if terrain_grid[y][x] == 6:  # Pop caps for farmlands
                updated_population_caps[y][x] = 10
                updated_population_caps[y][x] += 2 * sea_count
                updated_population_caps[y][x] -= 2 * town_count
                updated_population_caps[y][x] -= 0.2 * hunter_neighbors
                updated_population_caps[y][x] += 0.1 * farmer_neighbors
                # updated_population_caps[y][x] -= 0.2 * merchant_neighbors
                # updated_population_caps[y][x] -= 0.1 * population_grid[y][x][2]
                updated_population_caps[y][x] -= 0.3 * population_grid[y][x][3]
    
    population_grid[y][x][0] = sum(population_grid[y][x][1:])
    if updated_population_caps[y, x] < 0:
        updated_population_caps[y, x] = 0

    return updated_population_caps

def simulate_population_growth(current_tribe_location, population_grid, updated_population_caps, terrain_grid, y, x, states, territories):
    currentx, currenty = current_tribe_location
    population_neighbors, hunter_neighbors, farmer_neighbors, merchant_neighbors = get_population_neighbors(population_grid, terrain_grid, x, y)
    if updated_population_caps[y][x] < 0: updated_population_caps[y][x] = 5
    if population_grid[y][x][0] > 0:
        population_grid[y][x][0] = sum(population_grid[y][x][1:])
        if population_grid[y][x][0] < 0:
            population_grid[y][x][0] = 0

        pop_cap = updated_population_caps[y][x]

        if population_grid[y][x][0] > 0:    # Mechanics for pop growth
            if terrain_grid[y][x] == 2:            # Growth in fields
                population_grid[y][x][1] += population_grid[y][x][1]*0.5
                if population_grid[y][x][0] < 5:
                    population_grid[y][x][1] += 1
                population_grid[y][x][1] -= 0.2 * hunter_neighbors
                population_grid[y][x][1] -= 0.3 * farmer_neighbors

            elif terrain_grid[y][x] == 6:            # Growth in farmlands
                population_grid[y][x][2] += 0.5*population_grid[y][x][2]
                population_grid[y][x][1] -= (population_grid[y][x][2]*0.5 + 2)
                # population_grid[y][x][2] += 0.2 * hunter_neighbors

            elif terrain_grid[y][x] == 5:            # Growth in towns
                if population_grid[y][x][2] > 0:
                    population_grid[y][x][3] += population_grid[y][x][2]*0.2
                    population_grid[y][x][2] -= population_grid[y][x][2]*0.1
                population_grid[y][x][3] += population_grid[y][x][3]*0.1
                population_grid[y][x][3] += 0.1 * farmer_neighbors
                population_grid[y][x][3] -= 0.1 * merchant_neighbors
                # population_grid[y][x][5] += 0.2 * farmer_neighbors
                # population_grid[y][x][5] += population_grid[y][x][5]
                # population_grid[y][x][6] += 0.1 * population_grid[y][x][4]
                # population_grid[y][x][6] += 0.1 * population_grid[y][x][5]
                # population_grid[y][x][4] -= 0.1 * population_grid[y][x][6]

                if territories[y][x] != 0:
                    n = territories[y][x]
                    state = states[n-1]
                    if state["commodities"] < -10 and population_grid[y][x][3] > 4 and random.randint(1, 20) > 15:
                        population_grid[y][x][3] -= 4
                        population_grid[y][x][5] += 3
                        population_grid[y][x][6] += 1

    if population_grid[y][x][1] < 0:
        population_grid[y][x][1] = 0
    if population_grid[y][x][2] < 0:
        population_grid[y][x][2] = 0
    if population_grid[y][x][3] < 0:
        population_grid[y][x][3] = 0

    if population_grid[currenty][currentx][0] < 3:
        population_grid[currenty][currentx][1] = 3
    if updated_population_caps[y][x] < 0: updated_population_caps[y][x] = 5

    return population_grid, terrain_grid

def simulate_population_attrition(population_grid, updated_population_caps, terrain_grid, towns, states, territories, y, x):
    size_y, size_x = terrain_grid.shape
    if updated_population_caps[y][x] < 0: updated_population_caps[y][x] = 5
    pop_cap = updated_population_caps[y][x]
    population_grid[y][x][0] = sum(population_grid[y][x][1:])

    if population_grid[y][x][0] < 0:
        for n in range(len(population_grid[y][x])):
            population_grid[y][x][n] = 0

    excess_pops = population_grid[y][x][0] - pop_cap
    if excess_pops > 0:
        if population_grid[y][x][0] > pop_cap and population_grid[y][x][0] > 0:    # Mechanics for pop attrition
            least_populated = 1000
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if (dx != 0 or dy != 0) and 0 <= nx < size_x and 0 <= ny < size_y:
                        population = population_grid[ny][nx][0]
                        if population < least_populated:
                            least_populated = population
                            least_populated_neighbors = [(nx, ny)]
                        elif population == least_populated:
                            least_populated_neighbors.append((nx, ny))

            selected_tile = random.choice(least_populated_neighbors)

            excess_pops = population_grid[y][x][0] - pop_cap

            rx, ry = selected_tile

            for p in range(len(population_grid[y][x])):
                migrants = 0
                if p == 0:
                    pass
                elif excess_pops == 0:
                    pass
                elif excess_pops > population_grid[y][x][p]:
                    excess_pops -= population_grid[y][x][p]
                    migrants += round(population_grid[y][x][p]/2, 2)
                    population_grid[y][x][p] = 0
                elif excess_pops <= population_grid[y][x][p]:
                    population_grid[y][x][p] -= excess_pops
                    migrants += round(excess_pops/2, 2)
                    excess_pops = 0
                if terrain_grid[y][x] == 1:
                    survival = np.random.randint(1, 20)
                    if survival > 10:
                        migrants = migrants*2
                if migrants > 5: migrants = 5
                if migrants < 0: migrants = 0
                if updated_population_caps[y][x] < 0: updated_population_caps[y][x] = 5
                population_grid[ry][rx][p] += migrants
    
    population_grid[y][x][0] = sum(population_grid[y][x][1:])
    if population_grid[y][x][0] < 0:
        for n in range(len(population_grid[y][x])):
            population_grid[y][x][n] = 0

    if updated_population_caps[y][x] < 0: updated_population_caps[y][x] = 5

    return population_grid, terrain_grid, towns, states, territories

def terrain_development(terrain_grid, population_grid, updated_population_caps, towns, states, territories, y, x):
    settlement_decision = np.random.randint(0, 20)
    if terrain_grid[y][x] == 2 and population_grid[y][x][2] > 0:                #Farmers colonise new land         
        if settlement_decision + population_grid[y][x][2] > 15: terrain_grid[y][x] = 6
    if population_grid[y][x][1] > 19 and terrain_grid[y][x] == 2:              #Decision for AI hunter-gatherers to become farmers
        if settlement_decision > 13:
            terrain_grid[y][x] = 6
            population_grid[y][x][1] -= 10
            population_grid[y][x][2] += 10
    if terrain_grid[y][x] == 6 and population_grid[y][x][1] > 0:               #Hunter-gatherers become farmers
        population_grid[y][x][2] += round(population_grid[y][x][1]/3, 1)
        population_grid[y][x][1] -= round(population_grid[y][x][1]/3, 1)
    if terrain_grid[y][x] == 6 and population_grid[y][x][0] == 0 and population_grid[y][x][2] == 0:                #Depopulated farms become fields
        if settlement_decision < 10: terrain_grid[y][x] = 2
    if terrain_grid[y][x] == 6 and population_grid[y][x][2] > 25:               #Forms town
        updated_population_caps[y][x] = 35
        terrain_grid[y][x] = 5
        population_grid[y][x][4] = 1
        population_grid[y][x][3] += 5
        population_grid[y][x][2] -= 6
        name, position = get_name(y, x)
        towns.append({"name": name, "position_x": x, "position_y": y, "colour": (0,0,0), "founder": 0, "owner": 0, "movement": 'Revolt', "unrest": 0})
        find_towns(population_grid, towns, states, territories, terrain_grid)

    if terrain_grid[y][x] == 1 and population_grid[y][x][0] > 5:                #Seas can't be overpopulated
        if population_grid[y][x][1] > population_grid [y][x][2]:
            population_grid[y][x][1] = 5
        else:
            population_grid[y][x][2] = 5

    return terrain_grid, population_grid, updated_population_caps, towns, states, territories

def remove_towns(current_tribe_location, population_grid, terrain_grid, towns, states, territories, y, x):
    towns_to_remove = []
    currentx, currenty = current_tribe_location

    # Find towns to remove
    for i, town in enumerate(towns):
        x = town['position_x']
        y = town['position_y']
        if terrain_grid[y][x] == 5 and population_grid[y][x][0] < 20:
            towns_to_remove.append(i)
            terrain_grid[y][x] = 6

    # Remove towns from towns dictionary
    for index in sorted(towns_to_remove, reverse=True):
        del towns[index]

    # Remove corresponding towns from states dictionary
    for state in states:
        state['towns'] = [town_name for town_name in state['towns'] if town_name not in [town['name'] for town in towns]]

    if population_grid[currenty][currentx][0] < 3:
        population_grid[currenty][currentx][1] = 3

    if population_grid[y][x][1] < 0:
        population_grid[y][x][1] = 0
    population_grid[y][x][0] = sum(population_grid[y][x][1:])

    return population_grid, terrain_grid, towns, states, territories

def generate_road_grid(size, terrain_grid, population_grid, current_tribe_location):
    # Initialize road grid with all zeros
    size = len(terrain_grid)
    road_grid = np.zeros((size, size), dtype=int)
    currentx, currenty = current_tribe_location

    if population_grid[currenty][currentx][0] < 3:
        population_grid[currenty][currentx][1] = 3

    return road_grid