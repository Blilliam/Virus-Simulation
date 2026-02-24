import random
import pygame
from person import Person
from pulse import Pulse
from graph import Graph
from config import Config
import person  # for handle_collisions

class Box:
    def __init__(self, x, y, width, height, game):
        c = Config.load()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.peopleSize = c.get("person", "personRadius")

        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, "black", (self.x, self.y, self.width, self.height))

