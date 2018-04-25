#Author: John Marrs
import pickle
import game_data
import os
class GameHistory:
	gamehistory = []
	chunk_size = 900
	n = 0
	def __init__(self, file_stem):
		self.file_stem = file_stem
		if not os.path.exists('GameHistory'):
			os.makedirs('GameHistory')

		if not os.path.exists('GameHistory/' + file_stem):
			os.makedirs('GameHistory/' + file_stem)

	def save_to_file(self):
		if len(self.gamehistory) > 0:
			print("Wrote " + str(self.n) + ' chunk')
			f = open(('GameHistory/' + self.file_stem + '/chunk' + str(self.n) + '.ck') , 'wb')
			pickle.dump(self.gamehistory,f)
			self.n = self.n+1
			self.gamehistory = []
			return True
		return False

	def load_from_file(self, file_name):
		f = open(file_name, 'rb')
		self.gamehistory = pickle.load(f)

	def add_game_data_instance(self, gamedata):
		if len(self.gamehistory) < self.chunk_size:
			self.gamehistory.append(gamedata)
		else:
			self.save_to_file()

	def is_empty(self):
		if len(self.gamehistory) == 0:
			return True
		else:
			return False
		

