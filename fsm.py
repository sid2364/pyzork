import json

class Map:
	def __init__(self):
		with open("map.json") as map_f:
			self.fsm = json.load(map_f)

map_o = Map()
