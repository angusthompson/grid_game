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