#Author: John Marrs
import socket
import struct
import pickle

def send_data(socket, data):
	data = struct.pack('>I', len(data)) + data
	socket.sendall(data)

def recv_data(socket):
	length = recv_all(socket, 4)
	if (not length):
		return None
	length = struct.unpack('>I', length)[0]

	return recv_all(socket, length)

def recv_all(socket, n_bytes):
	data = b''
	while len(data) < n_bytes:
		packet = socket.recv(n_bytes - len(data))
		if not packet:
			return None
		data += packet
	return data

# Methods for converting data to bytes or back to object form
def convert_to_bytes(data):
	try:
		return pickle.dumps(data)
	except Exception as e:
		print(e)
		return None

def convert_to_object(bytes):
	try:
		return pickle.loads(bytes)
	except Exception as e:
		print(e)
		return None