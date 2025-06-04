# -*- coding: utf-8 -*-

try:
        import nltk, os, json
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
GRAMMAR_CONFIG = os.path.join(os.path.dirname(__file__), 'grammar_config.json')
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
examineObject = "examineObject"
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
                7: dropObject,\
                8: openObject,\
                9: examineObject,\
                10: whereAmI,\
                11: helpF,\
                12: inventory,\
                13: sayOkay}


class Grammar:
        def __init__(self):
                cfg = {}
                if os.path.exists(GRAMMAR_CONFIG):
                        try:
                                with open(GRAMMAR_CONFIG) as f:
                                        cfg = json.load(f)
                        except Exception:
                                cfg = {}

                self.move_words = cfg.get('move_words', move_words)
                self.direction_words = cfg.get('direction_words', direction_words)
                self.fight_words = cfg.get('fight_words', fight_words)
                self.take_words = cfg.get('take_words', take_words)
                self.drop_words = cfg.get('drop_words', drop_words)
                self.unlock_words = cfg.get('unlock_words', unlock_words)
                self.look_words = cfg.get('look_words', look_words)
                self.inventory_words = cfg.get('inventory_words', inventory_words)
                self.sayOkay_words = cfg.get('sayOkay_words', sayOkay_words)

                self.grammar = [[self.take_words, wildcard, from_, wildcard],\
                        [self.fight_words, wildcard, with_, wildcard],\
                        [with_, wildcard, self.fight_words, wildcard],\
                        [from_, wildcard, self.take_words, wildcard],\
                        [self.move_words, self.direction_words],\
                        [self.take_words, wildcard],\
                        [self.fight_words, wildcard],\
                        [self.drop_words, wildcard],\
                        [self.unlock_words, wildcard],\
                        [self.look_words, wildcard],\
                        [self.look_words],\
                        [helpF],\
                        [self.inventory_words],\
                        [self.sayOkay_words]]

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
                                        if p_input[word_i] in self.direction_words:
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
