import pygame
from pygame.locals import *
import sys
import numpy as np
import random
from ui import draw_button, is_hover, WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, WINDOW_WIDTH, WINDOW_HEIGHT, UI_WIDTH, UI_HEIGHT, UI_POSITION, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, display_population_info, counters
from population_simulation import generate_population_grid, initial_population_caps, update_population_caps, simulate_population_growth, generate_road_grid
from terrain_generation import generate_terrain_grid
from graphics import draw_terrain, determine_terrain_color, draw_terrain_and_population, draw_road_overlay, draw_tribe_location, borders
from primitive_movement import move_population_up, move_population_down, move_population_left, move_population_right, find_starting_location, convert_to_farmers
from controls import move_down, move_left, move_right, move_up, advance, convert_to_farmers_button

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
game_display = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Grid Game!                                              v1.0.6')

overlay_visible = False

# Main game loop
def main():
    # Generate terrain grid
    # Define the size of the x and y axes separately
    x_size = 53
    y_size = 33
    cell_size = 24
    # Generate terrain grid
    terrain_grid = generate_terrain_grid(size_x=x_size, size_y=y_size, num_iterations=5)
    population_grid, initial_caps, town_names, town_positions = generate_population_grid(size_y=y_size, size_x=x_size, terrain_grid=terrain_grid)
    population_caps_grid = initial_population_caps(terrain_grid)
    #Stage and turn
    turn_counter = 0
    stage = 0
    town_positions = []
    town_names = []
    initial_population_caps_grid = initial_population_caps(terrain_grid)
    global overlay_visible  # Add this line

    # Calculate cell sizes based on the dimensions of the window and terrain grid
    cell_width = (WINDOW_WIDTH - UI_WIDTH) // x_size
    cell_height = WINDOW_HEIGHT // y_size
    TILE_WIDTH = cell_size
    TILE_HEIGHT = cell_size
    GRID_WIDTH = cell_width*x_size
    GRID_HEIGHT = cell_height*y_size

    button_labels = ['^', 'v', '<-', '->','S','-','-','-','Borders','SD','SL','SR','-','-','-','-']

    current_tribe_location = (0, 0)
    current_tribe_location = find_starting_location(population_grid)

    while True:

        # Clear the display
        game_display.fill(WHITE)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw main game window
        pygame.draw.rect(game_display, BLACK, (0, 0, WINDOW_WIDTH - UI_WIDTH, WINDOW_HEIGHT))

        # Draw UI
        pygame.draw.rect(game_display, GRAY, (UI_POSITION[0], UI_POSITION[1], UI_WIDTH, UI_HEIGHT))

        # Draw terrain
        draw_terrain_and_population(terrain_grid, population_grid, cell_size)
            
        advance_button_rect = pygame.Rect(UI_POSITION[0] + 10, UI_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)
        button_1_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_2_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 1, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_3_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_4_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 3, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_5_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 4, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_10_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10, BUTTON_WIDTH, BUTTON_HEIGHT)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw population info boxes
        if 0 <= mouse_x < WINDOW_WIDTH and 0 <= mouse_y < WINDOW_HEIGHT:
            # Calculate tile coordinates based on mouse position
            tile_x = (mouse_x // TILE_WIDTH)
            tile_y = (mouse_y // TILE_HEIGHT)
                    
            # Display population info box when hovering over a tile
            if 0 <= tile_x < x_size and 0 <= tile_y < y_size:
                display_population_info(game_display, population_grid[tile_y][tile_x], population_caps_grid, mouse_x, mouse_y, tile_x, tile_y)

        road_grid = generate_road_grid(population_grid, terrain_grid, population_grid, current_tribe_location)

        draw_road_overlay(len(road_grid), len(road_grid[0]), road_grid)

        draw_tribe_location(current_tribe_location, cell_size)  # Draw the population grid

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for button clicks
                if is_hover(pygame.mouse.get_pos(), advance_button_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif is_hover(pygame.mouse.get_pos(), button_1_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_up(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif is_hover(pygame.mouse.get_pos(), button_2_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_down(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif is_hover(pygame.mouse.get_pos(), button_3_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_left(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif is_hover(pygame.mouse.get_pos(), button_4_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_right(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif is_hover(pygame.mouse.get_pos(), button_5_rect):
                    population_grid, terrain_grid, population_caps_grid, road_grid, turn_counter, stage, town_names, town_positions = convert_to_farmers_button(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, stage, town_names, town_positions)
                elif is_hover(pygame.mouse.get_pos(), button_10_rect):
                    overlay_visible = not overlay_visible
            elif event.type == pygame.KEYDOWN:
                # Check for keyboard input
                if event.key == pygame.K_UP:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_up(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif event.key == pygame.K_DOWN:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_down(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif event.key == pygame.K_LEFT:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_left(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif event.key == pygame.K_RIGHT:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = move_right(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif event.key == pygame.K_RETURN:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif event.key == pygame.K_SPACE:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, town_names, town_positions = advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, town_names, town_positions)
                elif event.key == pygame.K_s:
                    population_grid, terrain_grid, population_caps_grid, road_grid, turn_counter, stage, town_names, town_positions = convert_to_farmers_button(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, stage, town_names, town_positions)
                        
        # Draw buttons
        button_positions = []
        for i in range(16):  # Increased number of buttons
            x = UI_POSITION[0] + 10 if i < 8 else UI_POSITION[0] + 10 + BUTTON_WIDTH + BUTTON_MARGIN
            y = UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * (i % 8)
            size = (BUTTON_WIDTH, BUTTON_HEIGHT) if i < 16 else (BUTTON_WIDTH + BUTTON_MARGIN, BUTTON_HEIGHT)  # Double width for the 'Advance' button
            button_positions.append((x, y, size))
        
        # Draw buttons
        for position, label in zip(button_positions, button_labels):
            button_rect = pygame.Rect(position[0], position[1], position[2][0], position[2][1])
            hover = is_hover(mouse_pos, button_rect)
            draw_button(game_display, label, position[:2], position[2], hover)

        # Draw 'Advance' button
        draw_button(game_display, 'Advance', (UI_POSITION[0] + 10, UI_HEIGHT - BUTTON_HEIGHT - 10), (BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT), is_hover(mouse_pos, pygame.Rect(UI_POSITION[0] + 10, UI_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)))
        counters(terrain_grid, game_display, turn_counter, stage)

        for town_name, town_position in zip(town_names, town_positions):
            font = pygame.font.Font(None, 20)
            # Render merchant text
            text = town_name
            surface = font.render(text, True, (255, 255, 255))
            # Calculate text rect for merchants
            rect = surface.get_rect()
            # Calculate the position on the game display
            tile_y, tile_x = town_position  # Assuming town_position is in tile coordinates
            display_y = tile_x * TILE_WIDTH
            display_x = tile_y * TILE_HEIGHT

            rect = surface.get_rect(topleft=(display_x + 25, display_y))
            pygame.draw.rect(game_display, (0, 0, 0), rect)        # Background color for merchants
            game_display.blit(surface, rect)


        if overlay_visible:
            borders(terrain_grid, population_grid)

        # Update the display
        pygame.display.flip()

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        pygame.time.Clock().tick(30)

if __name__ == '__main__':
    main()
