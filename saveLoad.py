import pygame, os
from pygame.locals import MOUSEBUTTONDOWN
from misc import pow2, escapeCheck, quitCheck
from colors import WHITE

#import pdb;

pygame.init()
Font = pygame.font.Font('freesansbold.ttf', 24)



#/////////////////////////////////////////////SAVE////////////////////////////////////////////////
def saveGame(gamespace, maps, mainMenu, saveMenu):
	displaySurf = gamespace.viewscreen.displaySurf
	Exited = False
	
	pygame.display.update(displaySurf.blit(saveMenu.surface, saveMenu.rect)) 

	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			if escapeCheck(event) or Exited == True:
				mainMenu.buttonUnclicked('Save')
				gamespace.drawViewscreen()
				saveMenu.buttonList['SaveName'].reset()
				return
			
			elif (event.type == MOUSEBUTTONDOWN):
				if saveMenu.getButtonCollision(event.pos):
					pressedButton = saveMenu.buttonList[
										saveMenu.getButtonCollision(event.pos)].name
					Exited = saveMenuHandler(gamespace, maps, saveMenu, pressedButton)


					
def saveMenuHandler(gamespace, maps, saveMenu, pressedButton):
	if pressedButton == "Cancel":
		return True
	
	
	elif pressedButton == "Save":
		name = saveMenu.buttonList['SaveName'].text
		
		#Warning if you are about to overwrite and older save:
		# if name in os.listdir("SavedGames"):
			# pass
		
		
		if name != '':
			for i in range(3):
				level = pow2(i)
				filename = ''.join(["SavedGames\\" ,name, "_", str(level), ".png"])
				pygame.image.save(maps[level].mapSurface, filename)
			return True
			
			
	elif pressedButton == 'SaveName':
		result = saveMenu.buttonList['SaveName'].getInput()
		if result != None: #handles mouse clicks from inside getInput loop
			pygame.event.post(result)


	return False



#/////////////////////////////////////////////////LOAD////////////////////////////////////////////

	
def loadGame(gamespace, maps, mainMenu, loadMenu):
	loadMenuSuper, loadMenuSub = loadMenu
	displaySurf = gamespace.viewscreen.displaySurf
	Exited = False
	
	#we want a small dict just for keeping track of a few variables that we'll need to
	#swap back and fourth with the subfunction
	loadMenuDict = {"SelectedGame": False, "PressedButton": None, "EventPosition": None,
					"LoadGameOffset": 0, "LoadGameOffsetLimit": 0}
	
	loadMenuSubCreator(loadMenuSub, loadMenuDict)
	loadMenuSubDraw(loadMenu, displaySurf, loadMenuDict)	
			

	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			if escapeCheck(event) or Exited == True:
				mainMenu.buttonUnclicked('Load')
				gamespace.drawViewscreen()
				return
			
			elif (event.type == MOUSEBUTTONDOWN):
				if loadMenuSuper.getButtonCollision(event.pos):
					loadMenuDict["PressedButton"] = loadMenuSuper.buttonList[
												loadMenuSuper.getButtonCollision(event.pos)].name
					loadMenuDict["EventPosition"] = event.pos
					Exited = loadMenuHandler(displaySurf, maps, loadMenu, loadMenuDict)


	mainMenu.buttonUnclicked('Load')
	gamespace.drawViewscreen()
	
	
#create the loadMenuSub	
def loadMenuSubCreator(loadMenuSub, loadMenuDict):
	#determine the saved games
	savedGamesFolderContents = os.listdir("SavedGames")
	savedGameList = {}
	
	for item in savedGamesFolderContents:
		if item[-6:] == "_1.png":
			savedGameList[item[:-6]] = item
	
	loadMenuDict["LoadGameOffsetLimit"] = max(len(savedGameList) - 4, 0)
	
	#create buttons for each saved game
	loadMenuSub.buttonList = {}
	loadMenuSub.surface = pygame.Surface(
							(loadMenuSub.rect.width, 30*max(len(savedGameList), 4))).convert()
	loadMenuSub.surface.fill((255,255,255))
	i = 0
	
	for key in savedGameList:
		loadMenuSub.addTextButton(key, key, (0,i*30))
		i += 1
	loadMenuSub.blitButtons()


#blit loadMenuSub
def loadMenuSubDraw(loadMenu, displaySurf, loadMenuDict):
		
	loadMenuSuper, loadMenuSub = loadMenu
	savedGamesArea = loadMenuSuper.buttonList['SavedGames'].rect
	loadGamesRect = pygame.Rect((0, loadMenuDict["LoadGameOffset"] * 30), savedGamesArea.size)
	loadMenuSuper.surface.blit(loadMenuSub.surface, savedGamesArea, loadGamesRect)
	
	pygame.display.update(displaySurf.blit(loadMenuSuper.surface, loadMenuSuper.rect)) 
	
	
#handle button presses in the load menu	
def loadMenuHandler(displaySurf, maps, loadMenu, loadMenuDict):
	loadMenuSuper, loadMenuSub = loadMenu
	pressedButton = loadMenuDict["PressedButton"]
	selectedGame = loadMenuDict["SelectedGame"]
	
	if pressedButton == "Cancel":
		return True
	
	elif (pressedButton == "SavedGames"
		  and loadMenuSub.getButtonCollision(loadMenuDict["EventPosition"])):
		if selectedGame:
			loadMenuSub.buttonUnclicked(selectedGame, WHITE, False)
			loadMenuSubDraw(loadMenu, displaySurf, loadMenuDict)
		loadMenuDict["SelectedGame"] = loadMenuSub.getButtonCollision(
														loadMenuDict["EventPosition"])
		loadMenuSub.buttonClicked(loadMenuDict["SelectedGame"])
	
	elif pressedButton == "Load" and selectedGame:
		LoadedMap1 = pygame.image.load("SavedGames\\" + selectedGame + "_1.png")
		LoadedMap2 = pygame.image.load("SavedGames\\" + selectedGame + "_2.png")
		LoadedMap4 = pygame.image.load("SavedGames\\" + selectedGame + "_4.png")

		maps[1].mapSurface = LoadedMap1.convert()
		maps[2].mapSurface = LoadedMap2.convert()
		maps[4].mapSurface = LoadedMap4.convert()
		
		loadMenuSub.buttonUnclicked(selectedGame)
		return True
		
	elif pressedButton == "Delete" and selectedGame:
		os.remove("SavedGames\\" + selectedGame + "_1.png")
		os.remove("SavedGames\\" + selectedGame + "_2.png")
		os.remove("SavedGames\\" + selectedGame + "_4.png")
		loadMenuSubCreator(loadMenuSub, loadMenuDict)
		loadMenuSubDraw(loadMenu, displaySurf, loadMenuDict)
		
	elif pressedButton == "UpButton":
		if loadMenuDict["LoadGameOffset"] > 0:
			loadMenuDict["LoadGameOffset"] -= 1
			loadMenuSub.move((0,30))
			loadMenuSubDraw(loadMenu, displaySurf, loadMenuDict)
		
	elif pressedButton == "DownButton":
		if loadMenuDict["LoadGameOffset"] < loadMenuDict["LoadGameOffsetLimit"]:
			loadMenuDict["LoadGameOffset"] += 1
			loadMenuSub.move((0,-30))
			loadMenuSubDraw(loadMenu, displaySurf, loadMenuDict)

	return False