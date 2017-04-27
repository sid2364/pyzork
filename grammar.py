from nltk import PorterStemmer
from nltk import word_tokenize
from nltk import corpus

move_words = ["travel", "go", "move", "walk", "run"]
direction_words = ["north", "north-east", "east", "south-east", "south", \
			"south-west", "west", "north-west"]
fight_words = ["fight", "kill", "strike", "hit", "beat", "injur"]
take_words = ["take", "pick", "lift"]
drop_words = ["drop", "leave"]
unlock_words = ["open", "unlock"]
look_words = ["look", "see", "gaze", "where"]
object_wildcard = []
fighter_wildcard = []
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

stopwords = list(set(corpus.stopwords.words("english")) - set(["with", "from", "where"]))

grammarToFunctionMap = {0: goToNextState, \
		1: takeObject,\
		2: killFighter,\
		3: dropObject,\
		4: openObject,\
		5: whereAmI,\
		6: takeObject,\
		7: killFighter,
		8: killFighter,\
		9: takeObject,\
		10: helpF}


class Grammar:
	def __init__(self):
		self.grammar = [[move_words, direction_words],\
	                [take_words, wildcard],\
	                [fight_words, wildcard],\
	                [drop_words, wildcard],\
	                [unlock_words, wildcard],\
	                [look_words],\
	                [take_words, wildcard, from_, wildcard],\
	                [fight_words, wildcard, with_, wildcard],\
	                [with_, wildcard, fight_words, wildcard],\
	                [from_, wildcard, take_words, wildcard]]

	def filterInput(self, p_input):
		return [word for word in word_tokenize(p_input) if word not in stopwords]
	
	def getGrammarType(self, p_input):
		p_input = self.filterInput(p_input)
		word_i = 0
		selected_i = -1
		for index_g in range(len(self.grammar)):
			word_i = 0
			thingMentioned = []
			for i in range(len(self.grammar[index_g])):
				if wildcard in self.grammar[index_g][i]:
					thingMentioned.append(p_input[word_i])
					if i == len(self.grammar[index_g]) -1:
						return grammarToFunctionMap[index_g], thingMentioned
					continue
				if p_input[word_i] in self.grammar[index_g][i]:
					if p_input[word_i] in direction_words:
						thingMentioned.append(p_input[word_i])
					if i == len(self.grammar[index_g]) - 1:
						return grammarToFunctionMap[index_g], thingMentioned
					word_i += 1
				else:
					break
		if selected_i == -1:
			return None
	
#print(getGrammarType(filterInput("kill the fighter_ with the object_")))
#print(getGrammarType(filterInput("go to north")))

