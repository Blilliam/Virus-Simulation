import random
import pygame
from person import Person
from pulse import Pulse
from graph import Graph
from config import Config
import person  # for handle_collisions

class Box:
    def __init__(self, x, y, width, height, numOfPeople=50):
        c = Config.load()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.numOfPeople = numOfPeople
        self.peopleSize = c.get("person", "personRadius")

        self.people = []
        self.pulses = []
        self.history = []
        self.historyTimer = 0

        self.graph = Graph(self, x + 50 + self.width, y + 50, 400, 400)

        for _ in range(self.numOfPeople):
            px = random.randint(self.peopleSize, width - self.peopleSize)
            py = random.randint(self.peopleSize, height - self.peopleSize)
            p = Person(self, px, py)
            self.people.append(p)
            self.pulses.append(Pulse(p))

        random.choice(self.people).state = 1  # start with one infected

    def update(self):
        for i in range(len(self.people)):
            self.people[i].update()
            self.pulses[i].update(self.people[i])

        self.historyTimer += 1
        if self.historyTimer % 3 == 0:
            self.updateHistory()

        # Handle collisions inside this box
        person.handleCollisions(self.people)

    def draw(self, screen):
        pygame.draw.rect(screen, "black", (self.x, self.y, self.width, self.height))
        self.graph.draw(screen)
        for i in range(len(self.people)):
            self.people[i].draw(screen)
            self.pulses[i].draw(self.people[i], screen)

    def updateHistory(self):
        infectedCount = sum(1 for p in self.people if p.state == 1)
        uninfectedCount = sum(1 for p in self.people if p.state == 0)
        recoveredCount = sum(1 for p in self.people if p.state == -1)
        self.history.append([uninfectedCount, infectedCount, recoveredCount])
