import player
import gameMap

import pdb

import random

def whatNext():
	return what_next[random.randint(0, len(what_next)-1)]

def test():
	map_o = gameMap.Map()
	player_o = player.Player()
	map_o.goToNextState(player_o, "north")
	map_o.goToNextState(player_o, "east")

	print("\n\n")
	
	player_o = player.Player(position="dragonCell")
	map_o.goToNextState(player_o, "south")
	
	player_o = player.Player(position="dragonCell", have=['key'])
	map_o.goToNextState(player_o, "south")
	
	print("\n\n")
	
	print(player_o.have)
	map_o.takeObject(player_o, "sword")
	map_o.takeObject(player_o, "key")
	map_o.takeObject(player_o, "banana")
	print(player_o.have)
	
	map_o.goToNextState(player_o, "north")
	print("\n\nKJANSKJNASKJNAKSJNASKJNAKSJn")
	map_o.killFighter(player_o, "dragon", "dagger")
	map_o.killFighter(player_o, "dragon", "sword")

	map_o.whereAmI(player_o)

	print("\n\n")	
	map_o.goToNextState(player_o, "west")
	map_o.takeObject(player_o, "bone")
	map_o.takeObject(player_o, "candle")
	map_o.takeObject(player_o, "blue")
	print(player_o.have)
	map_o.takeObject(player_o, "bone")
	print(player_o.have)
	map_o.whereAmI(player_o)

	print("\n\n")
	player_o = player.Player()
	map_o = gameMap.Map()
	map_o.goToNextState(player_o, "east")
	map_o.goToNextState(player_o, "north")
	map_o.openObject(player_o, "ketchup")
	print("\n")
	map_o.openObject(player_o, "chest")
	map_o.openObject(player_o, "chest")
	print("\n\n")
	map_o.whereAmI(player_o)
	print("\n\n")
	map_o.takeObject(player_o, "key2")
	map_o.takeObject(player_o, "key")
	map_o.takeObject(player_o, "key")
	
	print("\n\n")
	map_o.goToNextState(player_o, "south")
	map_o.openObject(player_o, "dragon")
	map_o.openObject(player_o, "balloon")
	map_o.openObject(player_o, "gate")
	map_o.whereAmI(player_o)
	map_o.goToNextState(player_o, "south")
	map_o.takeObject(player_o, "sword")
	print(player_o.have)
	map_o.takeObject(player_o, "sword")
	print(player_o.have)
	map_o.takeObject(player_o, "spear")
	map_o.takeObject(player_o, "asd")
	print(player_o.have)
		

def main():
	map_o = gameMap.Map()
	player_o = player.Player()
	
	map_o.whereAmI(player_o)

	while said != "quit" or said != "q" :
		# map_o.whereAmI(player_o)
		said = raw_input(whatNext()).lower()
		if said in direction_words:
			map_o.goToNextState(player_o, said)

		

if __name__ == "__main__":
	test()
