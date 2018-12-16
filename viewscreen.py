import pygame
from pygame.locals import *

import characterMovement
import globals
import mapHandling
from colors import *
from constants import BOXSIZE

pygame.init()

class Viewscreen:
	def __init__(self, displaySurf, viewscreenRect, boxsize = BOXSIZE):
		self.leftAdjust = 0
		self.topAdjust = 0
		self.viewscreenRect = viewscreenRect
		self.leftMargin = viewscreenRect.left
		self.topMargin = viewscreenRect.top
		self.width = viewscreenRect.width
		self.height = viewscreenRect.height
		self.boxsize = boxsize
		self.fovcols = self.width/self.boxsize
		self.fovrows = self.height/self.boxsize
		self.mapLocation = (0,0, self.width, self.height)
		self.displaySurf = displaySurf
	
	def drawGrid(self, mapObject):
		#draw grid
		for i in range(self.fovcols):
			xcoord = self.leftMargin + (i+1)*self.boxsize - mapObject.viewRect.left%self.boxsize
			pygame.draw.line(self.displaySurf, BLACK, (xcoord, self.topMargin), 
							(xcoord, self.topMargin+self.height)
							)
		for j in range(self.fovrows):
			ycoord = self.topMargin + (j+1)*self.boxsize - mapObject.viewRect.top%self.boxsize
			pygame.draw.line(self.displaySurf, BLACK, (self.leftMargin, ycoord),
							(self.leftMargin+self.width, ycoord)
							)
		
	def drawFrame(self):
		#frame around the grid
		pygame.draw.rect(self.displaySurf, BLACK, self.viewscreenRect, 3)
		
	def draw(self, tuple):
		(map, characterSpace, zoomLevel) = tuple
		self.displaySurf.blit(map.mapSurface, self.viewscreenRect, (map.getLocation(),
							 (self.width, self.height))
							 )
		self.drawGrid(map)
		characterSpace.drawCharacters(self.displaySurf, zoomLevel)
		self.drawFrame()
		pygame.display.update(self.viewscreenRect)

		
	

def viewscreenHandler(event, gamespace, maps, undoList):
	if event.type == MOUSEBUTTONDOWN:
		if event.button == 4:
			mapHandling.zoomIn(event.pos, gamespace, maps)
		
		elif event.button == 5:
			mapHandling.zoomOut(event.pos, gamespace, maps)
			
		elif event.button == 3 and globals.secretButtonPressed:
			mapHandling.annotate(event.pos, gamespace, maps, undoList)
		
		else:
			viewscreenGrab(event.pos, gamespace)

	if event.type == KEYDOWN:
		if event.key == K_z:
			mapHandling.zoomIn(pygame.mouse.get_pos(), gamespace, maps)
			
		elif event.key == K_x:
			mapHandling.zoomOut(pygame.mouse.get_pos(), gamespace, maps)			

		
def viewscreenGrab(position, gamespace):
	#we only allow character movement in the closest zoom
	if gamespace.zoomLevel == 1:
		name = gamespace.characterSpace.getCharacterCollision(position)
		if name == None:
			mapHandling.dragMap(position, gamespace)
		else:
			characterMovement.moveCharacter(name, position, gamespace)			
	else:
		mapHandling.dragMap(position, gamespace)
		
def viewscreenHover(position, gamespace):
	characterSpace = gamespace.characterSpace
	zoomLevel = gamespace.zoomLevel

	if gamespace.hoveringOnCharacter: #redraw screen only if last hovering over a character
		gamespace.drawViewscreen()
	
	name = characterSpace.getCharacterCollision(position, zoomLevel)
	if name != None:
		characterSpace.list[name].mouseHover(characterSpace, zoomLevel)
		gamespace.hoveringOnCharacter = True
		
	elif gamespace.hoveringOnCharacter:
		gamespace.hoveringOnCharacter = False