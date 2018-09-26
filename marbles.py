import math
import random
import time
import pygame
from pygame.locals import *


class ball:
    def __init__(self, surf, name="Sebastian", color=(255, 255, 255), pos=[0, 0], vel=[0, 0]):
        self.surf = surf
        self.pos = pos
        self.vel = vel
        self.acc = [0, 10]
        self.color = color
        self.name = name

    def update(self, limit):
        self.vel[0] += int(self.acc[0] / 4)
        self.vel[1] += int(self.acc[1] / 4)
        self.pos[0] += int(self.vel[0] / 4)
        self.pos[1] += int(self.vel[1] / 4)

        if (self.pos[1] < 0 or self.pos[1] > limit[1]):
            self.pos[1] = 0 if self.pos[1] < 0 else limit[1]
            self.vel[0] = self.vel[0]  * 0.8
            self.vel[1] = -self.vel[1] / 2
        if (self.pos[0] < 0 or self.pos[0] > limit[0]):
            self.vel[0] = -self.vel[0] / 2

    def debug(self):
    	textsurface = myfont.render(str(self.pos[0]), False, (255, 255, 255))
        self.surf.blit(textsurface,(0,0))
        textsurface = myfont.render(str(self.vel[0]), False, (255, 255, 255))
        self.surf.blit(textsurface,(0,20))
        textsurface = myfont.render(str(self.pos[1]), False, (255, 255, 255))
        self.surf.blit(textsurface,(50,0))
        textsurface = myfont.render(str(self.vel[1]), False, (255, 255, 255))
        self.surf.blit(textsurface,(50,20))

    def draw(self):
    	self.debug()
        pygame.draw.circle(self.surf, self.color, tuple(self.pos), 6)

    def __call__(self):
        self.__init__()


class board:
    def __init__(self, size, color):
        self.players = []
        self.ww = size[0]
        self.wh = size[1]
        self.surf = pygame.display.set_mode((self.ww, self.wh))
        self.bg = color
        self.surf.fill(color)
        pygame.mouse.set_visible(0)

    def addPlayer(self, name="Sebastian", color=(255, 255, 255), pos=[0, 0], vel=[0, 0]):
        player = ball(self.surf, name, color, pos, vel)
        self.players.append(player)

    def draw(self):
        for marble in self.players:
            marble.draw()
        pygame.display.update()

    def update(self):
        self.surf.fill(self.bg)
        for player in self.players:
            player.update((self.ww, self.wh))


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

bg = (20, 20, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
ww = 800
wh = 600


a = board((ww, wh), bg)
a.addPlayer("Sebastian", white, [ww // 2, 1], [20, 110])

i = 150
while(i):
    a.update()
    a.draw()
    pygame.display.update()
    pygame.time.wait(20)
    i -= 1


pygame.quit()


#
