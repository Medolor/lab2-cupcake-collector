import pygame
import sys
import random
import io
import base64

# Initialize Pygame
pygame.init()

# Window & World Setup
WIDTH, HEIGHT = 800, 600
WORLD_WIDTH = 2400  # World size (3 screen widths)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloud Chaser")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (30, 30, 40)
STAR_COLOR = (140, 140, 180)
RED = (255, 0, 0)
CLOUD = (190, 170, 190, 10)
WHITE = (235, 235, 235)

# Player Configuration (World Space Coordinates)
player_rect = pygame.Rect(100, 100, 40, 40)
player_vel_x = 0
player_vel_y = 0
player_speed = 6

# Physics Constants
GRAVITY = 0.8
JUMP_STRENGTH = -15
is_grounded = False  

# 2. BASE64 CONVERTED SPRITE IMAGE
RAW_BASE64_SPRITE = ("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")

# Convert Raw Base64 string back into a Pygame Surface
image_data = base64.b64decode(RAW_BASE64_SPRITE)
image_file = io.BytesIO(image_data)
sprite_surface = pygame.image.load(image_file).convert_alpha()

# Scale sprite to fit player rect size
sprite_surface = pygame.transform.scale(sprite_surface, (player_rect.width, player_rect.height))

# Platforms across the 2400px World
platforms = [
    pygame.Rect(0, 550, WORLD_WIDTH, 50),       # Ground floor spanning full world
    pygame.Rect(200, 420, 200, 20),
    pygame.Rect(550, 320, 200, 20),
    pygame.Rect(900, 400, 220, 20),              # Moving Platform
    pygame.Rect(1350, 300, 200, 20),
    pygame.Rect(1750, 380, 220, 20),
    pygame.Rect(2150, 260, 200, 20)              # Platform wrapping near boundary
]

# Moving Platform Setup
moving_platform = platforms[3]
moving_speed = 3
moving_direction = 1
moving_min_x = 850
moving_max_x = 1200
player_on_moving = False

# Cupcakes Setup
cupcakes = []
for _ in range(20):
    cx = random.randint(100, WORLD_WIDTH - 100)
    cy = random.randint(100, 480)
    cupcakes.append(pygame.Rect(cx, cy, 16, 16))

# Background Stars Setup
stars = []
for _ in range(120):
    sx = random.randint(0, WORLD_WIDTH)
    sy = random.randint(0, HEIGHT)
    parallax_speed = random.choice([0.2, 0.4, 0.7])
    stars.append([sx, sy, parallax_speed])

# Main Game Loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 2. Controls
    keys = pygame.key.get_pressed()
    player_vel_x = 0
    
    if keys[pygame.K_LEFT]:
        player_vel_x = -player_speed
    if keys[pygame.K_RIGHT]:
        player_vel_x = player_speed
    if keys[pygame.K_UP] and is_grounded:
        player_vel_y = JUMP_STRENGTH
        is_grounded = False

    # 3. Update Moving Platform
    plat_move_x = moving_speed * moving_direction
    moving_platform.x += plat_move_x
    if moving_platform.left <= moving_min_x or moving_platform.right >= moving_max_x:
        moving_direction *= -1

    if player_on_moving:
        player_rect.x += plat_move_x

    # 4. Movement + Wrapping
    player_vel_y += GRAVITY
    player_rect.x += player_vel_x
    player_rect.x %= WORLD_WIDTH
    player_rect.y += player_vel_y
    is_grounded = False  
    player_on_moving = False
    
    # 5. Check collisions
    for platform in platforms:
        for offset in (-WORLD_WIDTH, 0, WORLD_WIDTH):
            test_plat = platform.move(offset, 0)
            if player_rect.colliderect(test_plat):
                if player_vel_y > 0:  # Falling
                    player_rect.bottom = test_plat.top
                    player_vel_y = 0
                    is_grounded = True
                    if platform == moving_platform:
                        player_on_moving = True
                elif player_vel_y < 0:  # Jumping upward
                    player_rect.top = test_plat.bottom
                    player_vel_y = 0

    if player_rect.bottom > 550:
        player_rect.bottom = 550
        player_vel_y = 0
        is_grounded = True

    # Cupcake Collection Logic
    for cupcake in cupcakes[:]:
        for offset in (-WORLD_WIDTH, 0, WORLD_WIDTH):
            test_cupcake = cupcake.move(offset, 0)
            if player_rect.colliderect(test_cupcake):
                cupcakes.remove(cupcake)
                break

    # Camera Tracking
    camera_x = player_rect.centerx - WIDTH // 2
    screen.fill(BACKGROUND)
    OFFSETS = (-WORLD_WIDTH, 0, WORLD_WIDTH)

    # Draw Background Stars
    for star in stars:
        for offset in OFFSETS:
            screen_star_x = (star[0] + offset) - (camera_x * star[2])
            screen_star_x %= WORLD_WIDTH  # Wrap star position within view
            if -10 <= screen_star_x <= WIDTH + 10:
                pygame.draw.circle(screen, STAR_COLOR, (int(screen_star_x), star[1]), int(star[2] * 3))

    # Draw Platforms
    for platform in platforms:
        for offset in OFFSETS:
            screen_x = platform.x + offset - camera_x
            if -platform.width <= screen_x <= WIDTH:
                pygame.draw.rect(screen, CLOUD, (screen_x, platform.y, platform.width, platform.height))

    # Draw Cupcakes
    for cupcake in cupcakes:
        for offset in OFFSETS:
            screen_x = cupcake.centerx + offset - camera_x
            if -20 <= screen_x <= WIDTH + 20:
                pygame.draw.circle(screen, WHITE, (int(screen_x), cupcake.centery), 8)

    # Draw Player Sprite
    screen_player_x = player_rect.x - camera_x
    screen.blit(sprite_surface, (screen_player_x, player_rect.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
