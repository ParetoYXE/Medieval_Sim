import pygame

from render import Renderer
from map import Map
from player import Player
from game import Game
from npc import NPC

GUI = Renderer(832,800,16,13) 
game_map = Map(256,256)
Current_Game = Game(game_map)
player = Player(6,6,10,10,10)

running = True

scroll_x = 0
scroll_y = 0

npcs = game_map.generate_random_npcs(game_map.width,game_map.height,100)

GUI.load_tileset("tileset_1bit.png")

render_inventory = False


GUI.render_opening_scene()


# Variable to store the time at which NPC AI was last called
last_npc_ai_call = pygame.time.get_ticks()
hunger_check_call = pygame.time.get_ticks()


while running:


	running = Current_Game.check_game_state(player)
	
	current_time = pygame.time.get_ticks()
	
	if current_time - last_npc_ai_call >= 1000:  # Call NPC AI every 1000 milliseconds (1 second)
		last_npc_ai_call = current_time
		for i in npcs:
			i.wander(game_map.width,game_map.height)

	if current_time - hunger_check_call >= 3000:
		hunger_check_call = current_time
		Current_Game.hunger_check(player, 50, 1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
			
			#interaction handler, move to a new function eventually
			mouse_x, mouse_y = pygame.mouse.get_pos()
			# # Convert mouse coordinates to map coordinates
			# map_x = int(mouse_x - GUI.screen_width / 4) // GUI.tile_size
			# map_y = int(mouse_y - GUI.screen_height / 4) // GUI.tile_size
			# tile_value = game_map.map[int(map_y)+scroll_y][int(map_x)+scroll_x]
			# print(f"Clicked on map coordinates ({map_x}, {map_y})")
			# print(f"Location contains ({tile_value})")

			# if(tile_value == 1):
			# 	game_map.map[map_y+scroll_y][map_x+scroll_x] = 0
			# 	player.add_inventory("wood")
			Current_Game.interaction(player,game_map,mouse_x,mouse_y,GUI,scroll_x,scroll_y)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:  # Move up (decrease player_y)
				player.y -= 1
				scroll_y -= 1
				context = Current_Game.collision_detection(player)
				if context['collision']:
					player.y += 1
					scroll_y += 1
				Current_Game.exhaustion_check(player, 10, 1)
				
			elif event.key == pygame.K_s:  # Move down (increase player_y)
				player.y += 1
				scroll_y += 1
				context = Current_Game.collision_detection(player)
				if context['collision']:
					player.y -= 1
					scroll_y -= 1
				Current_Game.exhaustion_check(player, 10, 1)
				
			elif event.key == pygame.K_a:  # Move left (decrease player_x)
				player.x -= 1
				scroll_x -= 1
				context = Current_Game.collision_detection(player)
				if context['collision']:
					player.x += 1
					scroll_x += 1
				Current_Game.exhaustion_check(player, 10, 1)
				
			elif event.key == pygame.K_d:  # Move right (increase player_x)
				player.x += 1
				scroll_x += 1
				context = Current_Game.collision_detection(player)
				if context['collision']:
					player.x -= 1
					scroll_x -= 1
				Current_Game.exhaustion_check(player, 10, 1)
				
			elif event.key == pygame.K_LSHIFT:
				render_inventory = not render_inventory




	#GUI.render_grid()
	GUI.render_background()
	GUI.render_map(game_map,player,scroll_x,scroll_y,npcs)



	context = Current_Game.collision_detection(player)
	

	if(not context['collision']):
		if(context['dialog']):
			GUI.render_dialog_window(game_map.width,game_map.height,context['text'])

	
	if(render_inventory):
		GUI.render_inventory(player)
		
	pygame.display.flip()


