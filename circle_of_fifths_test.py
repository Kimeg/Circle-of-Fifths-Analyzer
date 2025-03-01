import pygame as pg
import numpy as np
import math

class Graph:
	def __init__(self, nVertices):
		self.nVertices = nVertices
		self.generate_vertices()
		return

	def generate_vertices(self):
		#self.vertices = [Vertex( np.random.random()*WIDTH, np.random.random()*HEIGHT, ORANGE ) for _ in range(self.nVertices)]
		self.vertices = []

		for i in range(self.nVertices):
			angle = (i*(360/self.nVertices)-90)*math.pi/180

			self.vertices.append(Vertex(i, angle, ORANGE, self.nVertices))
		return

	def update(self):
		N = self.nVertices
		[self.vertices[i%N].update(self.vertices[(i+1)%N]) for i in range(N)]
		return

	def draw_pivot_edges(self):
		for i in range(self.nVertices):
			cur_v = self.vertices[i%self.nVertices]
			next_v = self.vertices[(i+1)%self.nVertices]

			cur_x, cur_y = cur_v.pivot_x, cur_v.pivot_y
			next_x, next_y = next_v.pivot_x, next_v.pivot_y

			pg.draw.line(WINDOW, PURPLE, (cur_x, cur_y), (next_x, next_y), 3)
		return

	def draw_moving_edges(self):
		for i in range(self.nVertices):
			cur_v = self.vertices[i%self.nVertices]
			next_v = self.vertices[(i+1)%self.nVertices]

			cur_x, cur_y = cur_v.xi, cur_v.yi
			next_x, next_y = next_v.xi, next_v.yi

			pg.draw.line(WINDOW, ORANGE, (cur_x, cur_y), (next_x, next_y), 3)
			pg.draw.circle(WINDOW, GREEN, (cur_x, cur_y), 10)
		return

class Vertex:
	def __init__(self, index, angle, color, nVertices):
		self.index = index 
		self.angle = angle
		self.moving_angle = angle
		self.nVertices = nVertices 

		cos_angle = math.cos(self.angle)
		sin_angle = math.sin(self.angle)

		x = PIVOT_RADIUS*cos_angle+HALF_WIDTH
		y = PIVOT_RADIUS*sin_angle+HALF_HEIGHT

		self.x = x
		self.y = y

		self.pivot_x = x
		self.pivot_y = y

		self.next_angle = self.angle + (360/self.nVertices)*math.pi/180
		self.color = color 

		self.center = [HALF_WIDTH, HALF_HEIGHT]

		self.reached_next_vertex = False
		#self.vx = np.random.random()*0.01
		#self.vy = np.random.random()*0.01
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
		self.moving_angle += 0.02*math.pi/180
		self.v = [math.cos(self.moving_angle)*PIVOT_RADIUS+self.center[0], math.sin(self.moving_angle)*PIVOT_RADIUS+self.center[1]]

		x1, x2, x3, x4 = self.center[0], self.v[0], self.x, next_v.x
		y1, y2, y3, y4 = self.center[1], self.v[1], self.y, next_v.y

		#pg.draw.line(WINDOW, GREEN, (x1, y1), (x2, y2))
		pg.draw.line(WINDOW, WHITE, (x3, y3), (x4, y4))

		try:
			self.xi = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
			self.yi = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))	
		except Exception as e:
			return

		if abs(self.moving_angle-self.next_angle)<0.01:
			print(self.index, 'ok')
			self.angle += (360/self.nVertices)*math.pi/180
			self.next_angle = self.angle + (360/self.nVertices)*math.pi/180
			self.moving_angle = self.angle

			self.x = PIVOT_RADIUS*math.cos(self.angle)+HALF_WIDTH
			self.y = PIVOT_RADIUS*math.sin(self.angle)+HALF_HEIGHT
		return

def draw_pyplot():
	import matplotlib.pyplot as plt

	X = []
	Y = []

	fig = plt.figure(figsize=(8,8))
	for i in range(len(NOTES)):
		angle = i*(360/len(NOTES))+90
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
	ts = font.render(NOTES[i%len(NOTES)], False, WHITE)
	WINDOW.blit(ts, (x-WIDTH_RECT/2, y-HEIGHT_RECT/2))
	return

def main():
	#draw_pyplot()
	nKey = 4 
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
		for i in range(len(NOTES)):
			angle = (i*(360/len(NOTES))-90)*math.pi/180

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
		graph.draw_pivot_edges()
		graph.draw_moving_edges()

		pg.display.flip()

	pg.quit()
	return

if __name__=="__main__":
	NOTES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
	#NOTES = ["C", "D", "E", "F", "G", "A", "B"]
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

	pg.init()
	pg.font.init()
	WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption("Circle of Fifths")

	font = pg.font.Font("lemon.ttf", 30)
	main()
