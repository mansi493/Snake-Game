import pygame
import random

# initialize pygame
pygame.init()

# set window size
width = 1000
height = 600
window = pygame.display.set_mode((width, height))

# set title
pygame.display.set_caption("🐍Snake Game🐍")

# snake setting
snake_block = 20

# Function to reset the game
def reset_game():
    global snake, snake_direction, score, food_x, food_y
    snake = [[100, 100], [80, 100], [60, 100]]
    snake_direction = 'RIGHT'
    score = 0
    food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

# Initialize game variables
reset_game()

# game clock
clock = pygame.time.Clock()
snake_speed = 10

# Set up font for displaying score
font = pygame.font.SysFont("Arial", 25)

# Function to display score on the screen
def display_score(score):
    value = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(value, [0, 0])

# Function for Game Over screen
def game_over():
    background_image = pygame.image.load("main.jpeg")
    background_image = pygame.transform.scale(background_image, (width, height))

    window.blit(background_image, (0, 0))
    
    game_over_text = font.render("Game Over! Press Enter to Restart", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 3))
    score_rect = score_text.get_rect(center=(width // 2, height // 2))

    window.blit(game_over_text, game_over_rect)
    window.blit(score_text, score_rect)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    waiting = False

# Load background image and scale it to window size
background_image = pygame.image.load("main.jpeg")
background_image = pygame.transform.scale(background_image, (width, height))

# gaming loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture key presses
    keys = pygame.key.get_pressed()
    
    # Check for pause
    if keys[pygame.K_SPACE]:
        paused = not paused  
    
    if not paused:
        # Update direction based on arrow keys
        if keys[pygame.K_LEFT] and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'
        elif keys[pygame.K_UP] and snake_direction != 'DOWN':
            snake_direction = 'UP'
        elif keys[pygame.K_DOWN] and snake_direction != 'UP':
            snake_direction = 'DOWN'

        # move snake
        head_x, head_y = snake[0]
        
        if snake_direction == 'RIGHT':
            head_x += snake_block
        elif snake_direction == 'LEFT':
            head_x -= snake_block
        elif snake_direction == 'UP':
            head_y -= snake_block
        elif snake_direction == 'DOWN':
            head_y += snake_block
            
        # add new head
        new_head = [head_x, head_y]
        snake.insert(0, new_head)
        
        # Check for food collision
        if head_x == food_x and head_y == food_y:
            food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            score += 1
        else:
            snake.pop()

        # Check for wall collision
        if head_x >= width or head_x < 0 or head_y >= height or head_y < 0:
            game_over()
        
        # Check for self collision
        if new_head in snake[1:]:
            game_over()
        
        # clear screen and draw background
        window.blit(background_image, (0, 0))
        
        # draw snake
        for block in snake:
            pygame.draw.rect(window, (255, 255, 0), (block[0], block[1], snake_block, snake_block))
        
        # draw food
        pygame.draw.rect(window, (255, 0, 0), (food_x, food_y, snake_block, snake_block))
        
        # Display score
        display_score(score)
            
        # update display
        pygame.display.update()
    
    else:
        # Display paused message
        pause_text = font.render("Paused. Press Space to continue.", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(width // 2, height // 2))
        window.blit(pause_text, pause_rect)
        pygame.display.update()
    
    # snake speed control
    clock.tick(snake_speed)
    
# exit the window
pygame.quit()

