import pygame
from box import Box

class Game:
    def __init__(self):
        self.simulation_boxes = []

    def add_box(self, box):
        self.simulation_boxes.append(box)

    def update(self):
        for box in self.simulation_boxes:
            box.update()

    def draw(self, screen):
        for box in self.simulation_boxes:
            box.draw(screen)
