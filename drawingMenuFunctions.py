import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION

from drawing import *
from misc import escapeCheck, quitCheck, toDisplayCoordinates
from menuAnimation import *
import undo
import viewscreen as vs


WIDTH_LOWER_LIMIT = {'Rect': 0, 'Circle': 0, 'Line': 1, 'Ellipse': 0}
WIDTH_UPPER_LIMIT = {'Rect': 9, 'Circle': 9, 'Line': 9, 'Ellipse': 9}


Font = pygame.font.Font('freesansbold.ttf', 24)


		
#//////////////////////////////////DRAWING MENU FUNCTIONS///////////////////////////////////		
			
def drawingMenu(gamespace, maps, mainMenu, drawingMenu, undolist):
	'''
	Drawing menu
	'''
	viewscreen = gamespace.viewscreen
	displaySurf = viewscreen.displaySurf
	#initial animation
	animateMenuForward(displaySurf, drawingMenu)
	global width
	width = WIDTH_LOWER_LIMIT.copy()

	
	
	while True:

		for event in pygame.event.get():
			quitCheck(event)
			
			if escapeCheck(event):
				mainMenu.buttonUnclicked('Draw')
				animateMenuBackward(displaySurf, mainMenu, drawingMenu)
				shapeWidthReset(drawingMenu)
				return
				
			elif(event.type == MOUSEMOTION):
				if viewscreen.viewscreenRect.collidepoint(event.pos):
					vs.viewscreenHover(event.pos, gamespace)
			
			elif (event.type == MOUSEBUTTONDOWN):
				if viewscreen.viewscreenRect.collidepoint(event.pos):
					vs.viewscreenHandler(event, gamespace, maps, undolist)
				
				else:
					drawingMenuSubFunction(event, gamespace, maps, mainMenu, drawingMenu,
										   undolist)


					
def drawingMenuSubFunction(event, gamespace, maps, mainMenu, drawingMenu, undolist):
	shapeMenu, colorMenu = drawingMenu
	global width
	
	if shapeMenu.getButtonCollision(event.pos):
			shape = shapeMenu.buttonList[shapeMenu.getButtonCollision(event.pos)].name
			shapeMenu.buttonClicked(shape)
			if shape == 'Undo':
				undo.undo(gamespace, maps, shapeMenu, undolist)
			elif shape == 'Polygon':
				sketchPolygon(gamespace, drawingMenu, maps, undolist)
			elif shape in ('Rect', 'Circle', 'Line', 'Ellipse'):
				sketchOnMap(shape, gamespace, drawingMenu, maps, undolist, width[shape])
			
			else:
				suffix = shape[-12:]
				shape = shape[:-12]
				
				if suffix == 'SizeDecrease' and width[shape] > WIDTH_LOWER_LIMIT[shape]:
					width[shape] -= 1
					shapeMenu.imageList[shape+"Size"].update(width[shape], True)
				elif suffix == 'SizeIncrease' and width[shape] < WIDTH_UPPER_LIMIT[shape]:
					width[shape] += 1
					shapeMenu.imageList[shape+"Size"].update(width[shape], True)

			shapeMenu.buttonUnclicked(shape)

	elif colorMenu.getButtonCollision(event.pos):
			gamespace.drawingColor = colorMenu.buttonList[
				colorMenu.getButtonCollision(event.pos)].color
			shapeMenu.imageList['ColorImage'].update(gamespace.drawingColor, True)
			

def shapeWidthReset(drawingMenu):
	shapeMenu, colorMenu = drawingMenu
	shapeMenu.imageList["LineSize"].update(1)
	for shape in ('Rect', 'Circle', 'Ellipse'):
		shapeMenu.imageList[shape+"Size"].update(0)

