__version__ = '1.0'
__author__ = 'Sean Clemens'
import os

import pygame
from pygame.locals import *

import character
import characterMenuFunctions
import distanceTool
import drawingMenuFunctions
import globals
import mapClass
import menuInit
import message
import saveLoad
import undo
import viewscreen

from colors import *
from constants import *
from misc import *

#import pdb; pdb.set_trace()

pygame.init()


#create display surface
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

#create Font
FONT = pygame.font.Font('freesansbold.ttf', 24)


#----------------MENU INITIALIZATION-------------------------
MAINMENU = menuInit.initMainMenu(DISPLAYSURF)

shapeMenu = menuInit.initShapeMenu(DISPLAYSURF)
colorMenu = menuInit.initColorMenu(DISPLAYSURF)
DRAWINGMENU = [shapeMenu, colorMenu]

characterCreator = menuInit.initCharacterCreator(DISPLAYSURF)
CHARACTERCREATORSUPER = [characterCreator, colorMenu]

SAVEMENU = menuInit.initSaveMenu(DISPLAYSURF)

loadMenuSuper = menuInit.initLoadMenuSuper(DISPLAYSURF)
loadMenuSub = menuInit.initLoadMenuSub(DISPLAYSURF)
LOADMENU = [loadMenuSuper, loadMenuSub]

ABOUT = menuInit.initAbout(DISPLAYSURF)

#inintialize undolist
UNDOLIST = undo.UndoList()




class Gamespace:
	'''A container to hold all the main objects that will need to be passed regularly'''
	def __init__(self, map, characterSpace, viewscreen):
		self.map = map
		self.characterSpace = characterSpace
		self.viewscreen = viewscreen
		self.zoomLevel = 1 #this will take the value of 1,2 or 4.
							#1 is the closest, 4 is the furthest out
		self.drawingColor = RED
		self.characterColor = RED
		self.hoveringOnCharacter = False #a boolean to save on map redrawing
		
	def drawViewscreen(self):
		self.viewscreen.draw((self.map, self.characterSpace, self.zoomLevel))


#//////////////////////////////////////MAIN//////////////////////////////////////////////
def main():
	#create global variables
	global GAMESPACE, MAP, CHARACTERSPACE, VIEWSCREEN, MAPS, UNDOLIST
	
	#initialize maps
	mapZoom1 = mapClass.Map((MAPWIDTH, MAPHEIGHT), 1, (VIEWWIDTH, VIEWHEIGHT), BOXSIZE)
	mapZoom2 = mapClass.Map((MAPWIDTH/2, MAPHEIGHT/2), 2, (VIEWWIDTH, VIEWHEIGHT), BOXSIZE)
	mapZoom4 = mapClass.Map((MAPWIDTH/4, MAPHEIGHT/4), 4, (VIEWWIDTH, VIEWHEIGHT), BOXSIZE)
	MAPS = {1: mapZoom1, 2: mapZoom2, 4: mapZoom4}
	
	#initialize the gamespace
	MAP = mapZoom1
	CHARACTERSPACE = character.CharacterSpace((MAPWIDTH, MAPHEIGHT))
	VIEWSCREEN = viewscreen.Viewscreen(DISPLAYSURF, VIEWRECT)
	GAMESPACE = Gamespace(MAP, CHARACTERSPACE, VIEWSCREEN) 
	
	#set name for window
	pygame.display.set_caption('DungeonMaster')
	
	#create folder for savegames if it doesn't exist
	try:
		os.mkdir("SavedGames")
	except Exception:
		pass
	
	pygame.display.update(DISPLAYSURF.fill(WHITE))
	draw()
			
	while True:
		for event in pygame.event.get():
			quitCheck(event)
			eventHandler(event)

#/////////////////////////////////////DRAW/////////////////////////////////////////////
def draw():
	GAMESPACE.drawViewscreen()
	MAINMENU.draw()
			
#/////////////////////////////////////HANDLERS////////////////////////////////////////
def eventHandler(event):

	if(event.type == MOUSEMOTION):
		if VIEWSCREEN.viewscreenRect.collidepoint(event.pos):
			viewscreen.viewscreenHover(event.pos, GAMESPACE)
			
	elif (event.type == MOUSEBUTTONDOWN):
		if MAINMENU.getButtonCollision(event.pos):
			name = MAINMENU.getButtonCollision(event.pos)
			MAINMENU.buttonClicked(name)
			menuButtonHandler(name)
			
		elif VIEWSCREEN.viewscreenRect.collidepoint(event.pos):
			viewscreen.viewscreenHandler(event, GAMESPACE, MAPS, UNDOLIST)
			
	elif (event.type == KEYDOWN):
		if event.key == K_F5:
			globals.secretButtonPressed = not globals.secretButtonPressed
			draw()
	
		elif VIEWSCREEN.viewscreenRect.collidepoint(pygame.mouse.get_pos()):
			viewscreen.viewscreenHandler(event, GAMESPACE, MAPS, UNDOLIST)


def menuButtonHandler(name):	
	if name == 'Draw':
		drawingMenuFunctions.drawingMenu(GAMESPACE, MAPS, MAINMENU, DRAWINGMENU, UNDOLIST)
	elif name == 'Distance':
		distanceTool.distanceMeasure(GAMESPACE, MAINMENU)
	elif name == 'Save':
		saveLoad.saveGame(GAMESPACE, MAPS, MAINMENU, SAVEMENU)
	elif name == 'Load':
		saveLoad.loadGame(GAMESPACE, MAPS, MAINMENU, LOADMENU)
	elif name == 'Undo':
		undo.undo(GAMESPACE, MAPS, MAINMENU, UNDOLIST)
	elif name == 'CharacterCreator':
		characterMenuFunctions.characterCreator(GAMESPACE, MAPS, MAINMENU,
												CHARACTERCREATORSUPER, UNDOLIST)
	elif name == 'About':
		message.message(GAMESPACE, MAINMENU, ABOUT, 'About')

		
		
if __name__ == '__main__':
	main()