from terrain_generation import get_name
from ui import UI_POSITION, UI_HEIGHT
import pygame

def calculate_city_territories(population_grid, town_positions):
    city_territories = []

    for city_position in town_positions:
        city_x, city_y = city_position
        territory = []

        # Iterate over tiles within 2 tiles of the city (including the city itself)
        for y in range(city_y - 2, city_y + 3):
            for x in range(city_x - 2, city_x + 3):
                # Ensure the tile is within the bounds of the population grid
                if 0 <= x < len(population_grid[0]) and 0 <= y < len(population_grid):
                    territory.append((x, y))

        city_territories.append(territory)

    return city_territories

def update_towns_with_territory_population(population_grid, towns, town_positions):
    city_territories = calculate_city_territories(population_grid, town_positions)
    for i, city_territory in enumerate(city_territories):
        total_population = 0

        for x, y in city_territory:
            total_population += population_grid[y][x][0]

        towns[i]["territory_population"] = total_population


def display_towns(screen, font, towns):
    font_size = 16  # Font size for town names

    # Iterate over towns
    for i, town in enumerate(towns):
        name = town["name"]
        position = town["position"]
        color = town["color"]
        population = town["territory_population"]  # New population information

        # Render town name on a background of the town's color
        name_surface = font.render(name + " City", True, (255, 255, 255))  # White text color
        text_rect = name_surface.get_rect()
        text_rect.topleft = (UI_POSITION[0] + 10, UI_HEIGHT - 300 + (i) * font_size * 3)
        pygame.draw.rect(screen, color, text_rect)  # Draw background of town color
        screen.blit(name_surface, text_rect.topleft)

        # Render population information
        population_surface = font.render(f"Population: {population}", True, (255, 255, 255))  # White text color
        population_rect = population_surface.get_rect()
        population_rect.topleft = (UI_POSITION[0] + 10, UI_HEIGHT - 285 + (i) * font_size * 3)  # Adjust y position
        screen.blit(population_surface, population_rect.topleft)


