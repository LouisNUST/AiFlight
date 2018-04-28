#Author: John Marrs
import socket
import socket_utilities
import pickle
import client_message
import server_message
import init_message
import time
import math
import game_data
class Client:
	def __init__(self,hostname, port):
		self.hostname = hostname
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.id = -1
		self.t = time.time()

		

		try:
			self.sock.connect((hostname, port))
			print('Connected to: ' + str(hostname) + ':' + str(port))
			print('Waiting for other clients...')
			print('Exchanging init information...')

			# RECEIVE SERVER INIT MESSAGE and RESPOND WITH CLIENT INIT MESSAGE -------------------------------------------------------------------
			cli_init = init_message.InitMessageFromClient()
			cli_init = socket_utilities.convert_to_bytes(cli_init)
			socket_utilities.send_data(self.sock, cli_init)

			ser_init = socket_utilities.recv_data(self.sock)
			ser_init = socket_utilities.convert_to_object(ser_init)

			self.id = ser_init.id


			# STARTING NORMAL GAME FLOW -----------------------------------------------------------------------------------------------------------
			while True:
				data = self.listen_for_update()
				if data == b'END':
					print('Simulation ended successfully!')
					return
				elif data == b'START':
					print("Simulation running...")
					self.send_response(None)

				else:
					server_message = socket_utilities.convert_to_object(data)
					self.send_response(server_message)

		except socket.error as e:
			print(e)

			return


	def listen_for_update(self):
		#print('Listening for update...')
		data = b''
		#temp = self.sock.recv(1024)
		
		data = socket_utilities.recv_data(self.sock)
		#while len(temp.decode('utf-8')) > 0:
			#data += temp
			#break
			#temp = self.sock.recv(1024)


		return data;

	def send_response(self, serv_mess):
		#print('Sending response...')

		resp = client_message.ClientMessage(self.id)

		if serv_mess != None:
			if len(serv_mess.enemies_in_sight) > 0:
				xenem = serv_mess.enemies_in_sight[0].x
				yenem = serv_mess.enemies_in_sight[0].y

				a = serv_mess.angle

				x_next = serv_mess.x + math.cos(math.radians(a)) * 100.0
				y_next = serv_mess.y + math.sin(math.radians(a)) * 100.0
				dist = game_data.calculate_distance_points(xenem, yenem, x_next, y_next)



				x_pos = serv_mess.x + math.cos(math.radians(a + 45.0/100.0)) * 100
				y_pos = serv_mess.y + math.sin(math.radians(a + 45.0/100.0)) * 100
				dist_pos = game_data.calculate_distance_points(xenem, yenem, x_pos, y_pos)

				x_neg = serv_mess.x + math.cos(math.radians(a - 45.0/100.0)) * 100
				y_neg = serv_mess.y + math.sin(math.radians(a - 45.0/100.0)) * 100
				dist_neg = game_data.calculate_distance_points(xenem, yenem, x_neg, y_neg)



				#print('MyLoc -> x: ' + str(serv_mess.x) + ' y: ' + str(serv_mess.y))
				#print('Next -> x: ' + str(x_next) + ' y: ' + str(y_next) + ' dist: ' + str(dist))
				#print('Pos -> x: ' + str(x_pos) + ' y: ' + str(y_pos) + ' dist: ' + str(dist_pos))
				#print('Neg -> x: ' + str(x_neg) + ' y: ' + str(y_neg) + ' dist: ' + str(dist_neg))


				if dist_pos < dist:
					resp.add_turn(45)
				elif dist_neg < dist:
					resp.add_turn(-45)

				d2 = game_data.distance_between_point_and_line(serv_mess.x, serv_mess.y, x_next, y_next, xenem, yenem)
				if (serv_mess.can_shoot) & (dist < 1200) & (d2 < 10):
					resp.add_shoot()
				



			#if serv_mess.x > 9000 or serv_mess.y > 9000 or serv_mess.x < -9000 or serv_mess.y < -9000:
			#	resp.add_turn(45)
		#resp.add_turn(1)


		resp = socket_utilities.convert_to_bytes(resp)
		socket_utilities.send_data(self.sock, resp)
		#self.sock.send('a'.encode())


def main():
	print('Welcome to an AIGAME client.')
	h = input("Enter server hostname: ")
	p = input('Enter server port: ')
	c = Client(h, int(p))

if __name__=='__main__':
	main()




