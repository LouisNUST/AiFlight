#Author: John Marrs
class ClientMessage:
	radioMessage = ''
	turn = 0
	accelerate = False
	decelerate = False
	shoot_gun = False
	shoot_missile = False
	
	def __init__(self, identity):
		self.id = identity

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

	def add_fire_missle(self):
		self.shoot_missle = True
