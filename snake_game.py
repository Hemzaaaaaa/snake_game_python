import pygame
import time
import random
import os

pygame.init()

# Load sounds
eat_sound = pygame.mixer.Sound("eat.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Define themes
light_theme = {
    'background': (255, 255, 255),
    'snake': (0, 0, 0),
    'food': (0, 255, 0),
    'obstacle': (255, 0, 0),  # red for obstacles
    'text': (0, 0, 0),
    'message': (213, 50, 80)
}

dark_theme = {
    'background': (50, 50, 50),
    'snake': (255, 255, 255),
    'food': (0, 255, 0),
    'obstacle': (255, 0, 0),  # red for obstacles
    'text': (255, 255, 255),
    'message': (213, 50, 80)
}

# Display
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game - Settings & AI")

# Constants
snake_block = 10
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)

# Highscore system
def get_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return int(file.read())
    return 0

def save_highscore(score):
    highscore = get_highscore()
    if score > highscore:
        with open("highscore.txt", "w") as file:
            file.write(str(score))

# Draw snake
def draw_snake(snake_list, theme):
    for x in snake_list:
        pygame.draw.rect(window, theme['snake'], [x[0], x[1], snake_block, snake_block])

# Draw obstacles
def draw_obstacles(obstacles, theme):
    for obs in obstacles:
        pygame.draw.rect(window, theme['obstacle'], [obs[0], obs[1], snake_block, snake_block])


# Draw info
def draw_info(score, level, elapsed_time, highscore, theme):
    window.blit(font.render(f"Score: {score}", True, theme['text']), [10, 10])
    window.blit(font.render(f"Level: {level}", True, theme['text']), [10, 40])
    window.blit(font.render(f"Time: {int(elapsed_time)}s", True, theme['text']), [10, 70])
    window.blit(font.render(f"Highscore: {highscore}", True, theme['text']), [width - 150, 10])

# Message helper
def message(msg, color, theme, y_offset=0):
    mesg = font.render(msg, True, color)
    rect = mesg.get_rect(center=(width / 2, height / 2 + y_offset))
    window.blit(mesg, rect)

# Settings menu
def settings_menu():
    difficulty = "Medium"
    ai_mode = False
    theme = light_theme  # Default theme
    options = ["Difficulty: Medium", "Play Mode: Player", "Theme: Light", "Start Game"]
    current = 0

    while True:
        window.fill(theme['background'])
        message("Settings Menu", theme['message'], theme, -100)
        for idx, opt in enumerate(options):
            color = theme['message'] if idx == current else theme['text']
            message(opt, color, theme, 50 * idx)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current = (current - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    current = (current + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if current == 0:
                        # Toggle difficulty
                        if difficulty == "Easy":
                            difficulty = "Medium"
                        elif difficulty == "Medium":
                            difficulty = "Hard"
                        else:
                            difficulty = "Easy"
                        options[0] = f"Difficulty: {difficulty}"
                    elif current == 1:
                        ai_mode = not ai_mode
                        options[1] = f"Play Mode: {'AI Demo' if ai_mode else 'Player'}"
                    elif current == 2:
                        # Toggle theme
                        if theme == light_theme:
                            theme = dark_theme
                            options[2] = "Theme: Dark"
                        else:
                            theme = light_theme
                            options[2] = "Theme: Light"
                    else:
                        # Start game
                        return difficulty, ai_mode, theme

# Basic AI movement: move toward food
def get_ai_direction(snake_head, food_pos):
    dx, dy = 0, 0
    if snake_head[0] < food_pos[0]: dx = snake_block
    elif snake_head[0] > food_pos[0]: dx = -snake_block
    elif snake_head[1] < food_pos[1]: dy = snake_block
    elif snake_head[1] > food_pos[1]: dy = -snake_block
    return dx, dy

# Generate obstacles
def generate_obstacles(num):
    obstacles = []
    for _ in range(num):
        obs_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        obs_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])
    return obstacles

# Game loop
def game_loop(speed, ai_mode, theme):
    game_over = False
    game_close = False

    x, y = width / 2, height / 2
    x_change = y_change = 0

    snake_list = []
    length = 1
    score = 0
    level = 1
    base_speed = speed

    start_time = time.time()

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    obstacles = generate_obstacles(level * 3)
    highscore = get_highscore()

    while not game_over:
        while game_close:
            window.fill(theme['background'])
            message("Game Over! Press C to Play Again or Q to Quit", theme['message'], theme)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: return
                    if event.key == pygame.K_c: return main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if not ai_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block; y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block; y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block; x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block; x_change = 0

        if ai_mode:
            x_change, y_change = get_ai_direction([x, y], [food_x, food_y])

        if x >= width or x < 0 or y >= height or y < 0:
            gameover_sound.play()
            game_close = True

        x += x_change
        y += y_change
        window.fill(theme['background'])
        pygame.draw.rect(window, theme['food'], [food_x, food_y, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                gameover_sound.play()
                game_close = True

        # Collision with obstacles
        for obs in obstacles:
            if snake_head == obs:
                gameover_sound.play()
                game_close = True

        draw_snake(snake_list, theme)
        draw_obstacles(obstacles, theme)
        elapsed_time = time.time() - start_time
        draw_info(score, level, elapsed_time, highscore, theme)
        pygame.display.update()

        if x == food_x and y == food_y:
            eat_sound.play()
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1
            score += 1
            if score % 5 == 0:
                level += 1
                speed += 2
                obstacles += generate_obstacles(2)

        save_highscore(score)
        clock.tick(speed)

def main():
    difficulty, ai_mode, theme = settings_menu()
    if difficulty == "Easy":
        speed = 10
    elif difficulty == "Hard":
        speed = 25
    else:
        speed = 15
    game_loop(speed, ai_mode, theme)

main()
