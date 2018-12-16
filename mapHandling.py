import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONUP

from colors import BLACK
from constants import VIEWWIDTH, VIEWHEIGHT
from misc import *
import textInput

pygame.init()
#////////////////////////////////MAP MOVEMENT//////////////////////////////////////////
		
def dragMap(eventpos, gamespace):
	map = gamespace.map
	xpos1, ypos1 = eventpos
	while True:
		
		for event in pygame.event.get():
			quitCheck(event)
			
			if (event.type == MOUSEMOTION):
				xpos2, ypos2 = event.pos
				xchange, ychange = xpos1 - xpos2, ypos1 - ypos2
				map.moveView(xchange, ychange)
				gamespace.characterSpace.move(map.getLocation())
				gamespace.drawViewscreen()
				xpos1, ypos1 = xpos2, ypos2
						
			elif event.type == MOUSEBUTTONUP:
				return
				
#////////////////////////////////ZOOM//////////////////////////////////////////				
def zoomIn(eventPos, gamespace, maps):
	zoomLevel = gamespace.zoomLevel
	if zoomLevel > 1:
		zoomLevel /= 2
		map = gamespace.map
		x, y = map.mapCoord(eventPos)
		newCenter = (x*2, y*2)
		gamespace.map = maps[zoomLevel]
		gamespace.map.recenterView(newCenter)
		gamespace.characterSpace.viewRect = gamespace.map.viewRect
		gamespace.zoomLevel = zoomLevel
		gamespace.drawViewscreen()
		
def zoomOut(eventPos, gamespace, maps):
	zoomLevel = gamespace.zoomLevel
	if zoomLevel < 4:
		zoomLevel *= 2
		map = gamespace.map
		x, y = map.mapCoord(eventPos)
		newCenter = (x/2, y/2)
		gamespace.map = maps[zoomLevel]
		gamespace.map.recenterView(newCenter)
		gamespace.characterSpace.viewRect = gamespace.map.viewRect
		gamespace.zoomLevel = zoomLevel
		gamespace.drawViewscreen()
		
		
#////////////////////////////////ANNOTATE/////////////////////////////////////////////////////////
def annotate(eventPos, gamespace, maps, undoList):
	displaySurf = gamespace.viewscreen.displaySurf
	map = gamespace.map
	zoomLevel = gamespace.zoomLevel
	if eventPos[0] < VIEWWIDTH/2:
		textEntryBox = textInput.TextInput("TextEntryBox", displaySurf, (0,0),
										   displaySurf, pygame.Rect(eventPos, (200,30))
										   )
	else:
		textEntryBox = textInput.TextInput("TextEntryBox", displaySurf, (0,0),
										   displaySurf,
										   pygame.Rect((eventPos[0]-200, eventPos[1]), (200,30))
										   )
	textEntryBox.draw()
	textEntryBox.getInput()
	text = textEntryBox.text

	undoList.add(getMapsCopy(maps))
	
	for i in (1,2,4):
		mapPos = map.mapCoord(eventPos)
		maps[i].addText(text, zoomCoordinate(mapPos, i, zoomLevel),
							  BLACK, 28/i)
							  
	
	gamespace.drawViewscreen()
	