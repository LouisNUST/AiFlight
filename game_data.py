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
	acceleration = 10.0
	max_speed = 500.0
	min_speed = 100.0
	max_turn_speed = 45.0
	collision_radius = 8.0
	magazine_size = 300
	missile_fire_rate = 0.5 #Missiles per second
	fire_rate = 10.0 #Shots per second
	bullet_reload_time = 2.0
	def __init__(self, identity, x, y, angle):
		self.health = 100.0
		self.speed = 250.0
		self.missiles = 8
		self.bullet_ammo = 300
		self.magazine_size = 300
		self.fire_iteration_count = 0
		self.missile_iteration_count = 0
		self.reload_iteration_count = 0
		self.identity = identity
		self.x = float(x)
		self.y = float(y)
		self.angle = float(angle)
		self.alive = True

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
	damage = 60.0
	speed = 750.0
	lifespan = 6.0
	max_turn_speed = 25.0

	def __init__(self, owner, x, y, angle, enemy):
		self.owner = owner
		self.x = float(x)
		self.y = float(y)
		self.angle = float(angle)
		self.enemy = enemy
		self.age = 0

	def turn(self, deg, dt):
		#deg = degrees per second
		if abs(deg) > self.max_turn_speed:
			deg = self.max_turn_speed
		self.angle = self.angle + deg * dt
		if self.angle >= 360:
			self.angle = self.angle - 360 

	def move(self, dt):
		self.age = self.age+1
		#dt is the change in time and it is in seconds
		self.x = self.x + math.cos(math.radians(self.angle)) * self.speed*dt
		self.y = self.y + math.sin(math.radians(self.angle)) * self.speed*dt


		if self.enemy != None:
			xenem = self.enemy.x
			yenem = self.enemy.y

			a = self.angle

			x_next = self.x + math.cos(math.radians(a)) * 100.0
			y_next = self.y + math.sin(math.radians(a)) * 100.0
			dist = calculate_distance_points(xenem, yenem, x_next, y_next)

			x_pos = self.x + math.cos(math.radians(a + 45.0/100.0)) * 100
			y_pos = self.y + math.sin(math.radians(a + 45.0/100.0)) * 100
			dist_pos = calculate_distance_points(xenem, yenem, x_pos, y_pos)

			x_neg = self.x + math.cos(math.radians(a - 45.0/100.0)) * 100
			y_neg = self.y + math.sin(math.radians(a - 45.0/100.0)) * 100
			dist_neg = calculate_distance_points(xenem, yenem, x_neg, y_neg)

			if dist_pos < dist:
				self.turn(self.max_turn_speed, dt)
			elif dist_neg < dist:
				self.turn(self.max_turn_speed * -1.0 , dt)


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


def check_hit(missile_or_bullet, player):
	if (calculate_distance_entities(missile_or_bullet,player) < player.collision_radius) & (missile_or_bullet.owner != player.identity):
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