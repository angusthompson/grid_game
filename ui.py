import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
GREEN = (0, 255, 0)

# Define sizes and positions for UI elements
UI_WIDTH = 180
WINDOW_WIDTH = 1450  # Increased width
WINDOW_HEIGHT = 800
UI_HEIGHT = WINDOW_HEIGHT
UI_POSITION = (WINDOW_WIDTH - UI_WIDTH, 0)
BUTTON_WIDTH = 50  # Narrower buttons
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10
x_size = 53
y_size = 33
cell_size = 24
cell_width = (WINDOW_WIDTH - UI_WIDTH) // x_size
cell_height = WINDOW_HEIGHT // y_size
GRID_WIDTH = cell_width*x_size
GRID_HEIGHT = cell_height*y_size




# Function to draw buttons
def draw_button(surface, text, position, size, hover):
    font = pygame.font.Font(None, 24)
    button_text = font.render(text, True, BLACK)
    button_rect = pygame.Rect(position, size)
    
    if hover:
        pygame.draw.rect(surface, LIGHT_GRAY, button_rect)
    else:
        pygame.draw.rect(surface, GRAY, button_rect)
    pygame.draw.rect(surface, BLACK, button_rect, 2)  # Add border
    surface.blit(button_text, (position[0] + 10, position[1] + 10))

# Function to check if mouse is hovering over a button
def is_hover(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

# Function to display the population information box
def display_population_info(game_display, population, population_caps_grid, x, y, tile_x, tile_y):
    font = pygame.font.Font(None, 20)

    popcap = population_caps_grid[tile_y][tile_x]

    # Render tile coordinates text
    tile_text = "Tile: " + str(tile_x) + " , " + str(tile_y) + ', ' + str(popcap)
    tile_surface = font.render(tile_text, True, (255, 255, 255))
    # Calculate text rect for tile coordinates
    tile_rect = tile_surface.get_rect()
    tile_rect.topleft = (x + 15, y + 25)
    pygame.draw.rect(game_display, (0, 0, 0), tile_rect)        # Background color for tile

    # Render population text
    population_text = "Population: " + str(population[0])
    population_surface = font.render(population_text, True, (255, 255, 255))
    # Calculate text rect for population
    population_rect = population_surface.get_rect()
    population_rect.topleft = (x + 15, y + 25 + population_rect.height)
    pygame.draw.rect(game_display, (0, 0, 0), population_rect)  # Background color for population

    # Render hunter-gatherer text
    huntergatherer_text = "Hunter-gatherers: " + str(population[1])
    huntergatherer_surface = font.render(huntergatherer_text, True, (255, 255, 255))
    # Calculate text rect for hunter gatherers
    huntergatherer_rect = huntergatherer_surface.get_rect()
    huntergatherer_rect.topleft = (x + 15, y  + population_rect.height*2 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), huntergatherer_rect)        # Background color for tile

    # Render farmer text
    farmer_text = "Farmers: " + str(population[2])
    farmer_surface = font.render(farmer_text, True, (255, 255, 255))
    # Calculate text rect for farmers
    farmer_rect = farmer_surface.get_rect()
    farmer_rect.topleft = (x + 15, y  + population_rect.height*3 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), farmer_rect)        # Background color for farmers

    # Render merchant text
    merchant_text = "Merchants: " + str(population[3])
    merchant_surface = font.render(merchant_text, True, (255, 255, 255))
    # Calculate text rect for merchants
    merchant_rect = merchant_surface.get_rect()
    merchant_rect.topleft = (x + 15, y  + population_rect.height*4 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), merchant_rect)        # Background color for merchants


    # Blit population text onto game display
    game_display.blit(population_surface, population_rect)

    # Blit tile coordinates text onto game display
    game_display.blit(tile_surface, tile_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(huntergatherer_surface, huntergatherer_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(farmer_surface, farmer_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(merchant_surface, merchant_rect)

def counters(terrain_grid, surface, turn_counter, stage):
        # Display turn counter
        font = pygame.font.Font(None, 17)
        turn_text = f"Turn: {turn_counter}"
        turn_surface = font.render(turn_text, True, (0, 0, 0))
        surface.blit(turn_surface, (UI_POSITION[0] + 10, UI_HEIGHT - 100))
        size_y, size_x = terrain_grid.shape

        for y in range(size_y):
            for x in range(size_x):
                 if terrain_grid[y][x] == 6 and stage < 1:
                      stage += 1
                 if terrain_grid[y][x] == 5 and stage < 2:
                      stage += 1

        if stage == 0:
            stage_name = 'Hunter-Gatherers'
        if stage == 1:
            stage_name = 'Farming Communities'
        if stage == 2:
            stage_name = 'Permanent Settlements'
        elif stage > 2:
            stage_name = 'Broken History'
        # Display stage
        stage_text = f"Stage: {stage_name}"
        stage_surface = font.render(stage_text, True, (0, 0, 0))
        surface.blit(stage_surface, (UI_POSITION[0] + 10, UI_HEIGHT - 80))

import pygame

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
    for state in states:
        populations = state["population_counts"]
        commodities = state["commodities"]
        farmer_population = populations[2]
        merchant_population = populations[3]
        commodities += merchant_population * 0.3
        commodities -= farmer_population * 0.1
        state["commodities"] = round(commodities, 1)


def display_towns(screen, font, states, overlay_width, overlay_height, overlay_x, overlay_y):
    font_size = 16  # Font size for state names
    commodities(states)

    # Iterate over states
    for i, state in enumerate(states):
        name = state["name"]
        color = state["colour"]
        populations = state["population_counts"]
        state_commodities = state["commodities"]
        total_population = populations[0]  # Get total population from the state dictionary
        merchant_population = populations[3]

        # Render state name, total population, merchant population, and state commodities on separate lines
        name_surface = font.render(name, True, (255, 255, 255))  # White text color
        total_pop_surface = font.render(f"Total Population: {total_population}", True, (255, 255, 255))
        merchant_pop_surface = font.render(f"Merchant Population: {merchant_population}", True, (255, 255, 255))
        commodities_surface = font.render(f"Commodities: {i}", True, (255, 255, 255))

        # Calculate vertical position for each line
        name_rect = name_surface.get_rect()
        total_pop_rect = total_pop_surface.get_rect()
        merchant_pop_rect = merchant_pop_surface.get_rect()
        commodities_rect = commodities_surface.get_rect()
        if i < 11:
            name_rect.topleft = (100, UI_HEIGHT - 700 + (i) * font_size * 4)
            total_pop_rect.topleft = (100, UI_HEIGHT - 700 + 15 + (i) * font_size * 4)
            merchant_pop_rect.topleft = (100, UI_HEIGHT - 700 + 30 + (i) * font_size * 4)
            commodities_rect.topleft = (100, UI_HEIGHT - 700 + 45 + (i) * font_size * 4)
        if i > 11:
            name_rect.topleft = (200, UI_HEIGHT - 700 + (i - 10) * font_size * 4)
            total_pop_rect.topleft = (200, UI_HEIGHT - 700 + 15 + (i - 10) * font_size * 4)
            merchant_pop_rect.topleft = (200, UI_HEIGHT - 700 + 30 + (i - 10) * font_size * 4)
            commodities_rect.topleft = (200, UI_HEIGHT - 700 + 45 + (i - 10) * font_size * 4)
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
