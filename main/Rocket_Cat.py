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

        ##Cat Sound
        self.cat_unhappy = pygame.mixer.Sound('Audio/Unhappy_Meow.wav')
        self.cat_unhappy.set_volume(0.15)

        self.cat_happy = pygame.mixer.Sound('Audio/meow.wav')
        self.cat_happy.set_volume(0.3)

        self.rocket_sound = pygame.mixer.Sound('Audio/Jet_Hiss.wav')
        self.rocket_sound.set_volume(0.09)

        ##Background music
        self.contact = pygame.mixer.Sound('Audio/thud.wav')
        self.contact.set_volume(0.01)

        ##Coin Music
        self.coinhit = pygame.mixer.Sound('Audio/Lazer.wav')
        self.coinhit.set_volume(0.01)

        ##Music
        self.music = pygame.mixer.music.load('Audio/Space_Walk.wav')
        pygame.mixer.music.play(-1, 0.0)

        ##List of all animations put into one
        self.catSprites = [self.catStationary, self.catBlastOff1,
                           self.catBlastOff2, self.catDead]

        ##Obstacles & Coins
        self.spikesUp = pygame.image.load("images/spikes_btm.png").convert_alpha()
        self.spikesDown = pygame.image.load("images/spikes_top.png").convert_alpha()

        self.tubeUp = pygame.image.load("images/top.png").convert_alpha()
        self.tubeDown = pygame.image.load("images/bottom.png").convert_alpha()

        self.coin = pygame.image.load("images/coin.png").convert_alpha()
        self.coin = pygame.transform.scale(self.coin, (50, 50))

        self.coinGrey = pygame.image.load("images/coin_grey.png")
        self.coinGrey = pygame.transform.scale(self.coinGrey, (50, 50))

        self.coinSprites = [self.coin, self.coinGrey]

        self.meteor = pygame.image.load("images/asteroid.png")
        self.meteor = pygame.transform.scale(self.meteor, (50, 50))

        ##Obstacle and Cat settings
        self.gap = 130
        self.wallx = 400
        self.offset = random.randint(-110, 110)

        ##Coin parameters
        self.coinx = random.randint(300, 600)
        self.coiny = random.randint(100, 600)
        self.coinSprite = 0
        self.coinDead = False

        ##Meteor Parameters
        self.meteorX = random.randint(300, 600)
        self.meteorY = random.randint(100, 600)

        ##Cat Parameters
        self.catY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0

    ##Update the walls positions
    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    ##Update the coins positions
    def updatecoin(self):
        self.coinx -= 6

        self.coinDead = False

        if self.coinx < -80:
            self.coinx = random.randint(300, 600)
            self.coiny = random.randint(-200, 400)

    ##Adds another meteor if player is above 5 points
    def meteorCounter(self):

        meteorCount = self.counter

        meteorCount /= 5

        if meteorCount > 1:
            return meteorCount

    ##Updates meteor position
    def updateMeteor(self):
        self.meteorX -= 6

        if self.meteorX < -80:
            self.meteorX = random.randint(300, 600)
            self.meteorY = random.randint(-100, 400)

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
        tubeUpRect = pygame.Rect(self.wallx,
                                 0 - self.gap - self.offset - 10,
                                 self.tubeUp.get_width() - 10,
                                 self.tubeUp.get_height())

        tubeDownRect = pygame.Rect(self.wallx,
                                   360 + self.gap - self.offset + 10,
                                   self.tubeDown.get_width() - 10,
                                   self.tubeDown.get_height())

        ##Spike Boundairies
        spikesDownRect = pygame.Rect(self.wallx,
                                     615 + self.gap - self.offset + 10,
                                     self.spikesDown.get_width() - 10,
                                     self.spikesDown.get_height())

        spikesUpRect = pygame.Rect(self.wallx,
                                   0 - self.gap - self.offset - 10,
                                   self.spikesUp.get_width() - 10,
                                   self.spikesUp.get_height())

        ##Coin Boundaries
        coinRect = pygame.Rect(self.coinx, self.coiny,
                               self.coin.get_width(), self.coin.get_height())

        ##Meteor Boundaries
        meteorRect = pygame.Rect(self.meteorX, self.meteorY,
                                 14.5, 12.5)

        ##Tube Up
        if tubeUpRect.colliderect(self.cat):
            self.contact.play()
            self.cat_unhappy.play()
            self.dead = True

        ##Tube down
        if tubeDownRect.colliderect(self.cat):
            self.contact.play()
            self.cat_unhappy.play()
            self.dead = True

        ##Spikes up
        if spikesDownRect.colliderect(self.cat):
            self.contact.play()
            self.cat_unhappy.play()
            self.dead = True

        ##Spikes down
        if spikesUpRect.colliderect(self.cat):
            self.cat_unhappy.play()
            self.contact.play()
            self.dead = True

        ##Coin Collision
        if coinRect.colliderect(self.cat):
            self.cat_happy.play()
            self.contact.play()
            self.coinhit.play()
            self.coinDead = True
            self.counter += 1
            pygame.time.delay(15)

        # Meteor Collision
        if meteorRect.colliderect(self.cat):
            self.cat_happy.play()
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

            ##Spikes
            self.screen.blit(self.spikesUp,
                             (self.wallx - self.offset, 615))
            self.screen.blit(self.spikesDown,
                             (self.wallx - self.offset, -5))

            ##Tubes
            self.screen.blit(self.tubeDown,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.tubeUp,
                             (self.wallx, 0 - self.gap - self.offset))

            ##Score
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

            ##Gray out Coin
            if self.coinDead:
                self.coinSprite = 1;

            ##Blits Cat
            self.screen.blit(self.catSprites[self.sprite], (70, self.catY))

            ##Blits Coin
            self.screen.blit(self.coinSprites[self.coinSprite],
                             (self.coinx, self.coiny))

            ##Blits Meteor
            self.screen.blit(self.meteor,
                             (self.meteorX, self.meteorY))

            ##If not dead then update wall accordingly and first sprite
            if not self.dead:
                self.sprite = 0

            if not self.coinDead:
                self.coinSprite = 0

            ##Update obstacles and cat
            self.updateWalls()
            self.updatecoin()
            self.catUpdate()
            self.updateMeteor()
            pygame.display.update()


if __name__ == "__main__":
    Rocket_Cat().main()
