#///////////////////////////////////DISTANCE TOOL//////////////////////////////////////
import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from colors import *
from misc import nonEuclideanDistance, quitCheck

pygame.init()

FONT = pygame.font.Font('freesansbold.ttf', 24)

def distanceMeasure(gamespace, mainMenu):
	'''Tool to get distance in non-euclidean space'''
	distanceToolColor = RED
	map = gamespace.map
	map_Initial = map.mapSurface.copy()
	clicked = False

	
	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			if event.type == MOUSEBUTTONDOWN:
				startpos = map.mapCoord(event.pos)
				startBox = map.getBoxAtCoord(event.pos)
				clicked = True
			
			elif event.type == MOUSEMOTION and clicked:
				endpos = map.mapCoord(event.pos)
				endBox = map.getBoxAtCoord(event.pos)
				dist = nonEuclideanDistance(startBox, endBox)
				distBox = FONT.render(str(dist), 1, BLACK)
				distBoxRect = distBox.get_rect(topleft = map.mapCoord(event.pos))
				distBoxRect.top += 10
				distBoxRect.left -= 10
				
				map = gamespace.map

				map.mapSurface = map_Initial.copy()
				map.addCircle(distanceToolColor, startpos, 3)
				map.addLine(distanceToolColor, startpos, endpos)
				map.addCircle(distanceToolColor, endpos, 3)
				map.mapSurface.blit(distBox, distBoxRect)
				gamespace.drawViewscreen()
				
			elif event.type == MOUSEBUTTONUP and clicked:
				map.mapSurface = map_Initial.copy()
				gamespace.drawViewscreen()
				mainMenu.buttonUnclicked('Distance')
				return
