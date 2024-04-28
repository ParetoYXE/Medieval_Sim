import pygame
from pygame.locals import *

class Renderer:
    def __init__(self, screen_width, screen_height, tile_size, grid_size):
        pygame.init()  # Initialize Pygame
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.scale = 2
        self.tile_size = tile_size * self.scale
        self.player_image = pygame.transform.scale(pygame.image.load("player.png"),(self.tile_size,self.tile_size))
        self.bg_image = pygame.transform.scale(pygame.image.load("OIG3.jpg"),(self.screen_width,self.screen_height))
        self.dialog_rect = pygame.Rect((screen_width - 400) / 2, (screen_height - 100) / 2, 400, 100)  # Dialog window rectangle
        self.dialog_width = self.tile_size * self.grid_size  # Width of the dialog window
        self.dialog_height = self.tile_size * 2  # Height of the dialog window
        self.font = pygame.font.Font(None, 36)  # Font for the text

    def render_opening_scene(self):
        # Render white background
        self.screen.fill((0, 0, 0))
        
        # Render title text
        title_font = pygame.font.SysFont(None, 48)
        title_text = title_font.render("The Necromancer", True, (255,255,255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_text, title_rect)
        
        # Render body text
        body_font = pygame.font.SysFont(None, 24)
        body_text = [
            "Darkness has fallen upon the land.",
            "A being long thought dead from the Elder Days has returned.",
            "The Necromancer awaits in his crypt somewhere in these lands.",
            "Find him and banish this heretical entity back to the hell it once came.",
            "(Press Space to Begin)"
        ]
        y_offset = self.screen_height // 2
        for line in body_text:
            line_text = body_font.render(line, True, (255,255,255))
            line_rect = line_text.get_rect(center=(self.screen_width // 2, y_offset))
            self.screen.blit(line_text, line_rect)
            y_offset += 30

        pygame.display.flip()

        # Wait for SPACEBAR to continue
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return

    def render_background(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg_image,(0,0))

    def render_grid(self):
        middle_offset_x = self.screen_width / 4
        middle_offset_y = self.screen_height / 4

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile_rect = pygame.Rect(x*self.tile_size+middle_offset_x,y*self.tile_size+middle_offset_y,self.tile_size,self.tile_size)
                pygame.draw.rect(self.screen,(255,255,255),tile_rect)
        
        pygame.display.flip()


    def render_dialog_window(self, map_width, map_height, text=""):
        dialog_x = self.screen_width / 4
        dialog_y = (self.screen_height / 4) * 3
        dialog_rect = pygame.Rect(dialog_x, dialog_y, self.dialog_width, self.dialog_height)

        # Draw white rectangle
        pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect)
        # Draw black border
        pygame.draw.rect(self.screen, (0, 0, 0), dialog_rect, 2)

        # Render text in the middle of the dialog window
        lines = text.split("\n")
        y_offset = dialog_rect.centery - (len(lines) * self.font.get_linesize()) // 2
        for line in lines:
            text_surface = self.font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(dialog_rect.centerx, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += self.font.get_linesize()



    def render_inventory(self, player):
        inv_x = self.screen_width / 4
        inv_y = (self.screen_height / 4) 
        # Render white background
        pygame.draw.rect(self.screen, (255, 255, 255), (inv_x, inv_y, self.grid_size*self.tile_size, self.grid_size*self.tile_size))
            
        # Render inventory items
        inventory_text = []
        for item, quantity in player.inventory.items():
            inventory_text.append(f"{item}: {quantity}")
        
        # Render player stats
        stats_text = [
            f"Health: {player.health}",
            f"Attack: {player.attack}",
            f"Defense: {player.defense}",
            f"Exhaustion: {player.exhaustion}",
            f"Hunger: {player.hunger}"
        ]

        # Render text
        y_offset = inv_y
        for text in inventory_text + stats_text:
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (inv_x, y_offset))
            y_offset += 40
        
        pygame.display.flip()

    def load_tileset(self, filename):
        self.tileset = pygame.image.load(filename)
        self.tileset_width = self.tileset.get_width()
        self.tileset_height = self.tileset.get_height()
        self.tiles = []
        self.tile_set_size = 16

        for y in range(0, self.tileset_height, self.tile_set_size):
            for x in range(0, self.tileset_width, self.tile_set_size):
                tile = self.tileset.subsurface(pygame.Rect(x, y, self.tile_set_size, self.tile_set_size))
                self.tiles.append(pygame.transform.scale(tile,(self.tile_size,self.tile_size)))

    def render_map(self, game_map, player, scroll_x, scroll_y, npcs):
        middle_offset_x = self.screen_width / 4
        middle_offset_y = self.screen_height / 4

        map_index = player.x + player.y * game_map.width

        # Draw the map background
        tile_rect = pygame.Rect(0 * self.tile_size + middle_offset_x, 0 * self.tile_size + middle_offset_y, self.tile_size * self.grid_size, self.tile_size * self.grid_size)
        pygame.draw.rect(self.screen, (255, 255, 255), tile_rect)

        # Render the map tiles and player sprite
        for x in range(scroll_x, self.grid_size + scroll_x):
            for y in range(scroll_y, self.grid_size + scroll_y):
                if game_map.map[y][x] == 1:
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.tiles[7], tile_rect.topleft)
                elif game_map.map[y][x] == 2:
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.tiles[48], tile_rect.topleft)
                elif game_map.map[y][x] == 3:
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.tiles[3], tile_rect.topleft)
                elif game_map.map[y][x] == 4:
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.tiles[50], tile_rect.topleft)
                elif game_map.map[y][x] == 5:
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.tiles[36], tile_rect.topleft)
                elif (x, y) in [(npc.x, npc.y) for npc in npcs]:
                    npc_image = self.player_image #pygame.Surface((self.tile_size, self.tile_size))
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(npc_image, tile_rect.topleft)
                else:
                    tile_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.tiles[6], tile_rect.topleft)
                if x == player.x and y == player.y:
                    player_rect = pygame.Rect(x * self.tile_size + middle_offset_x - scroll_x * self.tile_size, y * self.tile_size + middle_offset_y - scroll_y * self.tile_size, self.tile_size, self.tile_size)
                    self.screen.blit(self.player_image, player_rect.topleft)

