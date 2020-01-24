#Author: John Marrs
import socket
import time
import socket_utilities
import pickle
import game_history
import game_data
import client_message
import server_message
import init_message
import copy
import random
class Server:
	connections = []
	gamedata = None
	gamehistory = None

	iterations_per_second = 100
	dt = float(1)/iterations_per_second
	
	def __init__(self, hostname, port, n_clients, n_iterations, sim_name):
		#Create history object for this simulation
		self.gamehistory = game_history.GameHistory(sim_name)
		self.gamedata = game_data.GameData()
		#Program Process

		#Initialize Server with Values
		
		print("Started game at " + hostname + ':'+ str(port))
		self.hostname = hostname
		self.port = port

		#Creating and binding a server socket to a port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.sock.bind((hostname, port))
		except socket.error as e:
			return

		#Waiting for and connecting to clients
		print('Waiting for ' + str(n_clients) + ' clients...')
		self.sock.listen(n_clients)

		#Accepting connections and saving them
		for c in range(0, n_clients):
			conn, addr = self.sock.accept()
			self.connections.append(conn)
			print('Client ' + str(len(self.connections)-1) + ' Connected at: ' + str(addr[0]) + ':' + str(addr[1]))

			self.gamedata.players.append(game_data.Player(c,float(random.randint(-8000, 8000)), float(random.randint(-8000, 8000)), float(random.randint(0,360))))

			print('\tExchanging init information...')

			cli_init = socket_utilities.recv_data(conn)
			cli_init = socket_utilities.convert_to_object(cli_init)

			ser_init = init_message.InitMessageFromServer(c)
			ser_init = socket_utilities.convert_to_bytes(ser_init)
			socket_utilities.send_data(conn, ser_init)

			print('\tFinished exchanging init information...\n')
		

		#Starting Game Process
		print('Starting ' + str(n_iterations) + ' iterations...')
		start = time.time()
		for c in self.connections:
			#c.send('START'.encode())
			socket_utilities.send_data(c,'START'.encode())

		for i in range(0,n_iterations):
			if self.gamedata.game_over:
				break;
			self.broadcast_game_data()
			given = self.receive_client_inputs()
			self.process_game_data(given)

		if (not self.gamedata.game_over):
			self.gamedata.game_over = True
			print("The game ended in a draw!")

		#Saves last bit of data
		if not self.gamehistory.is_empty():
			self.gamehistory.save_to_file()


		#Closes client connections
		self.close_connections()

		#print(self.gamedatahistory)
		print('Simulation ending...')
		print('Elapsed time: ' + str(time.time() - start))



		
	def broadcast_game_data(self):
		#print('broadcasting game data...')
		for c in self.connections:
			temp_message = server_message.ServerMessage()
			#CUSTOMIZE WHAT TO SEND TO CLIENTS
			p = self.gamedata.players[self.connections.index(c)]
			if p.alive:
				if p.fire_iteration_count == 0:
					temp_message.add_can_shoot()
				if p.missile_iteration_count == 0:
					temp_message.add_can_fire_missile()
				temp_message.add_location(self.gamedata.players[self.connections.index(c)].x, self.gamedata.players[self.connections.index(c)].y)
				temp_message.add_angle(self.gamedata.players[self.connections.index(c)].angle)
				for c2 in self.connections:
					if c != c2 and self.gamedata.players[self.connections.index(c2)].alive:
						temp_message.add_enemy(str(self.connections.index(c2)) , self.gamedata.players[self.connections.index(c2)].x, self.gamedata.players[self.connections.index(c2)].y)


			temp_message = socket_utilities.convert_to_bytes(temp_message)
			socket_utilities.send_data(c, temp_message)

	def receive_client_inputs(self):
		#print('waiting for client inputs...')
		inputs = []

		for c in self.connections:
			#print("receiveing from: " + str(self.connections.index(c)))
			temp = socket_utilities.recv_data(c)
			temp = socket_utilities.convert_to_object(temp)
			#temp = c.recv(1024).decode('utf-8')
			inputs.append(temp)

		return inputs

#------------------------------------------------------------------------------------------------------------------------- GAME LOGIC HERE
	def process_game_data(self, inputs):

		for i in inputs:
			p = self.gamedata.players[i.id]
			p.turn(float(i.turn), self.dt)
			if i.accelerate:
				p.accelerate( self.dt)
			if i.decelerate:
				p.decelerate( self.dt)
			if i.shoot_gun:
				if p.bullet_ammo > 0 & p.fire_iteration_count == 0:
					self.gamedata.bullets.append(game_data.Bullet(i.id, p.x, p.y, p.angle))
					p.bullet_ammo = p.bullet_ammo - 1
					p.fire_iteration_count = 1
			if i.shoot_missile:
				if p.missiles > 0 & p.missile_iteration_count == 0:
					self.gamedata.missiles.append(game_data.Missile(i.id, p.x, p.y, p.angle, i.lock))
					#NEED TO CONVERT LOCK TO ENEMY
					p.missiles = p.missiles - 1
					p.missile_iteration_count = 1


			#self.gamedata.players[i.id].move(self.dt)
		for p in self.gamedata.players:
			if p.alive:
				p.move(self.dt)
				if p.fire_iteration_count >= self.iterations_per_second/p.fire_rate + 1:
					p.fire_iteration_count = 0
				elif p.fire_iteration_count > 0:
					p.fire_iteration_count = p.fire_iteration_count + 1

				if p.missile_iteration_count >= self.iterations_per_second/p.missile_fire_rate + 1:
					p.missile_iteration_count = 0
				elif p.missile_iteration_count > 0:
					p.missile_iteration_count = p.missile_iteration_count + 1
			#print('angle: ' + str(self.gamedata.players[0].angle) + ' x: ' + str(self.gamedata.players[0].x) + ' y: ' + str(self.gamedata.players[0].y))

		for b in self.gamedata.bullets:
			b.move(self.dt)
			if b.age > b.lifespan * self.iterations_per_second:
				self.gamedata.bullets.remove(b)
				del b

			#for p in self.gamedata.players:
				#if self.gamedata.check_hit(p,b):
					#p.health = p.health - b.damage

		for m in self.gamedata.missiles:
			m.move(self.dt)
			if m.age > m.lifespan * self.iterations_per_second:
				self.gamedata.missiles.remove(m)
				del m

		for p in self.gamedata.players:
			if p.alive:
				for b in self.gamedata.bullets:
					if game_data.check_hit(b,p):
						p.health = p.health - b.damage
						self.gamedata.bullets.remove(b)

				for m in self.gamedata.missiles:
					if game_data.check_hit(m,p):
						p.health = p.health - m.damage
						self.gamedata.missiles.remove(m)

		for p in self.gamedata.players:
			if p.alive:
				if p.health <= 0:
					p.alive = False

		# CHECK WIN CONDITIONS ----------------------------------------
		alive_counts = 0
		last_alive = -1
		for i in range(0, len(self.gamedata.players)):
			if (self.gamedata.players[i].alive):
				alive_counts += 1
				last_alive = i 

		if (alive_counts == 1):
			print("Player " + str(last_alive) +" won the game!")
			self.gamedata.game_over = True
			self.gamedata.game_winner = last_alive
		elif(alive_counts == 0):
			print("The game ended in a draw!")
			self.gamedata.game_over = True

		# END CHECK WIN CONDITIONS -------------------------------------

		# SAVE GAME STATE ----------------------------------------------
		self.gamehistory.add_game_data_instance(copy.deepcopy(self.gamedata))
		# END SAVE GAME STATE ------------------------------------------


		#print('angle: ' + str(self.gamedata.players[0].angle) + ' x: ' + str(self.gamedata.players[0].x) + ' y: ' + str(self.gamedata.players[0].y))
		# THIS FUNCTION DEFINES GAME RULES/ITERATIONS #UPDATES POSITIONS>>> ETC

#---------------------------------------------------------------------------------------------------------------------------- END GAME LOGIC


	def close_connections(self):
		for c in self.connections:
			socket_utilities.send_data(c, 'END'.encode())
			c.close()



def main():
	print('Welcome to the AIGAME server.')
	hostname = input("Enter hostname ('myip' for your machine's address): ")
	if str(hostname) == 'myip':
		hostname = socket.gethostbyname(socket.gethostname())

	p = input('Enter port: ')
	num_c = input('Enter number of clients: ')
	num_i = input('Enter number of iterations: ')
	game_name = input('Enter a name for this simulation: ')


	print('Starting server at ' + str(hostname) + ':' + str(p) + '...')

	#ts = TestServer('localhost',5555,2,10)
	ts = Server(hostname, int(p), int(num_c), int(num_i), str(game_name))

	render_option = input('A - None\nB - Render from Player\nEnter Here:')


	if (render_option == 'B' or render_option == 'b'):
		player_to_follow = int(input('Which player would you like to follow? '))
		meters_per_pixel = int(input("How many meters per pixel should be rendered? "))
		print("Rendering...")
		ts.gamehistory.playback_from_scaled(ts.gamehistory.file_stem, player_to_follow, 600, 600, 25, ts.iterations_per_second, meters_per_pixel)
	else:
		return

	#ts.gamehistory.playback_overview(ts.gamehistory.file_stem, 1024, 1024, 25, ts.iterations_per_second)
	#ts.gamehistory.playback_from_scaled(ts.gamehistory.file_stem, 0, 600, 600, 25, ts.iterations_per_second, 5)

if __name__ == '__main__':
	main()