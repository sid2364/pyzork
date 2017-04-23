from nltk import PorterStemmer
from nltk import word_tokenizer

move_words = ["travel", "go", "move", "walk", "run"]
direction_words = ["north", "north-east", "east", "south-east", "south", \
			"south-west", "west", "north-west"]
fight_words = ["fight", "kill", "strike", "hit", "beat", "injur"]
take_words = ["take", "pick", "lift"]
drop_words = ["drop", "leave"]
unlock_words = ["open", "unlock"]
look_words = ["look", "see", "gaze"]
object_wildcard = "object_"
fighter_wildcard = "fighter_"

what_next = ["What do you do? ", "What next? ", \
		"What do you do next? "]

grammar = [[[move_words], [direction_words]],\
		[[take_words], object_wildcard],\
		[[fight_words], fighter_wildcard],\
		[[drop_words], object_wildcard],\
		[[unlock_words], object_wildcard],\
		[[look_words]]
		]
