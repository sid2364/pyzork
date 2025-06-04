import sys
import types
import unittest

# Provide stubs for missing modules
nltk_stub = types.ModuleType("nltk")
class DummyPorterStemmer:
    def stem(self, word):
        w = word.lower()
        return 'inventori' if w == 'inventory' else w

def word_tokenize(text):
    return text.split()

nltk_stub.PorterStemmer = DummyPorterStemmer
nltk_stub.word_tokenize = word_tokenize
nltk_stub.corpus = types.SimpleNamespace(stopwords=types.SimpleNamespace(words=lambda lang: []))
nltk_stub.data = types.SimpleNamespace(path=[])
sys.modules.setdefault('nltk', nltk_stub)
sys.modules.setdefault('sets', types.ModuleType('sets'))

import player
import gameMap
import grammar

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = player.Player()

    def test_take_and_drop_item(self):
        res = self.player.takeItem('bone')
        self.assertEqual(res, 0)
        self.assertIn('bone', self.player.have)
        res_again = self.player.takeItem('bone')
        self.assertEqual(res_again, 1)
        self.player.dropItem('bone')
        self.assertNotIn('bone', self.player.have)

class MapTestCase(unittest.TestCase):
    def setUp(self):
        # override byteify to avoid converting strings to bytes under Python3
        gameMap.byteify = lambda data, ignore_dicts=False: data
        self.map = gameMap.Map()
        self.player = player.Player()

    def test_object_lifecycle(self):
        objs = self.map.getObjectList(self.player)
        self.assertIn('bone', objs)
        self.map.takeObject(self.player, 'bone')
        self.assertIn('bone', self.player.have)
        self.assertNotIn('bone', self.map.getObjectList(self.player))
        self.map.dropObject(self.player, 'bone')
        self.assertIn('bone', self.map.getObjectList(self.player))
        self.assertNotIn('bone', self.player.have)

    def test_movement_and_fighter(self):
        self.map.goToNextState(self.player, 'east')
        self.assertEqual(self.player.position, 'dragonCell')
        # give player a weapon and kill the dragon
        self.player.have.append('sword')
        self.map.killFighter(self.player, 'dragon', 'sword')
        fighter = self.map.fsm['dragonCell']['fighters'][0]['dragon']
        self.assertTrue(fighter['alreadyKilled']['killed'])
        self.assertIn('east', self.map.fsm['dragonCell']['directions'])

    def test_open_object(self):
        self.map.goToNextState(self.player, 'east')
        self.map.goToNextState(self.player, 'north')
        self.map.openObject(self.player, 'chest')
        objs = self.map.getObjectList(self.player)
        self.assertIn('key', objs)

class GrammarTestCase(unittest.TestCase):
    def setUp(self):
        self.grammar = grammar.Grammar()

    def test_basic_commands(self):
        fn, args = self.grammar.getGrammarType('take bone')
        self.assertEqual(fn, 'takeObject')
        self.assertEqual(args, ['bone'])
        fn, args = self.grammar.getGrammarType('go north')
        self.assertEqual(fn, 'goToNextState')
        self.assertEqual(args, ['north'])
        fn, args = self.grammar.getGrammarType('fight dragon with sword')
        self.assertEqual(fn, 'killFighter')
        self.assertEqual(args, ['dragon', 'sword'])
        fn, args = self.grammar.getGrammarType('drop bone')
        self.assertEqual(fn, 'dropObject')
        self.assertEqual(args, ['bone'])
        fn, args = self.grammar.getGrammarType('open chest')
        self.assertEqual(fn, 'openObject')
        self.assertEqual(args, ['chest'])
        fn, args = self.grammar.getGrammarType('look')
        self.assertEqual(fn, 'whereAmI')
        self.assertEqual(args, [])
        fn, args = self.grammar.getGrammarType('help')
        self.assertEqual(fn, 'help')
        self.assertEqual(args, [])
        fn, args = self.grammar.getGrammarType('inventory')
        self.assertEqual(fn, 'inventory')
        self.assertEqual(args, [])
        fn, args = self.grammar.getGrammarType('stand')
        self.assertEqual(fn, 'sayOkay')
        self.assertEqual(args, [])
        fn, args = self.grammar.getGrammarType('some gibberish')
        self.assertIsNone(fn)
        self.assertEqual(args, [])

    def test_expanded_vocabulary(self):
        fn, args = self.grammar.getGrammarType('grab bone')
        self.assertEqual(fn, 'takeObject')
        self.assertEqual(args, ['bone'])

        fn, args = self.grammar.getGrammarType('attack dragon with sword')
        self.assertEqual(fn, 'killFighter')
        self.assertEqual(args, ['dragon', 'sword'])

        fn, args = self.grammar.getGrammarType('discard bone')
        self.assertEqual(fn, 'dropObject')
        self.assertEqual(args, ['bone'])

        fn, args = self.grammar.getGrammarType('look door')
        self.assertEqual(fn, 'examineObject')
        self.assertEqual(args, ['door'])

        fn, args = self.grammar.getGrammarType('inspect chest')
        self.assertEqual(fn, 'examineObject')
        self.assertEqual(args, ['chest'])

if __name__ == '__main__':
    unittest.main()
