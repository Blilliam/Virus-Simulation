import warnings
import pygame
from game import Game
from box import Box
from config import Config

warnings.filterwarnings("ignore", category=UserWarning)

c = Config.load()

pygame.init()

# Fullscreen
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Simulation Controller")

# Clock
gameSpeed = 6

clock = pygame.time.Clock()
FPS = 60

# Create game
game = Game()

boxHeight = c.get("box", "height")
boxWidth = c.get("box", "width")

# Add multiple simulation boxes
game.add_box(Box(50, 50, boxWidth, boxHeight))
game.add_box(Box(50, 600, boxWidth, boxHeight))

# Main loop
running = True
while running:
    diffTime = clock.tick(FPS)/1000
    dt = diffTime * gameSpeed * FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    game.update(dt)

    screen.fill((0, 128, 255))  # background
    game.draw(screen)

    pygame.display.flip()

pygame.quit()
