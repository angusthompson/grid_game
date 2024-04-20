from terrain_generation import get_name
from graphics import get_random_color
import pygame

x_size = 53
y_size = 33

def generate_state(i, town, x, y, states, territories, terrain_grid):
    single_name = town["name"]
    # print("Adding ", single_name, " to new state")
    colour = get_random_color([state["colour"] for state in states])
    names_list = []
    names_list.append(single_name)
    states.append({"name": single_name, "state": i, "colour": colour, "towns": names_list})
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            nx, ny = x + dx, y + dy
            if nx < x_size and ny < y_size:
                if territories[ny][nx] == 0 and terrain_grid[ny][nx] != 1:
                    territories[ny][nx] = len(states)
    return states, territories

def add_to_state(i, n, town, x, y, states, territories, terrain_grid):
    name = town["name"]
    # print("n in add to state: ", n)
    state = states[n-1]
    if name in state["towns"]:
        # print("addded already")
        pass
    else:
        # print("Adding ", name, " to existing state")
        states[n - 1]["towns"].append(name)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = x + dx, y + dy
                if nx < x_size and ny < y_size:
                    if territories[ny][nx] == 0 and terrain_grid[ny][nx] != 1:
                        territories[ny][nx] = n
    states

def find_towns(population_grid, towns, states, territories, terrain_grid):
    # print(towns)
    z = 0
    for i in towns:
        town = towns[z]
        # print(town)
        x = town['position_x']
        y = town['position_y']
        if territories[y][x] == 0:
            generate_state(z, town, x, y, states, territories, terrain_grid)
        else:
            n = territories[y][x]
            add_to_state(z, n, town, x, y, states, territories, terrain_grid)
        z += 1
    return towns

def borders(territories, states):
    territory_colors = []
    white = (255, 255, 255)
    thick_boundary_color = (0, 0, 0)  # Choose your desired color for the thick boundary
    boundary_thickness = 3  # Choose the thickness of the boundary

    for y, row in enumerate(territories):
        color_row = []
        for x, tile in enumerate(row):
            if tile > 0:
                state_index = tile - 1
                state_color = states[state_index]["colour"]
                color_row.append(state_color)
            else:
                color_row.append(white)
        
        territory_colors.append(color_row)

    return territory_colors

def draw_territory_borders(territories, states, territory_colors, game_display, cell_size):
    for y in range(len(territories)):
        for x in range(len(territories[y])):
            current_territory = territories[y][x]
            current_state_index = current_territory - 1
            # current_state_color = states[current_state_index]["colour"]
            current_state_color = (0, 0, 0)
            # Check neighboring cells
            above = (y-1, x)
            below = (y+1, x)
            left = (y, x-1)
            right = (y, x+1)
            ny, nx = above
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory:
                    pygame.draw.line(game_display, current_state_color, (x * cell_size, y * cell_size), ((x + 1) * cell_size, y * cell_size), 2)
            ny, nx = below
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory:
                    pygame.draw.line(game_display, current_state_color, (x * cell_size, (y + 1) * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size), 2)
            ny, nx = left
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory:
                    pygame.draw.line(game_display, current_state_color, (x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size), 2)
            ny, nx = right
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory:
                    pygame.draw.line(game_display, current_state_color, ((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size), 2)


def count_population_by_state(territories, population_grid, states):
    # Initialize counts for each state
    state_populations = {state["name"]: [0, 0, 0, 0] for state in states}

    # Iterate over territories
    for y in range(len(territories)):
        for x in range(len(territories[y])):
            territory_owner = territories[y][x]
            if territory_owner > 0:
                state_index = territory_owner - 1
                state_name = states[state_index]["name"]
                # Update population counts for the corresponding state
                state_populations[state_name][0] += population_grid[y][x][0]  # Count of pop 1
                state_populations[state_name][1] += population_grid[y][x][1]  # Count of pop 2
                state_populations[state_name][2] += population_grid[y][x][2]  # Count of pop 3
                state_populations[state_name][3] += population_grid[y][x][3]  # Count of pop 4

    # Append population counts to the states list
    for state in states:
        state_name = state["name"]
        state["population_counts"] = state_populations[state_name]
        state["commodities"] = 0
