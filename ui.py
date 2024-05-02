import pygame
from parameters import WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY, GREEN, UI_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, UI_HEIGHT, UI_POSITION, BUTTON_HEIGHT, BUTTON_MARGIN, x_size, y_size, cell_size, cell_width, cell_height, GRID_WIDTH, GRID_HEIGHT, display_gov_dropdowns, player_government

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

# Function to display the population information box
def display_population_info(game_display, population, population_caps_grid, x, y, tile_x, tile_y, terrain_grid):
    font = pygame.font.Font(None, 20)

    popcap = population_caps_grid[tile_y][tile_x]

    # Render tile coordinates text
    tile_text = "Tile: " + str(tile_x) + " , " + str(tile_y) + ', ' + str(popcap)
    tile_surface = font.render(tile_text, True, (255, 255, 255))
    # Calculate text rect for tile coordinates
    tile_rect = tile_surface.get_rect()
    tile_rect.topleft = (x + 15, y + 25)
    pygame.draw.rect(game_display, (0, 0, 0), tile_rect)        # Background color for tile

    # Render population text
    population_text = "Population: " + str(population[0])
    population_surface = font.render(population_text, True, (255, 255, 255))
    # Calculate text rect for population
    population_rect = population_surface.get_rect()
    population_rect.topleft = (x + 15, y + 25 + population_rect.height)
    pygame.draw.rect(game_display, (0, 0, 0), population_rect)  # Background color for population

    # Render hunter-gatherer text
    huntergatherer_text = "Hunter-gatherers: " + str(population[1])
    huntergatherer_surface = font.render(huntergatherer_text, True, (255, 255, 255))
    # Calculate text rect for hunter gatherers
    huntergatherer_rect = huntergatherer_surface.get_rect()
    huntergatherer_rect.topleft = (x + 15, y  + population_rect.height*2 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), huntergatherer_rect)        # Background color for tile

    # Render farmer text
    farmer_text = "Farmers: " + str(population[2])
    farmer_surface = font.render(farmer_text, True, (255, 255, 255))
    # Calculate text rect for farmers
    farmer_rect = farmer_surface.get_rect()
    farmer_rect.topleft = (x + 15, y  + population_rect.height*3 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), farmer_rect)        # Background color for farmers

    # Render merchant text
    merchant_text = "Merchants: " + str(population[3])
    merchant_surface = font.render(merchant_text, True, (255, 255, 255))
    # Calculate text rect for merchants
    merchant_rect = merchant_surface.get_rect()
    merchant_rect.topleft = (x + 15, y  + population_rect.height*4 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), merchant_rect)        # Background color for merchants

    # Render noble text
    noble_text = "Nobles: " + str(population[4])
    noble_surface = font.render(noble_text, True, (255, 255, 255))
    # Calculate text rect for nobles
    noble_rect = noble_surface.get_rect()
    noble_rect.topleft = (x + 15, y  + population_rect.height*5 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), noble_rect)        # Background color for nobles

    # Render proletarians text
    proletarians_text = "Proletarians: " + str(population[5])
    proletarians_surface = font.render(proletarians_text, True, (255, 255, 255))
    # Calculate text rect for proletarianss
    proletarians_rect = proletarians_surface.get_rect()
    proletarians_rect.topleft = (x + 15, y  + population_rect.height*6 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), proletarians_rect)        # Background color for proletarians

    # Render bourgeoisie text
    bourgeoisie_text = "Bourgeoisie: " + str(population[6])
    bourgeoisie_surface = font.render(bourgeoisie_text, True, (255, 255, 255))
    # Calculate text rect for bourgeoisies
    bourgeoisie_rect = bourgeoisie_surface.get_rect()
    bourgeoisie_rect.topleft = (x + 15, y  + population_rect.height*7 + 25)
    pygame.draw.rect(game_display, (0, 0, 0), bourgeoisie_rect)        # Background color for bourgeoisie

    # Blit population text onto game display
    game_display.blit(population_surface, population_rect)

    # Blit tile coordinates text onto game display
    game_display.blit(tile_surface, tile_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(huntergatherer_surface, huntergatherer_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(farmer_surface, farmer_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(merchant_surface, merchant_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(noble_surface, noble_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(proletarians_surface, proletarians_rect)

    # Blit hunter gatherer text onto game display
    game_display.blit(bourgeoisie_surface, bourgeoisie_rect)

def counters(terrain_grid, surface, turn_counter, stage, states):
        # Display turn counter
        font = pygame.font.Font(None, 17)
        turn_text = f"Turn: {turn_counter}"
        turn_surface = font.render(turn_text, True, (0, 0, 0))
        surface.blit(turn_surface, (UI_POSITION[0] + 10, UI_HEIGHT - 100))
        size_y, size_x = terrain_grid.shape

        for y in range(size_y):
            for x in range(size_x):
                if terrain_grid[y][x] == 6 and stage < 1:
                      stage += 1
                if terrain_grid[y][x] == 5 and stage < 2:
                      stage += 1
                for state in states:
                    towns_in_state = sum(1 for town in state['towns'])
                    if towns_in_state > 1 and stage < 3:
                        stage +=1

        if stage == 0:
            stage_name = 'Hunter-Gatherers'
        if stage == 1:
            stage_name = 'Farming Communities'
        if stage == 2:
            stage_name = 'Permanent Settlements'
        if stage == 3:
            stage_name = 'Early States'
        elif stage > 3:
            stage_name = 'Broken History'
        # Display stage
        stage_text = f"Stage: {stage_name}"
        stage_surface = font.render(stage_text, True, (0, 0, 0))
        surface.blit(stage_surface, (UI_POSITION[0] + 10, UI_HEIGHT - 80))


def player_classes_overlay(screen):
    # player_taxes = list(player_taxes)

    x_parameter = 0
    y_parameter = 100

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

    # Draw the title "Taxes"
    font = pygame.font.Font(None, 40)
    title_label = font.render("Classes", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x, overlay_y + 35))


def player_diplomacy_overlay(screen):
    # player_taxes = list(player_taxes)

    x_parameter = 0
    y_parameter = 100

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

    # Draw the title "Taxes"
    font = pygame.font.Font(None, 40)
    title_label = font.render("Diplomacy", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x, overlay_y + 35))


def player_government_overlay(screen, display_gov_dropdowns, player_government, tick_box_checked, political_rights, selection, powerbase):
    
    x_parameter = -450

    # Get the dimensions of the game display
    display_width, display_height = screen.get_size()

    # Define the dimensions of the overlay rectangle
    overlay_width = display_width - 200  # Reduce width by 200 pixels
    overlay_height = display_height - 30  # Reduce height by 30 pixels

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

    # Draw the title "Government"
    font = pygame.font.Font(None, 40)
    title_label = font.render("Government", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x, overlay_y + 35))

    # Draw the title "Head of State"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Head of State", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x - 280, overlay_y + 100))

    # Draw the title "Lower Governmnet"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Central Government", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x, overlay_y + 100))

        # Draw the title "Lower Governmnet"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Local Government", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x + 280, overlay_y + 100))

    ### BUTTON 1 ###

    x_parameter = -350

    hos_selec_drop = display_gov_dropdowns[0]

    # Define button dimensions and position
    hos_selection_width = 130
    hos_selection_height = 50
    hos_selection_x = overlay_x + (overlay_width - hos_selection_width) // 2 + x_parameter
    hos_selection_y = overlay_y + 130

    # Draw the button
    pygame.draw.rect(screen, grey, (hos_selection_x, hos_selection_y, hos_selection_width, hos_selection_height))
    pygame.draw.rect(screen, black, (hos_selection_x, hos_selection_y, hos_selection_width, hos_selection_height), 3)  # Add black outline
    font = pygame.font.Font(None, 25)
    hos_selection_label = str(player_government["HOS selection"])
    button_hos_selection_label = font.render(hos_selection_label, True, (0, 0, 0))
    button_hos_selection_label_x = hos_selection_x + (hos_selection_width - button_hos_selection_label.get_width()) // 2
    button_hos_selection_label_y = hos_selection_y + (hos_selection_height - button_hos_selection_label.get_height()) // 2
    screen.blit(button_hos_selection_label, (button_hos_selection_label_x, button_hos_selection_label_y))

    ### BUTTON 2 ###
            
    x_parameter = -210
    hos_powerbase_drop = display_gov_dropdowns[1]

    # Define button dimensions and position
    hos_powerbase_width = 130
    hos_powerbase_height = 50
    hos_powerbase_x = overlay_x + (overlay_width - hos_powerbase_width) // 2 + x_parameter
    hos_powerbase_y = overlay_y + 130

    # Draw the button
    pygame.draw.rect(screen, grey, (hos_powerbase_x, hos_powerbase_y, hos_powerbase_width, hos_powerbase_height))
    pygame.draw.rect(screen, black, (hos_powerbase_x, hos_powerbase_y, hos_powerbase_width, hos_powerbase_height), 3)  # Add black outline
    font = pygame.font.Font(None, 25)
    hos_powerbase_label = str(player_government["HOS powerbase"])
    hos_powerbase_button_label = font.render(hos_powerbase_label, True, (0, 0, 0))
    hos_powerbase_button_label_x = hos_powerbase_x + (hos_powerbase_width - hos_powerbase_button_label.get_width()) // 2
    hos_powerbase_button_label_y = hos_powerbase_y + (hos_powerbase_height - hos_powerbase_button_label.get_height()) // 2
    screen.blit(hos_powerbase_button_label, (hos_powerbase_button_label_x, hos_powerbase_button_label_y))

    ### BUTTON 3 ###

    x_parameter = -70
    cg_selec_drop = display_gov_dropdowns[2]

    # Define button dimensions and position
    cg_selection_width = 130
    cg_selection_height = 50
    cg_selection_x = overlay_x + (overlay_width - cg_selection_width) // 2 + x_parameter
    cg_selection_y = overlay_y + 130

    # Draw the button
    pygame.draw.rect(screen, grey, (cg_selection_x, cg_selection_y, cg_selection_width, cg_selection_height))
    pygame.draw.rect(screen, black, (cg_selection_x, cg_selection_y, cg_selection_width, cg_selection_height), 3)  # Add black outline
    font = pygame.font.Font(None, 25)
    cg_selection_label = str(player_government["CG selection"])
    button_cg_selection_label = font.render(cg_selection_label, True, (0, 0, 0))
    button_cg_selection_label_x = cg_selection_x + (cg_selection_width - button_cg_selection_label.get_width()) // 2
    button_cg_selection_label_y = cg_selection_y + (cg_selection_height - button_cg_selection_label.get_height()) // 2
    screen.blit(button_cg_selection_label, (button_cg_selection_label_x, button_cg_selection_label_y))

    ### BUTTON 4 ###

    x_parameter = 70
    cg_powerbase_drop = display_gov_dropdowns[3]

    # Define button dimensions and position
    cg_powerbase_width = 130
    cg_powerbase_height = 50
    cg_powerbase_x = overlay_x + (overlay_width - cg_powerbase_width) // 2 + x_parameter
    cg_powerbase_y = overlay_y + 130

    # Draw the button
    pygame.draw.rect(screen, grey, (cg_powerbase_x, cg_powerbase_y, cg_powerbase_width, cg_powerbase_height))
    pygame.draw.rect(screen, black, (cg_powerbase_x, cg_powerbase_y, cg_powerbase_width, cg_powerbase_height), 3)  # Add black outline
    font = pygame.font.Font(None, 25)
    cg_powerbase_label = str(player_government["CG powerbase"])
    cg_powerbase_button_label = font.render(cg_powerbase_label, True, (0, 0, 0))
    cg_powerbase_button_label_x = cg_powerbase_x + (cg_powerbase_width - cg_powerbase_button_label.get_width()) // 2
    cg_powerbase_button_label_y = cg_powerbase_y + (cg_powerbase_height - cg_powerbase_button_label.get_height()) // 2
    screen.blit(cg_powerbase_button_label, (cg_powerbase_button_label_x, cg_powerbase_button_label_y))


    ### BUTTON 5 ###

    x_parameter = 210
    lg_selec_drop = display_gov_dropdowns[4]

    # Define button dimensions and position
    lg_selection_width = 130
    lg_selection_height = 50
    lg_selection_x = overlay_x + (overlay_width - lg_selection_width) // 2 + x_parameter
    lg_selection_y = overlay_y + 130

    # Draw the button
    pygame.draw.rect(screen, grey, (lg_selection_x, lg_selection_y, lg_selection_width, lg_selection_height))
    pygame.draw.rect(screen, black, (lg_selection_x, lg_selection_y, lg_selection_width, lg_selection_height), 3)  # Add black outline
    font = pygame.font.Font(None, 25)
    lg_selection_label = str(player_government["LG selection"])
    button_lg_selection_label = font.render(lg_selection_label, True, (0, 0, 0))
    button_lg_selection_label_x = lg_selection_x + (lg_selection_width - button_lg_selection_label.get_width()) // 2
    button_lg_selection_label_y = lg_selection_y + (lg_selection_height - button_lg_selection_label.get_height()) // 2
    screen.blit(button_lg_selection_label, (button_lg_selection_label_x, button_lg_selection_label_y))

    ### BUTTON 6 ###

    x_parameter = 350

    lg_powerbase_drop = display_gov_dropdowns[5]

    # Define button dimensions and position
    lg_powerbase_width = 130
    lg_powerbase_height = 50
    lg_powerbase_x = overlay_x + (overlay_width - lg_powerbase_width) // 2 + x_parameter
    lg_powerbase_y = overlay_y + 130

    # Draw the button
    pygame.draw.rect(screen, grey, (lg_powerbase_x, lg_powerbase_y, lg_powerbase_width, lg_powerbase_height))
    pygame.draw.rect(screen, black, (lg_powerbase_x, lg_powerbase_y, lg_powerbase_width, lg_powerbase_height), 3)  # Add black outline
    font = pygame.font.Font(None, 25)
    lg_powerbase_label = str(player_government["LG powerbase"])
    lg_powerbase_button_label = font.render(lg_powerbase_label, True, (0, 0, 0))
    lg_powerbase_button_label_x = lg_powerbase_x + (lg_powerbase_width - lg_powerbase_button_label.get_width()) // 2
    lg_powerbase_button_label_y = lg_powerbase_y + (lg_powerbase_height - lg_powerbase_button_label.get_height()) // 2
    screen.blit(lg_powerbase_button_label, (lg_powerbase_button_label_x, lg_powerbase_button_label_y))

    ### DROPDOWNS ###

    # Check for mouse click on the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if hos_selection_x <= mouse_x <= hos_selection_x + hos_selection_width and hos_selection_y <= mouse_y <= hos_selection_y + hos_selection_height and mouse_clicked:
        # Button is clicked, toggle the dropdown menu state
        hos_selec_drop += 1

    if hos_selec_drop > 0:
        # Display the dropdown menu
        dropdown_menu_options_hos_selection = ["Consent", "Force", "Inheritance", "None"]
        dropdown_menu_font = pygame.font.Font(None, 25)
        dropdown_menu_width = 130
        dropdown_menu_height = 30 * len(dropdown_menu_options_hos_selection)
        dropdown_menu_x = hos_selection_x
        dropdown_menu_y = hos_selection_y + hos_selection_height

        # Draw the dropdown menu options
        for i, option in enumerate(dropdown_menu_options_hos_selection):
            # Draw black outline for each option
            pygame.draw.rect(screen, black, (dropdown_menu_x, dropdown_menu_y + i * 30, dropdown_menu_width, 30), 3)
            option_hos_selection_label = dropdown_menu_font.render(option, True, (0, 0, 0))
            option_hos_selection_label_x = dropdown_menu_x + (dropdown_menu_width - option_hos_selection_label.get_width()) // 2
            option_hos_selection_label_y = dropdown_menu_y + i * 30 + (30 - option_hos_selection_label.get_height()) // 2
            screen.blit(option_hos_selection_label, (option_hos_selection_label_x, option_hos_selection_label_y))

    # Handle option selection
    if hos_selec_drop > 0 and mouse_clicked:
        selected_option_index = (mouse_y - dropdown_menu_y) // 30
        if 0 <= selected_option_index < len(dropdown_menu_options_hos_selection):
            selected_option = dropdown_menu_options_hos_selection[selected_option_index]
            player_government["HOS selection"] = selected_option
            hos_selec_drop -= 1
            
            selection[0] = selected_option
    display_gov_dropdowns[0] = hos_selec_drop

    # Check for mouse click on the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if hos_powerbase_x <= mouse_x <= hos_powerbase_x + hos_powerbase_width and hos_powerbase_y <= mouse_y <= hos_powerbase_y + hos_powerbase_height and mouse_clicked:
        # Button is clicked, toggle the dropdown menu state
        hos_powerbase_drop += 1

    if hos_powerbase_drop > 0:
        # Display the dropdown menu
        dropdown_menu_options_hos_powerbase = ["Peasants", "Merchants", "Nobles", "Military", "Priests", "Bourgeoisie", "Proletariat", "Intelligentsia"]
        dropdown_menu_font = pygame.font.Font(None, 25)
        dropdown_menu_width = 130
        dropdown_menu_height = 30 * len(dropdown_menu_options_hos_powerbase)
        dropdown_menu_x = hos_powerbase_x
        dropdown_menu_y = hos_powerbase_y + hos_powerbase_height

        # Draw the dropdown menu options
        for i, option in enumerate(dropdown_menu_options_hos_powerbase):
            # Draw black outline for each option
            pygame.draw.rect(screen, black, (dropdown_menu_x, dropdown_menu_y + i * 30, dropdown_menu_width, 30), 3)
            option_label = dropdown_menu_font.render(option, True, (0, 0, 0))
            option_label_x = dropdown_menu_x + (dropdown_menu_width - option_label.get_width()) // 2
            option_label_y = dropdown_menu_y + i * 30 + (30 - option_label.get_height()) // 2
            screen.blit(option_label, (option_label_x, option_label_y))

    # Handle option selection
    if hos_powerbase_drop > 0 and mouse_clicked:
        selected_option_index = (mouse_y - dropdown_menu_y) // 30
        if 0 <= selected_option_index < len(dropdown_menu_options_hos_powerbase):
            selected_option = dropdown_menu_options_hos_powerbase[selected_option_index]
            player_government["HOS powerbase"] = selected_option
            hos_powerbase_drop -= 1

            powerbase[0] = selected_option
    display_gov_dropdowns[1] = hos_powerbase_drop

   # Check for mouse click on the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if cg_selection_x <= mouse_x <= cg_selection_x + cg_selection_width and cg_selection_y <= mouse_y <= cg_selection_y + cg_selection_height and mouse_clicked:
        # Button is clicked, toggle the dropdown menu state
        cg_selec_drop += 1

    if cg_selec_drop > 0:
        # Display the dropdown menu
        dropdown_menu_options_cg_selection = ["Consent", "Force", "Inheritance", "Appointment", "None"]
        dropdown_menu_font = pygame.font.Font(None, 25)
        dropdown_menu_width = 130
        dropdown_menu_height = 30 * len(dropdown_menu_options_cg_selection)
        dropdown_menu_x = cg_selection_x
        dropdown_menu_y = cg_selection_y + cg_selection_height

        # Draw the dropdown menu options
        for i, option in enumerate(dropdown_menu_options_cg_selection):
            # Draw black outline for each option
            pygame.draw.rect(screen, black, (dropdown_menu_x, dropdown_menu_y + i * 30, dropdown_menu_width, 30), 3)
            option_cg_selection_label = dropdown_menu_font.render(option, True, (0, 0, 0))
            option_cg_selection_label_x = dropdown_menu_x + (dropdown_menu_width - option_cg_selection_label.get_width()) // 2
            option_cg_selection_label_y = dropdown_menu_y + i * 30 + (30 - option_cg_selection_label.get_height()) // 2
            screen.blit(option_cg_selection_label, (option_cg_selection_label_x, option_cg_selection_label_y))

    # Handle option selection
    if cg_selec_drop > 0 and mouse_clicked:
        selected_option_index = (mouse_y - dropdown_menu_y) // 30
        if 0 <= selected_option_index < len(dropdown_menu_options_cg_selection):
            selected_option = dropdown_menu_options_cg_selection[selected_option_index]
            player_government["CG selection"] = selected_option
            cg_selec_drop -= 1
            
            selection[1] = selected_option
    display_gov_dropdowns[2] = cg_selec_drop

    # Check for mouse click on the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if cg_powerbase_x <= mouse_x <= cg_powerbase_x + cg_powerbase_width and cg_powerbase_y <= mouse_y <= cg_powerbase_y + cg_powerbase_height and mouse_clicked:
        # Button is clicked, toggle the dropdown menu state
        cg_powerbase_drop += 1

    if cg_powerbase_drop > 0:
        # Display the dropdown menu
        dropdown_menu_options_cg_powerbase = ["Peasants", "Merchants", "Nobles", "Military", "Priests", "Bourgeoisie", "Proletariat", "Intelligentsia"]
        dropdown_menu_font = pygame.font.Font(None, 25)
        dropdown_menu_width = 130
        dropdown_menu_height = 30 * len(dropdown_menu_options_cg_powerbase)
        dropdown_menu_x = cg_powerbase_x
        dropdown_menu_y = cg_powerbase_y + cg_powerbase_height

        # Draw the dropdown menu options
        for i, option in enumerate(dropdown_menu_options_cg_powerbase):
            # Draw black outline for each option
            pygame.draw.rect(screen, black, (dropdown_menu_x, dropdown_menu_y + i * 30, dropdown_menu_width, 30), 3)
            option_label = dropdown_menu_font.render(option, True, (0, 0, 0))
            option_label_x = dropdown_menu_x + (dropdown_menu_width - option_label.get_width()) // 2
            option_label_y = dropdown_menu_y + i * 30 + (30 - option_label.get_height()) // 2
            screen.blit(option_label, (option_label_x, option_label_y))

    # Handle option selection
    if cg_powerbase_drop > 0 and mouse_clicked:
        selected_option_index = (mouse_y - dropdown_menu_y) // 30
        if 0 <= selected_option_index < len(dropdown_menu_options_cg_powerbase):
            selected_option = dropdown_menu_options_cg_powerbase[selected_option_index]
            player_government["CG powerbase"] = selected_option
            cg_powerbase_drop -= 1

            powerbase[1] = selected_option
    display_gov_dropdowns[3] = cg_powerbase_drop

    # Check for mouse click on the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if lg_selection_x <= mouse_x <= lg_selection_x + lg_selection_width and lg_selection_y <= mouse_y <= lg_selection_y + lg_selection_height and mouse_clicked:
        # Button is clicked, toggle the dropdown menu state
        lg_selec_drop += 1

    if lg_selec_drop > 0:
        # Display the dropdown menu
        dropdown_menu_options_lg_selection = ["Consent", "Force", "Inheritance", "Appointment", "None"]
        dropdown_menu_font = pygame.font.Font(None, 25)
        dropdown_menu_width = 130
        dropdown_menu_height = 30 * len(dropdown_menu_options_lg_selection)
        dropdown_menu_x = lg_selection_x
        dropdown_menu_y = lg_selection_y + lg_selection_height

        # Draw the dropdown menu options
        for i, option in enumerate(dropdown_menu_options_lg_selection):
            # Draw black outline for each option
            pygame.draw.rect(screen, black, (dropdown_menu_x, dropdown_menu_y + i * 30, dropdown_menu_width, 30), 3)
            option_lg_selection_label = dropdown_menu_font.render(option, True, (0, 0, 0))
            option_lg_selection_label_x = dropdown_menu_x + (dropdown_menu_width - option_lg_selection_label.get_width()) // 2
            option_lg_selection_label_y = dropdown_menu_y + i * 30 + (30 - option_lg_selection_label.get_height()) // 2
            screen.blit(option_lg_selection_label, (option_lg_selection_label_x, option_lg_selection_label_y))

    # Handle option selection
    if lg_selec_drop > 0 and mouse_clicked:
        selected_option_index = (mouse_y - dropdown_menu_y) // 30
        if 0 <= selected_option_index < len(dropdown_menu_options_lg_selection):
            selected_option = dropdown_menu_options_lg_selection[selected_option_index]
            player_government["LG selection"] = selected_option
            lg_selec_drop -= 1
            
            selection[2] = selected_option
    display_gov_dropdowns[4] = lg_selec_drop

    # Check for mouse click on the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if lg_powerbase_x <= mouse_x <= lg_powerbase_x + lg_powerbase_width and lg_powerbase_y <= mouse_y <= lg_powerbase_y + lg_powerbase_height and mouse_clicked:
        # Button is clicked, toggle the dropdown menu state
        lg_powerbase_drop += 1

    if lg_powerbase_drop > 0:
        # Display the dropdown menu
        dropdown_menu_options_lg_powerbase = ["Peasants", "Merchants", "Nobles", "Military", "Priests", "Bourgeoisie", "Proletariat", "Intelligentsia"]
        dropdown_menu_font = pygame.font.Font(None, 25)
        dropdown_menu_width = 130
        dropdown_menu_height = 30 * len(dropdown_menu_options_lg_powerbase)
        dropdown_menu_x = lg_powerbase_x
        dropdown_menu_y = lg_powerbase_y + lg_powerbase_height

        # Draw the dropdown menu options
        for i, option in enumerate(dropdown_menu_options_lg_powerbase):
            # Draw black outline for each option
            pygame.draw.rect(screen, black, (dropdown_menu_x, dropdown_menu_y + i * 30, dropdown_menu_width, 30), 3)
            option_label = dropdown_menu_font.render(option, True, (0, 0, 0))
            option_label_x = dropdown_menu_x + (dropdown_menu_width - option_label.get_width()) // 2
            option_label_y = dropdown_menu_y + i * 30 + (30 - option_label.get_height()) // 2
            screen.blit(option_label, (option_label_x, option_label_y))

    # Handle option selection
    if lg_powerbase_drop > 0 and mouse_clicked:
        selected_option_index = (mouse_y - dropdown_menu_y) // 30
        if 0 <= selected_option_index < len(dropdown_menu_options_lg_powerbase):
            selected_option = dropdown_menu_options_lg_powerbase[selected_option_index]
            player_government["LG powerbase"] = selected_option
            lg_powerbase_drop -= 1

            powerbase[2] = selected_option
    display_gov_dropdowns[5] = lg_powerbase_drop

    

    # print(powerbase)
    # print(selection)


    ### Political Rights, Taxation ###

    # Head of State
        
    x_parameter = -285
    y_parameter = 230

    tax_box = tick_box_checked["Taxation"]

    # Draw the title "Tick Box"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Taxation", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x - 500, overlay_y + y_parameter))



    # Define tick box dimensions and position
    tick_box_tax_hos_size = 30
    tick_box_tax_hos_x = overlay_x + x_parameter + (overlay_width - tick_box_tax_hos_size) // 2
    tick_box_tax_hos_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_tax_hos_x, tick_box_tax_hos_y, tick_box_tax_hos_size, tick_box_tax_hos_size), 3)

    # Draw the tick mark if the tick box is checked
    if tax_box == '1':
        pygame.draw.line(screen, black, (tick_box_tax_hos_x, tick_box_tax_hos_y), (tick_box_tax_hos_x + tick_box_tax_hos_size, tick_box_tax_hos_y + tick_box_tax_hos_size), 3)
        pygame.draw.line(screen, black, (tick_box_tax_hos_x + tick_box_tax_hos_size, tick_box_tax_hos_y), (tick_box_tax_hos_x, tick_box_tax_hos_y + tick_box_tax_hos_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_tax_hos_x <= mouse_x <= tick_box_tax_hos_x + tick_box_tax_hos_size and tick_box_tax_hos_y <= mouse_y <= tick_box_tax_hos_y + tick_box_tax_hos_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if tax_box != '1':
            political_rights["Taxation"] = powerbase[0]
            tax_box = '1'

        elif tax_box == '1':
            political_rights["Taxation"] = 'None'
            tax_box = '0'

        
    # Central Government
            
    x_parameter = 0

    # Define tick box dimensions and position
    tick_box_tax_cg_size = 30
    tick_box_tax_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_tax_cg_size) // 2
    tick_box_tax_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_tax_cg_x, tick_box_tax_cg_y, tick_box_tax_cg_size, tick_box_tax_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if tax_box == '2':
        pygame.draw.line(screen, black, (tick_box_tax_cg_x, tick_box_tax_cg_y), (tick_box_tax_cg_x + tick_box_tax_cg_size, tick_box_tax_cg_y + tick_box_tax_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_tax_cg_x + tick_box_tax_cg_size, tick_box_tax_cg_y), (tick_box_tax_cg_x, tick_box_tax_cg_y + tick_box_tax_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_tax_cg_x <= mouse_x <= tick_box_tax_cg_x + tick_box_tax_cg_size and tick_box_tax_cg_y <= mouse_y <= tick_box_tax_cg_y + tick_box_tax_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if tax_box != '2':
            political_rights["Taxation"] = powerbase[1]
            tax_box = '2'

        elif tax_box == '2':
            political_rights["Taxation"] = 'None'
            tax_box = '0'

    # Local Government
            
    x_parameter = 285

    # Define tick box dimensions and position
    tick_box_tax_cg_size = 30
    tick_box_tax_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_tax_cg_size) // 2
    tick_box_tax_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_tax_cg_x, tick_box_tax_cg_y, tick_box_tax_cg_size, tick_box_tax_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if tax_box == '3':
        pygame.draw.line(screen, black, (tick_box_tax_cg_x, tick_box_tax_cg_y), (tick_box_tax_cg_x + tick_box_tax_cg_size, tick_box_tax_cg_y + tick_box_tax_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_tax_cg_x + tick_box_tax_cg_size, tick_box_tax_cg_y), (tick_box_tax_cg_x, tick_box_tax_cg_y + tick_box_tax_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_tax_cg_x <= mouse_x <= tick_box_tax_cg_x + tick_box_tax_cg_size and tick_box_tax_cg_y <= mouse_y <= tick_box_tax_cg_y + tick_box_tax_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if tax_box != '3':
            political_rights["Taxation"] = powerbase[2]
            tax_box = '3'

        elif tax_box == '3':
            political_rights["Taxation"] = 'None'
            tax_box = '0'

    tick_box_checked["Taxation"] = tax_box



    ### Political Rights, Military recruitment ###

    # Head of State
        
    x_parameter = -285
    y_parameter = 265

    recr_box = tick_box_checked["Military recruitment"]

    # Draw the title "Tick Box"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Military recruitment", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x - 500, overlay_y + y_parameter))



    # Define tick box dimensions and position
    tick_box_recr_hos_size = 30
    tick_box_recr_hos_x = overlay_x + x_parameter + (overlay_width - tick_box_recr_hos_size) // 2
    tick_box_recr_hos_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_recr_hos_x, tick_box_recr_hos_y, tick_box_recr_hos_size, tick_box_recr_hos_size), 3)

    # Draw the tick mark if the tick box is checked
    if recr_box == '1':
        pygame.draw.line(screen, black, (tick_box_recr_hos_x, tick_box_recr_hos_y), (tick_box_recr_hos_x + tick_box_recr_hos_size, tick_box_recr_hos_y + tick_box_recr_hos_size), 3)
        pygame.draw.line(screen, black, (tick_box_recr_hos_x + tick_box_recr_hos_size, tick_box_recr_hos_y), (tick_box_recr_hos_x, tick_box_recr_hos_y + tick_box_recr_hos_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_recr_hos_x <= mouse_x <= tick_box_recr_hos_x + tick_box_recr_hos_size and tick_box_recr_hos_y <= mouse_y <= tick_box_recr_hos_y + tick_box_recr_hos_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if recr_box != '1':
            political_rights["Military recruitment"] = powerbase[0]
            recr_box = '1'

        elif recr_box == '1':
            political_rights["Military recruitment"] = 'None'
            recr_box = '0'

        
    # Central Government
            
    x_parameter = 0

    # Define tick box dimensions and position
    tick_box_recr_cg_size = 30
    tick_box_recr_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_recr_cg_size) // 2
    tick_box_recr_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_recr_cg_x, tick_box_recr_cg_y, tick_box_recr_cg_size, tick_box_recr_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if recr_box == '2':
        pygame.draw.line(screen, black, (tick_box_recr_cg_x, tick_box_recr_cg_y), (tick_box_recr_cg_x + tick_box_recr_cg_size, tick_box_recr_cg_y + tick_box_recr_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_recr_cg_x + tick_box_recr_cg_size, tick_box_recr_cg_y), (tick_box_recr_cg_x, tick_box_recr_cg_y + tick_box_recr_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_recr_cg_x <= mouse_x <= tick_box_recr_cg_x + tick_box_recr_cg_size and tick_box_recr_cg_y <= mouse_y <= tick_box_recr_cg_y + tick_box_recr_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if recr_box != '2':
            political_rights["Military recruitment"] = powerbase[1]
            recr_box = '2'

        elif recr_box == '2':
            political_rights["Military recruitment"] = 'None'
            recr_box = '0'

    # Local Government
            
    x_parameter = 285

    # Define tick box dimensions and position
    tick_box_recr_cg_size = 30
    tick_box_recr_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_recr_cg_size) // 2
    tick_box_recr_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_recr_cg_x, tick_box_recr_cg_y, tick_box_recr_cg_size, tick_box_recr_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if recr_box == '3':
        pygame.draw.line(screen, black, (tick_box_recr_cg_x, tick_box_recr_cg_y), (tick_box_recr_cg_x + tick_box_recr_cg_size, tick_box_recr_cg_y + tick_box_recr_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_recr_cg_x + tick_box_recr_cg_size, tick_box_recr_cg_y), (tick_box_recr_cg_x, tick_box_recr_cg_y + tick_box_recr_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_recr_cg_x <= mouse_x <= tick_box_recr_cg_x + tick_box_recr_cg_size and tick_box_recr_cg_y <= mouse_y <= tick_box_recr_cg_y + tick_box_recr_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if recr_box != '3':
            political_rights["Military recruitment"] = powerbase[2]
            recr_box = '3'

        elif recr_box == '3':
            political_rights["Military recruitment"] = 'None'
            recr_box = '0'

    tick_box_checked["Military recruitment"] = recr_box



    ### Political Rights, Control of Commerce ###

    # Head of State
        
    x_parameter = -285
    y_parameter = 300

    comm_box = tick_box_checked["Control of commerce"]

    # Draw the title "Tick Box"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Control of Commerce", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x - 500, overlay_y + y_parameter))

    # Define tick box dimensions and position
    tick_box_comm_hos_size = 30
    tick_box_comm_hos_x = overlay_x + x_parameter + (overlay_width - tick_box_comm_hos_size) // 2
    tick_box_comm_hos_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_comm_hos_x, tick_box_comm_hos_y, tick_box_comm_hos_size, tick_box_comm_hos_size), 3)

    # Draw the tick mark if the tick box is checked
    if comm_box == '1':
        pygame.draw.line(screen, black, (tick_box_comm_hos_x, tick_box_comm_hos_y), (tick_box_comm_hos_x + tick_box_comm_hos_size, tick_box_comm_hos_y + tick_box_comm_hos_size), 3)
        pygame.draw.line(screen, black, (tick_box_comm_hos_x + tick_box_comm_hos_size, tick_box_comm_hos_y), (tick_box_comm_hos_x, tick_box_comm_hos_y + tick_box_comm_hos_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_comm_hos_x <= mouse_x <= tick_box_comm_hos_x + tick_box_comm_hos_size and tick_box_comm_hos_y <= mouse_y <= tick_box_comm_hos_y + tick_box_comm_hos_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if comm_box != '1':
            political_rights["Control of commerce"] = powerbase[0]
            comm_box = '1'

        elif comm_box == '1':
            political_rights["Control of commerce"] = 'None'
            comm_box = '0'

        
    # Central Government
            
    x_parameter = 0

    # Define tick box dimensions and position
    tick_box_comm_cg_size = 30
    tick_box_comm_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_comm_cg_size) // 2
    tick_box_comm_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_comm_cg_x, tick_box_comm_cg_y, tick_box_comm_cg_size, tick_box_comm_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if comm_box == '2':
        pygame.draw.line(screen, black, (tick_box_comm_cg_x, tick_box_comm_cg_y), (tick_box_comm_cg_x + tick_box_comm_cg_size, tick_box_comm_cg_y + tick_box_comm_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_comm_cg_x + tick_box_comm_cg_size, tick_box_comm_cg_y), (tick_box_comm_cg_x, tick_box_comm_cg_y + tick_box_comm_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_comm_cg_x <= mouse_x <= tick_box_comm_cg_x + tick_box_comm_cg_size and tick_box_comm_cg_y <= mouse_y <= tick_box_comm_cg_y + tick_box_comm_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if comm_box != '2':
            political_rights["Control of commerce"] = powerbase[1]
            comm_box = '2'

        elif comm_box == '2':
            political_rights["Control of commerce"] = 'None'
            comm_box = '0'

    # Local Government
            
    x_parameter = 285

    # Define tick box dimensions and position
    tick_box_comm_cg_size = 30
    tick_box_comm_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_comm_cg_size) // 2
    tick_box_comm_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_comm_cg_x, tick_box_comm_cg_y, tick_box_comm_cg_size, tick_box_comm_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if comm_box == '3':
        pygame.draw.line(screen, black, (tick_box_comm_cg_x, tick_box_comm_cg_y), (tick_box_comm_cg_x + tick_box_comm_cg_size, tick_box_comm_cg_y + tick_box_comm_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_comm_cg_x + tick_box_comm_cg_size, tick_box_comm_cg_y), (tick_box_comm_cg_x, tick_box_comm_cg_y + tick_box_comm_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_comm_cg_x <= mouse_x <= tick_box_comm_cg_x + tick_box_comm_cg_size and tick_box_comm_cg_y <= mouse_y <= tick_box_comm_cg_y + tick_box_comm_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if comm_box != '3':
            political_rights["Control of commerce"] = powerbase[2]
            comm_box = '3'

        elif comm_box == '3':
            political_rights["Control of commerce"] = 'None'
            comm_box = '0'

    tick_box_checked["Control of commerce"] = comm_box




    ### Political Rights, Infrastructure ###

    # Head of State
        
    x_parameter = -285
    y_parameter = 335

    infr_box = tick_box_checked["Infrastructure"]

    # Draw the title "Tick Box"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Infrastructure", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x - 500, overlay_y + y_parameter))

    # Define tick box dimensions and position
    tick_box_infr_hos_size = 30
    tick_box_infr_hos_x = overlay_x + x_parameter + (overlay_width - tick_box_infr_hos_size) // 2
    tick_box_infr_hos_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_infr_hos_x, tick_box_infr_hos_y, tick_box_infr_hos_size, tick_box_infr_hos_size), 3)

    # Draw the tick mark if the tick box is checked
    if infr_box == '1':
        pygame.draw.line(screen, black, (tick_box_infr_hos_x, tick_box_infr_hos_y), (tick_box_infr_hos_x + tick_box_infr_hos_size, tick_box_infr_hos_y + tick_box_infr_hos_size), 3)
        pygame.draw.line(screen, black, (tick_box_infr_hos_x + tick_box_infr_hos_size, tick_box_infr_hos_y), (tick_box_infr_hos_x, tick_box_infr_hos_y + tick_box_infr_hos_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_infr_hos_x <= mouse_x <= tick_box_infr_hos_x + tick_box_infr_hos_size and tick_box_infr_hos_y <= mouse_y <= tick_box_infr_hos_y + tick_box_infr_hos_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if infr_box != '1':
            political_rights["Infrastructure"] = powerbase[0]
            infr_box = '1'

        elif infr_box == '1':
            political_rights["Infrastructure"] = 'None'
            infr_box = '0'

        
    # Central Government
            
    x_parameter = 0

    # Define tick box dimensions and position
    tick_box_infr_cg_size = 30
    tick_box_infr_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_infr_cg_size) // 2
    tick_box_infr_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_infr_cg_x, tick_box_infr_cg_y, tick_box_infr_cg_size, tick_box_infr_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if infr_box == '2':
        pygame.draw.line(screen, black, (tick_box_infr_cg_x, tick_box_infr_cg_y), (tick_box_infr_cg_x + tick_box_infr_cg_size, tick_box_infr_cg_y + tick_box_infr_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_infr_cg_x + tick_box_infr_cg_size, tick_box_infr_cg_y), (tick_box_infr_cg_x, tick_box_infr_cg_y + tick_box_infr_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_infr_cg_x <= mouse_x <= tick_box_infr_cg_x + tick_box_infr_cg_size and tick_box_infr_cg_y <= mouse_y <= tick_box_infr_cg_y + tick_box_infr_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if infr_box != '2':
            political_rights["Infrastructure"] = powerbase[1]
            infr_box = '2'

        elif infr_box == '2':
            political_rights["Infrastructure"] = 'None'
            infr_box = '0'

    # Local Government
            
    x_parameter = 285

    # Define tick box dimensions and position
    tick_box_infr_cg_size = 30
    tick_box_infr_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_infr_cg_size) // 2
    tick_box_infr_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_infr_cg_x, tick_box_infr_cg_y, tick_box_infr_cg_size, tick_box_infr_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if infr_box == '3':
        pygame.draw.line(screen, black, (tick_box_infr_cg_x, tick_box_infr_cg_y), (tick_box_infr_cg_x + tick_box_infr_cg_size, tick_box_infr_cg_y + tick_box_infr_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_infr_cg_x + tick_box_infr_cg_size, tick_box_infr_cg_y), (tick_box_infr_cg_x, tick_box_infr_cg_y + tick_box_infr_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_infr_cg_x <= mouse_x <= tick_box_infr_cg_x + tick_box_infr_cg_size and tick_box_infr_cg_y <= mouse_y <= tick_box_infr_cg_y + tick_box_infr_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if infr_box != '3':
            political_rights["Infrastructure"] = powerbase[2]
            infr_box = '3'

        elif infr_box == '3':
            political_rights["Infrastructure"] = 'None'
            infr_box = '0'

    tick_box_checked["Infrastructure"] = infr_box




    ### Political Rights, Subsidies ###

    # Head of State
        
    x_parameter = -285
    y_parameter = 370

    subs_box = tick_box_checked["Subsidies"]

    # Draw the title "Tick Box"
    font = pygame.font.Font(None, 30)
    title_label = font.render("Subsidies", True, (0, 0, 0))
    title_x = overlay_x + (overlay_width - title_label.get_width()) // 2
    screen.blit(title_label, (title_x - 500, overlay_y + y_parameter))

    # Define tick box dimensions and position
    tick_box_subs_hos_size = 30
    tick_box_subs_hos_x = overlay_x + x_parameter + (overlay_width - tick_box_subs_hos_size) // 2
    tick_box_subs_hos_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_subs_hos_x, tick_box_subs_hos_y, tick_box_subs_hos_size, tick_box_subs_hos_size), 3)

    # Draw the tick mark if the tick box is checked
    if subs_box == '1':
        pygame.draw.line(screen, black, (tick_box_subs_hos_x, tick_box_subs_hos_y), (tick_box_subs_hos_x + tick_box_subs_hos_size, tick_box_subs_hos_y + tick_box_subs_hos_size), 3)
        pygame.draw.line(screen, black, (tick_box_subs_hos_x + tick_box_subs_hos_size, tick_box_subs_hos_y), (tick_box_subs_hos_x, tick_box_subs_hos_y + tick_box_subs_hos_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_subs_hos_x <= mouse_x <= tick_box_subs_hos_x + tick_box_subs_hos_size and tick_box_subs_hos_y <= mouse_y <= tick_box_subs_hos_y + tick_box_subs_hos_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if subs_box != '1':
            political_rights["Subsidies"] = powerbase[0]
            subs_box = '1'

        elif subs_box == '1':
            political_rights["Subsidies"] = 'None'
            subs_box = '0'

        
    # Central Government
            
    x_parameter = 0

    # Define tick box dimensions and position
    tick_box_subs_cg_size = 30
    tick_box_subs_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_subs_cg_size) // 2
    tick_box_subs_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_subs_cg_x, tick_box_subs_cg_y, tick_box_subs_cg_size, tick_box_subs_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if subs_box == '2':
        pygame.draw.line(screen, black, (tick_box_subs_cg_x, tick_box_subs_cg_y), (tick_box_subs_cg_x + tick_box_subs_cg_size, tick_box_subs_cg_y + tick_box_subs_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_subs_cg_x + tick_box_subs_cg_size, tick_box_subs_cg_y), (tick_box_subs_cg_x, tick_box_subs_cg_y + tick_box_subs_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_subs_cg_x <= mouse_x <= tick_box_subs_cg_x + tick_box_subs_cg_size and tick_box_subs_cg_y <= mouse_y <= tick_box_subs_cg_y + tick_box_subs_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if subs_box != '2':
            political_rights["Subsidies"] = powerbase[1]
            subs_box = '2'

        elif subs_box == '2':
            political_rights["Subsidies"] = 'None'
            subs_box = '0'

    # Local Government
            
    x_parameter = 285

    # Define tick box dimensions and position
    tick_box_subs_cg_size = 30
    tick_box_subs_cg_x = overlay_x + x_parameter + (overlay_width - tick_box_subs_cg_size) // 2
    tick_box_subs_cg_y = overlay_y + y_parameter - 10

    # Draw the tick box outline
    pygame.draw.rect(screen, black, (tick_box_subs_cg_x, tick_box_subs_cg_y, tick_box_subs_cg_size, tick_box_subs_cg_size), 3)

    # Draw the tick mark if the tick box is checked
    if subs_box == '3':
        pygame.draw.line(screen, black, (tick_box_subs_cg_x, tick_box_subs_cg_y), (tick_box_subs_cg_x + tick_box_subs_cg_size, tick_box_subs_cg_y + tick_box_subs_cg_size), 3)
        pygame.draw.line(screen, black, (tick_box_subs_cg_x + tick_box_subs_cg_size, tick_box_subs_cg_y), (tick_box_subs_cg_x, tick_box_subs_cg_y + tick_box_subs_cg_size), 3)

    # Check for mouse click on the tick box
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if tick_box_subs_cg_x <= mouse_x <= tick_box_subs_cg_x + tick_box_subs_cg_size and tick_box_subs_cg_y <= mouse_y <= tick_box_subs_cg_y + tick_box_subs_cg_size and mouse_clicked:
        # Toggle the tick box state and update the variable
        if subs_box != '3':
            political_rights["Subsidies"] = powerbase[2]
            subs_box = '3'

        elif subs_box == '3':
            political_rights["Subsidies"] = 'None'
            subs_box = '0'

    tick_box_checked["Subsidies"] = subs_box

    # print(political_rights)

    return display_gov_dropdowns, player_government, tick_box_checked, political_rights, selection, powerbase