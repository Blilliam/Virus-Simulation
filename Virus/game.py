import random
from turtle import width
import pygame
from box import Box
from center import Center
from config import Config
from graph import Graph
import person
from person import Person
from pulse import Pulse

class Game:
    def __init__(self):
        c = Config.load()

        boxHeight = c.get("box", "height")
        boxWidth = c.get("box", "width")

        self.simulation_boxes = []

        self.add_box(Box(50, 50, boxWidth, boxHeight, self))
        self.add_box(Box(50, 600, boxWidth, boxHeight, self))

        self.center = Center(800, 400, 100, 100)

        self.history = []

        self.people = []
        self.pulses = []

        self.historyTimer = 0

        self.graph = Graph(self, 600, 600, 400, 400)

        for i in range(50):
            p = person.Person(self, self.simulation_boxes[i%2])
            self.people.append(p)
            self.pulses.append(Pulse(p))

        random.choice(self.people).state = 1  # start with one infected

    def add_box(self, box):
        self.simulation_boxes.append(box)

    def update(self, dt):
        self.dt = dt

        for i in range(len(self.people)):
            self.people[i].update(dt)
            self.pulses[i].update(self.people[i], dt)

        self.historyTimer += 1
        if self.historyTimer % 3 == 0:
            self.updateHistory()

        # Handle collisions inside this box
        Person.handleCollisions(self.people, dt)


    def draw(self, screen):
        self.center.draw(screen)

        for box in self.simulation_boxes:
            box.draw(screen)

        for i in range(len(self.people)):
            self.people[i].draw(screen)
            self.pulses[i].draw(self.people[i], screen)

        self.graph.draw(screen)



    def updateHistory(self):
        infectedCount = sum(1 for p in self.people if p.state == 1)
        uninfectedCount = sum(1 for p in self.people if p.state == 0)
        recoveredCount = sum(1 for p in self.people if p.state == -1)
        self.history.append([uninfectedCount, infectedCount, recoveredCount])
