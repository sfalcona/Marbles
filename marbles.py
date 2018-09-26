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
		self.radius = 6

	def update(self, limit):
		self.vel[0] += int(self.acc[0] / 4)
		self.vel[1] += int(self.acc[1] / 4)
		self.pos[0] += int(self.vel[0] / 4)
		self.pos[1] += int(self.vel[1] / 4)

		if (self.pos[1] < 0 or self.pos[1] > limit[1]):
			self.pos[1] = 0 if self.pos[1] < 0 else limit[1]
			self.vel[0] = self.vel[0] * 0.8
			self.vel[1] = -self.vel[1] / 2
		if (self.pos[0] < 0 or self.pos[0] > limit[0]):
			self.pos[0] = 0 if self.pos[0] < 0 else limit[0]
			self.vel[0] = -self.vel[0] / 2

	def debug(self):
		textsurface = myfont.render(str(self.pos[0]), False, (255, 255, 255))
		self.surf.blit(textsurface, (0, 0))
		textsurface = myfont.render(str(self.vel[0]), False, (255, 255, 255))
		self.surf.blit(textsurface, (0, 20))
		textsurface = myfont.render(str(self.pos[1]), False, (255, 255, 255))
		self.surf.blit(textsurface, (50, 0))
		textsurface = myfont.render(str(self.vel[1]), False, (255, 255, 255))
		self.surf.blit(textsurface, (50, 20))

	def draw(self):
		textsurface = myfont.render(self.name, False, (255, 255, 255))
		self.surf.blit(textsurface, tuple(self.pos))
		pygame.draw.circle(self.surf, self.color, tuple(self.pos), self.radius)

	def __call__(self):
		self.__init__()


class obstacle:
	def __init(self, coord):
		self.coord = coord


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

	def resolveColl(self, p1, p2):
		p1Speed = math.sqrt((p1.vel[0]**2) + (p1.vel[1]**2))
		XDiff = -(p1.pos[0] - p2.pos[0])
		YDiff = -(p1.pos[1] - p2.pos[1])
		if XDiff > 0:
			if YDiff >= 0:
				Angle = math.degrees(math.atan(YDiff/XDiff))
				XSpeed = -p1Speed*math.cos(math.radians(Angle))
				YSpeed = -p1Speed*math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = math.degrees(math.atan(YDiff/XDiff))
				XSpeed = -p1Speed*math.cos(math.radians(Angle))
				YSpeed = -p1Speed*math.sin(math.radians(Angle))
		elif XDiff < 0:
			if YDiff >= 0:
				Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
				XSpeed = -p1Speed*math.cos(math.radians(Angle))
				YSpeed = -p1Speed*math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
				XSpeed = -p1Speed*math.cos(math.radians(Angle))
				YSpeed = -p1Speed*math.sin(math.radians(Angle))
		elif XDiff == 0:
			if YDiff >= 0:
				Angle = -90
			else:
				Angle = 90
			XSpeed = p1Speed*math.cos(math.radians(Angle))
			YSpeed = p1Speed*math.sin(math.radians(Angle))
		elif YDiff == 0:
			if XDiff < 0:
				Angle = 0
			else:
				Angle = 180
			XSpeed = p1Speed*math.cos(math.radians(Angle))
			YSpeed = p1Speed*math.sin(math.radians(Angle))
		p1.vel[0] = XSpeed * 0.8
		p1.vel[1] = YSpeed * 0.8

	
	def checkColl(self):
		for player1 in self.players:
			for player2 in self.players:
				if player1 != player2:
					if math.sqrt(((player1.pos[0]-player2.pos[0])**2)  +  ((player1.pos[1]-player2.pos[1])**2)  ) <= (player1.radius+player2.radius):
						self.resolveColl(player1,player2)


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
colors = (black, white, red, blue, green)
ww = 800
wh = 600


a = board((ww, wh), bg)
for i in range(10):
	a.addPlayer("Player " + str(i), random.choice(colors), [random.randint(0,ww), random.randint(0,wh)], [random.randint(-100,100), random.randint(-100,100)])

# a.addPlayer("Player " + str(1), white, [300, 0],  [-10, 0])
# a.addPlayer("Player " + str(2), white, [100, 0], [10, 0])
i = 150
while(i):
	a.update()
	a.draw()
	a.checkColl()
	pygame.display.update()
	pygame.time.delay(20)
	i -= 1


pygame.quit()


#
