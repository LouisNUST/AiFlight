#Author: John Marrs
class ServerMessage:
	
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.angle = 0.0
		self.can_shoot = False
		self.can_shoot_missile = False
		self.ammo = 300
		self.missiles = 8
		self.enemies_in_sight =[]

	def add_enemy(self, identity, x_enem, y_enem):
		self.enemies_in_sight.append(Enemy(identity, x_enem, y_enem))

	def add_location(self, x, y):
		self.x = x
		self.y = y

	def add_angle(self, ang):
		self.angle = ang

	def add_can_shoot(self):
		self.can_shoot = True

	def add_can_fire_missile(self):
		self.can_shoot_missile = True

	
class Enemy:
	def __init__(self, identity, x, y):
		self.x = x
		self.y = y
