#Author: John Marrs
import pickle
import game_data
import os
import cv2
import numpy as np
import time
import math
import copy
class GameHistory:
	gamehistory = []
	chunk_size = 1000
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
		if len(self.gamehistory) < self.chunk_size and not gamedata.game_over:
			self.gamehistory.append(gamedata)
		else:
			self.gamehistory.append(gamedata)
			self.save_to_file()

	def is_empty(self):
		if len(self.gamehistory) == 0:
			return True
		else:
			return False

	def playback_from(self, gamename, center_player, width, height, framerate, ips):
		chunk = 0

		f_name = 'GameHistory/' + str(gamename) + '/chunk' + str(chunk) + '.ck'


		t_last = time.time()
		v = cv2.VideoWriter('GameHistory/' + str(gamename) + '/output' + str(center_player) + '.mp4', cv2.VideoWriter_fourcc(*'MJPG'), framerate, (width, height))
		t_start = time.time()
		while os.path.exists(f_name):
			self.load_from_file(f_name)
			print('Writing chunk: ' +str(chunk))

			for i in range(0, len(self.gamehistory)):

				if i % (ips/framerate):
			
					img = np.zeros((width, height, 3), np.uint8)
					for player in self.gamehistory[i].players:
						if player.alive:
							x = player.x - self.gamehistory[i].players[center_player].x + width/2.0
							y = player.y - self.gamehistory[i].players[center_player].y + height/2.0
							#print(player.y)
							x = int(round(x))
							y = int(round(y))
							cv2.circle(img, (x, y), int(player.collision_radius),(0, 0, 255), 2 )
							cv2.line(img, (x, y), (x + int(player.collision_radius * math.cos(math.radians(player.angle))), y + int(player.collision_radius * math.sin(math.radians(player.angle)))), (0, 0, 255), 2)

				

					for bullet in self.gamehistory[i].bullets:
						x = bullet.x - self.gamehistory[i].players[center_player].x + width/2.0
						y = bullet.y - self.gamehistory[i].players[center_player].y + height/2.0
						#print(player.y)
						x = int(round(x))
						y = int(round(y))
					
						cv2.line(img, (x, y), (x + int(1 * 5 * math.cos(math.radians(bullet.angle))), y + int(1 * 2 * math.sin(math.radians(bullet.angle)))), (0, 0, 255), 2)

					for missile in self.gamehistory[i].missiles:
						x = missile.x - self.gamehistory[i].players[center_player].x + width/2.0
						y = missile.y - self.gamehistory[i].players[center_player].y + height/2.0

						x = int(round(x))
						y = int(round(y))

						cv2.line(img, (x, y), (x + int(1 * 5 * math.cos(math.radians(bullet.angle))), y + int(1 * 5 * math.sin(math.radians(missile.angle)))), (0, 255, 0), 2)

					v.write(img)


					

			chunk = chunk + 1
			f_name = 'GameHistory/' + str(gamename) + '/chunk' + str(chunk) + '.ck'

		v.release()
		t_end = time.time()
		print('Finished Rendering')
		print('Time elapsed: ' + str(t_end-t_start))

		# MAP OVERVIEW PLAYBACK

	def playback_overview(self, gamename, width, height, framerate, ips):
		chunk = 0

		f_name = 'GameHistory/' + str(gamename) + '/chunk' + str(chunk) + '.ck'
		background = cv2.imread('RenderResources/background_map.jpg', -1)

		t_last = time.time()
		v = cv2.VideoWriter('GameHistory/' + str(gamename) + '/output.mp4', 0x00000020, framerate, (width, height))
		t_start = time.time()
		while os.path.exists(f_name):
			self.load_from_file(f_name)
			print('Writing chunk: ' +str(chunk))

			
			for i in range(0, len(self.gamehistory)):
				if i % (ips/framerate) == 0:

			
					#img = np.zeros((width, height, 3), np.uint8)
					img = copy.copy(background)
					for player in self.gamehistory[i].players:
						if player.alive:
							x = (player.x + 10000)/20000 * width
							y = (player.y + 10000)/20000 * height
							#print(player.y)
							x = int(round(x))
							y = int(round(y))
							cv2.circle(img, (x, y), int(player.collision_radius),(0, 0, 255), 2 )
							cv2.line(img, (x, y), (x + int(player.collision_radius * math.cos(math.radians(player.angle))), y + int(player.collision_radius * math.sin(math.radians(player.angle)))), (0, 0, 255), 2)

				

					for bullet in self.gamehistory[i].bullets:
						x = (bullet.x + 10000)/20000 * width
						y = (bullet.y + 10000)/20000 * height
						#print(player.y)
						x = int(round(x))
						y = int(round(y))
					
						cv2.line(img, (x, y), (x + int(1 * 5 * math.cos(math.radians(bullet.angle))), y + int(1* 2 * math.sin(math.radians(bullet.angle)))), (0, 0, 255), 2)

					for missile in self.gamehistory[i].missiles:
						#print('SHOULD HAVE RENDERED MISSILE')
						x = (missile.x + 10000)/20000 * width
						y = (missile.y + 10000)/20000 * height

						x = int(round(x))
						y = int(round(y))

						cv2.line(img, (x, y), (x + int(1 * 5 * math.cos(math.radians(missile.angle))), y + int(1* 5 * math.sin(math.radians(missile.angle)))), (0, 255, 0), 2)


					v.write(img)



					

			chunk = chunk + 1
			f_name = 'GameHistory/' + str(gamename) + '/chunk' + str(chunk) + '.ck'

		v.release()
		t_end = time.time()
		print('Finished Rendering')
		print('Time elapsed: ' + str(t_end-t_start))


	def playback_from_scaled(self, gamename, center_player, width, height, framerate, ips, meters_per_pixel):
		meters_per_pixel = float(meters_per_pixel)
		chunk = 0

		f_name = 'GameHistory/' + str(gamename) + '/chunk' + str(chunk) + '.ck'


		t_last = time.time()
		v = cv2.VideoWriter('GameHistory/' + str(gamename) + '/output' + str(center_player) + '.mp4', 0x00000020, framerate, (width, height))

		background = cv2.imread('RenderResources/background_map.jpg', -1)
		img_height, img_width, img_channels = background.shape

		width_from = (width * meters_per_pixel * img_width) / (20000.0)
		height_from = (height * meters_per_pixel * img_width) / (20000.0)

		t_start = time.time()
		while os.path.exists(f_name):
			self.load_from_file(f_name)
			print('Writing chunk: ' +str(chunk))
			
			for i in range(0, len(self.gamehistory)):

				if i % (ips/framerate):
			
					center_actual_x = ((self.gamehistory[i].players[center_player].x + 10000) * img_width)/20000
					center_actual_y = ((self.gamehistory[i].players[center_player].y + 10000) * img_height)/20000
					x_start = int(center_actual_x - (width_from/2))
					x_end = int(center_actual_x + (width_from/2))
					y_start = int(center_actual_y - (width_from/2))
					y_end = int(center_actual_y + (width_from/2))

					if x_start < 0:
						x_start = 0
					if x_end > img_width:
						x_end = img_width
					if y_start < 0:
						y_start = 0
					if y_end > img_height:
						y_end = img_height

					sub_img = background[y_start:y_end, x_start:x_end]
					#print("x: " + str(x_start) + " -> "+ str(x_end))
					#print("y: " + str(y_start) + " -> "+ str(y_end))
					#print("--------------------------------------------------------")

					img = np.zeros((img_width, img_height, 3), np.uint8)
					sub_img = cv2.resize(sub_img, (img_width, img_height))
					img[0:img_height, 0: img_width] = sub_img


					img = cv2.resize(img, (width, height)) 
					#img = np.zeros((width, height, 3), np.uint8)

					for player in self.gamehistory[i].players: 
						if player.alive:
							x = (player.x - self.gamehistory[i].players[center_player].x)/meters_per_pixel + width/2.0
							y = (player.y - self.gamehistory[i].players[center_player].y)/meters_per_pixel + height/2.0
							#print(player.y)
							x = int(round(x))
							y = int(round(y))
							cv2.circle(img, (x, y), int(player.collision_radius),(0, 0, 255), 2 )
							cv2.line(img, (x, y), (x + int(player.collision_radius * math.cos(math.radians(player.angle))), y + int(player.collision_radius * math.sin(math.radians(player.angle)))), (0, 0, 255), 2)

				

					for bullet in self.gamehistory[i].bullets:
						x = (bullet.x - self.gamehistory[i].players[center_player].x)/meters_per_pixel + width/2.0
						y = (bullet.y - self.gamehistory[i].players[center_player].y)/meters_per_pixel + height/2.0
						#print(player.y)
						x = int(round(x))
						y = int(round(y))
					
						cv2.line(img, (x, y), (x + int(1 * 5 * math.cos(math.radians(bullet.angle))), y + int(1 * 2 * math.sin(math.radians(bullet.angle)))), (0, 0, 255), 2)

					for missile in self.gamehistory[i].missiles:
						x = (missile.x - self.gamehistory[i].players[center_player].x)/meters_per_pixel + width/2.0
						y = (missile.y - self.gamehistory[i].players[center_player].y)/meters_per_pixel + height/2.0

						x = int(round(x))
						y = int(round(y))

						cv2.line(img, (x, y), (x + int(1 * 5 * math.cos(math.radians(missile.angle))), y + int(1 * 5 * math.sin(math.radians(missile.angle)))), (0, 255, 0), 2)

					v.write(img)


					

			chunk = chunk + 1
			f_name = 'GameHistory/' + str(gamename) + '/chunk' + str(chunk) + '.ck'

		v.release()
		t_end = time.time()
		print('Finished Rendering')
		print('Time elapsed: ' + str(t_end-t_start))

		# MAP OVERVIEW PLAYBACK
		

