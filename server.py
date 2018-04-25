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

			self.gamedata.players.append(game_data.Player(c,0,0,0))

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
			self.broadcast_game_data()
			given = self.receive_client_inputs()
			self.process_game_data(given)

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
			#CUSSTOMIZE WHAT TO SEND TO CLIENTS


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
		self.gamehistory.add_game_data_instance(copy.deepcopy(self.gamedata))

		for i in inputs:
			self.gamedata.players[i.id].turn(float(i.turn), self.dt)
			if i.accelerate:
				self.gamedata.players[i.id].accelerate( self.dt)
			if i.decelerate:
				self.gamedata.players[i.id].decelerate( self.dt)
			if i.shoot_gun:
				self.gamedata.bullets.append(game_data.Bullet(i.id, self.gamedata.players[i.id].x, self.gamedata.players[i.id].y), self.gamedata.players[i.id].angle)
			if i.shoot_missile:
				pass


			#self.gamedata.players[i.id].move(self.dt)
		for p in self.gamedata.players:
			p.move(self.dt)
			print('angle: ' + str(self.gamedata.players[0].angle) + ' x: ' + str(self.gamedata.players[0].x) + ' y: ' + str(self.gamedata.players[0].y))

		for b in self.gamedata.bullets:
			b.move()


		print('angle: ' + str(self.gamedata.players[0].angle) + ' x: ' + str(self.gamedata.players[0].x) + ' y: ' + str(self.gamedata.players[0].y))
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

if __name__ == '__main__':
	main()