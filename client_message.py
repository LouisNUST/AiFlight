#Author: John Marrs
class ClientMessage:
	
	def __init__(self, identity):
		self.id = identity
		self.accelerate = False
		self.decelerate = False
		self.shoot_gun = False
		self.shoot_missile = False
		self.turn = 0
		self.radio_message = ''
		self.lock = None

	def add_turn(self, rate):
		self.turn = rate

	def add_accelerate(self):
		self.accelerate = True

	def add_decelerate(self):
		self.decelerate = True

	def add_radio_message(self, msg):
		self.radio_message = msg

	def add_shoot(self):
		self.shoot_gun = True

	def add_fire_missile(self):
		self.shoot_missile = True

	def lock_on(self, enemy_id):
		self.lock = enemy_id
