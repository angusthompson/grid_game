from terrain_generation import get_name

def find_towns(population_grid, terrain_grid, town_names, town_positions):
    towns = []
    for y in range(len(population_grid)):
        for x in range(len(population_grid[y])):
            if terrain_grid[y][x] == 5:
                towns.append((x, y))
                name, position = get_name(y, x)
                town_names.append(name)
                town_positions.append(position)
    return towns, town_names, town_positions

# def identify_towns(population_grid, terrain_grid, town_names, town_positions):
#     towns, town_names, town_positions = find_towns(population_grid, terrain_grid, town_names, town_positions)
#     states = []
#     for town, (name, position) in zip(towns, zip(town_names, town_positions)):
#         x, y = position
#         states.append({'name': f'{name}', 'location': f'{x}{y}'})
#     return states, towns, town_names, town_positions


def identify_towns(population_grid, terrain_grid, town_names, town_positions):
    towns, town_names, town_positions = find_towns(population_grid, terrain_grid, town_names, town_positions)
    states = []
    for town, name in zip(towns, town_names):
        x, y = town
        states.append({'name': name, 'location': f'{x}{y}'})
    return states, towns, town_names, town_positions

