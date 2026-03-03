import math
import random
import pygame
from config import Config

class Person:
    STATE_INFECTED = 1
    STATE_UNINFECTED = 0
    STATE_RECOVERED = -1

    STATE_NORMAL = "STATE_NORMAL"
    STATE_IN_POINT = "STATE_IN_POINT"
    STATE_DASH_TO = "STATE_DASH_TO"
    STATE_DASH_BACK = "STATE_DASH_BACK"

    def __init__(self, game, box):
        c = Config.load()

        # 0: uninfected, 1: infected, -1: recovered
        self.state = 0
        self.movementState = self.STATE_NORMAL

        self.size = c.get("person", "personRadius")
        self.game = game
        self.box = box

        self.infectionRadius = c.get("person", "infectionRadius")
        self.infectionThreshold = c.get("person", "infectionThreshold")

        self.currInfectionCount = 0
        self.infectedTime = 0
        self.maxInfectedTime = random.randint(900, 1200)

        self.centerTimer = 0
        self.centerTimerMax = random.uniform(1.0, 3.0)

        self.dashTimer = 0
        self.dashTimerMax = 0.1

        # Position (Vector2 now)
        self.pos = pygame.Vector2(
            random.randint(box.x + self.size, box.x + box.width - self.size),
            random.randint(box.y + self.size, box.y + box.height - self.size)
        )

        # Movement system
        self.theta = random.uniform(0, 2 * math.pi)

        self.min_speed = 18
        self.max_speed = 72
        self.speed = random.uniform(self.min_speed, self.max_speed)

        self.accel_sigma = 0.05

        self.vel = pygame.Vector2(
            math.cos(self.theta),
            math.sin(self.theta)
        ) * self.speed

    def update(self, dt):

        # Infection timer
        if self.state == 1:
            self.infectedTime += dt
            if self.infectedTime >= self.maxInfectedTime:
                self.state = -1

        # Boundary collision

        if self.movementState == self.STATE_NORMAL:
            self.bounceInBox(self.box)
            #normal movement
            self.normalMovement(dt)

            if random.random() < 0.01 * (dt):
                self.movementState = self.STATE_DASH_TO
            

        elif self.movementState == self.STATE_IN_POINT:
            #normal movement
            self.normalMovement(dt)
            self.bounceInBox(self.game.center)

            self.centerTimer += dt

            if self.centerTimer >= self.centerTimerMax:
                self.movementState = self.STATE_DASH_BACK
                self.centerTimer = 0

        elif self.movementState == self.STATE_DASH_TO:
            #self.game.center.x + (self.game.center.width/2)
            #self.game.center.y + (self.game.center.height/2)
            expectedPoint = pygame.Vector2(self.game.center.x + (self.game.center.width/2), self.game.center.y + (self.game.center.height/2))
            self.dashTimer+= dt
            if (self.dashTimer >= self.dashTimerMax / dt or self.moveTo(expectedPoint, 500, dt)):
                self.movementState = self.STATE_IN_POINT
                self.dashTimer = 0

        elif self.movementState == self.STATE_DASH_BACK:
            #self.game.center.x + (self.game.center.width/2)
            #self.game.center.y + (self.game.center.height/2)
            expectedPoint = pygame.Vector2(self.box.x + (self.box.width/2), self.box.y + (self.box.height/2))
            self.dashTimer+= dt
            if (self.dashTimer >= self.dashTimerMax / dt or self.moveTo(expectedPoint, 500, dt)):
                self.movementState = self.STATE_NORMAL
                self.dashTimer = 0
            


    def moveTo(self, expectedPoint, speed, dt):
        vectorTo = expectedPoint - self.pos

        if vectorTo.length_squared() <= 50:
            self.pos= expectedPoint
            return True
        vectorTo.normalize_ip()
        self.pos += (vectorTo * dt * speed)
        return False


    def normalMovement(self, dt) :
        # Random turning
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

            


    def draw(self, screen):
        if self.state == -1:
            color = (128, 128, 128)
        elif self.state == 0:
            color = (255, 255, 255)
        else:
            color = (255, 0, 0)

        pygame.draw.circle(screen, color, self.pos, self.size)

    def bounceInBox(self, box):
        r = self.size

        left = box.x + r
        right = box.x + box.width - r
        top = box.y + r
        bottom = box.y + box.height - r

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
                    ...
                    # # swap velocity directions (simple bounce)
                    # p1.theta, p2.theta = p2.theta, p1.theta

                    # # separate overlap
                    # overlap = (p1.size + p2.size) - distance
                    # if distance != 0:
                    #     nx = dx / distance
                    #     ny = dy / distance

                    #     p1.pos.x += nx * overlap / 2
                    #     p1.pos.y += ny * overlap / 2
                    #     p2.pos.x -= nx * overlap / 2
                    #     p2.pos.y -= ny * overlap / 2

                # Infection logic
                if distance < p1.infectionRadius:

                    if p1.state == Person.STATE_INFECTED and p2.state == Person.STATE_UNINFECTED:
                        p2.currInfectionCount += dt
                        if p2.currInfectionCount >= p1.infectionThreshold:
                            p2.state = Person.STATE_INFECTED

                    if p2.state == Person.STATE_INFECTED and p1.state == Person.STATE_UNINFECTED:
                        p1.currInfectionCount += dt
                        if p1.currInfectionCount >= p2.infectionThreshold:
                            p1.state = Person.STATE_INFECTED
                else:
                    ...
                    # if p1.state == Person.STATE_UNINFECTED:
                    #     p1.currInfectionCount = Person.STATE_UNINFECTED
                    # if p2.state == Person.STATE_UNINFECTED:
                    #     p2.currInfectionCount = Person.STATE_UNINFECTED

