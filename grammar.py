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
look_words = ["look", "see", "gaze"]
object_wildcard = []
fighter_wildcard = []
with_ = "with"
from_ = "from"

what_next = ["What do you do? ", "What next? ", \
		"What do you do next? "]

goToNextState = "goToNextState"
takeObject = "takeObject"
dropObject = "dropObject"
killFighter = "killFighter"
whereAmI = "whereAmI"
openObject = "openObject"


stopwords = list(set(corpus.stopwords.words("english")) - set(["with", "from"]))

grammar = [[move_words, direction_words],\
		[take_words, object_wildcard],\
		[fight_words, fighter_wildcard],\
		[drop_words, object_wildcard],\
		[unlock_words, object_wildcard],\
		[look_words],\
		[take_words, object_wildcard, from_, object_wildcard],\
		[fight_words, fighter_wildcard, with_, object_wildcard],\
		[with_, object_wildcard, fight_words, fighter_wildcard],\
		[from_, object_wildcard, take_words, object_wildcard]]

grammarToFunctionMap = {0: goToNextState, \
		1: takeObject,\
		2: killFighter,\
		3: dropObject,\
		4: openObject,\
		5: whereAmI,\
		6: takeObject,\
		7: killFighter,
		8: killFighter,\
		9: takeObject}

class Grammar:
	def __init__(self):
		self.grammar = []
		self.object_wildcard = []
		self.fighter_wildcard = []
	def resetObjectsAndFighters(self):
		self.grammar = [[move_words, direction_words],\
	                [take_words, self.object_wildcard],\
	                [fight_words, self.fighter_wildcard],\
	                [drop_words, self.object_wildcard],\
	                [unlock_words, self.object_wildcard],\
	                [look_words],\
	                [take_words, self.object_wildcard, from_, self.object_wildcard],\
	                [fight_words, self.fighter_wildcard, with_, self.object_wildcard],\
	                [with_, self.object_wildcard, fight_words, self.fighter_wildcard],\
	                [from_, self.object_wildcard, take_words, self.object_wildcard]]

	def filterInput(self, p_input):
		return [word for word in word_tokenize(p_input) if word not in stopwords]
	
	def getGrammarType(self, p_input, p_objects, p_fighters):
		self.object_wildcard = p_objects
		self.fighter_wildcard = p_fighters
		self.resetObjectsAndFighters()
		p_input = self.filterInput(p_input)
		word_i = 0
		selected_i = -1
		for index_g in range(len(self.grammar)):
			word_i = 0
			for i in range(len(self.grammar[index_g])):
				if p_input[word_i] in self.grammar[index_g][i]:
					if i == len(self.grammar[index_g]) - 1:
						return grammarToFunctionMap[index_g]
					word_i += 1
				else:
					break
		if selected_i == -1:
			return None
	
#print(getGrammarType(filterInput("kill the fighter_ with the object_")))
#print(getGrammarType(filterInput("go to north")))

