## Alex McCorristin
## Spring 2017
## Audio.py

import pygame
import sys
from pygame.locals import*
from random import randint

pygame.mixer.pre_init(44100, -16, 2, 1024*4)
pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Sound!!")

cat_unhappy = pygame.mixer.Sound('Audio/Unhappy_Meow.wav')
cat_happy = pygame.mixer.Sound('Audio/pur_meow.wav')
rocket_sound = pygame.mixer.Sound('Audio/Rumbel.wav')
  
Sound_check = 3
cat_dead = True

                

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and not cat_dead:
            rocket_sound.play()
            Sound_check = randint(1,3)
            print(x)
            
        elif cat_dead is True:
            cat_unhappy.play()
            quit

        else:
            if Sound_check == 3:
                cat_happy.play()
