#/////////////////////////////////////////UNDO////////////////////////////

class UndoList:
	def __init__(self):
		self.list = []
		
	def add(self, maps):
		if len(self.list) >= 5:
			self.list.pop(0)
		self.list.append(maps)
		
	def undo(self):
		if len(self.list) > 0:
			return self.list.pop()
		return None
		
def undo(gamespace, maps, passedMenu, undoList):
	prevMaps = undoList.undo()
	if prevMaps != None:
		(prevMap1, prevMap2, prevMap4) = prevMaps
		maps[1].mapSurface = prevMap1
		maps[2].mapSurface = prevMap2
		maps[4].mapSurface = prevMap4
	passedMenu.buttonUnclicked('Undo')
	gamespace.drawViewscreen()