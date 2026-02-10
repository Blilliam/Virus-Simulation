import pygame

class Pulse:
    def __init__(self, person):
        self.infectionRadius = person.infectionRadius
        self.x = person.x
        self.y = person.y

        self.size = person.size
        self.min_size = person.size
        self.max_size = self.infectionRadius

        self.growth_speed = 1
        self.growing = True

    def update(self, person, dt):
        if person.state == 1:
            # Follow the person
            self.x = person.x
            self.y = person.y

            # Pulse logic
            if self.growing:
                self.size += self.growth_speed * dt
                if self.size >= self.max_size:
                    self.growing = False
            else:
                self.size -= self.growth_speed * dt
                if self.size <= self.min_size:
                    self.growing = True

        

    def draw(self, person, screen):
        if person.state == 1:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), int(self.size), 2)
