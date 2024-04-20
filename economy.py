from terrain_generation import get_name
from graphics import get_random_color
from ui import UI_POSITION, UI_HEIGHT
import pygame

x_size = 53
y_size = 33

def generate_state(i, town, x, y, states, territories):
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
                if territories[ny][nx] == 0:
                    territories[ny][nx] = len(states)
    return states, territories

def add_to_state(i, n, town, x, y, states, territories):
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
                    if territories[ny][nx] == 0:
                        territories[ny][nx] = n
    states

def find_towns(population_grid, terrain_grid, towns, states, territories):
    # print(towns)
    z = 0
    for i in towns:
        town = towns[z]
        # print(town)
        x = town['position_x']
        y = town['position_y']
        if territories[y][x] == 0:
            generate_state(z, town, x, y, states, territories)
        else:
            n = territories[y][x]
            add_to_state(z, n, town, x, y, states, territories)
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

def display_towns(screen, font, states):
    font_size = 16  # Font size for town names

    # Iterate over towns
    for i, state in enumerate(states):
        name = state["name"]
        color = state["colour"]
        # population = state["territory_population"]  # New population information

        # Render town name on a background of the town's color
        name_surface = font.render(name+'ia', True, (255, 255, 255))  # White text color
        text_rect = name_surface.get_rect()
        text_rect.topleft = (UI_POSITION[0] + 10, UI_HEIGHT - 300 + (i) * font_size)
        pygame.draw.rect(screen, color, text_rect)  # Draw background of town color
        screen.blit(name_surface, text_rect.topleft)

        # # Render population information
        # population_surface = font.render(f"Population: {population}", True, (255, 255, 255))  # White text color
        # population_rect = population_surface.get_rect()
        # population_rect.topleft = (UI_POSITION[0] + 10, UI_HEIGHT - 285 + (i) * font_size * 3)  # Adjust y position
        # screen.blit(population_surface, population_rect.topleft)

