from playsound import playsound
import pygame as pg
import numpy as np
import threading
import math
import time 

class Graph:
	def __init__(self, nVertices: int):
		''' number of vertices of the moving polygon '''
		self.nVertices = nVertices

		self.generate_vertices()

		''' store the initial time value '''
		self.t0 = time.time()

		''' direction of the polygon rotation '''
		self.is_dir_changed = False
		return

	def generate_vertices(self):
		#self.vertices = [Vertex( np.random.random()*WIDTH, np.random.random()*HEIGHT, ORANGE ) for _ in range(self.nVertices)]
		self.vertices = []

		for i in range(self.nVertices):
			''' add an offset of 270 degrees for visual representation '''
			angle = i*(TWO_PI/self.nVertices)+(math.pi*3/2)

			self.vertices.append( Vertex(i, angle, ORANGE) )
		return

	def update(self):
		N = self.nVertices
		[self.vertices[i%N].update() for i in range(N)]

		if time.time()-self.t0>60:
			self.is_dir_changed = True
			self.t0 = time.time()
		return

	def draw_edges(self):
		for i in range(self.nVertices):
			''' store current and next vertices '''
			cur_v = self.vertices[i%self.nVertices]
			next_v = self.vertices[(i+1)%self.nVertices]

			''' change the rotation direction of each vertex '''
			if self.is_dir_changed:
				cur_v.change_dir()

			cur_x, cur_y = cur_v.x, cur_v.y
			next_x, next_y = next_v.x, next_v.y

			''' draw the vertices and edges connecting adjacent vertices '''
			pg.draw.line(WINDOW, ORANGE, (cur_x, cur_y), (next_x, next_y), 3)
			pg.draw.circle(WINDOW, cur_v.color, (cur_x, cur_y), 10)

		self.is_dir_changed = False
		return

class Vertex:
	def __init__(self, index: int, angle: float, color: set):

		''' index of the vertex  '''
		self.index = index 

		''' angle of the vertex with respect to the origin '''
		self.angle = angle

		''' set the vertex to rotate along the clockwise direction '''
		self.rot_dir = 1

		''' search the nearest note from the vertex '''
		self.search_nearest_angle()

		''' pixel coordinates of the vertex '''
		self.x = PIVOT_RADIUS*math.cos(self.angle)+HALF_WIDTH
		self.y = PIVOT_RADIUS*math.sin(self.angle)+HALF_HEIGHT

		''' color of the vertex '''
		self.color = color 

		#self.vx = np.random.random()*np.random.choice([-1,1])
		#self.vy = np.random.random()*np.random.choice([-1,1])
		#self.is_chaotic_period = False

		''' store the initial time value '''
		self.t0 = time.time()

		''' hit parameter '''
		self.is_hit = False
		return

	def search_nearest_angle(self):
		self.nearest_angle = TWO_PI
		self.nearest_key = None

		for i in range(nNote):
			note_angle = (i+1)*TWO_PI/nNote

			diff = note_angle-self.angle

			#if diff<self.nearest_angle and diff>=0.:
			if diff<self.nearest_angle:
				self.nearest_angle = note_angle 
				self.nearest_key = i+4
		return

	def apply_random_force(self):
		self.x += self.vx
		self.y += self.vy

		if self.x>WIDTH or self.x<0:
			self.vx *= -1
		if self.y>HEIGHT or self.y<0:
			self.vy *= -1
		return

	def change_dir(self):
		self.rot_dir *= -1
		self.nearest_angle += self.rot_dir*TWO_PI/nNote
		self.nearest_key += self.rot_dir
		return

	def update(self):
		''' upon hit, keep light on within the duration '''
		if time.time()-self.t0>LIGHT_DURATION and self.is_hit:	
		#	self.is_chaotic_period = not self.is_chaotic_period
		#	self.t0 = time.time()
			self.color = ORANGE 
			self.is_hit = False

		''' update the angle value per frame '''
		self.angle += self.rot_dir*ROT_SPEED*math.pi/180

		''' keep the anglue value between 0 and 2pi '''
		if self.angle>TWO_PI or self.angle<0:
			self.angle -= self.rot_dir*TWO_PI

		#if self.is_chaotic_period:
		#	self.apply_random_force()
		#else:

		''' pixel position of the vertex '''
		self.x = math.cos(self.angle)*PIVOT_RADIUS+HALF_WIDTH
		self.y = math.sin(self.angle)*PIVOT_RADIUS+HALF_HEIGHT

		''' if the distance between the vertex and its nearest note is within the threshold '''
		if abs(self.angle-self.nearest_angle)<HIT_THRESHOLD:

			''' store corresponding note '''
			AUDIO[(self.nearest_key)*KEY_INTERVAL%nNote].play()


			''' update the nearest note in the direction of the polygon rotation '''
			self.nearest_angle += self.rot_dir*TWO_PI/nNote
			self.nearest_key += self.rot_dir 

			''' keep the anglue value between 0 and 2pi '''
			if self.nearest_angle>TWO_PI or self.nearest_angle<0:
				self.nearest_angle -= self.rot_dir*TWO_PI

			''' apply light color to the vertex '''
			self.color = WHITE 

			''' reset the timer of light duration '''
			self.t0 = time.time()

			''' toggle hit parameter '''
			self.is_hit = True
		return

def play_audio(key: pg.mixer.Sound):
	key.play()
	return

def draw_circle(x: float, y: float):
	pg.draw.circle(WINDOW, GREEN, (x, y), 10)
	return

def draw_rect(x: float, y: float):
	pg.draw.rect(WINDOW, ORANGE, (x-WIDTH_RECT/2, y-HEIGHT_RECT/2, WIDTH_RECT, HEIGHT_RECT))
	return

def draw_text(i: int, x: float, y: float):
	ts = font.render(NOTES[i%nNote], False, WHITE)
	WINDOW.blit(ts, (x-WIDTH_RECT/2, y-HEIGHT_RECT/2))
	return

def main():
	''' object to process data and visualization '''
	graph = Graph(nKey)

	is_running = True
	while is_running:
		WINDOW.fill(BLACK)

		for event in pg.event.get():
			if event.type==pg.QUIT:
				is_running = False
				break

		pg.draw.circle(WINDOW, BLUE, (WIDTH/2, HEIGHT/2), PIVOT_RADIUS, 3)

		''' draw fixed notes along a circle '''
		index = 0
		for i in range(nNote):
			angle = i*(TWO_PI/nNote)-(math.pi/2)

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

			index += KEY_INTERVAL 

		''' render the rotating polygon '''
		graph.update()
		graph.draw_edges()

		pg.display.flip()

	pg.quit()
	return

if __name__=="__main__":

	''' window size '''
	WIDTH = 800
	HEIGHT = 800

	HALF_WIDTH = int(WIDTH/2)
	HALF_HEIGHT = int(HEIGHT/2) 

	''' pygame configuration '''
	pg.init()
	pg.mixer.init()
	pg.font.init()
	pg.display.set_caption("Circle of Fifths")

	font = pg.font.Font("lemon.ttf", 30)

	WINDOW = pg.display.set_mode((WIDTH, HEIGHT))

	''' store all 12 notes '''
	NOTES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

	nNote = len(NOTES)

	''' number of vertices of a rotating polygon '''
	nKey = 5

	''' octave range of the notes being played upon hit '''
	OCTAVE = 4

	''' store audio of all notes '''
	AUDIO = [pg.mixer.Sound(f"keys/{note}{OCTAVE}.mp3") for note in NOTES]
	#NOTES = ["C", "D", "Eb", "E", "G", "A"]

	''' key distance between each note '''
	KEY_INTERVAL = 5

	TWO_PI = 2*math.pi

	''' color rgb values '''
	WHITE = (255, 255, 255)
	PINK = (255, 192, 203)
	ORANGE = (255, 140, 0)
	GREEN = (0, 183, 127)
	BLUE = (0, 181, 255)
	PURPLE = (224, 94, 250)
	BLACK = (0, 0, 0)
	
	''' distance of the notes from the origin '''
	PIVOT_RADIUS = 300
	''' distance of the labels from the origin '''
	LABEL_RADIUS = 360

	''' rotation speed of the polygon '''
	ROT_SPEED = 0.03

	''' duration of the light upon hitting a note '''
	LIGHT_DURATION = 0.2

	''' a threshold used to determine a note hit '''
	HIT_THRESHOLD = 0.1

	''' dimensions of the rectangle at each note '''
	WIDTH_RECT = 30
	HEIGHT_RECT = 30

	main()
