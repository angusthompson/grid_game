import pygame
import random
import math
import noise
import numpy as np
from parameters import cell_height, cell_size, cell_width, x_size, y_size, WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, GRID_WIDTH, GRID_HEIGHT
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
game_display = pygame.display.set_mode(WINDOW_SIZE)

# Define terrain images and scale them to the correct size
terrain_images = {
    1: pygame.transform.scale(pygame.image.load('assets/water2.png'), (cell_size, cell_size)),
    2: pygame.transform.scale(pygame.image.load('assets/grass2.png'), (cell_size, cell_size)),
    3: pygame.transform.scale(pygame.image.load('assets/mountain2.png'), (cell_size, cell_size)),
    4: pygame.transform.scale(pygame.image.load('assets/desert2.png'), (cell_size, cell_size)),
    5: pygame.transform.scale(pygame.image.load('assets/town2.png'), (cell_size, cell_size)),
    6: pygame.transform.scale(pygame.image.load('assets/farmland2.png'), (cell_size, cell_size)),
    8: pygame.transform.scale(pygame.image.load('assets/ice3.png'), (cell_size, cell_size)),
    9: pygame.transform.scale(pygame.image.load('assets/forest4.png'), (cell_size, cell_size)),

    # Add more terrain images as needed
}


# Define colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (200, 200, 150, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_ORANGE = (255, 140, 0)
DARK_GREEN = (0, 100, 0)
DARKER_GREEN = (0, 200, 0)
DARK_GREY = ((64, 128, 128))
DARK_GREY = ((32, 128, 128))
RED = (255, 80, 80)
TRANSLUCENT_RED = (255, 0, 0, 64)  # Semi-transparent red (alpha = 128)

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
TILE_SIZE = 12  # Adjust this value as per your tile size, make sure to also adjust in 'ui' module.


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
    elif terrain_type == 5:  # Town
        return DARK_ORANGE
    elif terrain_type == 6:  # Farmland
        return DARK_GREEN
    elif terrain_type == 7:  # City
        return RED
    elif terrain_type == 8:  # Ice cap
        return WHITE
    elif terrain_type == 9:  # Ice cap
        return DARKER_GREEN

def draw_terrain_and_population(terrain_grid, population_grid, cell_size):
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            # Draw terrain image
            terrain_type = terrain_grid[y][x]
            image = y%3 + x%3
            terrain_image = terrain_images.get(terrain_type, None)
            if terrain_type != 1 and terrain_type != 8:
                if image == 2:
                    terrain_image = pygame.transform.rotate(terrain_image, -90)
                if image > 2:
                    terrain_image = pygame.transform.rotate(terrain_image, -180)

            if terrain_image:
                game_display.blit(terrain_image, (x * cell_size, y * cell_size), special_flags=pygame.BLEND_RGBA_ADD)

            # Generate Perlin noise texture with adjusted scale
            # noise_value = noise.pnoise2(x / 100, y / 100, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=50, repeaty=50, base=0)

            # Normalize noise value to range [0, 255]
            # noise_value = int(np.interp(noise_value, (-1, 1), (0, 150)))

            # Create surface for overlay effect
            overlay_surface = pygame.Surface((cell_size, cell_size))
            overlay_surface.set_alpha(100)  # Adjust the alpha value to control the transparency of the overlay effect

            # Draw noise texture onto overlay surface
            # color = (noise_value, noise_value, noise_value)  # Use noise value as grayscale color
            # pygame.draw.rect(overlay_surface, color, (0, 0, cell_size, cell_size))

            # Blit overlay surface onto game display
            game_display.blit(overlay_surface, (x * cell_size, y * cell_size))

            # Render population number
            population = int(population_grid[y][x][0])  # Convert to integer
            if population > 0:
                font = pygame.font.Font(None, 15)
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

from ui import GRID_WIDTH, GRID_HEIGHT, cell_size

def borders(terrain_grid, population_grid, town_positions, cell_size, game_display):
    # Create a surface for the translucent overlay
    translucent_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT), pygame.SRCALPHA)

    # Create a dictionary to store town borders
    town_borders = {}

    # Iterate through town positions
    for town_position in town_positions:
        # Get town position coordinates
        town_x, town_y = town_position

        # Check if the town is already assigned a border color
        if town_position not in town_borders:
            # Generate a random translucent color for the border
            border_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100)

            # Cover tiles within two tiles of the town with the border color
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    new_y = town_y + dy
                    new_x = town_x + dx
                    if 0 <= new_y < len(terrain_grid) and 0 <= new_x < len(terrain_grid[0]) and terrain_grid[new_y][new_x] != 1:
                        # Modify the alpha value of the color to make it translucent
                        pygame.draw.rect(translucent_surface, border_color, (new_x * cell_size, new_y * cell_size, cell_size, cell_size))

            # Store the border color for the town
            town_borders[town_position] = border_color

    # Blit the translucent surface onto the screen without any offset
    game_display.blit(translucent_surface, (0, 0))

    # Return the updated town borders dictionary
    return town_borders

def get_random_color(existing_colors):
    while True:
        # Generate a random color
        color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        # Check similarity with existing colors
        similar_color = False
        for existing_color in existing_colors:
            # Calculate Euclidean distance between colors
            distance = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color, existing_color)))
            if distance < 70:  # Adjust this threshold as needed
                color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        
        if not similar_color:
            return color
        

def draw_towns_overlay(screen, towns):
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

    display_towns_only(screen, pygame.font.Font(None, 20), towns, overlay_width, overlay_height, overlay_x, overlay_y)


def display_towns_only(screen, font, towns, overlay_width, overlay_height, overlay_x, overlay_y):
    if len(towns) > 0:
        # Font settings
        title_font = pygame.font.SysFont(None, 20, bold=True)
        font_size = 12  # Font size for other cells

        overlay_x += 25
        overlay_y += 10  # Move down vertically by 10 pixels
        # Calculate cell dimensions
        cell_width = (overlay_width-70) // 7  # Adjusted to make room for wider "Populations" column
        cell_height = font_size * 1.5  # Adjust based on font size

        titles = ["Name", "Position x", "Position y", "Founder", "Owner", "Movement", "Unrest"]

        # Extract color values from "Colour" column
        colors = [town["colour"] for town in towns]
        town_values_to_show = [{key: value for key, value in town.items() if key not in ["colour"]} for town in towns]

        # Draw column titles
        for i, title in enumerate(titles):
            title_surface = title_font.render(title, True, BLACK)
            title_rect = title_surface.get_rect(center=(overlay_x + (i + 0.5) * cell_width, overlay_y + cell_height / 2))
            screen.blit(title_surface, title_rect)

        # Loop through data and draw each cell
        for i, town in enumerate(town_values_to_show):
            # Calculate row position
            row_y = overlay_y + (i + 1) * cell_height  # Start after the title row
            
            # Loop through town attributes and draw each cell
            for j, (key, value) in enumerate(town.items()):
                # Calculate cell position
                cell_x = overlay_x + j * cell_width

                # Draw cell rectangle
                pygame.draw.rect(screen, colors[i], (cell_x, row_y, cell_width, cell_height))
                pygame.draw.rect(screen, BLACK, (cell_x, row_y, cell_width, cell_height), 1)

                # Render text
                text_surface = font.render(str(value), True, BLACK)
                text_rect = text_surface.get_rect(center=(cell_x + cell_width / 2, row_y + cell_height / 2))

                # Blit text to screen
                screen.blit(text_surface, text_rect)
    else:
        pass

def player_decisions_overlay(screen, towns):
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

# Function to detect sea borders
def detect_sea_borders(terrain_grid):
    sea_borders = []
    neighbors = []
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            if terrain_grid[y][x] == 1:
                # Select sea tiles and check neighboring cells
                neighbors1 = [(x, y+dy) for dy in (-1, 0, 1) if (dy != 0)]
                neighbors2 = [(x+dx, y) for dx in (-1, 0, 1) if (dx != 0)]
                for nx, ny in neighbors1:
                    if 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid) and terrain_grid[ny][nx] != 1:
                        if terrain_grid[ny][nx] != 8 and terrain_grid[ny][nx] != 3:
                            sea_borders.append((x, y))
                            # This returns a list of all tiles adjacent to seas which are not seas
                            break
                for nx, ny in neighbors2:
                    if 0 <= nx < len(terrain_grid[0]) and 0 <= ny < len(terrain_grid) and terrain_grid[ny][nx] != 1:
                        if terrain_grid[ny][nx] != 8 and terrain_grid[ny][nx] != 3:
                            sea_borders.append((x, y))
                            # This returns a list of all tiles adjacent to seas which are not seas
                            break
    return sea_borders

def draw_beach_lines(terrain_grid, cell_size, game_display):
    offsets = [-2, -1, 0, 0, 0, 1, 2]
    sea_borders = detect_sea_borders(terrain_grid)
    for x, y in sea_borders:
        # Draw semi-transparent yellow lines along the sea borders
        if (x + 1, y) not in sea_borders and (x + 1) < len(terrain_grid[0]):
            if terrain_grid[y][x+1] != 1:
                for offset in offsets:
                    line_surface = pygame.Surface((5, cell_size), pygame.SRCALPHA)  # Create a surface for the line
                    if terrain_grid[y][x+1] == 4:
                        line_surface.fill((241, 160, 96, 30))
                    else:
                        line_surface.fill((200, 200, 150, 50))
                    game_display.blit(line_surface, ((x + 1) * cell_size + offset, y * cell_size))  # Blit the line surface to the game display
        if (x - 1, y) not in sea_borders and (x + 1) < len(terrain_grid[0]):
            if terrain_grid[y][x-1] != 1:
                for offset in offsets:
                    line_surface = pygame.Surface((5, cell_size), pygame.SRCALPHA)
                    if terrain_grid[y][x-1] == 4:
                        line_surface.fill((241, 160, 96, 30))
                    else:
                        line_surface.fill((200, 200, 150, 50))                    
                    game_display.blit(line_surface, (x * cell_size + offset, y * cell_size))
        if (x, y + 1) not in sea_borders and (x + 1) < len(terrain_grid[0]):
            if terrain_grid[y+1][x] != 1:
                for offset in offsets:
                    line_surface = pygame.Surface((cell_size, 5), pygame.SRCALPHA)
                    if terrain_grid[y+1][x] == 4:
                        line_surface.fill((241, 160, 96, 30))
                    else:
                        line_surface.fill((200, 200, 150, 30))                    
                    game_display.blit(line_surface, (x * cell_size, (y + 1) * cell_size + offset))
        if (x, y - 1) not in sea_borders and (x + 1) < len(terrain_grid[0]):            
            if terrain_grid[y-1][x] != 1:
                for offset in offsets:
                    line_surface = pygame.Surface((cell_size, 5), pygame.SRCALPHA)
                    if terrain_grid[y-1][x] == 4:
                        line_surface.fill((241, 160, 96, 30))
                    else:
                        line_surface.fill((200, 200, 150, 50))                    
                    game_display.blit(line_surface, (x * cell_size, y * cell_size + offset))

