

x_size = 53
y_size = 33
WINDOW_WIDTH = 1450  # Increased width
WINDOW_HEIGHT = 800
UI_HEIGHT = WINDOW_HEIGHT
UI_WIDTH = 180

# Define sizes and positions for UI elements
UI_POSITION = (WINDOW_WIDTH - UI_WIDTH, 0)
BUTTON_WIDTH = 50  # Narrower buttons
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10
x_size = 53
y_size = 33
cell_size = 24
cell_width = (WINDOW_WIDTH - UI_WIDTH) // x_size
cell_height = WINDOW_HEIGHT // y_size
GRID_WIDTH = cell_width*x_size
GRID_HEIGHT = cell_height*y_size
x_size = 53
y_size = 33
cell_size = 24

state_claimed = 0

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
PUREPLE = (160, 32, 240)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)

slider_position = 0
variable = 0

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