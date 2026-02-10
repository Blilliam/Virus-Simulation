import math
import random
import pygame
from config import Config

class Person:
    def __init__(self, game, x=0, y=0):
        c = Config.load()

        # 0: uninfected, 1: infected, -1: recovered
        self.state = 0
        
        self.size = c.get("person", "personRadius")
        self.game = game

        self.infectionRadius = c.get("person", "infectionRadius")

        self.currInfectionCount = 0

        self.infectedTime = 0
        self.maxInfectedTime = random.randint(900, 1200)  # frames until recovery

        self.infectionThreshold = c.get("person", "infectionThreshold")

        self.x = x + game.x
        self.y = y + game.y

        self.speed = 0.5
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self, dt):
        if self.state == 1:
            self.infectedTime += 1 * dt

            if self.infectedTime >= self.maxInfectedTime:
                self.state = -1
        
        # Random wiggle
        wiggle_angle = random.uniform(-0.2, 0.2)
        cosa = math.cos(wiggle_angle)
        sina = math.sin(wiggle_angle)

        newDx = self.dx * cosa - self.dy * sina
        newDy = self.dx * sina + self.dy * cosa

        mag = math.hypot(newDx, newDy)
        self.dx = (newDx / mag) * self.speed
        self.dy = (newDy / mag) * self.speed

        # Move
        self.x += self.dx * dt
        self.y += self.dy * dt


        # Boundary collision
        if self.x <= self.game.x + self.size or self.x >= self.game.width + self.game.x - self.size:
            self.dx *= -1
        if self.y <= self.game.y + self.size or self.y >= self.game.height + self.game.y - self.size:
            self.dy *= -1

    def draw(self, screen):
        if self.state == -1:
            color = (128, 128, 128)  # grey
        elif self.state == 0:
            color = (255, 255, 255)  # white
        else:
            color = (255, 0, 0)      # red

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


# Collision function
def circleCollision(p1, p2, radius):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance_sq = dx * dx + dy * dy
    radius_sum = 2 * radius
    return distance_sq <= radius_sum * radius_sum


# Handle collisions and spread infection
@staticmethod
def handleCollisions(people, dt):
    for i in range(len(people)):
        for j in range(len(people)):
            p1 = people[i]
            p2 = people[j]

            dx = p1.x - p2.x
            dy = p1.y - p2.y
            distance = math.hypot(dx, dy)

            if distance < p1.size + p2.size:
                # bounce
                p1.dx *= -1
                p1.dy *= -1
                p2.dx *= -1
                p2.dy *= -1

                # separate them to prevent sticking
                overlap = (p1.size + p2.size) - distance
                if distance != 0:
                    nx = dx / distance
                    ny = dy / distance
                    p1.x += nx * (overlap / 2)
                    p1.y += ny * (overlap / 2)
                    p2.x -= nx * (overlap / 2)
                    p2.y -= ny * (overlap / 2)

            if distance < p1.infectionRadius + p2.size and p1.state == 1 and p2.state == 0:
                p2.currInfectionCount += 1 * dt
                if p2.currInfectionCount > p1.infectionThreshold:
                    p2.state = 1
