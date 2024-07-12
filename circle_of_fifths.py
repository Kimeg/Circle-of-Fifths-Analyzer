import pygame as pg
import numpy as np
import math
import time 

class Graph:
	def __init__(self, nVertices):
		self.nVertices = nVertices
		self.generate_vertices()
		self.t0 = time.time()
		self.is_dir_changed = False
		return

	def generate_vertices(self):
		#self.vertices = [Vertex( np.random.random()*WIDTH, np.random.random()*HEIGHT, ORANGE ) for _ in range(self.nVertices)]
		self.vertices = []

		for i in range(self.nVertices):
			angle = (i*(360/self.nVertices)-90)*math.pi/180

			self.vertices.append(Vertex(i, angle, ORANGE))
		return

	def update(self):
		N = self.nVertices
		[self.vertices[i%N].update(self.vertices[(i+1)%N]) for i in range(N)]

		if time.time()-self.t0>3:
			self.is_dir_changed = True
			self.t0 = time.time()
		return

	def draw_edges(self):
		for i in range(self.nVertices):
			cur_v = self.vertices[i%self.nVertices]
			next_v = self.vertices[(i+1)%self.nVertices]

			#if self.is_dir_changed:
			#	cur_v.rot_dir *= -1

			cur_x, cur_y = cur_v.x, cur_v.y
			next_x, next_y = next_v.x, next_v.y

			pg.draw.line(WINDOW, ORANGE, (cur_x, cur_y), (next_x, next_y), 3)
			pg.draw.circle(WINDOW, cur_v.color, (cur_x, cur_y), 10)

		self.is_dir_changed = False
		return

class Vertex:
	def __init__(self, index, angle, color):
		self.index = index 
		self.angle = angle
		self.rot_dir = 1
		self.search_nearest_angle()

		self.x = PIVOT_RADIUS*math.cos(self.angle)+HALF_WIDTH
		self.y = PIVOT_RADIUS*math.sin(self.angle)+HALF_HEIGHT

		self.color = color 

		#self.vx = np.random.random()*np.random.choice([-1,1])
		#self.vy = np.random.random()*np.random.choice([-1,1])
		#self.is_chaotic_period = False
		self.t0 = time.time()
		self.is_hit = False
		return

	def search_nearest_angle(self):
		self.nearest_angle = TWO_PI
		for i in range(nNote):
			note_angle = (i+1)*TWO_PI/nNote

			diff = note_angle-self.angle

			#if diff<self.nearest_angle and diff>=0.:
			if diff<self.nearest_angle:
				self.nearest_angle = note_angle 
		return

	def apply_random_force(self):
		self.x += self.vx
		self.y += self.vy

		if self.x>WIDTH or self.x<0:
			self.vx *= -1
		if self.y>HEIGHT or self.y<0:
			self.vy *= -1
		return

	def update(self, next_v):

		if time.time()-self.t0>0.2 and self.is_hit:	
		#	self.is_chaotic_period = not self.is_chaotic_period
		#	self.t0 = time.time()
			self.color = ORANGE 
			self.is_hit = False

		self.angle += self.rot_dir*0.03*math.pi/180

		if self.angle>TWO_PI or self.angle<0:
			self.angle -= self.rot_dir*TWO_PI

		#if self.is_chaotic_period:
		#	self.apply_random_force()
		#else:
		self.x = math.cos(self.angle)*PIVOT_RADIUS+HALF_WIDTH
		self.y = math.sin(self.angle)*PIVOT_RADIUS+HALF_HEIGHT

		if abs(self.angle-self.nearest_angle)<0.1:
			print(self.index, 'ok')

			self.nearest_angle += self.rot_dir*TWO_PI/nNote

			if self.nearest_angle>TWO_PI or self.nearest_angle<0:
				self.nearest_angle -= self.rot_dir*TWO_PI

			self.color = WHITE 
			self.t0 = time.time()
			self.is_hit = True
		return

def draw_pyplot():
	import matplotlib.pyplot as plt

	X = []
	Y = []

	fig = plt.figure(figsize=(8,8))
	for i in range(nNote):
		angle = i*(360/nNote)+90
		x = RADIUS*math.cos(angle*math.pi/180) 
		y = RADIUS*math.sin(angle*math.pi/180) 

		X.append(x)
		Y.append(y)

		#print(x,y)

	plt.scatter(X,Y)
	plt.plot(X,Y)
	plt.grid()
	plt.show()
	return

def draw_circle(x, y):
	pg.draw.circle(WINDOW, GREEN, (x, y), 10)
	return

def draw_rect(x, y):
	pg.draw.rect(WINDOW, ORANGE, (x-WIDTH_RECT/2, y-HEIGHT_RECT/2, WIDTH_RECT, HEIGHT_RECT))
	return

def draw_text(i, x, y):
	ts = font.render(NOTES[i%nNote], False, WHITE)
	WINDOW.blit(ts, (x-WIDTH_RECT/2, y-HEIGHT_RECT/2))
	return

def main():
	#draw_pyplot()
	nKey = 5
	graph = Graph(nKey)

	is_running = True
	while is_running:
		WINDOW.fill(BLACK)

		for event in pg.event.get():
			if event.type==pg.QUIT:
				is_running = False
				break

		pg.draw.circle(WINDOW, BLUE, (WIDTH/2, HEIGHT/2), PIVOT_RADIUS, 3)
		index = 0
		for i in range(nNote):
			angle = (i*(360/nNote)-90)*math.pi/180

			cos_angle = math.cos(angle)
			sin_angle = math.sin(angle)

			px = PIVOT_RADIUS*cos_angle+(HALF_WIDTH)
			py = PIVOT_RADIUS*sin_angle+(HALF_HEIGHT)

			lx = LABEL_RADIUS*cos_angle+(HALF_WIDTH)
			ly = LABEL_RADIUS*sin_angle+(HALF_HEIGHT)

			#print(x, y)
			#draw_rect(px, py)
			draw_circle(px, py)
			draw_text(index, lx, ly)

			index += 5

		graph.update()
		graph.draw_edges()

		pg.display.flip()

	pg.quit()
	return

if __name__=="__main__":
	NOTES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
	#NOTES = ["C", "D", "E", "F", "G", "A", "B"]

	nNote = len(NOTES)

	WHITE = (255, 255, 255)
	PINK = (255, 192, 203)
	ORANGE = (255, 140, 0)
	GREEN = (0, 183, 127)
	BLUE = (0, 181, 255)
	PURPLE = (224, 94, 250)
	BLACK = (0, 0, 0)

	WIDTH = 800
	HEIGHT = 800

	HALF_WIDTH = int(WIDTH/2)
	HALF_HEIGHT = int(HEIGHT/2) 

	PIVOT_RADIUS = 300
	LABEL_RADIUS = 360

	WIDTH_RECT = 30
	HEIGHT_RECT = 30

	TWO_PI = 2*math.pi

	pg.init()
	pg.font.init()
	WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Circle of Fifths")

	font = pg.font.Font("lemon.ttf", 30)
	main()
