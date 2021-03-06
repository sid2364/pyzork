# -*- coding: utf-8 -*-

try:
	import nltk, os
	nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))
	from nltk import PorterStemmer
	from nltk import word_tokenize
	from nltk import corpus
except ImportError:
	print("You do not have NLTK installed on this system. Cannot run the game without it.")
	sys.exit()


move_words = ["travel", "go", "move", "walk", "run"]
direction_words = ["north", "north-east", "east", "south-east", "south", \
			"south-west", "west", "north-west"]
fight_words = ["fight", "kill", "strike", "hit", "beat", "injur"]
take_words = ["take", "pick", "lift"]
drop_words = ["drop", "leave"]
unlock_words = ["open", "unlock"]
look_words = ["look", "see", "gaze", "where"]
inventory_words = ["inventori"]
sayOkay_words = ["noth", "stand"]
with_ = "with"
from_ = "from"
help_ = "help"
wildcard = "\_(**)_/"

what_next = ["What do you do? ", "What next? ", \
		"What do you do next? "]

goToNextState = "goToNextState"
takeObject = "takeObject"
dropObject = "dropObject"
killFighter = "killFighter"
whereAmI = "whereAmI"
openObject = "openObject"
helpF = "help"
inventory = "inventory"
sayOkay = "sayOkay"

stopwords = list(set(corpus.stopwords.words("english")) - set(["with", "from", "where"]))

grammarToFunctionMap = {0: takeObject, \
		1: killFighter,\
		2: killFighter,\
		3: takeObject,\
		4: goToNextState,\
		5: takeObject,\
		6: killFighter,\
		7: dropObject,
		8: openObject,\
		9: whereAmI,\
		10: helpF,\
		11: inventory,\
		12: sayOkay}


class Grammar:
	def __init__(self):
		self.grammar = [[take_words, wildcard, from_, wildcard],\
	                [fight_words, wildcard, with_, wildcard],\
	                [with_, wildcard, fight_words, wildcard],\
	                [from_, wildcard, take_words, wildcard],\
			[move_words, direction_words],\
	                [take_words, wildcard],\
	                [fight_words, wildcard],\
	                [drop_words, wildcard],\
	                [unlock_words, wildcard],\
	                [look_words],\
			[helpF],\
			[inventory_words],\
			[sayOkay_words]]

	def filterInput(self, p_input):
		ps = PorterStemmer()
		return [ps.stem(word) for word in word_tokenize(p_input) if word not in stopwords]
	
	def getGrammarType(self, p_input):
		p_input = self.filterInput(p_input)
		if not p_input:
			return None, []
		word_i = 0
		selected_i = -1
		for index_g in range(len(self.grammar)):
			word_i = 0
			thingMentioned = []
			if with_ in self.grammar[index_g][0] or from_ in self.grammar[index_g][0]:
				reverse = True
			else:
				reverse = False
			for i in range(len(self.grammar[index_g])):
				if word_i >= len(p_input):
					break
				if wildcard in self.grammar[index_g][i]:
					thingMentioned.append(p_input[word_i])
					if i == len(self.grammar[index_g]) -1:
						if reverse:
							return grammarToFunctionMap[index_g],list(reversed(thingMentioned))
						return grammarToFunctionMap[index_g], thingMentioned
					word_i += 1
					continue
				if p_input[word_i] in self.grammar[index_g][i]:
					if p_input[word_i] in direction_words:
						thingMentioned.append(p_input[word_i])
					if i == len(self.grammar[index_g]) - 1:
						if reverse:
							return grammarToFunctionMap[index_g], list(reversed(thingMentioned))
						return grammarToFunctionMap[index_g], thingMentioned
					word_i += 1
				else:
					break
		if selected_i == -1:
			return None, []
