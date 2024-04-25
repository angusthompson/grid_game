import numpy as np
import random

def generate_terrain_grid(size_x, size_y, num_iterations=5):
    # Generate initial terrain grid separately for x and y axes
    terrain_grid = np.random.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4], size=(size_y, size_x))
    
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
            if y == len(terrain_grid)-1 or y == 0:
                new_terrain_grid[y][x] = 8  
            elif random_integer > 2:
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

def get_population_neighbors(population_grid, grid, x, y):
    population_neighbors = 0
    hunter_neighbors = 0
    farmer_neighbors = 0
    merchant_neighbors = 0
    if population_grid[y][x][0] > 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx != x or ny != y):
                    population_neighbors += population_grid[ny][nx][0]
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx != x or ny != y):
                    hunter_neighbors += population_grid[ny][nx][1]
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx != x or ny != y):
                    farmer_neighbors += population_grid[ny][nx][2]
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx != x or ny != y):
                    merchant_neighbors += population_grid[ny][nx][3]
    return population_neighbors, hunter_neighbors, farmer_neighbors, merchant_neighbors

def get_name(y, x):
    prefixes = ['Port','Fort','San','Saint','Inver','Dun','Mont', 'Monte', 'Kil','New ','Nov','Novo','Nowy','New','Stara','Stary','Nan','Yan','Qing']
    names = ['buck','guang','storn','marn','kyot','der','luck','ber','lin','par','rom','bei','piet','mos','stan','sevast','then','mad','edin','']
    capitalised_names = ['Buck','Guang','Storn','Marn','Kyot','Der','Luck','Ber','Lin','Par','Rom','Bei','Piet','Mos','Stan','Sevast','Then','Mad','Edin']
    suffixes = ['ock','och','gorod','grad','burg','berg','bourg','ness','burgh','borough','zhou','gard','to','ople','insk','ovsk','stead','ham','opol','now','zuma', '']
    random_prefix = random.choice(prefixes)
    random_name = random.choice(names)
    capitalised_random_name = random.choice(capitalised_names)
    random_suffix = random.choice(suffixes)
    random_number = random.randint(1, 10)
    if random_number > 5:
        name = (random_prefix + random_name + random_suffix)
    else:
        name = (capitalised_random_name + random_suffix)
    position = x, y
    return name, position



# get_name()
# get_name()
# get_name()
# get_name()
# get_name()
# get_name()
# get_name()
# get_name()
# get_name()
