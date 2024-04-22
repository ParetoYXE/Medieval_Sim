import pygame, random, math
from pygame.locals import *

class Game:
	def __init__(self,game_map):
		self.map = game_map.map


	def collision_detection(self,player):
		x = player.x
		y = player.y

		if(self.map[y][x] == 1):
			return {'collision':True, 'text': 'A tree', 'dialog':True}
		elif(self.map[y][x] == 2):
			return {'collision':True, 'text': 'A river', 'dialog':True}
		elif(self.map[y][x] == 3):
			return {'collision':True, 'text': 'A brick wall', 'dialog':True}
		else:
			return {'collision':False, 'text': '', 'dialog':False}


	def interaction(self,player,game_map,mouse_x,mouse_y,GUI,scroll_x,scroll_y):
		map_x = int(mouse_x - GUI.screen_width / 4) // GUI.tile_size
		map_y = int(mouse_y - GUI.screen_height / 4) // GUI.tile_size
		tile_value = game_map.map[int(map_y)+scroll_y][int(map_x)+scroll_x]
		print(f"Clicked on map coordinates ({map_x}, {map_y})")
		print(f"Location contains ({tile_value})")

		if(tile_value == 1):
			self.chop_wood(player,game_map,map_x,map_y,scroll_x,scroll_y)




	#All main gameplay interactions go here. Resources and NPCs

	def chop_wood(self,player,game_map,map_x,map_y,scroll_x,scroll_y):
		if random.randint(0,100) < player.attack * 5:
			self.exhaustion_check(player,50,1)
			if(abs(map_x+scroll_x - player.x)) <= 1 and abs(map_y+scroll_y - player.y) <= 1:
				game_map.map[map_y+scroll_y][map_x+scroll_x] = 0
				player.add_inventory("wood")



	#CHECKS. All Gameplay checks go here


	def exhaustion_check(self,player,chance, mod):
		if random.randint(1,100) < chance:
			self.exhaustion_increase(player,mod)

	def exhaustion_increase(self,player,mod):
		if player.exhaustion < 100:
			player.exhaustion += mod

	def hunger_check(self,player,chance,mod):
		if random.randint(1,100) < chance:
			self.hunger_increase(player,mod)

	def hunger_increase(self,player,mod):
		if player.hunger < 100:
			player.hunger += mod

	def check_game_state(self,player):
		if player.hunger == 100:
			return False
		else:
			return True 