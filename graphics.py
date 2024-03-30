import pygame

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
GRID_SIZE = 30
BOX_SIZE = 20
WINDOW_SIZE = (GRID_SIZE * BOX_SIZE, GRID_SIZE * BOX_SIZE)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT_HOVER_COLOR = (255, 255, 255)

# Function to draw terrain grid
def draw_terrain_grid(screen, terrain_grid):
    for y in range(len(terrain_grid)):
        for x in range(len(terrain_grid[y])):
            color = None
            if terrain_grid[y][x] == 1:
                color = BLUE
            elif terrain_grid[y][x] == 2:
                color = GREEN
            elif terrain_grid[y][x] == 3:
                color = GREY
            elif terrain_grid[y][x] == 4:
                color = YELLOW
            elif terrain_grid[y][x] == 5:  # Town
                color = DARK_ORANGE
            elif terrain_grid[y][x] == 6:  # Farmland
                color = DARK_GREEN
            pygame.draw.rect(screen, color, (x * BOX_SIZE, y * BOX_SIZE, BOX_SIZE, BOX_SIZE))
            pygame.draw.rect(screen, WHITE, (x * BOX_SIZE, y * BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)

# Function to draw population grid
def draw_population_grid(screen, population_grid):
    font = pygame.font.Font(None, 20)
    for y in range(len(population_grid)):
        for x in range(len(population_grid[y])):
            if population_grid[y][x] > 0:
                text = font.render(str(population_grid[y][x]), True, BLACK)
                text_rect = text.get_rect(center=(x * BOX_SIZE + BOX_SIZE // 2, y * BOX_SIZE + BOX_SIZE // 2))
                screen.blit(text, text_rect)

# Function to draw button
def draw_button(screen, button_rect, button_hover):
    button_color = BUTTON_HOVER_COLOR if button_hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    font = pygame.font.Font(None, 24)
    text = font.render("Advance", True, BUTTON_TEXT_HOVER_COLOR if button_hover else BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)