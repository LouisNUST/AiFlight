#Author: John Marrs
class ServerMessage:
	
	x = float(0)
	y = float(0)

	angle = float(0)
	can_shoot = True
	can_shoot_missile = True
	ammo = 300
	missiles = 8
	enemies_in_sight = []

	def __init__(self):
		pass
