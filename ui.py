import pygame
from parameters import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, x_size, y_size, cell_size, cell_width, cell_height, GRID_WIDTH, GRID_HEIGHT

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

    # Render noble text
    noble_text = "Nobles: " + str(population[4])
    noble_surface = font.render(noble_text, True, (255, 255, 255))
    # Calculate text rect for nobles
    noble_rect = noble_surface.get_rect()
    noble_rect.topleft = (x + 15, y  + population_rect.height*5 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), noble_rect)        # Background color for nobles

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

    # Blit hunter gatherer text onto game display
    game_display.blit(noble_surface, noble_rect)

def counters(terrain_grid, surface, turn_counter, stage, states):
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
                for state in states:
                    towns_in_state = sum(1 for town in state['towns'])
                    if towns_in_state > 1 and stage < 3:
                        stage +=1

        if stage == 0:
            stage_name = 'Hunter-Gatherers'
        if stage == 1:
            stage_name = 'Farming Communities'
        if stage == 2:
            stage_name = 'Permanent Settlements'
        if stage == 3:
            stage_name = 'Early States'
        elif stage > 3:
            stage_name = 'Broken History'
        # Display stage
        stage_text = f"Stage: {stage_name}"
        stage_surface = font.render(stage_text, True, (0, 0, 0))
        surface.blit(stage_surface, (UI_POSITION[0] + 10, UI_HEIGHT - 80))

import pygame