class Player:
	def __init__(self,x,y,health,attack,defense):
		self.x = x 
		self.y = y
		self.health = health
		self.attack = attack
		self.defense = defense
		self.exhaustion = 0
		self.hunger = 0
		self.inventory = {}



	def add_inventory(self,item):
		if item not in self.inventory:
			self.inventory[item] = 1
		else:
			self.inventory[item] +=1