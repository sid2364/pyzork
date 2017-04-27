import player
import grammar
import gameMap

import pdb

import random

what_next = ["What do you do? ", "What next? ", \
                "What do you do next? "]

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
	
	print("\n\n")
	map_o.goToNextState(player_o, "north")
	map_o.goToNextState(player_o, "east")
	print("asdasdn\n\n")
	map_o.dropObject(player_o, "sword")
	map_o.dropObject(player_o, "blue")
	map_o.whereAmI(player_o)
	print(player_o.have)
	map_o.takeObject(player_o, "something")
	map_o.takeObject(player_o, "sword")
	print(player_o.have)
	
	print("\n\n")
	print(map_o.whereAmI(player_o))
	print(map_o.getFighterList(player_o))
	print(map_o.getObjectList(player_o))
	map_o.goToNextState(player_o, "west")
	print(map_o.getFighterList(player_o))
        print(map_o.getObjectList(player_o))
	#print(grammar.replaceObjects(map_o.getObjectList(player_o)))
	map_o.goToNextState(player_o, "south")
	g = grammar.Grammar()
	print("\n\n")
	objects = map_o.getObjectList(player_o)
	fighters = map_o.getFighterList(player_o)
	#print(grammar.getGrammarType("go to north"))
	print(g.getGrammarType("take the hammer"))
	print(g.getGrammarType("take the hat"))
	print(g.getGrammarType("see"))
	print(g.getGrammarType("drop the hammer"))
	print(g.getGrammarType("take key from chest"))
	print(g.getGrammarType("go south"))
	print(g.getGrammarType("kill the dragon"))
	ret, ol = g.getGrammarType("open the chest I see here blah blah")
	method_to_call = getattr(map_o, ret)
	method_to_call(player_o, *ol)

def do(p_input, map_o, player_o, grammar):
	functionName, misc = grammar.getGrammarType(p_input)
	print(misc)
	if functionName is None:
		print("Did not catch that...")
		return
	function = getattr(map_o, functionName)
	function(player_o, *misc)
	return

def main():
	map_o = gameMap.Map()
	player_o = player.Player()
	gr = grammar.Grammar()
	map_o.whereAmI(player_o)
	
	said = ""
	while said != "quit" or said != "q" :
		said = raw_input(whatNext()).lower()
		do(said, map_o, player_o, gr)

		

if __name__ == "__main__":
	main()
