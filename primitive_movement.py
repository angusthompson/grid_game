import numpy as np

def move_population_up(population_grid, terrain_grid, current_tribe_location):
    max_population = 0
    max_population_tile = current_tribe_location  # Start with the current tribe's location

    # Find the tile with the highest population
    for y in range(1, len(population_grid)):  # Start from the second row to have a tile above
        for x in range(len(population_grid[0])):
            population = population_grid[y][x][1]
            if population > max_population and terrain_grid[y - 1][x] != 1:  # Check if tile above is not sea
                max_population = population
                max_population_tile = (x, y)

    if max_population == 0:
        # If no population found or the tile above is sea, return without moving
        return population_grid, current_tribe_location

    x, y = max_population_tile

    # Remove population from the selected tile
    population_removed = population_grid[y][x][1]
    population_grid[y][x][1] = 0

    # Move the population to the tile above
    population_grid[y - 1][x][1] += population_removed

    # Update the current tribe's location
    current_tribe_location = (x, y - 1)

    return population_grid, current_tribe_location


def move_population_down(population_grid, terrain_grid, current_tribe_location):
    max_population = 0
    max_population_tile = current_tribe_location  # Start with the current tribe's location

    # Find the tile with the highest population
    for y in range(1, len(population_grid)):  # Start from the second row to have a tile above
        for x in range(len(population_grid[0])):
            population = population_grid[y][x][1]
            if population > max_population and terrain_grid[y + 1][x] != 1:  # Check if tile above is not sea
                max_population = population
                max_population_tile = (x, y)

    if max_population == 0:
        # If no population found or the tile above is sea, return without moving
        return population_grid, current_tribe_location

    x, y = max_population_tile

    # Remove population from the selected tile
    population_removed = population_grid[y][x][1]
    population_grid[y][x][1] = 0

    # Move the population to the tile above
    population_grid[y + 1][x][1] += population_removed

    # Update the current tribe's location
    current_tribe_location = (x, y + 1)

    return population_grid, current_tribe_location

def move_population_left(population_grid, terrain_grid, current_tribe_location):
    max_population = 0
    max_population_tile = current_tribe_location  # Start with the current tribe's location

    # Find the tile with the highest population
    for y in range(1, len(population_grid)):  # Start from the second row to have a tile above
        for x in range(len(population_grid[0])):
            population = population_grid[y][x][1]
            if population > max_population and terrain_grid[y][x-1] != 1:  # Check if tile above is not sea
                max_population = population
                max_population_tile = (x, y)

    if max_population == 0:
        # If no population found or the tile above is sea, return without moving
        return population_grid, current_tribe_location

    x, y = max_population_tile

    # Remove population from the selected tile
    population_removed = population_grid[y][x][1]
    population_grid[y][x][1] = 0

    # Move the population to the tile above
    population_grid[y][x-1][1] += population_removed

    # Update the current tribe's location
    current_tribe_location = (x-1, y)

    return population_grid, current_tribe_location

def move_population_right(population_grid, terrain_grid, current_tribe_location):
    max_population = 0
    max_population_tile = current_tribe_location  # Start with the current tribe's location

    # Find the tile with the highest population
    for y in range(1, len(population_grid)):  # Start from the second row to have a tile above
        for x in range(len(population_grid[0])):
            population = population_grid[y][x][1]
            if population > max_population and terrain_grid[y][x+1] != 1:  # Check if tile above is not sea
                max_population = population
                max_population_tile = (x, y)

    if max_population == 0:
        # If no population found or the tile above is sea, return without moving
        return population_grid, current_tribe_location

    x, y = max_population_tile

    # Remove population from the selected tile
    population_removed = population_grid[y][x][1]
    population_grid[y][x][1] = 0
    population_grid[y][x][0] = 0


    # Move the population to the tile above
    population_grid[y][x+1][1] += population_removed

    # Update the current tribe's location
    current_tribe_location = (x+1, y)

    return population_grid, current_tribe_location
