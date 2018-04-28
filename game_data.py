#Author: John Marrs
import pickle
import math
import time
class GameData:
	#Define variables for game

	#Size from origin until edge of map
	x_size = 10000
	y_size = 10000

	def __init__(self):
		self.players = []
		self.missiles = []
		self.bullets = []


	#Define methods for working with game variables
class Player:


	def __init__(self, identity, x, y, angle):
		self.acceleration = 10.0
		self.health = 100.0
		self.speed = 250.0
		self.max_speed = 500.0
		self.min_speed = 100.0
		self.max_turn_speed = 45.0
		self.collision_radius = 8.0
		self.missiles = 8
		self.bullet_ammo = 300
		self.magazine_size = 300
		self.fire_iteration_count = 0
		self.fire_rate = 20.0 # SHOTS PER SECOND
		self.reloat_iteration_count = 0
		self.bullet_reload_time = 2.0 #Seconds to reload
		self.locks_on_enemy = []
		self.locks_on_player = []
		self.identity = identity
		self.x = float(x)
		self.y = float(y)
		self.angle = float(angle)

	def turn(self, deg, dt):
		#deg = degrees per second
		if abs(deg) > self.max_turn_speed:
			deg = deg/abs(deg) * self.max_turn_speed
		self.angle = self.angle + deg * dt
		if self.angle >= 360:
			self.angle = self.angle - 360 


	def move(self, dt):
		#dt is the change in time and it is in seconds
		self.x = self.x + math.cos(math.radians(self.angle)) * self.speed*dt
		self.y = self.y + math.sin(math.radians(self.angle)) * self.speed*dt

	def reload(self, dt):
		self.bullet_ammo = self.magazine_size
		self.reloat_iteration_count = 0


class Missile:
	speed = float(600)
	damage = float(60)
	lifespan = float(6)
	max_turn_speed = float(10)

	def __init__(self, owner, x, y, angle, lock):
		self.owner = owner
		self.x = float(x)
		self.y = float(y)
		self.angle = float(angle)
		self.lock = lock
		self.age = 0

	def turn(self, deg, dt):
		#deg = degrees per second
		if abs(deg) > self.max_turn_speed:
			deg = self.max_turn_speed
		self.angle = self.angle + deg * dt
		if self.angle >= 360:
			self.angle = self.angle - 360 

	def move(self, dt):
		#dt is the change in time and it is in seconds
		self.x = self.x + math.cos(math.radians(self.angle)) * self.speed*dt
		self.y = self.y + math.sin(math.radians(self.angle)) * self.speed*dt

class Bullet:
	owner = None
	x = float(0)
	y = float(0)
	angle = float(0)
	speed = float(1000)
	lifespan = float(3)
	possible_shot_offset = float(2) #Degrees to which the shot could be off from the owner's firing angle
	def __init__(self, owner, x, y, angle):
		self.owner = owner
		self.x = float(x)
		self.y = float(y)
		self.angle = float(angle)
		self.age = 0
		self.damage = 1

	def move(self, dt):
		#dt is the change in time and it is in seconds
		self.x = self.x + math.cos(math.radians(self.angle)) * self.speed*dt
		self.y = self.y + math.sin(math.radians(self.angle)) * self.speed*dt
		self.age = self.age + 1

class Lock:
	owner = None
	target = None
	def __init__(self, owner, target):
		self.owner = owner
		self.target = target


def check_hit(missle_or_bullet, player):
	if calculate_distance_entities(missle_or_bullet,player) < player.collision_radius:
		return True
	else:
		return False


def calculate_distance_entities(entity1,entity2):
	dy = entity2.y - entity1.y
	dx = entity2.x - entity1.x

	return math.hypot(dx,dy)

def calculate_distance_points(x1,y1,x2,y2):
	dy = y2 - y1
	dx = x2 - x1

	return math.hypot(dx,dy)

def distance_between_point_and_line(lx1, ly1, lx2, ly2, x_point, y_point):
	lx1 = float(lx1)
	ly1 = float(ly1)
	lx2 = float(lx2)
	ly2 = float(ly2)
	x_point = float(x_point)
	y_point = float(y_point)
	#Line is given by a set of two points
	if (lx1 == lx2) and (ly1 == ly2):
		return 0

	numerator = abs((ly2-ly1)*x_point-(lx2-lx1)*y_point+lx2*ly1-ly2*lx1)
	denom = math.sqrt(math.pow((ly2-ly1),2)+math.pow((lx2-lx1), 2))
	result = numerator/denom
	return result