import math
import random
import time
import pygame
import sys
from pygame.locals import *
import copy


bg = (20, 20, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
colors = (white, red, blue, green)
ww = 400
wh = 800

jugadores = ['Sebastian', 'Chino']

fric = 0.95

class ball:
	def __init__(self, surf, name="Sebastian", color=(255, 255, 255), pos=[0, 0], vel=[0, 0]):
		self.surf = surf
		self.pos = pos
		self.vel = vel
		self.acc = [0, 10]
		self.color = color
		self.name = name
		self.radius = 7

	def update(self, limit):
		self.vel[0] += int(self.acc[0] / 4)
		self.vel[1] += int(self.acc[1] / 4)
		self.pos[0] += int( - 0.5 + self.vel[0] / 4)
		self.pos[1] += int( - 0.5 + self.vel[1] / 4)

		if (self.pos[1] < 0 or self.pos[1] > limit[1]):
			self.pos[1] = 0 if self.pos[1] < 0 else limit[1]
			self.vel[0] = self.vel[0] * fric
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
		textpos = (self.pos[0], self.pos[1] - 20)
		self.surf.blit(textsurface, textpos)
		pygame.draw.circle(self.surf, self.color, tuple(self.pos), self.radius)

	def __call__(self):
		self.__init__()


class obstacle:
	def __init__(self, surf, color, coord1, coord2):
		self.coord1 = coord1
		self.coord2 = coord2
		self.surf = surf
		self.color = color
		self.width = 2
		self.norm = []

	def draw(self):
		pygame.draw.line(self.surf, self.color, tuple(self.coord1), tuple(self.coord2), self.width)

	def getNorm(self):
		mod = math.sqrt((self.coord1[0] - self.coord2[0])**2 + (self.coord1[1] - self.coord2[1])**2) 
		difx = (self.coord2[0] - self.coord1[0])
		dify = (self.coord2[1] - self.coord1[1])
		try:
			self.norm = [-dify/mod, difx/mod]
		except ZeroDivisionError:
			self.norm = [0,0]


class board:
	def __init__(self, size, color):
		self.gameMode = "menu"
		self.players = []
		self.temp = []
		self.obstacles = []
		self.ww = size[0]
		self.wh = size[1]
		self.surf = pygame.display.set_mode((self.ww, self.wh))
		self.bg = color
		self.surf.fill(color)
		self.drawState = "idle"
		self.tempClick = []
		self.textedit = False
		self.text = ''
		pygame.mouse.set_visible(1)

	def addPlayer(self, name="Sebastian", color=(255, 255, 255), pos=[0, 0], vel=[0, 0]):
		player = ball(self.surf, name, color, pos, vel)
		self.players.append(player)
		player2 = copy.copy(player)
		return player2

	def addObstacle(self, color, coord1, coord2):
		obs = obstacle(self.surf, color, coord1, coord2)
		self.obstacles.append(obs)

	def draw(self):
		for marble in self.players:
			marble.draw()
		for obstacle in self.obstacles:
			obstacle.draw()

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
		p1.vel[0] = XSpeed * fric
		p1.vel[1] = YSpeed * fric

	def resolveObs(self, player, obs):
		obs.getNorm()
		intermedio = [ i * 2 * (obs.norm[0]*player.vel[0] + obs.norm[1]*player.vel[1]) for i in obs.norm ]
		player.vel = [player.vel[0] - intermedio[0], player.vel[1] - intermedio[1]]
		player.vel = [fric * i for i in player.vel]

	def selfDot(self, item):
		return  reduce((lambda x, y: x + y), [i*i for i in item])

	def checkColl(self):
		for player1 in self.players:
			for player2 in self.players:
				if player1 != player2:
					if math.sqrt(((player1.pos[0]-player2.pos[0])**2)  +  ((player1.pos[1]-player2.pos[1])**2)  ) <= (player1.radius+player2.radius):
						self.resolveColl(player1,player2)

		for player in self.players:
			for obstacle in self.obstacles:
				v = [obstacle.coord2[0] - obstacle.coord1[0], obstacle.coord2[1] - obstacle.coord1[1]]
				a = self.selfDot(v)
				dum = [obstacle.coord1[0] - player.pos[0], obstacle.coord1[1] - player.pos[1]]
				b = 2 * (v[0]*dum[0] + v[1]*dum[1])
				c = self.selfDot(obstacle.coord1) + self.selfDot(player.pos) - 2 * (obstacle.coord1[0] * player.pos[0] + obstacle.coord1[1] * player.pos[1])  - ( player.radius + obstacle.width)**2
				disc = b**2 - 4 * a * c
				maxx = max(obstacle.coord1[0], obstacle.coord2[0])
				minx = min(obstacle.coord1[0], obstacle.coord2[0])
				maxy = max(obstacle.coord1[1], obstacle.coord2[1])
				miny = min(obstacle.coord1[1], obstacle.coord2[1])
				if(disc > 0 and player.pos[0] > minx-15 and player.pos[1] > miny-15 and player.pos[0] < maxx+15 and player.pos[1] < maxy+15 ):
					# self.players[0].color = red
					self.resolveObs(player, obstacle)

	def update(self):
		self.surf.fill(self.bg)
		for player in self.players:
			player.update((self.ww, self.wh))



pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
myfont2 = pygame.font.SysFont('Comic Sans MS', 40)
myfont3 = pygame.font.SysFont('Comic Sans MS', 25)
a = board((ww, wh), bg)

	

# a.addPlayer("Player " + str(2), white, [100, 0], [10, 0])


input_box = pygame.Rect(100, 300, 140, 32)
input_box.center = (a.surf.get_width()/2, 300)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive


done = False


def checkQuit():
	keystate = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT or keystate[K_ESCAPE]:
			pygame.quit(); sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if input_box.collidepoint(event.pos):
				a.textedit = True
			else:
				a.textedit = False
		elif event.type == pygame.KEYDOWN:
			if a.textedit:
				if event.key == pygame.K_RETURN:
					pos = [random.randint(20,400), 20]
					vel = [random.randint(-5,5), random.randint(-5,5)]
					pl = a.addPlayer(a.text, random.choice(colors), pos , vel )
					pos2 = copy.deepcopy(pos)
					vel2 = copy.deepcopy(vel)
					a.temp.append((pos2,vel2))
					a.text = ''
				elif event.key == pygame.K_BACKSPACE:
					a.text = a.text[:-1]
				else:
					a.text += event.unicode
					
			else:
				if event.key == pygame.K_e:
					a.gameMode = "edit"	
				if event.key == pygame.K_p:
					a.gameMode = "play"
				if event.key == pygame.K_m:
					a.gameMode = "menu"		
				if event.key == pygame.K_r:
					a.gameMode = "reset"	

i = 0
while(1):
	i += 1
	checkQuit()
	if a.gameMode == "menu":
		a.surf.fill(bg)
		textsurface = myfont2.render("LAS BOLITAS xd", False, (255, 255, 255))
		text_rect = textsurface.get_rect()
		text_rect.center = (a.surf.get_width()/2, 48)
		a.surf.blit(textsurface, text_rect)
		textsurface = myfont3.render("E para editar", False, (255, 255, 255))
		text_rect = textsurface.get_rect()
		text_rect.center = (a.surf.get_width()/2, 88)
		a.surf.blit(textsurface, text_rect)
		textsurface = myfont3.render("P para jugar", False, (255, 255, 255))
		text_rect = textsurface.get_rect()
		text_rect.center = (a.surf.get_width()/2, 118)
		a.surf.blit(textsurface, text_rect)

		for i, player in enumerate(a.players):
			textsurface = myfont3.render(player.name, False, (255, 255, 255))
			text_rect = textsurface.get_rect()
			text_rect.center = (a.surf.get_width()/2, 400 + i*40)
			a.surf.blit(textsurface, text_rect)
		txt_surface = myfont3.render(a.text, True, color)
		width = max(200, txt_surface.get_width()+10)
		a.surf.blit(txt_surface, (input_box.x+5, input_box.y+5))
		pygame.draw.rect(a.surf, color, input_box, 2)

	elif a.gameMode == "play":	
		a.update()
		a.draw()
		a.checkColl()
	elif a.gameMode == "reset":
		for i, player in enumerate(a.players):
			player.pos = copy.deepcopy(a.temp[i][0])
			player.vel = copy.deepcopy(a.temp[i][1])
		a.gameMode = "play"
	elif a.gameMode == "edit":
		a.surf.fill(bg)
		left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
		if a.drawState == "idle":
			if left_pressed:
				a.tempClick = list(pygame.mouse.get_pos())
				a.drawState = "clicked"
				i = 0
		if a.drawState == "clicked":
			if i == 10:
				i = 0
				if left_pressed:
					if (a.tempClick[0]!=pygame.mouse.get_pos()[0] or a.tempClick[1]!=pygame.mouse.get_pos()[1]):
						if math.sqrt(( a.tempClick[0] - pygame.mouse.get_pos()[0]) ** 2 + ( a.tempClick[1] - pygame.mouse.get_pos()[1]) ** 2 ) > 2:
							a.addObstacle(white, tuple(a.tempClick), pygame.mouse.get_pos() )
							# a.addObstacle(white, (a.tempClick[0] +1, a.tempClick[1], ), (pygame.mouse.get_pos()[0] +1, pygame.mouse.get_pos()[1]) )
							# a.addObstacle(white, (a.tempClick[0] , a.tempClick[1] + 1, ), (pygame.mouse.get_pos()[0] , pygame.mouse.get_pos(1)[1] +1) )
							a.tempClick = list(pygame.mouse.get_pos())
							print(len(a.obstacles))
				else:
					a.drawState = "idle"
		a.draw()

	pygame.display.update()
	pygame.time.wait(20)



pygame.quit()

