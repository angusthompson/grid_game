

def move_population_up(population_grid, terrain_grid, current_tribe_location):
    x, y = current_tribe_location
    if population_grid[y][x][1] == 0:
        population_grid[y][x][1] = 3
    # Check if the tile above is not sea
    if y > 0 and terrain_grid[y - 1][x] != 1:
        # Move the population to the tile above
        population_grid[y - 1][x][1] += population_grid[y][x][1]
        population_grid[y][x][1] = 0
        current_tribe_location = (x, y - 1)
        if population_grid[y-1][x][1] < 3:
            population_grid[y-1][x][1] = 3
        
    return population_grid, current_tribe_location

def move_population_down(population_grid, terrain_grid, current_tribe_location):
    x, y = current_tribe_location
    if population_grid[y][x][1] == 0:
        population_grid[y][x][1] = 3
    # Check if the tile below is not sea
    if y < len(population_grid) - 1 and terrain_grid[y + 1][x] != 1:
        # Move the population to the tile below
        population_grid[y + 1][x][1] += population_grid[y][x][1]
        population_grid[y][x][1] = 0
        current_tribe_location = (x, y + 1)
        if population_grid[y+1][x][1] < 3:
            population_grid[y+1][x][1] = 3

    return population_grid, current_tribe_location

def move_population_left(population_grid, terrain_grid, current_tribe_location):
    x, y = current_tribe_location
    if population_grid[y][x][1] == 0:
        population_grid[y][x][1] = 3
    # Check if the tile to the left is not sea
    if x > 0 and terrain_grid[y][x - 1] != 1:
        # Move the population to the tile to the left
        population_grid[y][x - 1][1] += population_grid[y][x][1]
        population_grid[y][x][1] = 0
        current_tribe_location = (x - 1, y)
        if population_grid[y][x-1][1] < 3:
            population_grid[y][x-1][1] = 3
        
    return population_grid, current_tribe_location

def move_population_right(population_grid, terrain_grid, current_tribe_location):
    x, y = current_tribe_location
    if population_grid[y][x][1] == 0:
        population_grid[y][x][1] = 3
    # Check if the tile to the right is not sea
    if x < len(population_grid[0]) - 1 and terrain_grid[y][x + 1] != 1:
        # Move the population to the tile to the right
        population_grid[y][x + 1][1] += population_grid[y][x][1]
        population_grid[y][x][1] = 0
        current_tribe_location = (x + 1, y)
        if population_grid[y][x+1][1] < 3:
            population_grid[y][x+1][1] = 3
        
    return population_grid, current_tribe_location

def find_starting_location(population_grid):
    max_population = 0
    starting_location = (0, 0)

    # Iterate through the population grid to find the tile with the highest population
    for y in range(len(population_grid)):
        for x in range(len(population_grid[0])):
            population = population_grid[y][x][1]
            if population > max_population:
                max_population = population
                starting_location = (x, y)

    return starting_location

# Function to convert population to farmers and update terrain
def convert_to_farmers(population_grid, terrain_grid, current_tribe_location):
    x, y = current_tribe_location
    total_population = population_grid[y][x][0]
    farmers_count = int(total_population * 0.5)  # Convert 80% of the population to farmers
    population_grid[y][x][2] = farmers_count  # Update the population grid with the new farmer count
    population_grid[y][x][1] -= farmers_count  # Reduce the hunter-gatherer count accordingly
    terrain_grid[y][x] = 6  # Convert the tile to farmland