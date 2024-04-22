import random

class NPC:
    def __init__(self, x, y, npc_type, health, attack, defense, xp):
        self.x = x
        self.y = y
        self.type = npc_type
        self.health = health
        self.attack = attack
        self.defense = defense
        self.xp = xp

    def wander(self, map_width, map_height):
        # Randomly choose a direction to move (up, down, left, right)
        direction = random.choice(['up', 'down', 'left', 'right'])
        
        # Calculate the new position based on the chosen direction
        if direction == 'up':
            new_y = max(0, self.y - 1)
            self.y = new_y
        elif direction == 'down':
            new_y = min(map_height - 1, self.y + 1)
            self.y = new_y
        elif direction == 'left':
            new_x = max(0, self.x - 1)
            self.x = new_x
        elif direction == 'right':
            new_x = min(map_width - 1, self.x + 1)
            self.x = new_x


