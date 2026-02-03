import pygame


class Graph:
    def __init__(self, game, x, y, w, h):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, [255, 255, 255], [self.x, self.y, self.w, self.h])

        self.barX = 1

        for u, i, r in self.game.history:
            self.total = u + i + r

            uPercent = u/self.total
            iPercent = i/self.total
            rPercent = r/self.total

            uHeight = uPercent * self.h
            iHeight = iPercent * self.h
            rHeight = rPercent * self.h

            pygame.draw.rect(screen, [255, 255, 255], [self.barX + self.x, self.y, 1, uHeight])
            pygame.draw.rect(screen, [255, 0, 0], [self.barX + self.x, self.y + uHeight, 1, iHeight])
            pygame.draw.rect(screen, [0, 0, 0], [self.barX + self.x, self.y + uHeight + iHeight, 1, rHeight])


            self.barX += 1

        

            

        



