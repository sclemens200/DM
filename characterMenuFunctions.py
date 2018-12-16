import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION

from character import Character
import characterMovement
from misc import escapeCheck, quitCheck, toDisplayCoordinates
from menuAnimation import *
import viewscreen as vs


WIDTH_LOWER_LIMIT = {'Rect': 0, 'Circle': 0, 'Line': 1, 'Ellipse': 0}
WIDTH_UPPER_LIMIT = {'Rect': 9, 'Circle': 9, 'Line': 9, 'Ellipse': 9}


Font = pygame.font.Font('freesansbold.ttf', 24)



#//////////////////////////////////CHARACTER MENU FUNCTIONS///////////////////////////////////////					

def characterCreator(gamespace, maps, mainMenu, characterCreatorWithColor, undoList):
	'''
	Character Creator
	'''
	
	characterCreator, colorMenu = characterCreatorWithColor
	
	viewscreen = gamespace.viewscreen 
	displaySurf = viewscreen.displaySurf
	
	global characterSize, newCharacterName
	characterSize = 1
	newCharacterName = None
	exited = False
	
	#initial animation
	animateMenuForward(displaySurf, characterCreatorWithColor)
		
	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			# If 'Escape' is pressed close the menu and reset everything
			if escapeCheck(event) or exited:
				mainMenu.buttonUnclicked('CharacterCreator')
				animateMenuBackward(displaySurf, mainMenu, characterCreatorWithColor)
				characterCreator.imageList["Size"].update(1)
				characterCreator.buttonList['CharacterName'].reset()
				pygame.draw.rect(characterCreator.surface, characterCreator.color,
								 characterCreator.buttonList['CharacterIcon'].rect)
				return
				
			elif(event.type == MOUSEMOTION):
				if viewscreen.viewscreenRect.collidepoint(event.pos):
					vs.viewscreenHover(event.pos, gamespace)
					
			elif event.type == MOUSEBUTTONDOWN:
				if viewscreen.viewscreenRect.collidepoint(event.pos):
					vs.viewscreenHandler(event, gamespace, maps, undoList)
			
				elif characterCreator.getButtonCollision(event.pos):
					exited = characterMenuHandler(gamespace, characterCreator, event.pos)
					
				elif colorMenu.getButtonCollision(event.pos):
					gamespace.characterColor = colorMenu.buttonList[
						colorMenu.getButtonCollision(event.pos)].color
					characterCreator.imageList['ColorImage'].update(
						gamespace.characterColor, True)
							
							
def characterMenuHandler(gamespace, characterCreator, eventPosition):
	displaySurf = gamespace.viewscreen.displaySurf
	characterSpace = gamespace.characterSpace
	
	pressedButton = characterCreator.buttonList[
						characterCreator.getButtonCollision(eventPosition)].name
	
	
	global characterSize, newCharacterName

	# If 'Exit' is pressed close the menu and reset everything
	if pressedButton == 'Exit':
		return True
	
	
	#Size Handling
	#If Size is Increased or Decreased then change the size image and Draw it
	elif pressedButton == 'SizeDecrease' and characterSize > 1:
		characterSize -= 1
		characterCreator.imageList["Size"].update(characterSize, True)	
	elif pressedButton == 'SizeIncrease' and characterSize < 4:
		characterSize += 1
		characterCreator.imageList["Size"].update(characterSize, True)	
	
	#'CharacterName' is pressed
	elif pressedButton == 'CharacterName':
		result = characterCreator.buttonList['CharacterName'].getInput()
		if result != None: #handles mouse clicks from inside getInput loop
			pygame.event.post(result)

	#'NewCharacter' is pressed
	#Create new character, add them to the character space and then exit
	elif pressedButton == "NewCharacter":
		characterName = characterCreator.buttonList['CharacterName'].text
		if len(characterName) > 0 and characterSpace.nameIsNotTaken(characterName):
			newChar = Character(characterName, displaySurf,
								toDisplayCoordinates(
								characterCreator.buttonList['CharacterIcon'].rect.topleft, 
								characterCreator.rect.topleft),
								gamespace.characterColor, characterSize)
			newCharacterName = characterName
			characterSpace.addToSpace(newChar)
			characterCreator.buttonList['CharacterIcon'].update(newChar.images[1])
			characterCreator.buttonList['CharacterName'].reset()
			characterCreator.redraw()
			
	elif (pressedButton == "CharacterIcon" and newCharacterName != None
		  and gamespace.zoomLevel == 1):
		pygame.draw.rect(characterCreator.surface, characterCreator.color,
						 characterCreator.buttonList['CharacterIcon'].rect)
		characterCreator.redraw()
		
		if characterMovement.moveCharacter(newCharacterName, eventPosition, gamespace, True):
			newCharacterName = None
		
		#If the character is not added to the board we need to keep the icon where it was
		#With the draw-rect above, we did not wipe out the character icon in the button,
		#so we just re-blit the button and the icon returns.
		else:
			characterCreator.reblit()
			characterCreator.redraw()
		
		
			
	return False