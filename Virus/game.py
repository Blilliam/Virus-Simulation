import pygame
from box import Box
from center import Center

class Game:
    def __init__(self):
        self.simulation_boxes = []
        self.center = Center(500, 100, 100, 100)

    def add_box(self, box):
        self.simulation_boxes.append(box)

    def update(self, dt):
        self.dt = dt
        for box in self.simulation_boxes:
            box.update(self.dt)

    def draw(self, screen):
        for box in self.simulation_boxes:
            box.draw(screen)

        self.center.draw(screen)
