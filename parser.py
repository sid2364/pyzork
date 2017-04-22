import json
import sets

map_file = "map.json"

description = "description"
prerequisites = "prerequisites"
objects = "objects"
directions = "directions"
north = "north"
east = "east"
south = "south"
west = "west"
take = "take"
message = "message"
noPrerequisites = "noPrerequisites"
problem = "problem"
solution = "solution"

class Map:
	def __init__(self):
		with open(map_file, 'r') as map_f:
			self.fsm = json.load(map_f)

	'''
	Returns
		0, successfully moved to new position
		1, cannot go in that direction
		2, doesn't have prerequisites
	'''
	def goToNextState(self, p_player, p_direction):
		prerequisites_d = {}
		try:
			newState = self.fsm[p_player.position][directions][p_direction]
		except KeyError:
			print("There is nothing " + p_direction + ".")
			return 1
		print(newState)
		try:
			prerequisites_d =  self.fsm[newState][prerequisites]
		except KeyError:
			pass
		for item in prerequisites_d:
			for key in item:
				if set(key) > set(p_player.have):
					try:
						print(item[key][problem])
					except KeyError:
						print("You cannot go there.")
					return 2
				else:
					try:
						print(item[key][solution])
					except KeyError:
						continue
		p_player.moveToNewState(newState, p_direction)
		self.whereAmI(p_player)
		return 0

	'''
	Returns
		True, took item
		False, cannot take item
	'''
	def takeObject(self, p_player, p_object):
		if set([p_object]) < set(p_player.have):
			print("You already have that.")
			return False
		try:
			obj_l = self.fsm[p_player.position][objects]
			for obj in obj_l:
				for key in obj:
					if p_object == key:
						print(obj[key][message])
						if obj[key][take]:
							p_player.takeItem(p_object)
						return obj[key][take]
		except KeyError:
			print("There is nothing here you can take")
			return False
		
	'''
	Prints the description of current position
	'''
	def whereAmI(self, p_player):
		try:
			print(self.fsm[p_player.position][description])
		except KeyError: # map has no description (but, why?)
			print("There is darkness all around. All you can sense is your heavy breathing.")
		


if __name__ == "__main__":
	map_o = Map()
