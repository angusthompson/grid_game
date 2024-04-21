from terrain_generation import get_name
from graphics import get_random_color
import pygame
from parameters import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, x_size, y_size, cell_size, cell_width, cell_height, GRID_WIDTH, GRID_HEIGHT

def generate_state(i, town, x, y, states, territories, terrain_grid):
    single_name = town["name"]
    # print("Adding ", single_name, " to new state")
    colour = get_random_color([state["colour"] for state in states])
    names_list = []
    names_list.append(single_name)
    population_counts = [0, 0, 0, 0, 0]
    states.append({"name": single_name, "state": i, "colour": colour, "towns": names_list, "commodities": 0, "tax_rev": 0, "population_counts": population_counts})
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
        states[n - 1]["towns"].append(name)
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


def commodities(states):
    if len(states) > 0:
        for state in states:
            populations = state["population_counts"]
            commodities = state["commodities"]
            tax_rev = state["tax_rev"]
            farmer_population = populations[2]
            merchant_population = populations[3]
            noble_population = populations[4]
            commodities += merchant_population * 0.2
            commodities -= noble_population * 3
            tax_rev = farmer_population*0.1
            state["commodities"] = round(commodities, 2)
            state["tax_rev"] = round(tax_rev, 2)


def display_towns(screen, font, states, overlay_width, overlay_height, overlay_x, overlay_y):
    font_size = 16  # Font size for state names

    # commodities(states)

    # Iterate over states
    for i, state in enumerate(states):
        name = state["name"]
        color = state["colour"]
        populations = state["population_counts"]
        state_commodities = state["commodities"]
        tax_rev = state["tax_rev"]
        total_population = populations[0]  # Get total population from the state dictionary
        farmer_population = populations[2]
        merchant_population = populations[3]
        noble_population = populations[4]

        # Render state name, total population, merchant population, and state commodities on separate lines
        name_surface = font.render(name, True, (255, 255, 255))  # White text color
        total_pop_surface = font.render(f"Total Population: {total_population}", True, (255, 255, 255))
        merchant_pop_surface = font.render(f"Merchant Population: {merchant_population}            Noble Population: {noble_population}            Farmer Population: {farmer_population}", True, (255, 255, 255))
        commodities_surface = font.render(f"Commodities: {state_commodities}                      Tax Revenue: {tax_rev}", True, (255, 255, 255))

        # Calculate vertical position for each line
        name_rect = name_surface.get_rect()
        total_pop_rect = total_pop_surface.get_rect()
        merchant_pop_rect = merchant_pop_surface.get_rect()
        commodities_rect = commodities_surface.get_rect()
        if i < 10:
            name_rect.topleft = (100, UI_HEIGHT - 700 + (i) * font_size * 4)
            total_pop_rect.topleft = (100, UI_HEIGHT - 700 + 15 + (i) * font_size * 4)
            merchant_pop_rect.topleft = (100, UI_HEIGHT - 700 + 30 + (i) * font_size * 4)
            commodities_rect.topleft = (100, UI_HEIGHT - 700 + 45 + (i) * font_size * 4)
        if i > 9 and i < 20:
            name_rect.topleft = (500, UI_HEIGHT - 700 + (i - 10) * font_size * 4)
            total_pop_rect.topleft = (500, UI_HEIGHT - 700 + 15 + (i - 10) * font_size * 4)
            merchant_pop_rect.topleft = (500, UI_HEIGHT - 700 + 30 + (i - 10) * font_size * 4)
            commodities_rect.topleft = (500, UI_HEIGHT - 700 + 45 + (i - 10) * font_size * 4)
        if i > 20:
            name_rect.topleft = (900, UI_HEIGHT - 700 + (i - 10) * font_size * 4)
            total_pop_rect.topleft = (900, UI_HEIGHT - 700 + 15 + (i - 10) * font_size * 4)
            merchant_pop_rect.topleft = (900, UI_HEIGHT - 700 + 30 + (i - 10) * font_size * 4)
            commodities_rect.topleft = (900, UI_HEIGHT - 700 + 45 + (i - 10) * font_size * 4)
        # Draw background of state color for each line
        pygame.draw.rect(screen, color, name_rect)
        pygame.draw.rect(screen, color, total_pop_rect)
        pygame.draw.rect(screen, color, merchant_pop_rect)
        pygame.draw.rect(screen, color, commodities_rect)

        # Blit text onto the overlay
        screen.blit(name_surface, name_rect.topleft)
        screen.blit(total_pop_surface, total_pop_rect.topleft)
        screen.blit(merchant_pop_surface, merchant_pop_rect.topleft)
        screen.blit(commodities_surface, commodities_rect.topleft)