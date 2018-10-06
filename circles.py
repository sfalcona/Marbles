import pygame
import math

circles = 20

white = (255, 255, 255)
gray = (100, 100, 100)
black = (0, 0, 0)
ww = 1920	
wh = 1080
angle = 0

pygame.init()
display =  pygame.display.set_mode((ww, wh), pygame.FULLSCREEN)
display.fill((0, 0, 0))
pygame.mouse.set_visible(1)
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()


radius = ww // (2*(circles	+ 1))
circlesy = wh//(2*radius) 


class curve():
	def __init__(self):
		self.points = []

	def __call__(self):
		self.__init__()

	def addPoint(self, point):
		self.points.append(point)

	def drawPoints(self):
		for el in self.points:
			pygame.draw.circle(display, white, el, 1 )

	def clearPoints(self):
		self.points = []

def drawCircles():
	display.fill(black)
	for i in range(2, circlesy + 1):
		pygame.draw.circle(display,	white, (radius, i*2*radius - radius), int(0.8*radius))
		pygame.draw.circle(display,	black, (radius, i*2*radius - radius), int(0.8*radius*0.98))

	for i in range(2,circlesy + 1):
		pygame.draw.circle(display,	white, (i*2*radius - radius, radius), int(0.8*radius))
		pygame.draw.circle(display,	black, (i*2*radius - radius, radius), int(0.8*radius*0.98))

def nextFrame(angle):
	for i in range(2, circlesy + 1):
		offsetx = int(radius*0.8*math.cos(i*angle))
		offsety = int(radius*0.8*math.sin(i*angle))

		pygame.draw.circle(display,	white, (radius + offsetx, i*2*radius - radius + offsety), int(radius*0.07))
		pygame.draw.circle(display,	white, (i*2*radius - radius + offsetx, radius + offsety), int(radius*0.07))

		pygame.draw.line(display, gray, (0, i*2*radius - radius + offsety), (ww, i*2*radius - radius + offsety))
		pygame.draw.line(display, gray, (i*2*radius - radius + offsetx, 0), (i*2*radius - radius + offsetx, wh))
	
	for i in range(2, circlesy + 1):	
		for j in range(2, circlesy + 1):
			offsetx = int(radius*0.8*math.cos(i*angle))
			offsety = int(radius*0.8*math.sin(j*angle))
			curves[i-1].addPoint((i*2*radius - radius + offsetx, j*2*radius - radius + offsety))


draw = True
curves = []
for i in range(2*circlesy):
	a = curve()
	curves.append(a)


while(draw):
	try:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_x:
					draw = False
		angle -= 0.01
		if angle < -2*math.pi:
			for drawing in curves:
				drawing.clearPoints()
			angle = 0
		drawCircles()
		nextFrame(angle)
		for el in curves:
			el.drawPoints()

		fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
		display.blit(fps, (50, 50))
		clock.tick(30)
		pygame.display.update()
		pygame.time.wait(1)		
				
	except SystemExit:
		pygame.quit()

pygame.quit()