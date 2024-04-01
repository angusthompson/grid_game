import pygame
from ui import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, WINDOW_WIDTH, WINDOW_HEIGHT, UI_WIDTH, UI_HEIGHT, UI_POSITION, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
game_display = pygame.display.set_mode(WINDOW_SIZE)

# Define colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_ORANGE = (255, 140, 0)
DARK_GREEN = (0, 100, 0)
DARK_GREY = ((64, 128, 128))
RED = (255, 80, 80)

# Define constants
# GRID_SIZE = 60
BOX_SIZE = 15
# WINDOW_SIZE = (GRID_SIZE * BOX_SIZE, GRID_SIZE * BOX_SIZE)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT_HOVER_COLOR = (255, 255, 255)
# Assuming these constants are defined in your code
PURPLE = (128, 0, 128)
TILE_SIZE = 12  # Adjust this value as per your tile size


# Function to draw terrain
def draw_terrain(terrain_grid):
    # Assuming terrain grid is a numpy array
    cell_size = (WINDOW_WIDTH - UI_WIDTH) // len(terrain_grid)
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            terrain_type = terrain_grid[y][x]
            color = determine_terrain_color(terrain_type)
            pygame.draw.rect(game_display, color, (x * cell_size, y * cell_size, cell_size, cell_size))

# Function to determine color based on terrain type
def determine_terrain_color(terrain_type):
    if terrain_type == 1:
        return BLUE
    elif terrain_type == 2:
        return GREEN
    elif terrain_type == 3:
        return GREY
    elif terrain_type == 4:
        return YELLOW
    elif terrain_type == 5:  # Village
        return DARK_ORANGE
    elif terrain_type == 6:  # Farmland
        return DARK_GREEN
    elif terrain_type == 7:  # Town
        return RED
    

def draw_terrain_and_population(terrain_grid, population_grid, cell_size):
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            terrain_type = terrain_grid[y][x]
            color = determine_terrain_color(terrain_type)
            pygame.draw.rect(game_display, color, (x * cell_size, y * cell_size, cell_size, cell_size))

            # Render population number
            population = int(population_grid[y][x][0])  # Convert to integer
            if population > 0:
                font = pygame.font.Font(None, 20)
                text_surface = font.render(str(population), True, BLACK)
                text_rect = text_surface.get_rect(center=(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2))
                game_display.blit(text_surface, text_rect)

def draw_road_overlay(x_size, y_size, road_grid):
    # for y in range(x_size):
    #     for x in range(y_size):
    #         if road_grid[y][x] == 1:
    #             # Draw a thick border around tiles with roads
    #             pygame.draw.rect(game_display, BLACK, (x * BOX_SIZE, y * BOX_SIZE, BOX_SIZE, BOX_SIZE), 3)
    return('hello')

def draw_tribe_location(current_tribe_location, cell_size):
    x, y = current_tribe_location
    # Calculate the pixel coordinates of the tile
    tile_x = x * cell_size
    tile_y = y * cell_size
    # Draw a purple border around the tile
    pygame.draw.rect(game_display, PURPLE, (tile_x, tile_y, cell_size, cell_size), 1)
