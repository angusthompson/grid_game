import pygame
import terrain_generation
from terrain_generation import generate_terrain_grid
from terrain_generation import update_terrain_grid
from terrain_generation import get_neighbors
import population_simulation_2
from population_simulation_2 import generate_population_grid
from population_simulation_2 import count_coast_adjacency
from population_simulation_2 import simulate_population_growth
from population_simulation_2 import update_population_caps
import graphics
from graphics import draw_terrain_grid
from graphics import draw_population_grid
from graphics import draw_button

# Main game loop and event handling here

import pygame
import random
import numpy as np

# Define colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_ORANGE = (255, 140, 0)
DARK_GREEN = (0, 100, 0)

# Define constants
GRID_SIZE = 40
BOX_SIZE = 20
WINDOW_SIZE = (GRID_SIZE * BOX_SIZE * 1.5, GRID_SIZE * BOX_SIZE)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT_HOVER_COLOR = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Terrain Simulation")

    terrain_grid = terrain_generation.generate_terrain_grid(GRID_SIZE)
    population_grid, initial_population_caps = population_simulation_2.generate_population_grid(GRID_SIZE, terrain_grid)
    
    # Initialize farmland adjacency grid
    farmland_adjacency = population_simulation_2.update_farmland_adjacency(terrain_grid)

    button_width, button_height = 100, 50
    button_x = (WINDOW_SIZE[0] - button_width) // 2
    button_y = WINDOW_SIZE[1] - 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    running = True
    button_hover = False
    while running:
        screen.fill(WHITE)
        graphics.draw_terrain_grid(screen, terrain_grid)
        graphics.draw_population_grid(screen, population_grid)
        graphics.draw_button(screen, button_rect, button_hover)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    # Update population caps based on coast and farmland adjacency
                    population_caps = population_simulation_2.update_population_caps(initial_population_caps, terrain_grid, farmland_adjacency)
                    
                    # Simulate population growth using the updated population caps
                    population_grid, terrain_grid = population_simulation_2.simulate_population_growth(population_grid, initial_population_caps, terrain_grid, farmland_adjacency)
            elif event.type == pygame.MOUSEMOTION:
                button_hover = button_rect.collidepoint(event.pos)

    pygame.quit()

if __name__ == "__main__":
    main()
