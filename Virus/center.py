import pygame


class Center:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.w, self.h))