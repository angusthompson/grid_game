import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)
GREEN = (0, 255, 0)

# Define sizes and positions for UI elements
UI_WIDTH = 130
WINDOW_WIDTH = 1400  # Increased width
WINDOW_HEIGHT = 800
UI_HEIGHT = WINDOW_HEIGHT
UI_POSITION = (WINDOW_WIDTH - UI_WIDTH, 0)
BUTTON_WIDTH = 50  # Narrower buttons
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10


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
def display_population_info(game_display, population, x, y, tile_x, tile_y):
    font = pygame.font.Font(None, 20)

    # Render tile coordinates text
    tile_text = "Tile: " + str(tile_x) + " , " + str(tile_y)
    tile_surface = font.render(tile_text, True, (255, 255, 255))

    # Render population text
    population_text = "Population: " + str(population[0])
    population_surface = font.render(population_text, True, (255, 255, 255))

    # Render hunter-gatherer text
    huntergatherer_text = "Hunter-gatherers: " + str(population[1])
    huntergatherer_surface = font.render(huntergatherer_text, True, (255, 255, 255))

    # Calculate text rect for population
    population_rect = population_surface.get_rect()
    population_rect.topleft = (x + 15, y + 25 + population_rect.height)

    # Calculate text rect for tile coordinates
    tile_rect = tile_surface.get_rect()
    tile_rect.topleft = (x + 15, y + 25)

    # Calculate text rect for hunter gatherers
    huntergatherer_rect = huntergatherer_surface.get_rect()
    huntergatherer_rect.topleft = (x + 15, y  + population_rect.height*2 + 25)

    # Draw background rectangles
    pygame.draw.rect(game_display, (0, 0, 0), population_rect)  # Background color for population
    pygame.draw.rect(game_display, (0, 0, 0), tile_rect)        # Background color for tile
    pygame.draw.rect(game_display, (0, 0, 0), huntergatherer_rect)        # Background color for tile

    # Blit population text onto game display
    game_display.blit(population_surface, population_rect)

    # Blit tile coordinates text onto game display
    game_display.blit(tile_surface, tile_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(huntergatherer_surface, huntergatherer_rect)