from population_simulation import generate_population_grid, initial_population_caps, update_population_caps, simulate_population_growth, generate_road_grid, simulate_population_attrition, remove_towns, terrain_development
from terrain_generation import generate_terrain_grid
from graphics import draw_terrain, determine_terrain_color, draw_terrain_and_population, draw_road_overlay, draw_tribe_location
from primitive_movement import move_population_up, move_population_down, move_population_left, move_population_right, find_starting_location, convert_to_farmers
from economy import commodities, check_towns
import time

def move_up(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories):
    # Simulate the 'Up' button click
    population_grid, current_tribe_location = move_population_up(population_grid, terrain_grid, current_tribe_location)
    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories= advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories)
    return population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories

def move_down(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories):
    # Simulate the 'Down' button click
    population_grid, current_tribe_location = move_population_down(population_grid, terrain_grid, current_tribe_location)
    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories= advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories)
    return population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories

def move_left(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories):
    # Simulate the 'Left' button click
    population_grid, current_tribe_location = move_population_left(population_grid, terrain_grid, current_tribe_location)
    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories= advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories)
    return population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories

def move_right(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories):
    # Simulate the 'Right' button click
    population_grid, current_tribe_location = move_population_right(population_grid, terrain_grid, current_tribe_location)
    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories= advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories)
    return population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories

def advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories):
    population_caps_grid = update_population_caps(initial_population_caps_grid, terrain_grid, population_grid)
    # print("updated population caps")
    size_y, size_x = terrain_grid.shape  # Get the shape of the terrain grid
    for y in range(size_y):
        for x in range(size_x):
            population_grid, terrain_grid = simulate_population_growth(current_tribe_location, population_grid, population_caps_grid, terrain_grid, y, x)
            population_grid, terrain_grid, towns, states, territories = simulate_population_attrition(population_grid, population_caps_grid, terrain_grid, towns, states, territories, y, x)
    # print("population grown")
    # print("population attrited")
    population_grid, terrain_grid, towns, states, territories = remove_towns(current_tribe_location, population_grid, terrain_grid, towns, states, territories, y, x)
    for y in range(size_y):
        for x in range(size_x):
            terrain_grid, population_grid, population_caps_grid, towns, states, territories = terrain_development(terrain_grid, population_grid, population_caps_grid, towns, states, territories, y, x)
    population_caps_grid = update_population_caps(initial_population_caps_grid, terrain_grid, population_grid)
    # print("updated population caps")
    road_grid = generate_road_grid(population_grid, terrain_grid, population_grid, current_tribe_location)
    turn_counter += 1
    commodities(states, territories, population_grid, terrain_grid, towns)
    # print("calculated commodities")
    check_towns(towns, states, territories)
    # print("checked towns")
    return population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories

def convert_to_farmers_button(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, stage, towns, states, territories):
    # Convert population to farmers and update terrain
    convert_to_farmers(population_grid, terrain_grid, current_tribe_location, stage)
    # stage += 1
    population_grid, terrain_grid, current_tribe_location, population_caps_grid, road_grid, turn_counter, towns, states, territories= advance(population_grid, terrain_grid, current_tribe_location, population_caps_grid, initial_population_caps_grid, turn_counter, towns, states, territories)
    return population_grid, terrain_grid, population_caps_grid, road_grid, turn_counter, stage, towns, states, territories
