import pygame
from pygame.locals import *
import sys
import numpy as np
import random
import time
from ui import draw_button, is_hover, display_population_info, counters, player_classes_overlay, player_diplomacy_overlay, player_government_overlay
from population_simulation import generate_population_grid, initial_population_caps, update_population_caps, simulate_population_growth, generate_road_grid
from terrain_generation import generate_terrain_grid
from graphics import draw_terrain, determine_terrain_color, draw_terrain_and_population, draw_road_overlay, draw_tribe_location, borders, draw_towns_overlay, draw_beach_lines, player_decisions_overlay
from primitive_movement import move_population_up, move_population_down, move_population_left, move_population_right, find_starting_location, convert_to_farmers
from controls import move_down, move_left, move_right, move_up, advance, convert_to_farmers_button, claim_state_button
from economy import borders, draw_territory_borders, count_population_by_state, draw_economy_overlay
from parameters import cell_height, cell_size, cell_width, x_size, y_size, WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_MARGIN, GRID_WIDTH, GRID_HEIGHT, player_taxes,  slider_position, player_government

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
game_display = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Grid Game!                                                                                  v8.1.4')

class Button:
    def __init__(self, label, rect):
        self.label = label
        self.rect = rect

border_overlay_visible = False
names_overlay_visible = False
economy_overlay_visible = False
towns_overlay_visible = False
player_government_visible = False
player_policies_visible = False
player_classes_visible = False
player_diplomacy_visible = False

# Main game loop
def main():
    # Generate terrain grid
    # Define the size of the x and y axes separately
    # x_size = 53
    # y_size = 33
    # cell_size = 24
    # Generate terrain grid
    terrain_grid = generate_terrain_grid(size_x=x_size, size_y=y_size, num_iterations=5)
    print("terrain initialised")
    time.sleep(0.5)
    population_grid, initial_caps, towns, states, territories = generate_population_grid(size_y=y_size, size_x=x_size, terrain_grid=terrain_grid)
    print("population initialised")
    time.sleep(0.5)
    population_caps_grid = initial_population_caps(terrain_grid)
    print("pop caps initialised")
    time.sleep(0.5)
    #Stage and turn
    turn_counter = 0
    stage = 0
    commodities = 0
    player_taxes = {"tributes": 0.1, "grain rent": 0.1, "land rent": 0.1, "poll tax": 0.1, "tolls": 0.1}
    slider_position = (0,0.1,0.1,0.1,0.1,0,0,0)
    player_government = {"HOS selection": 'None', "HOS powerbase": 'None', "HOS powers": 'None', "CG selection": 'None', "CG powerbase": 'None', "LG selection": 'None', "LG powerbase": 'None',}
    political_rights = {"Taxation": 0, "Military recruitment": 0, "Control of commerce": 0, "Infrastructure": 0, "Subsidies": 0, "State Monopolies": 0, "Conscription": 0, "Tolls": 0, "Tariffs": 0, "Tribute": 0}

    initial_population_caps_grid = initial_population_caps(terrain_grid)
    global border_overlay_visible
    global names_overlay_visible
    global economy_overlay_visible
    global towns_overlay_visible
    global player_government_visible
    global player_policies_visible
    global player_classes_visible
    global player_diplomacy_visible

    # tick_box_checked = False
    # tick_box_checked = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    tick_box_checked = {"Taxation": '0', "Military recruitment": '0', "Control of commerce": '0', "Infrastructure": '0', "Subsidies": '0', "Military spending": '0', "State Monopolies": '0', "Generalship": '0', "Tariffs": '0', "Tribute": '0'}
    selection = ['None', 'None', 'None']
    powerbase = ['None', 'None', 'None']
    display_gov_dropdowns = [0, 0, 0, 0, 0, 0, 0, 0]
                             
    # Calculate cell sizes based on the dimensions of the window and terrain grid
    cell_width = (WINDOW_WIDTH - UI_WIDTH) // x_size
    cell_height = WINDOW_HEIGHT // y_size
    TILE_WIDTH = cell_size
    TILE_HEIGHT = cell_size
    GRID_WIDTH = cell_width*x_size
    GRID_HEIGHT = cell_height*y_size

    button_labels = ['^', 'v', '<-', '->','S','C','-','-','Borders','Names','Economies','Towns','Government','Policies','Classes','Diplomacy']

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
        menu_image = pygame.transform.scale(pygame.image.load('assets/ui_background_5.png'), (180, 685))
        game_display.blit(menu_image, (UI_POSITION[0], UI_POSITION[1], UI_WIDTH, UI_HEIGHT))

        # Draw terrain
        draw_terrain_and_population(terrain_grid, population_grid, cell_size)

        draw_beach_lines(terrain_grid, cell_size, game_display)

        advance_button_rect = pygame.Rect(UI_POSITION[0] + 10, UI_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH * 3.8 + BUTTON_MARGIN, BUTTON_HEIGHT)
        button_1_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_2_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 1, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_3_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_4_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 3, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_5_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 4, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_6_rect = pygame.Rect(UI_POSITION[0] + 10, UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 5, BUTTON_WIDTH, BUTTON_HEIGHT)

        button_10_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_11_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_12_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 2, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_13_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 3, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_14_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 4, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_15_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 5, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_16_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 6, BUTTON_WIDTH*2, BUTTON_HEIGHT)
        button_17_rect = pygame.Rect(UI_POSITION[0] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN), UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * 7, BUTTON_WIDTH*2, BUTTON_HEIGHT)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        road_grid = generate_road_grid(population_grid, terrain_grid, population_grid, current_tribe_location)

        draw_road_overlay(len(road_grid), len(road_grid[0]), road_grid)

        draw_tribe_location(current_tribe_location, cell_size)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for button clicks
                if is_hover(pygame.mouse.get_pos(), advance_button_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif is_hover(pygame.mouse.get_pos(), button_1_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_up(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif is_hover(pygame.mouse.get_pos(), button_2_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_down(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif is_hover(pygame.mouse.get_pos(), button_3_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_left(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif is_hover(pygame.mouse.get_pos(), button_4_rect):
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_right(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif is_hover(pygame.mouse.get_pos(), button_5_rect):
                    population_grid, terrain_grid, population_caps_grid, road_grid, turn_counter, stage, towns, states, territories, player_taxes = convert_to_farmers_button(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, stage, towns, states, territories, player_taxes)
                elif is_hover(pygame.mouse.get_pos(), button_6_rect):
                    claim_state_button(territories, states, current_tribe_location)

                elif is_hover(pygame.mouse.get_pos(), button_10_rect):
                    border_overlay_visible = not border_overlay_visible
                elif is_hover(pygame.mouse.get_pos(), button_11_rect):
                    names_overlay_visible = not names_overlay_visible
                elif is_hover(pygame.mouse.get_pos(), button_12_rect):
                    economy_overlay_visible = not economy_overlay_visible
                elif is_hover(pygame.mouse.get_pos(), button_13_rect):
                    towns_overlay_visible = not towns_overlay_visible
                elif is_hover(pygame.mouse.get_pos(), button_14_rect):
                    player_government_visible = not player_government_visible
                elif is_hover(pygame.mouse.get_pos(), button_15_rect):
                    player_policies_visible = not player_policies_visible
                elif is_hover(pygame.mouse.get_pos(), button_16_rect):
                    player_classes_visible = not player_classes_visible
                elif is_hover(pygame.mouse.get_pos(), button_17_rect):
                    player_diplomacy_visible = not player_diplomacy_visible

            elif event.type == pygame.KEYDOWN:
                # Check for keyboard input
                if event.key == pygame.K_UP:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_up(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif event.key == pygame.K_DOWN:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_down(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif event.key == pygame.K_LEFT:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_left(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif event.key == pygame.K_RIGHT:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = move_right(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif event.key == pygame.K_RETURN:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif event.key == pygame.K_SPACE:
                    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories, player_taxes = advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories, player_taxes)
                elif event.key == pygame.K_ESCAPE:
                    economy_overlay_visible = False
                    towns_overlay_visible = False
                    player_government_visible = False
                    player_policies_visible = False
                    player_classes_visible = False
                    player_diplomacy_visible = False
                elif event.key == pygame.K_s:
                    population_grid, terrain_grid, population_caps_grid, road_grid, turn_counter, stage, towns, states, territories, player_taxes = convert_to_farmers_button(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, stage, towns, states, territories, player_taxes)
                elif event.key == pygame.K_c:
                    claim_state_button(territories, states, current_tribe_location)
    
        # Draw buttons
        button_positions = []
        for i in range(16):  # Increased number of buttons
            x = UI_POSITION[0] + 10 if i < 8 else UI_POSITION[0] + 10 + BUTTON_WIDTH + BUTTON_MARGIN
            y = UI_POSITION[1] + 10 + (BUTTON_HEIGHT + BUTTON_MARGIN) * (i % 8)
            size = (BUTTON_WIDTH, BUTTON_HEIGHT) if i < 8 else (BUTTON_WIDTH * 1.8 + BUTTON_MARGIN, BUTTON_HEIGHT)  # Double width for the 'Advance' button
            button_positions.append((x, y, size))
        
        # Draw buttons
        for position, label in zip(button_positions, button_labels):
            button_rect = pygame.Rect(position[0], position[1], position[2][0], position[2][1])
            hover = is_hover(mouse_pos, button_rect)
            draw_button(game_display, label, position[:2], position[2], hover)

        # Draw 'Advance' button
        draw_button(game_display, 'Advance', (UI_POSITION[0] + 10, UI_HEIGHT - BUTTON_HEIGHT - 10), (BUTTON_WIDTH * 3.2, BUTTON_HEIGHT), is_hover(mouse_pos, pygame.Rect(UI_POSITION[0] + 10, UI_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)))
        counters(terrain_grid, game_display, turn_counter, stage, states)


        if border_overlay_visible:
            territory_colors = borders(territories, states)
            for y, row in enumerate(terrain_grid):
                for x, terrain_type in enumerate(row):
                    # Draw ownership color if applicable
                    ownership_color = territory_colors[y][x]
                    if ownership_color:
                        # Create a surface with per-pixel alpha
                        overlay_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                        # Set the overlay color with alpha channel
                        if ownership_color[0] < 255 and ownership_color[1] < 255 and ownership_color[2] < 255:
                            overlay_color = (ownership_color[0], ownership_color[1], ownership_color[2], 230)  # 150 is the transparency value
                        else:
                            overlay_color = (ownership_color[0], ownership_color[1], ownership_color[2], 10)  # 150 is the transparency value
                        # Fill the surface with the overlay color
                        overlay_surface.fill(overlay_color)
                        # Blit the overlay surface onto the game display
                        game_display.blit(overlay_surface, (x * cell_size, y * cell_size))

        territory_colors = borders(territories, states)
        draw_territory_borders(territories, states, territory_colors, game_display, cell_size)
        count_population_by_state(territories, population_grid, states)

        if names_overlay_visible:
            for town_info in towns:
                name = town_info["name"]
                x = town_info["position_x"]
                y = town_info["position_y"]
                font = pygame.font.Font(None, 16)
                # Render merchant text
                text = name
                surface = font.render(text, True, (255, 255, 255))
                # Calculate text rect for merchants
                rect = surface.get_rect()
                # Calculate the position on the game display
                tile_y = x
                tile_x = y
                display_y = tile_x * TILE_WIDTH
                display_x = tile_y * TILE_HEIGHT

                rect = surface.get_rect(topleft=(display_x + 25, display_y))
                pygame.draw.rect(game_display, (0, 0, 0), rect)        # Background color for merchants
                game_display.blit(surface, rect)


        # Draw population info boxes
        if 0 <= mouse_x < WINDOW_WIDTH and 0 <= mouse_y < WINDOW_HEIGHT:
            # Calculate tile coordinates based on mouse position
            tile_x = (mouse_x // TILE_WIDTH)
            tile_y = (mouse_y // TILE_HEIGHT)
                    
            # Display population info box when hovering over a tile
            if 0 <= tile_x < x_size and 0 <= tile_y < y_size:
                display_population_info(game_display, population_grid[tile_y][tile_x], population_caps_grid, mouse_x, mouse_y, tile_x, tile_y, terrain_grid)

        if economy_overlay_visible:
            draw_economy_overlay(game_display, states)

        if towns_overlay_visible:
            draw_towns_overlay(game_display, towns)

        if player_policies_visible:
            slider_position, player_taxes = player_decisions_overlay(game_display, towns, slider_position, player_taxes)

        if player_government_visible:
            display_gov_dropdowns, player_government, tick_box_checked, political_rights, selection, powerbase = player_government_overlay(game_display, display_gov_dropdowns, player_government, tick_box_checked, political_rights, selection, powerbase)

        if player_classes_visible:
            player_classes_overlay(game_display)

        if player_diplomacy_visible:
            player_diplomacy_overlay(game_display)

        # Update the display
        pygame.display.flip()

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        pygame.time.Clock().tick(30)

if __name__ == '__main__':
    main()
