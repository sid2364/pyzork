# -*- coding: utf-8 -*-

import sys
import random

try:
	import nltk, os
	nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))
	from nltk import word_tokenize
except ImportError:
	print("You must have NLTK data to run this game.")
	sys.exit()

import player
import grammar
import gameMap

what_next = ["What do you do? ", "What next? ",
			 "What do you do next? ", "What do you do now? ", "What is your next move? ", "What now? "]

did_not_catch_that = [
        "Did not catch that.",
        "What was that?",
        "I don't understand that.",
        "Could you say that again?",
        "Repeat that?",
        "Sorry?",
        "Did not understand that?",
        "Say that again?",
        "My vocabulary is limited. Could you say that again?",
]

def sayDidNotCatchThat():
	print(did_not_catch_that[random.randint(0, len(did_not_catch_that)-1)])

def whatNext():
	return what_next[random.randint(0, len(what_next)-1)]

def do(p_input, map_o, player_o, grammar):
	functionName, misc = grammar.getGrammarType(p_input)
	if functionName is None:
		sayDidNotCatchThat()
		return 1
	function = getattr(map_o, functionName)
	function(player_o, *misc)
	return 0

def getCommands(text):
	tokens = word_tokenize(text)
	command = ""
	for t in tokens:
		if t in ["and", ",", ".", "then"]:
			yield command
			command = ""
			continue
		command += t
		command += " "
	else:
		yield command

def gameLoop(map_o, player_o, grammar_o):
	map_o.whereAmI(player_o)
	said = ""
	bad_said = 0
	print("")
	while True:
		try:
			said = input(whatNext()).lower()
		except KeyboardInterrupt:#, EOFError:
			print("\n\nBuh-bye.")
			sys.exit()
		except:
			print("\nThat did not make sense to me.\nIf you wish to exit, type 'quit' or 'q' or press ctrl-C.")
			continue

		if said == "quit" or said == "q" or said=='exit':
			break

		if said == "save":
			print("Saving game...")
			gameMap.saveGame(map_o.fsm, player_o)
			print("Your progress has been saved.\n")
			continue

		commands = getCommands(said)
		for command in commands:
			if do(command, map_o, player_o, grammar_o):
				bad_said += 1
			else:
				bad_said = 0
			print("")

		if bad_said >= random.randint(3,5):
			print("To display a list of commands you can use, type 'help'.")
			bad_said = 0


def main():
	showHelp = True
	if gameMap.welcome():
		map_o = gameMap.Map()
		player_o = player.Player()
		print("Starting a new game.")
	else:
		map_, playerp_, playerd_, playerh_ = gameMap.loadGame()
		if map_ is not None:
			map_o = gameMap.Map(map_)
			player_o = player.Player(playerp_, playerh_, playerd_)
			showHelp = False
			print("Saved game loaded!\n")
		else:
			print("Starting a new game.")
			map_o = gameMap.Map()
			player_o = player.Player()
	try:
		input("Press enter to continue...")
	except (KeyboardInterrupt, EOFError):
		print("\nBye.")
		sys.exit()
	grammar_o = grammar.Grammar()
	# Display basic instructions before the game begins
	if showHelp:
		map_o.help(player_o)
	gameLoop(map_o, player_o, grammar_o)

if __name__ == "__main__":
	main()
