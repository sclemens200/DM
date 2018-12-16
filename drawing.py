import math
import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from misc import *
from constants import VIEWWIDTH, VIEWHEIGHT

FPS = 45
SCROLLSPEED = 5


pygame.init()

#///////////////////////////////////DRAWING RECT-CIRCLE-LINE//////////////////////////////////
def sketchOnMap(shape, gamespace, drawingMenu, maps, undoList, width):
	#unpacking
	map = gamespace.map
	viewscreen = gamespace.viewscreen
	color = gamespace.drawingColor
	map_initial = map.mapSurface.copy()
	zoomLevel = gamespace.zoomLevel
	
	shapeMenu, colorMenu = drawingMenu

	#booleans
	moving = False
	clicked = False
	escaped = False

	xmove, ymove = 0, 0
	
	fpsClock = pygame.time.Clock()

	while True:
		
		fpsClock.tick(FPS)
		#if the user puts the mouse to the edge of the map when drawing we want it to scroll
		if xmove or ymove:
			map.moveView(xmove, ymove)
			mousePosition = pygame.mouse.get_pos()
			if xmove > 0:
				mousePosition = (VIEWWIDTH, mousePosition[1])
				
			pos2 = map.mapCoord(mousePosition)
			map.mapSurface = map_initial.copy()
			drawShape(shape, map, pos1, pos2, color, width)
			gamespace.drawViewscreen()
			

		for event in pygame.event.get():
			quitCheck(event)
			
			if escapeCheck(event) or escaped:
				map.mapSurface = map_initial.copy()
				gamespace.drawViewscreen()
				return
			
			
			elif event.type == MOUSEBUTTONDOWN and not clicked:
				if viewscreen.viewscreenRect.collidepoint(event.pos):
					pos1 = map.mapCoord(event.pos)
					clicked = True
					undoList.add(getMapsCopy(maps))
					
				elif colorMenu.getButtonCollision(event.pos):
					gamespace.drawingColor = colorMenu.buttonList[
												colorMenu.getButtonCollision(event.pos)].color
					color = gamespace.drawingColor
					shapeMenu.imageList['ColorImage'].update(gamespace.drawingColor, True)	
					
				else:
					escaped = True

			
			elif ((event.type == MOUSEMOTION) and clicked) or moving:
				drawpoint = pygame.mouse.get_pos()
			
				#determine if mouse should scroll
				xmove, ymove = mouseOffMap(drawpoint)
				
				#if the mouse moves into the menu we don't want the drawing to continue off screen
				#since going into the menu would also cause the screen to scroll we will use that
				#to determine if the mouse is in the menu
				if xmove != 0:
					drawpoint = (VIEWWIDTH, drawpoint[1])
					
				#not in use
				# if ymove > 0:
					#drawpoint = (drawpoint[0], VIEWHEIGHT)
					
				pos2 = map.mapCoord(drawpoint)
				map.mapSurface = map_initial.copy()
				drawShape(shape, map, pos1, pos2, color, width)
				gamespace.drawViewscreen()
			
			
			elif event.type == MOUSEBUTTONUP and clicked:
				#we do not draw on the other zoom surfaces until the final shape is set
				for i in otherLevels(zoomLevel):
					modifiedWidth = width
					if width != 0:
						modifiedWidth = int(math.ceil(width * float(zoomLevel)/i))
					drawShape(shape, maps[i], zoomCoordinate(pos1, i, zoomLevel),
							  zoomCoordinate(pos2, i, zoomLevel), color, modifiedWidth)
				return
			
					



def drawShape(shape, mapObject, pos1, pos2, color, width=0):
			
	if shape == 'Rect':
		mapObject.addRect(color, getRect(pos1, pos2), width)
	elif shape == 'Circle':
		center = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
		radius = int(euclideanDistance(pos1, pos2) / 2)
		mapObject.addCircle(color, center, radius, width)
	elif shape == 'Line':
		if width == 0:
			width = 1
		mapObject.addLine(color, pos1, pos2, width)
	elif shape == 'Ellipse':
		mapObject.addEllipse(color, getRect(pos1, pos2), width)



def mouseOffMap(position):
	xmove, ymove = 0,0

	if  position[0] <= 0:
		xmove = -1*SCROLLSPEED
	elif position[0] >= VIEWWIDTH:
		xmove = SCROLLSPEED
					
	if position[1] <= 0:
		ymove = -1*SCROLLSPEED
	elif position[1] >= VIEWHEIGHT-1:
		ymove = SCROLLSPEED
		
	return xmove, ymove


#///////////////////////////////////DRAWING POLYGONS//////////////////////////////////
def sketchPolygon(gamespace, drawingMenu, maps, undoList):
		gameMap = gamespace.map #we don't want to call this 'map' as we will be using
								#the python 'map' function
		viewscreen = gamespace.viewscreen
		color = gamespace.drawingColor
		
		shapeMenu, colorMenu = drawingMenu
		
		gameMap_initial = gameMap.mapSurface.copy() # we need two maps copies here,
													# one for if user cancels
		gameMap_sketching = gameMap.mapSurface.copy() # another copy for drawing lines on 
													  # before polygon is complete
		vertexList = []
		firstPoint = True
		escaped = False
		
		while True:
		
			for event in pygame.event.get():
				quitCheck(event)
				
				if escapeCheck(event) or escaped:
					gameMap.mapSurface = gameMap_initial.copy()
					gamespace.drawViewscreen()
					return
				
				if event.type == MOUSEBUTTONDOWN:
				
					if viewscreen.viewscreenRect.collidepoint(event.pos) and firstPoint:
						vertexList.append(gameMap.mapCoord(event.pos))
						firstPoint = False
						undoList.add(getMapsCopy(maps))
						
					elif colorMenu.getButtonCollision(event.pos) and firstPoint:
						gamespace.drawingColor = colorMenu.buttonList[
							colorMenu.getButtonCollision(event.pos)].color
						color = gamespace.drawingColor
						shapeMenu.imageList['ColorImage'].update(gamespace.drawingColor, True)
						
					elif viewscreen.viewscreenRect.collidepoint(event.pos) and not firstPoint:
						#we will close the polygon if the user clicks within 5 pixels
						#of the starting point and there are at least 3 vertices
						if (euclideanDistance(vertexList[0], gameMap.mapCoord(event.pos)) < 6
							and len(vertexList) > 2):
							gameMap.mapSurface = gameMap_initial.copy()
							for i in range(3):
								func = zoomCoordinatePreset(pow2(i), gamespace.zoomLevel)
								maps[pow2(i)].addPolygon(color, map(func, vertexList))
							
							gamespace.drawViewscreen()
							return
						
						#if we are not closing the polygon then add the point to the list of
						#vertices
						else:					
							gameMap_sketching = gameMap.mapSurface.copy()
							vertexList.append(gameMap.mapCoord(event.pos))
					
					#if the user clicks outside the viewscreen then escape
					else:
						escaped = True

				
				elif event.type == MOUSEMOTION and not firstPoint:
					pos1 = vertexList[-1] #get the last vertex added
					pos2 = gameMap.mapCoord(event.pos)
					gameMap.mapSurface = gameMap_sketching.copy()
					drawShape('Line', gameMap, pos1, pos2, color)
					gamespace.drawViewscreen()
