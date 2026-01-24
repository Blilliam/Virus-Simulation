import random

import pygame
from person import Person
from pulse import Pulse
import person


class Game:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height


        self.numberOfPeople = 50
        self.people = []
        self.pulses = []

        self.peopleSize = 10

        for i in range(self.numberOfPeople):
            x = random.randint(self.peopleSize, width - self.peopleSize)
            y = random.randint(self.peopleSize, height - self.peopleSize)
            temp = Person(self, x, y, self.peopleSize)
            self.people.append(temp)

            self.pulses.append(Pulse(temp))

    def update(self):
        for i in range(len(self.people)):
            self.people[i].update()
            self.pulses[i].update(self.people[i])

        # collision between eachother
        person.handle_collisions(self.people)
    
    def draw(self, screen):
        pygame.draw.rect(screen, "black", (self.x, self.y, self.width, self.height))

        for i in range(len(self.people)):
            self.people[i].draw(screen)
            self.pulses[i].draw(self.people[i], screen)