import math
import random
import pygame
from config import Config

class Person:
    def __init__(self, game, box):
        c = Config.load()

        # 0: uninfected, 1: infected, -1: recovered
        self.state = 0

        self.size = c.get("person", "personRadius")
        self.game = game
        self.box = box

        self.infectionRadius = c.get("person", "infectionRadius")
        self.infectionThreshold = c.get("person", "infectionThreshold")

        self.currInfectionCount = 0
        self.infectedTime = 0
        self.maxInfectedTime = random.randint(900, 1200)

        # Position (Vector2 now)
        self.pos = pygame.Vector2(
            random.randint(box.x + self.size, box.x + box.width - self.size),
            random.randint(box.y + self.size, box.y + box.height - self.size)
        )

        # Movement system
        self.theta = random.uniform(0, 2 * math.pi)

        self.min_speed = 0.3
        self.max_speed = 1.2
        self.speed = random.uniform(self.min_speed, self.max_speed)

        self.accel_sigma = 0.05

        self.vel = pygame.Vector2(
            math.cos(self.theta),
            math.sin(self.theta)
        ) * self.speed

    def update(self, dt):

        # -----------------
        # Infection timer
        # -----------------
        if self.state == 1:
            self.infectedTime += dt
            if self.infectedTime >= self.maxInfectedTime:
                self.state = -1

        # -----------------
        # Random turning
        # -----------------
        self.theta += random.gauss(0, 1.2) * math.sqrt(dt)

        # Slight speed variation
        self.speed += random.gauss(0, self.accel_sigma) * math.sqrt(dt)
        self.speed = max(self.min_speed, min(self.speed, self.max_speed))

        # Update velocity vector
        self.vel = pygame.Vector2(
            math.cos(self.theta),
            math.sin(self.theta)
        ) * self.speed

        # Move
        self.pos += self.vel * dt

        # Boundary collision

        r = self.size

        left = self.box.x + r
        right = self.box.x + self.box.width - r
        top = self.box.y + r
        bottom = self.box.y + self.box.height - r

        if self.pos.x < left:
            self.pos.x = left
            self.theta = math.pi - self.theta

        elif self.pos.x > right:
            self.pos.x = right
            self.theta = math.pi - self.theta

        if self.pos.y < top:
            self.pos.y = top
            self.theta = -self.theta

        elif self.pos.y > bottom:
            self.pos.y = bottom
            self.theta = -self.theta

    def draw(self, screen):
        if self.state == -1:
            color = (128, 128, 128)
        elif self.state == 0:
            color = (255, 255, 255)
        else:
            color = (255, 0, 0)

        pygame.draw.circle(screen, color, self.pos, self.size)

    @staticmethod
    def handleCollisions(people, dt):
        for i in range(len(people)):
            for j in range(i + 1, len(people)):

                p1 = people[i]
                p2 = people[j]

                dx = p1.pos.x - p2.pos.x
                dy = p1.pos.y - p2.pos.y
                distance = math.hypot(dx, dy)


                # Physical collision

                if distance < p1.size + p2.size:

                    # swap velocity directions (simple bounce)
                    p1.theta, p2.theta = p2.theta, p1.theta

                    # separate overlap
                    overlap = (p1.size + p2.size) - distance
                    if distance != 0:
                        nx = dx / distance
                        ny = dy / distance

                        p1.pos.x += nx * overlap / 2
                        p1.pos.y += ny * overlap / 2
                        p2.pos.x -= nx * overlap / 2
                        p2.pos.y -= ny * overlap / 2

                # Infection logic
                if distance < p1.infectionRadius:

                    if p1.state == 1 and p2.state == 0:
                        p2.currInfectionCount += dt
                        if p2.currInfectionCount >= p1.infectionThreshold:
                            p2.state = 1

                    if p2.state == 1 and p1.state == 0:
                        p1.currInfectionCount += dt
                        if p1.currInfectionCount >= p2.infectionThreshold:
                            p1.state = 1
                else:
                    if p1.state == 0:
                        p1.currInfectionCount = 0
                    if p2.state == 0:
                        p2.currInfectionCount = 0

