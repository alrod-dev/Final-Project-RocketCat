##Rocket_Cat.py
# Date: 4/23/2017
# Class: EAE 1410
# Teacher: Dr. Mark C. van Langeveld
# TA: Rohan More
##Partners: Alfredo Rodriguez, Hao Quin, Alex McCorristin


import pygame
import sys
import random

pygame.mixer.pre_init(44100, -16, 2, 1024 * 4)
pygame.init()


class Rocket_Cat:
    def __init__(self):

        ##Initializes screen
        self.screen = pygame.display.set_mode((400, 708))
        self.cat = pygame.Rect(65, 50, 50, 50)

        ##Space background
        self.background = pygame.image.load("images/galaxy.jpg").convert()

        ##Cat Sprites Animations
        self.catStationary = pygame.image.load("images/Cat_Stationary.png").convert_alpha()
        self.catStationary = pygame.transform.scale(self.catStationary, (50, 50))

        self.catBlastOff1 = pygame.image.load("images/Cat_blast_off_1.png").convert_alpha()
        self.catBlastOff1 = pygame.transform.scale(self.catBlastOff1, (50, 50))

        self.catBlastOff2 = pygame.image.load("images/Cat_blast_off_2.png").convert_alpha()
        self.catBlastOff2 = pygame.transform.scale(self.catBlastOff2, (50, 50))

        self.catDead = pygame.image.load("images/Cat_DEAD.png")
        self.catDead = pygame.transform.scale(self.catDead, (50, 50))

        ##Sounds
        self.cat_unhappy = pygame.mixer.Sound('Audio/Unhappy_Meow.wav')
        self.cat_happy = pygame.mixer.Sound('Audio/meow.wav')
        self.rocket_sound = pygame.mixer.Sound('Audio/Jet_Hiss.wav')
        self.contact = pygame.mixer.Sound('Audio/thud.wav')
        self.coinhit = pygame.mixer.Sound('Audio/Lazer.wav')

        sound_check = 0

        ##Music
        self.music = pygame.mixer.music.load('Audio/Space_Walk.wav')
        pygame.mixer.music.play(-1, 0.0)

        ##List of all animations put into one
        self.catSprites = [self.catStationary, self.catBlastOff1,
                           self.catBlastOff2, self.catDead]

        ##Obstacles & Coins
        self.wallUp = pygame.image.load("images/spikes_btm.png").convert_alpha()
        self.wallDown = pygame.image.load("images/spikes_top.png").convert_alpha()

        self.wallDown1 = pygame.image.load("images/top.png").convert_alpha()
        self.wallUp1 = pygame.image.load("images/bottom.png").convert_alpha()

        self.coin = pygame.image.load("images/coin.png").convert_alpha()

        ##Obstacle and Cat settings
        self.gap = 130
        self.wallx = 400
        self.coinx = random.randint(50, 200)
        self.coiny = random.randint(100, 600)
        self.catY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)

    ##Update the walls positions
    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    ##Update the coins positions
    def updatecoin(self):
        self.coinx -= 2
        if self.coinx < -80:
            self.coinx = 300
            self.counter += 1
            self.offset = random.randint(-110, 110)

    ##Updates cat animations and whether its dead or not
    def catUpdate(self):

        ##Checks whether the cat is jumping or not
        ##Changes animations
        if self.jump:
            self.jumpSpeed -= 1
            self.catY -= self.jumpSpeed
            self.jump -= 1

        else:
            self.catY += self.gravity
            self.gravity += 0.2
        self.cat[1] = self.catY

        ##Obstacles Boundaries
        upRect = pygame.Rect(self.wallx,
                             615 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())

        upRect1 = pygame.Rect(self.wallx,
                              360 + self.gap - self.offset + 10,
                              self.wallUp1.get_width() - 10,
                              self.wallUp1.get_height())

        downRect1 = pygame.Rect(self.wallx,
                                0 - self.gap - self.offset - 10,
                                self.wallDown1.get_width() - 10,
                                self.wallDown1.get_height())

        coinRect = pygame.rect(self.coinx, self.coiny)

        ## coin colision ----what I'm having problems with----

        # if coinRect.colliderect(self.cat):
        #     self.coinhit.play()


        ##Tube Up
        if upRect.colliderect(self.cat):
            self.contact.play()
            self.cat_unhappy.play()
            self.dead = True

        ##Tube down
        if downRect.colliderect(self.cat):
            self.contact.play()
            self.cat_unhappy.play()
            self.dead = True

        ##Spikes up
        if upRect1.colliderect(self.cat):
            self.contact.play()
            self.cat_unhappy.play()
            self.dead = True

        ##Spikes down
        if downRect1.colliderect(self.cat):
            self.cat_unhappy.play()
            self.contact.play()
            self.dead = True

        if not 0 < self.cat[1] < 720:
            self.cat[1] = 50
            self.catY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    ##Main function of the game
    def main(self):

        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                ##User presses space, up or down key
                ##Play cat sounds, change animation, and change position
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10
                    sound_check = random.randint(1, 3)
                    if sound_check == 1:
                        self.cat_happy.play()

            ##Blits all items in to screen
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx - self.offset, 615))
            self.screen.blit(self.wallDown,
                             (self.wallx - self.offset, -5))
            self.screen.blit(self.coin,
                             (self.coinx - self.offset, self.coiny))

            self.screen.blit(self.wallUp1,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown1,
                             (self.wallx, 0 - self.gap - self.offset))

            self.screen.blit(font.render(str(self.counter), -1,
                                         (255, 255, 255)), (200, 50))

            ##If the cat dies play unhappy sound
            ##Change animation
            if self.dead:
                self.sprite = 3

            ##If cat jumps chnage animation to rockets
            elif self.jump:
                self.sprite = 1
                self.rocket_sound.play()

            self.screen.blit(self.catSprites[self.sprite], (70, self.catY))

            ##If not dead then update wall accordingly and first sprite
            if not self.dead:
                self.sprite = 0

            ##Update obstacles and cat
            self.updateWalls()
            self.updatecoin()
            self.catUpdate()
            pygame.display.update()


if __name__ == "__main__":
    Rocket_Cat().main()