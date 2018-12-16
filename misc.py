#/////////////////////////////////////MISC///////////////////////////////////////////
import math
import sys

import pygame
from pygame.locals import *


		
def escapeCheck(event):
	if event.type == KEYDOWN:
		if event.key == K_ESCAPE:
			return True
			
	if event.type == MOUSEBUTTONDOWN:
		if event.button == 3:
			return True
	return False
	
def euclideanDistance(coord1, coord2):
	(x1, y1) = coord1
	(x2, y2) = coord2
	return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))

def getMaps(maps):
	return (maps[1].mapSurface, maps[2].mapSurface, maps[4].mapSurface)

def getMapsCopy(maps):
	return (maps[1].mapSurface.copy(), maps[2].mapSurface.copy(), maps[4].mapSurface.copy())
	
def getRect(coord1, coord2):
	(x1, y1) = coord1
	(x2, y2) = coord2
	return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1-x2), abs(y1-y2))
	
def log2(i):
	return int(math.log(i,2))
	
def nonEuclideanDistance(coord1, coord2):
	(x1, y1) = coord1
	(x2, y2) = coord2
	return max(abs(x1-x2), abs(y1-y2))
	
def otherLevels(zoomLevel):
	levels = set([1,2,4])
	return levels - set([zoomLevel])
	
def pow2(i):
	return int(pow(2,i))
	
def quitCheck(event):
	if event.type == QUIT:
		pygame.quit()
		sys.exit()

def toDisplayCoordinates(topleft,pos):
		return (pos[0] + topleft[0], pos[1] + topleft[1])	
		
def zoomCoordinate(position, mapZoomLevel, zoomLevel):
	x, y = position
	return (x*zoomLevel/mapZoomLevel, y*zoomLevel/mapZoomLevel)
	
def zoomCoordinatePreset(mapZoomLevel, zoomLevel):
	return lambda position : zoomCoordinate(position, mapZoomLevel, zoomLevel)

