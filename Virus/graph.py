import pygame


class Graph:
    def __init__(self, game, x, y, w, h):
        self.x = x
        self.y = y

        self.x_scale = 1.0
        self.x_scale_rate = 0  # how fast it squishes horizontally
        self.hit_border = False



        self.w = w
        self.h = h

        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, [255, 255, 255], [self.x, self.y, self.w, self.h], 1)

        bar_count = len(self.game.history)

        # Calculate horizontal scale (only if needed)
        if bar_count <= self.w:
            x_scale = 1.0
        else:
            x_scale = self.w / bar_count  # squeeze JUST enough to fit

        bar_x = 0
        
        if self.game.history and self.game.history[-1][1] > 0:
            for u, i, r in self.game.history:
                total = u + i + r

                if total == 0:
                    continue

                uHeight = (u / total) * self.h
                iHeight = (i / total) * self.h
                rHeight = (r / total) * self.h

                draw_x = self.x + int(bar_x * x_scale)

                if draw_x > self.x + self.w:
                    break

                pygame.draw.rect(screen, [255, 255, 255],
                                [draw_x, self.y, 1, uHeight])
                pygame.draw.rect(screen, [255, 0, 0],
                                [draw_x, self.y + uHeight, 1, iHeight])
                pygame.draw.rect(screen, [0, 0, 0],
                                [draw_x, self.y + uHeight + iHeight, 1, rHeight])

                bar_x += 1




        

            

        



