from graphics import get_random_color
from parameters import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, x_size, y_size, cell_size, cell_width, cell_height, GRID_WIDTH, GRID_HEIGHT

def revolt(state, town, territories, population_grid):
    # print("Revolt in ", town["name"], ",", state["name"], "!")

    x = town["position_x"]
    y = town["position_y"]

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if nx < x_size and ny < y_size:
                if territories[ny][nx] != 0:
                    population_grid[ny][nx][2] -= round(population_grid[ny][nx][2] * 0.1, 1)
                    population_grid[ny][nx][3] -= round(population_grid[ny][nx][3] * 0.1, 1)
                    population_grid[ny][nx][4] -= round(population_grid[ny][nx][4] * 0.3, 1)
                    population_grid[ny][nx][5] -= round(population_grid[ny][nx][5] * 0.1, 1)
                    population_grid[ny][nx][6] -= round(population_grid[ny][nx][6] * 0.1, 1)

def secession(state, states, town, territories, population_grid):
    # print("Secession in ", town["name"], ",", state["name"], "!")

    # Assign values to new state
    single_name = town["name"]
    x = town["position_x"]
    y = town["position_y"]
    colour = get_random_color([state["colour"] for state in states])
    names_list = []
    names_list.append(single_name)
    population_counts = [0, 1, 1, 1, 1, 0, 0, 0]
    index = town["founder"]
    # Add new state 
    new_state = {"name": single_name, "state": index, "colour": colour, "towns": names_list, "commodities": 0, "tax_rev": 0, "population_counts": population_counts, "expansionism": 0, "military_power": 300, "noble_growth": 0, "unrest": 0, "status": 'Primitive Accumulation', "index": index, "capital": (y, x), "player": 'No', "taxes": (0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)}
    states.append({"name": single_name, "state": index, "colour": colour, "towns": names_list, "commodities": 0, "tax_rev": 0, "population_counts": population_counts, "expansionism": 0, "military_power": 300, "noble_growth": 0, "unrest": 0, "status": 'Primitive Accumulation', "index": index, "capital": (y, x), "player": 'No', "taxes": (0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)})
    test_capital = new_state["capital"]
    town["owner"] = town["founder"]
    town["colour"] = colour
    town["unrest"] = 0
    town["movement"] = 'Revolt'

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if nx < x_size and ny < y_size:
                if territories[ny][nx] != 0:
                    territories[ny][nx] = town["founder"]

    return states, town, territories

def bourgeois_revolution(state, town, territories, population_grid):
    # print("Revolution in ", town["name"], state["name"], "!")
    pass