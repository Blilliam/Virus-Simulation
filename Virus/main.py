import warnings
import pygame
from game import Game

print("Starting My First Pygame")

# Ignore Pygame warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Initialize Pygame
pygame.init()

# Get fullscreen size
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the window
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("My First Pygame")

# Create a Game instance
game = Game(400, 400, 500, 500)

# Set up the clock for consistent FPS
clock = pygame.time.Clock()
FPS = 60  # target 60 frames per second

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # allow exit with ESC
                running = False

    # Update game objects
    game.update()

    # Draw everything
    screen.fill((0, 128, 255))  # background color
    game.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
