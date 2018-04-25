#Author: John Marrs
import socket
import socket_utilities
import pickle
import client_message
import server_message
import init_message
class Client:
	def __init__(self,hostname, port):
		self.hostname = hostname
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.id = -1

		

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
				self.send_response()
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

	def send_response(self):
		#print('Sending response...')
		resp = client_message.ClientMessage(self.id)
		resp.add_turn(45)
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




