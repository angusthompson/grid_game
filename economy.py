from terrain_generation import get_name
from graphics import get_random_color
import pygame
from parameters import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, x_size, y_size, cell_size, cell_width, cell_height, GRID_WIDTH, GRID_HEIGHT, PURPLE, player_taxes
import random
from revolts import revolt, bourgeois_revolution, secession

def generate_state(i, town, x, y, states, territories, terrain_grid):
    single_name = town["name"]
    colour = get_random_color([state["colour"] for state in states])
    names_list = []
    names_list.append(single_name)
    population_counts = [0, 0, 0, 0, 0, 0, 0, 0]
    index = len(states)
    # new_state = {"name": single_name, "state": i, "colour": colour, "towns": names_list, "commodities": 0, "tax_rev": 0, "population_counts": population_counts, "expansionism": 0, "military_power": 0, "noble_growth": 0, "unrest": 0, "status": 1, "index": index, "capital": (y, x)}
    states.append({"name": single_name, "state": i, "colour": colour, "towns": names_list, "commodities": 0, "tax_rev": 0, "population_counts": population_counts, "expansionism": 0, "military_power": 0, "noble_growth": 0, "unrest": 0, "status": 'Primitive Accumulation', "index": index, "capital": (y, x), "player": 'No', "taxes": (0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)})
    # print(new_state)
    if town["founder"] == 0:
        town["founder"] = index
    town["owner"] = index
    town["colour"] = colour
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if nx < x_size and ny < y_size:
                if territories[ny][nx] == 0 and terrain_grid[ny][nx] != 1:
                    territories[ny][nx] = len(states)
    return states, territories, town

def add_to_state(i, n, town, x, y, states, territories, terrain_grid):
    name = town["name"]
    state = states[n-1]
    if name in state["towns"]:
        pass
    else:
        if states[n-1]["towns"] == 'none':
            pass
        if not isinstance(states[n-1].get("towns"), list):
            states[n-1]["towns"] = [states[n-1]["towns"]]
        states[n-1]["towns"].append(name)
        if town["founder"] == 0:
            town["founder"] = state["index"]
        town["owner"] = state["index"]
        town["colour"] = state["colour"]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if nx < x_size and ny < y_size:
                    if territories[ny][nx] == 0 and terrain_grid[ny][nx] != 1:
                        territories[ny][nx] = n
    return states, town

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
    player_ownership = -1
    for y in range(len(territories)):
        for x in range(len(territories[y])):            #Going through each tile
            current_territory = territories[y][x]
            current_state = states[current_territory - 1]

            if current_state["player"] == 'Yes':
                current_state_color = current_state["colour"]
                player_ownership = current_territory
            else: 
                current_state_color = BLACK

            # Check neighboring cells
            above = (y-1, x)
            below = (y+1, x)
            left = (y, x-1)
            right = (y, x+1)
            ny, nx = above
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory and neighbor_territory != player_ownership:
                    pygame.draw.line(game_display, current_state_color, (x * cell_size, y * cell_size), ((x + 1) * cell_size, y * cell_size), 2)
            ny, nx = below
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory and neighbor_territory != player_ownership:
                    pygame.draw.line(game_display, current_state_color, (x * cell_size, (y + 1) * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size), 2)
            ny, nx = left
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory and neighbor_territory != player_ownership:
                    pygame.draw.line(game_display, current_state_color, (x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size), 2)
            ny, nx = right
            if 0 <= ny < len(territories) and 0 <= nx < len(territories[0]):
                neighbor_territory = territories[ny][nx]
                if neighbor_territory != current_territory and neighbor_territory != player_ownership:
                    pygame.draw.line(game_display, current_state_color, ((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size), 2)


def count_population_by_state(territories, population_grid, states):
    # Initialize counts for each state
    state_populations = {state["name"]: [0, 0, 0, 0, 0, 0, 0] for state in states}

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
                state_populations[state_name][5] += population_grid[y][x][5]  # Count of Nobles
                state_populations[state_name][6] += population_grid[y][x][6]  # Count of Nobles

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


def commodities(states, territories, population_grid, terrain_grid, towns, player_taxes):
    if len(states) > 0:
        for state in states:
            state = get_taxes(state, player_taxes)
            populations = state["population_counts"]
            commodities = state["commodities"]
            noble_growth = state["noble_growth"]
            taxes = state["taxes"]             # Tax rates on full population, hunter-gatherers, farmers, mechants, nobles, etc.
            tax_rev = state["tax_rev"]
            expansionism = state["expansionism"]
            military_power = state["military_power"]
            unrest = state["unrest"]
            name = state["name"]
            farmer_population = populations[2]
            merchant_population = populations[3]
            noble_population = populations[4]
            if len(populations) < 6:
                populations.append(0)
                populations.append(0)
                populations.append(0)
            proletarian_population = populations[5]
            bourgeois_population = populations[6]

            # Commodity Production and consumption
            commodities += merchant_population * 2
            commodities += proletarian_population * 5
            commodities -= noble_population * 7
            commodities -= bourgeois_population * 15

            # Tax Revenue
            tax_rev = farmer_population*taxes[2] + merchant_population*taxes[3] + proletarian_population*taxes[5] + bourgeois_population*taxes[6]

            # Noble growth and expansion
            noble_growth += merchant_population*0.1
            if noble_growth > 10 and tax_rev > 5:
                expand_states(states, territories, population_grid, terrain_grid, towns)
                tax_rev -= 5
            if noble_growth > 10:
                # Step 1: Randomly select one of the town names from the current entry in 'states'
                if len(state["towns"]) > 0:
                    nobles_to_add = noble_growth // 10
                    noble_growth -= nobles_to_add*10
                    selected_town_name = random.choice(state["towns"])
                    # Step 2: Find the corresponding dictionary in 'towns' with the selected town name
                    selected_town = next((town for town in towns if town["name"] == selected_town_name), None)
                    if selected_town:
                        x_position = selected_town["position_x"]
                        y_position = selected_town["position_y"]
                        population_grid[y_position][x_position][4] += nobles_to_add
                    state["population_counts"] = populations
                    state["noble_growth"] = noble_growth

            # Unrest and Military Buildup
            military_power += tax_rev
            if commodities < 0:
                # military_power += tax_rev
                unrest += (-commodities)
            if commodities > 0 and unrest > 0:
                unrest -= commodities*0.2
                if unrest < 0: unrest = 0
            for town_name in state["towns"]:
                if town_name != 'none' and town_name != 'n' and town_name != 'o' and town_name != 'e':
                    selected_town = next((town for town in towns if town["name"] == town_name), None)
                    if selected_town:
                        town_unrest = selected_town["unrest"]
                        if town_unrest > 1000 and unrest > military_power:
                            # print("revolt type = ", selected_town["movement"])
                            if selected_town["movement"] == 'Separatism':
                                states, selected_town, territories = secession(state, states, selected_town, territories, population_grid)
                                # state["unrest"] -= 1000
                                state["unrest"] = 0
                            if selected_town["movement"] == 'Revolt':
                                revolt(state, selected_town, territories, population_grid)
                                state["unrest"] = 0
                                state["commodities"] = 0
                            if selected_town["movement"] == 'Bourgeois Revolution':
                                bourgeois_revolution(state, selected_town, territories, population_grid)
                                state["unrest"] = 0
            state["noble_growth"] = round(noble_growth, 3)
            state["commodities"] = round(commodities, 2)
            state["tax_rev"] = round(tax_rev, 2)
            state["unrest"] = round(unrest, 3)
            state["military_power"] = round(military_power, 3)


def display_towns(screen, font, states, overlay_width, overlay_height, overlay_x, overlay_y):
    # Font settings
    title_font = pygame.font.SysFont(None, 20, bold=True)
    font_size = 16  # Font size for other cells

    overlay_x += 25
    overlay_y += 10  # Move down vertically by 10 pixels
    # Calculate cell dimensions
    cell_width = (overlay_width-70) // (len(states[0])-7)  # Adjusted to accommodate the extra population columns
    cell_height = font_size * 1.5  # Adjust based on font size

    titles = ["Name", "Towns", "Commodities", "Tax Revenue", "Populations", "Military Power", "Noble Growth", "Unrest"]

    filtered_states = [state for state in states if state["towns"] != 'none']

    # Extract color values from "Colour" column
    colors = [state["colour"] for state in filtered_states]

    # Exclude "status", "index", "colour", and "Capital" columns
    states_without_status_index_colour_capital = [{key: value for key, value in state.items() if key not in ["state", "status", "index", "colour", "capital", "expansionism", "player", "taxes"]} for state in filtered_states]

    # Draw column titles
    for i, title in enumerate(titles):
        title_surface = title_font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(center=(overlay_x + (i + 0.5) * cell_width, overlay_y + cell_height / 2))
        screen.blit(title_surface, title_rect)

    # Loop through data and draw each cell
    for i, state in enumerate(states_without_status_index_colour_capital):
        # Calculate row position
        row_y = overlay_y + (i + 1) * cell_height  # Start after the title row

        # Extract color for current row
        color = colors[i]

        # Calculate the length of 'towns' entry
        towns_length = len(state["towns"])

        # Round the "Noble Growth" number to 1 decimal place
        noble_growth_rounded = round(state["noble_growth"], 1)

        # Modify the state dictionary with the updated values
        state_modified = {key: value if key != "Towns" else towns_length for key, value in state.items()}
        state_modified["noble_growth"] = noble_growth_rounded
        state_modified["towns"] = towns_length
        
        # Extract population list
        populations = state_modified["population_counts"]

        # Loop through state attributes and draw each cell
        for j, (_, value) in enumerate(state_modified.items()):
            # Calculate cell position
            cell_x = overlay_x + j * cell_width

            # Draw cell rectangle with color from "Colour" column
            pygame.draw.rect(screen, color, (cell_x, row_y, cell_width, cell_height))
            pygame.draw.rect(screen, BLACK, (cell_x, row_y, cell_width, cell_height), 1)

            # Render text
            if isinstance(value, list):  # Check if value is a list (for populations)
                for k, population_value in enumerate(value):
                    text_surface = font.render(str(population_value), True, BLACK)
                    text_rect = text_surface.get_rect(center=(cell_x + (k + 0.5) * (cell_width / len(value)), row_y + cell_height / 2))
                    screen.blit(text_surface, text_rect)
            else:
                text_surface = font.render(str(value), True, BLACK)
                text_rect = text_surface.get_rect(center=(cell_x + cell_width / 2, row_y + cell_height / 2))
                screen.blit(text_surface, text_rect)



def expand_states(states, territories, population_grid, terrain_grid, towns):
    for state in states:
        noble_growth = state["noble_growth"]
        if noble_growth >= 10:
            # Subtract 10 from noble_growth
            noble_growth -= 10
            state["noble_growth"] = noble_growth
            state_index = state["index"]
            # capital_y, capital_x = state["capital"]
            # Choose a random unclaimed tile neighboring the state's territory
            unclaimed_tiles = find_unclaimed_neighbors(territories, state, terrain_grid)
            if unclaimed_tiles:
                chosen_tile = random.choice(unclaimed_tiles)
                # Generate a new noble and add it to the state's territory
                x, y = chosen_tile
                population_grid[y][x][4] += 1
                territories[y][x] = state_index
                state["commodities"] += 1000
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
                        state["commodities"] += 1000
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
                town["owner"] = state["index"]
                town["colour"] = state["colour"]
                populations = state["population_counts"]
                if town["owner"] != town["founder"]:
                    town["movement"] = 'Separatism'
                    town["unrest"] = state["unrest"]*2
                elif town["owner"] == town["founder"] and populations[6] > populations[4]:
                    town["movement"] = 'Bourgeois Revolution'
                elif town["owner"] == town["founder"] and populations[4] >= populations[6]:
                    town["movement"] = 'Revolt'
                    town["unrest"] = state["unrest"]
        state["towns"] = town_names

        if not town_names:
            state["status"] = 'Primitive Accumulation'
            state["towns"] = "none"
            for y, row in enumerate(territories):
                for x, tile in enumerate(row):
                    if tile == state_index:
                        territories[y][x] = 0

        if state["name"] == 'blank':
            names = state["towns"]
            state["name"], position = get_name(y, x)
            state["colour"] = get_random_color([state["colour"] for state in states])



def get_taxes(state, player_taxes):
    if state["player"] == 'Yes':
        taxes = list(state["taxes"])  # Convert taxes tuple to a list
        grain_rent = player_taxes["grain rent"] / 1000
        land_rent = player_taxes["land rent"] / 1000
        poll_tax = player_taxes["poll tax"] / 1000
        corvee = player_taxes["tolls"] / 1000

        for n in range(len(taxes)):
            taxes[n] = grain_rent
        state["taxes"] = taxes  # Assign the modified taxes list back to the state dictionary
    return state
