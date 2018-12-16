import pygame
from pygame.locals import MOUSEBUTTONDOWN

from misc import quitCheck

def message(gamespace, mainMenu, message, messageButton):

	displaySurf = gamespace.viewscreen.displaySurf
	
	pygame.display.update(displaySurf.blit(message.surface, message.rect)) 

	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			if (event.type == MOUSEBUTTONDOWN) and message.getButtonCollision(event.pos):
				mainMenu.buttonUnclicked(messageButton)
				gamespace.drawViewscreen()
				return