import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONUP

from misc import quitCheck, zoomCoordinate


#/////////////////////////////////CHARACTER MOVEMENT////////////////////////////////////
def moveCharacter(name, mousePosition, gamespace, newCharacter = False):

	fpsClock = pygame.time.Clock()
	(xpos1, ypos1) = mousePosition
	characterSpace = gamespace.characterSpace
	displaySurf = gamespace.viewscreen.displaySurf
	
	character = characterSpace.list[name]
	if newCharacter:
		characterRect = character.rects[1]
	else:
		characterRect = characterSpace.viewscreenCoord(character.rects[1])
	
	initialCharacterRect = characterRect.copy() #if the character doesn't move
	characterImage = character.images[1]
	
	#A current character (newCharacter = False) needs to be taken off the surface
	characterSpace.clearFromField(name)
		
	gamespace.drawViewscreen()
	displaySurfCopy = displaySurf.copy()
	
	moved = False #boolean stating if the character was successfully moved to a new location
	newCharNotMoved = False
	
	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			if (event.type == MOUSEMOTION):
				#blank out the Character's last location
				pygame.display.update(displaySurf.blit(displaySurfCopy, characterRect,
													   characterRect)
									  )
				
				xpos2, ypos2 = event.pos
				xchange, ychange = xpos2 - xpos1, ypos2 - ypos1
				characterRect.left += xchange
				characterRect.top += ychange
				pygame.display.update(displaySurf.blit(characterImage, characterRect))
				xpos1, ypos1 = xpos2, ypos2
			
			
			elif event.type == MOUSEBUTTONUP:
				#if the character is dropped off the viewscreen,
				#remove from characterSpace and take off map
				if event.pos[0] >= gamespace.viewscreen.width:
					if not newCharacter:
						characterSpace.list.pop(name)
					else:
						newCharNotMoved = True
					pygame.display.update(displaySurf.blit(displaySurfCopy,
														   characterRect,
														   characterRect)
														   )

				#else, determine if the location is occupied
				#if not move character to that location
				else:
					if not characterSpace.occupied(characterSpace.mapCoord(characterRect)):
						character.relocate(characterSpace.mapCoord(characterRect).topleft)
						moved = True
							
					#moved or not a current character should be readded to the surface
					#if the character is new and the space is occupied (moved = False), 
					#then we don't want them to be added to the surface
					if not newCharacter or moved:
						characterSpace.addToField(name)
					
					
					elif newCharacter and not moved:
						newCharNotMoved = True
				
				#if the character was not moved we need to make sure it returns
				#to the correct spot
				if newCharNotMoved:
					character.rects[1] = initialCharacterRect.copy()
					gamespace.drawViewscreen()
			
				return moved
					
		fpsClock.tick(45)