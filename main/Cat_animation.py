## Cat_animation.py
## Alex McCorristin
## Spring 2017

import pygame
from pygame.locals import *
import sys

pygame.init()

Win_Width = 640
Win_height = 480
displaySurf = pygame.display.set_mode((Win_Width, Win_height), 0, 32)
pygame.display.set_caption("Cat Animation")
Background = pygame.image.load("background.png")
displaySurf.blit(Background, (0, 0))


class Cat:
    cat_x = 300
    cat_y = 200

    def __init__(self):
        self.cat_dead = False
        self.cat_anime = "Cat_Stationary Cat_blast_off_1 Cat_blast_off_2 Cat_DEAD".split()
        self.cat_OBJS = {}
        for self.cat_anime in self.cat_anime:
            image_Durations = [("%s.png" % (self.cat_anime, str(num).rjust(3, '0')), 0.1) for num in range(4)]
            self.cat_anime[self.cat_anime] = pygame.PygAnimation(image_Durations)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if (event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN) and self.cat_dead is False:
                    self.cat_OBJS["Cat_blast_off_1"].blit(displaySurf, (300, 200))
                elif self.cat_dead is True:
                    self.cat_OBJS["Cat_DEAD"].blit(displaySurf, (300, 200))
                else:
                    self.cat_OBJS["Cat_Stationary"].blit(displaySurf, (300, 200))

            pygame.display.update()

