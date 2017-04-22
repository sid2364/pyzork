
class Player:
	def __init__(self, position="start", have=[], direction="north"):
		self.position = position
		self.have = have
		self.direction = direction
		print(self.position, self.have, self.direction)
	def moveToNewState(self, position, direction):
		self.position = position
		self.direction = direction
	def takeItem(self, item):
		if item in self.have:
			return 1
		self.have.append(item)
		return 0
	def dropItem(self, item):
		try:
			self.have.pop(item)
		except:
			return 1
		return 0
