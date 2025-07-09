import pygame
import random
import time
import math

print("Instructions:")
print("To play use your arrow keys to dodge the blocks")
print("30 Seconds on the Clock. See if you can survive or not")
print("Have Fun!")

# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Window settings
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 600

# Player settings
PLAYER_SIZE = 20
player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT - PLAYER_SIZE * 2
player_dx = 0

# Game variables
falling_blocks = []
FALL_SPEED = 50
SPAWN_DELAY = 5
spawn_timer = 0
score = 0
game_duration = 30
game_start_time = time.time()
game_over = False
you_win = False

# FPS
FPS = 22
clock = pygame.time.Clock()

# Display
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dodge Blocks Game")

# Fonts
font = pygame.font.SysFont("Arial", 25)
gameover_font=pygame.font.SysFont("Arial", 60)
win_font=pygame.font.SysFont("Arial", 50)

# Sounds
collision_sound = pygame.mixer.Sound(r"C:\Users\omrad\OneDrive\Desktop\Dodge Blocks Game\collison_sound.wav")
background_sound = pygame.mixer.Sound(r"C:\Users\omrad\OneDrive\Desktop\Dodge Blocks Game\background_sound.wav.mp3")
victory_sound=pygame.mixer.Sound(r"C:\Users\omrad\OneDrive\Desktop\Dodge Blocks Game\Victory sound effect (pixabay).wav")

# Play the background sound infinitly
background_sound.play(loops=-1)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Arrow key movements
        if not game_over and not you_win and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -PLAYER_SIZE
            elif event.key == pygame.K_RIGHT:
                player_dx = PLAYER_SIZE

    #  Move the player and check for boundaries 
    if not game_over and not you_win:
        player_x += player_dx
        player_dx = 0
        player_x = max(0, min(player_x, WINDOW_WIDTH - PLAYER_SIZE))
        
        # Spawn Blocks
        spawn_timer += 1 # Increase spawn_timer by 1 each frame
        #Spawn a new block and reset spawn timer every 8 secs 
        if spawn_timer >= SPAWN_DELAY: 
            spawn_timer = 0 
            new_x = random.randint(0, (WINDOW_WIDTH - PLAYER_SIZE) // PLAYER_SIZE) * PLAYER_SIZE
            falling_blocks.insert(0, (new_x, 0, PLAYER_SIZE, PLAYER_SIZE))
        
        # Blocks
        new_blocks = [] # Store the new blocks in a list
        for block in falling_blocks: # All the block in the list
            block_x, block_y, block_w, block_h = block # X axis , y axis , width , height 
            block_y += FALL_SPEED # Move the block down along the Y-axis by the fall speed
            # If block is still on screen, keep it for next frame (append adds to the end of list)
            # otherwise, remove it and increase score for dodging it (add 1 to the score)
            if block_y < WINDOW_HEIGHT: 
                new_blocks.append((block_x, block_y, block_w, block_h))
            else:
                score += 1
        falling_blocks = new_blocks
       
        # Check collison with block
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        for block in falling_blocks:
            block_rect = pygame.Rect(block)
            if player_rect.colliderect(block_rect):
                background_sound.stop()
                collision_sound.play()
                pygame.time.delay(1000)
                game_over = True
                running = False
        
        # Time settings and controls 
        elapsed_time = time.time() - game_start_time
        remaining_time = max(0, math.floor(game_duration - elapsed_time))
        if remaining_time <= 0:
            background_sound.stop()
            you_win = True
            running = False

    # Drawing  and writing everything
    display.fill(white)
    pygame.draw.rect(display, (0, 0, 255), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
    for block in falling_blocks:
        pygame.draw.rect(display, (255, 0, 0), block)

    score_text = font.render(f"Score: {score}", True, black)
    timer_text = font.render(f"Time Left: {remaining_time}", True, black)
    display.blit(score_text, (10, 10))
    display.blit(timer_text, (10, 40))

    pygame.display.flip()
    clock.tick(FPS)

if game_over:
    display.fill(white)
    text = gameover_font.render("Game Over! You got hit!", True, red)
    display.blit(text, (100,200))
    pygame.display.flip()
    pygame.time.delay(1000)

elif you_win:
    display.fill(white)
    victory_sound.play()
    text = win_font.render("Congratulations! You Survived!", True, green)
    display.blit(text, (30, 200))
    pygame.display.flip()
    pygame.time.delay(1000)

pygame.quit()
