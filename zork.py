import player
import grammar
import gameMap

import random

what_next = ["What do you do? ", "What next? ", \
                "What do you do next? "]

def whatNext():
	return what_next[random.randint(0, len(what_next)-1)]

def do(p_input, map_o, player_o, grammar):
	functionName, misc = grammar.getGrammarType(p_input)
	if functionName is None:
		print("Did not catch that...")
		return 1
	function = getattr(map_o, functionName)
	function(player_o, *misc)
	return 0

def main():
	map_o = gameMap.Map()
	player_o = player.Player()
	gr = grammar.Grammar()
	map_o.whereAmI(player_o)
	
	said = ""
	bad_said = 0
	while True:
		try:
			said = raw_input(whatNext()).lower()
		except KeyboardInterrupt, EOFError:
			print("\n\nBuh-bye.")
			quit()
		except:
			print("\nThat did not make sense to me.\nIf you wish to exit, type 'quit' or 'q' or press ctrl-C.")
			continue

		if said == "quit" or said == "q":
			break
		
		if do(said, map_o, player_o, gr):
			bad_said += 1
		else:
			bad_said = 0
		print("")
		if bad_said >= 3:
			print("To display a list of commands you can use, type 'help'.")
			bad_said = 0

		

if __name__ == "__main__":
	main()
