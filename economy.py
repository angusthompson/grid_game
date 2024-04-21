from terrain_generation import get_name
from graphics import get_random_color
import pygame
from parameters import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, x_size, y_size, cell_size, cell_width, cell_height, GRID_WIDTH, GRID_HEIGHT
import random

def generate_state(i, town, x, y, states, territories, terrain_grid):
    single_name = town["name"]
    # print("Adding ", single_name, " to new state")
    colour = get_random_color([state["colour"] for state in states])
    names_list = []
    names_list.append(single_name)
    population_counts = [0, 0, 0, 0, 0]
    index = len(states)
    states.append({"name": single_name, "state": i, "colour": colour, "towns": names_list, "commodities": 0, "tax_rev": 0, "population_counts": population_counts, "expansionism": 0, "military_power": 0, "noble_growth": 0, "unrest": 0, "status": 1, "index": index, "capital": (y, x)})
    for dy in range(-1, 2):
        for dx in range(-1, 2):
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
        states[n-1]["towns"].append(name)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if nx < x_size and ny < y_size:
                    if territories[ny][nx] == 0 and terrain_grid[ny][nx] != 1:
                        territories[ny][nx] = n
    states

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
    state_populations = {state["name"]: [0, 0, 0, 0, 0] for state in states}

    # Iterate over territories
    for y in range(len(territories)):
        for x in range(len(territories[y])):
            territory_owner = territories[y][x]
            if territory_owner > 0:
                state_index = territory_owner - 1
                state_name = states[state_index]["name"]
                # Update population counts for the corresponding state
                state_populations[state_name][0] += population_grid[y][x][0]  # Sum of pops
                state_populations[state_name][1] += population_grid[y][x][1]  # Count of Hunter-Gatherers
                state_populations[state_name][2] += population_grid[y][x][2]  # Count of Farmers
                state_populations[state_name][3] += population_grid[y][x][3]  # Count of Merchants
                state_populations[state_name][4] += population_grid[y][x][4]  # Count of Nobles

    # Append population counts to the states list
    for state in states:
        state_name = state["name"]
        state["population_counts"] = state_populations[state_name]
    
    # Remove states with no towns
    states = [state for state in states if len(state["towns"]) > 0]
    # Update state indices
    for i, state in enumerate(states):
        state["index"] = i + 1
def draw_economy_overlay(screen, states):
    # Get the dimensions of the game display
    display_width, display_height = screen.get_size()

    # Define the dimensions of the overlay rectangle
    overlay_width = display_width - 200  # Reduce width by 20 pixels
    overlay_height = display_height - 30  # Reduce height by 20 pixels

    # Calculate the position of the overlay rectangle to center it on the screen
    overlay_x = ((display_width - overlay_width) // 2) - 90
    overlay_y = (display_height - overlay_height) // 2

    # Define colors
    grey = (192, 192, 192)
    black = (0, 0, 0)

    # Draw the grey rectangle
    pygame.draw.rect(screen, grey, (overlay_x, overlay_y, overlay_width, overlay_height))

    # Draw the black border
    pygame.draw.rect(screen, black, (overlay_x, overlay_y, overlay_width, overlay_height), 3)

    display_towns(screen, pygame.font.Font(None, 20), states, overlay_width, overlay_height, overlay_x, overlay_y)


def commodities(states, territories, population_grid, terrain_grid, towns):
    taxes = (0, 0, 0.1, 0.1, 0)             # Tax rates on full population, hunter-gatherers, farmers, mechants, nobles
    if len(states) > 0:
        for state in states:
            populations = state["population_counts"]
            commodities = state["commodities"]
            noble_growth = state["noble_growth"]
            tax_rev = state["tax_rev"]
            expansionism = state["expansionism"]
            military_power = state["military_power"]
            unrest = state["unrest"]
            farmer_population = populations[2]
            merchant_population = populations[3]
            noble_population = populations[4]
            commodities += merchant_population * 1
            commodities -= noble_population * 3
            tax_rev = farmer_population*taxes[2] + merchant_population*taxes[3]
            noble_growth += merchant_population*0.1
            if noble_growth > 10 and tax_rev > 5:
                expand_states(states, territories, population_grid, terrain_grid, towns)
                tax_rev -= 5
            if commodities < 0:
                military_power += tax_rev
                unrest -= commodities
            if commodities > 0 and unrest > 0:
                unrest -= commodities
            state["noble_growth"] = round(noble_growth, 3)
            state["commodities"] = round(commodities, 2)
            state["tax_rev"] = round(tax_rev, 2)
            state["unrest"] = round(unrest, 3)
            state["military_power"] = round(military_power, 3)

def display_towns(screen, font, states, overlay_width, overlay_height, overlay_x, overlay_y):
    font_size = 16  # Font size for state names
    # filtered_states = [state.copy() for state in states if state.get("status", 0) != 0]
    # Iterate over states
    sublist_states = [state.copy() for state in states if state.get("towns") != 'none']
    for i, state in enumerate(sublist_states):
        name = state["name"]
        color = state["colour"]
        populations = state["population_counts"]
        state_commodities = state["commodities"]
        tax_rev = state["tax_rev"]
        total_population = populations[0]  # Get total population from the state dictionary
        farmer_population = populations[2]
        merchant_population = populations[3]
        noble_population = populations[4]
        # expansionism = state["expansionism"]
        growth = state["noble_growth"]
        expansionism = round(growth, 3)
        military_power = state["military_power"]
        unrest = state["unrest"]
        towns = state["towns"]

        # Render state name, total population, merchant population, and state commodities on separate lines
        name_surface = font.render(name, True, (255, 255, 255))  # White text color
        total_pop_surface = font.render(f"Total Population: {total_population}                      Unrest: {unrest}", True, (255, 255, 255))
        merchant_pop_surface = font.render(f"Merchant Population: {merchant_population}            Noble Population: {noble_population}", True, (255, 255, 255))
        commodities_surface = font.render(f"Commodities: {state_commodities}                      Tax Revenue: {tax_rev}", True, (255, 255, 255))
        military_surface = font.render(f"Expansionism: {expansionism}                      Military Power: {military_power}", True, (255, 255, 255))
        towns_surface = font.render(f"Towns: {towns}", True, (255, 255, 255))

        # Calculate vertical position for each line
        name_rect = name_surface.get_rect()
        total_pop_rect = total_pop_surface.get_rect()
        merchant_pop_rect = merchant_pop_surface.get_rect()
        commodities_rect = commodities_surface.get_rect()
        military_rect = military_surface.get_rect()
        towns_rect = towns_surface.get_rect()

        if i < 8:
            name_rect.topleft = (100, UI_HEIGHT - 700 + (i) * font_size * 5)
            total_pop_rect.topleft = (100, UI_HEIGHT - 700 + 15 + (i) * font_size * 5)
            merchant_pop_rect.topleft = (100, UI_HEIGHT - 700 + 30 + (i) * font_size * 5)
            commodities_rect.topleft = (100, UI_HEIGHT - 700 + 45 + (i) * font_size * 5)
            towns_rect.topleft = (100, UI_HEIGHT - 700 + 60 + (i) * font_size * 5)
        if i > 7 and i < 16:
            name_rect.topleft = (500, UI_HEIGHT - 700 + (i - 8) * font_size * 5)
            total_pop_rect.topleft = (500, UI_HEIGHT - 700 + 15 + (i - 8) * font_size * 5)
            merchant_pop_rect.topleft = (500, UI_HEIGHT - 700 + 30 + (i - 8) * font_size * 5)
            commodities_rect.topleft = (500, UI_HEIGHT - 700 + 45 + (i - 8) * font_size * 5)
            towns_rect.topleft = (500, UI_HEIGHT - 700 + 60 + (i - 8) * font_size * 5)
        if i > 15:
            name_rect.topleft = (900, UI_HEIGHT - 700 + (i - 16) * font_size * 5)
            total_pop_rect.topleft = (900, UI_HEIGHT - 700 + 15 + (i - 16) * font_size * 5)
            merchant_pop_rect.topleft = (900, UI_HEIGHT - 700 + 30 + (i - 16) * font_size * 5)
            commodities_rect.topleft = (900, UI_HEIGHT - 700 + 45 + (i - 16) * font_size * 5)
            towns_rect.topleft = (900, UI_HEIGHT - 700 + 60 + (i - 16) * font_size * 5)

        # Draw background of state color for each line
        pygame.draw.rect(screen, color, name_rect)
        pygame.draw.rect(screen, color, total_pop_rect)
        pygame.draw.rect(screen, color, merchant_pop_rect)
        pygame.draw.rect(screen, color, commodities_rect)
        pygame.draw.rect(screen, color, towns_rect)

        # Blit text onto the overlay
        screen.blit(name_surface, name_rect.topleft)
        screen.blit(total_pop_surface, total_pop_rect.topleft)
        screen.blit(merchant_pop_surface, merchant_pop_rect.topleft)
        screen.blit(commodities_surface, commodities_rect.topleft)
        screen.blit(towns_surface, towns_rect.topleft)


def expand_states(states, territories, population_grid, terrain_grid, towns):
    for state in states:
        noble_growth = state["noble_growth"]
        if noble_growth >= 10:
            # Subtract 10 from noble_growth
            noble_growth -= 10
            state["noble_growth"] = noble_growth
            state_index = state["index"]
            capital_y, capital_x = state["capital"]
            # Choose a random unclaimed tile neighboring the state's territory
            unclaimed_tiles = find_unclaimed_neighbors(territories, state, terrain_grid)
            if unclaimed_tiles:
                chosen_tile = random.choice(unclaimed_tiles)
                # Generate a new noble and add it to the state's territory
                x, y = chosen_tile
                population_grid[y][x][4] += 1
                territories[y][x] = state_index
                state["commodities"] += 100
            elif foreign_neighbors := find_foreign_neighbors(territories, state, terrain_grid, states, towns):
                # If there are no unclaimed tiles but there are foreign neighbors, claim the foreign state's land
                foreign_neighbors.sort(key=lambda neighbor: neighbor[2])  # Sort by military power (index 2)
                chosen_tile = foreign_neighbors[0]  # Choose the foreign tile with the lowest military power
                x, y, neighbor_state_index = chosen_tile
                if population_grid[y][x][4] == 0: population_grid[y][x][4] += 1
                if population_grid[y][x][2] > 0: population_grid[y][x][2] -= population_grid[y][x][2]*0.3
                if population_grid[y][x][3] > 0: population_grid[y][x][3] -= population_grid[y][x][3]*0.3
                # Add check for comparative military power
                if neighbor_state_index != len(states):
                    if state["military_power"] > states[neighbor_state_index]["military_power"]:
                        territories[y][x] = state_index
                        state["military_power"] -= states[neighbor_state_index]["military_power"]
                        states[neighbor_state_index]["military_power"] = 0
                        state["commodities"] += 100
                        neighbor_state = states[neighbor_state_index - 1]
                elif neighbor_state_index == len(states): pass
                else:
                    state["military_power"] -= states[neighbor_state_index]["military_power"]
                    state["military_power"] = 0
                    states[neighbor_state_index]["military_power"] -= state["military_power"]
    return states


def find_unclaimed_neighbors(territories, state, terrain_grid):
    unclaimed_neighbors = []
    state_index = state["index"]
    # Define the directions to check for neighboring tiles (up, down, left, right)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]


    # Iterate over each tile in the state's territory
    for y in range(len(territories)):
        for x in range(len(territories[y])):
            if territories[y][x] == state_index:  # Check if the tile belongs to the state
                # Check neighboring tiles in each direction
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    # Ensure the neighboring tile is within bounds
                    if 0 <= nx < len(territories[0]) and 0 <= ny < len(territories):
                        # Check if the neighboring tile is unclaimed
                        if territories[ny][nx] == 0 and terrain_grid[ny][nx] != 1 and terrain_grid[ny][nx] != 8:
                            unclaimed_neighbors.append((nx, ny))

    return unclaimed_neighbors


def find_foreign_neighbors(territories, state, terrain_grid, states, towns):
    foreign_neighbors = []
    state_index = state["index"]
    state_military_power = state["military_power"]
    # Define the directions to check for neighboring tiles (up, down, left, right)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Iterate over each tile in the state's territory
    for y in range(len(territories)):
        for x in range(len(territories[y])):
            if territories[y][x] == state_index:  # Check if the tile belongs to the state
                # Check neighboring tiles in each direction
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    # Ensure the neighboring tile is within bounds
                    if 0 <= nx < len(territories[0]) and 0 <= ny < len(territories):
                        neighbor_state_index = territories[ny][nx]
                        # Check if the neighboring tile is owned by another state
                        if neighbor_state_index != 0 and neighbor_state_index != state_index:
                            neighbor_state = states[neighbor_state_index - 1]
                            neighbor_military_power = neighbor_state["military_power"]
                            # Check if the neighboring state has higher military power
                            # if neighbor_military_power > state_military_power:
                            foreign_neighbors.append((nx, ny, neighbor_state_index))

    # Sort foreign neighbors by the military power of the neighboring states
    foreign_neighbors.sort(key=lambda neighbor: states[neighbor[2] - 1]["military_power"], reverse=True)

    return foreign_neighbors

def check_towns(towns, states, territories):
    for state in states:
        state_index = state["index"]
        town_names = []
        for town in towns:
            town_y, town_x = town["position_y"], town["position_x"]
            if territories[town_y][town_x] == state_index:
                town_names.append(town["name"])
        state["towns"] = town_names

        if not town_names:
            state["status"] = 0
            state["towns"] = "none"
            for y, row in enumerate(territories):
                for x, tile in enumerate(row):
                    if tile == state_index:
                        territories[y][x] = 0
