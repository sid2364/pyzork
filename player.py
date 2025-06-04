# -*- coding: utf-8 -*-

'''
Class describes player
	Attributes:
		position, current position on the map
		have, list of objects player has currently
		direction, direction player has last moved in
'''
class Player:
	def __init__(self, position="start", have=None, direction="north"):
		self.position = position
		# avoid using a mutable default for the inventory list
		self.have = list(have) if have is not None else []
		self.direction = direction
	def moveToNewState(self, position, direction):
		self.position = position
		self.direction = direction
	def takeItem(self, item):
		if item in self.have:
			print("You already have this.")
			return 1
		self.have.append(item)
		return 0
	def dropItem(self, item):
		try:
			self.have.remove(item)
			print("Dropped.")
		except:
			print("Cannot drop item.")
