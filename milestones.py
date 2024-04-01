import pygame

BLACK = (0, 0, 0)
BOX_SIZE = 15

def check_milestone_events(population_grid, milestone_messages, milestone_duration):
    counter = 0
    for y in range(len(population_grid)):
        for x in range(len(population_grid[y])):
            population = population_grid[y][x]
            if population == 17 and counter < 1:
                add_milestone_message(milestone_messages, "Mining discovered", (x, y), milestone_duration)
                counter += 1
            elif population == 25 and counter < 2:
                add_milestone_message(milestone_messages, "Agriculture discovered", (x, y), milestone_duration)
                counter += 2

def draw_milestone_messages(screen, milestone_messages, population_count_position):
    font = pygame.font.Font(None, 24)
    counter = 0
    for message in milestone_messages:
        counter +=1 
        text = font.render(message["text"], True, BLACK)
        text_rect = text.get_rect(topright=(population_count_position[0], population_count_position[1] - counter*50))
        screen.blit(text, text_rect)


def add_milestone_message(milestone_messages, message, position, duration):
    milestone_messages.append({"text": message, "position": position, "duration": duration})

def update_message_durations(milestone_messages):
    for message in milestone_messages:
        message["duration"] -= 1

def remove_expired_messages(milestone_messages):
    milestone_messages[:] = [message for message in milestone_messages if message["duration"] > 0]
