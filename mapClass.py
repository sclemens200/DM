import pygame
from colors import *

class Map:

	def __init__(self, dimensions, zoomLevel, viewDimensions, boxsize, color = WHITE):
		self.width, self.height = dimensions
		self.zoomLevel = zoomLevel
		self.viewRect = pygame.Rect((0,0), viewDimensions) #this keeps track of where the 
															#viewscreen is over the map
		self.boxsize = boxsize
		self.mapSurface = pygame.Surface(dimensions).convert()
		self.mapSurface.fill(color)
		
		
	def moveView(self, xchange, ychange):
		self.viewRect.left += xchange
		if self.viewRect.left < 0:
			self.viewRect.left = 0		
		elif self.viewRect.left >= self.width-self.viewRect.width:
			self.viewRect.left = self.width-self.viewRect.width
		
		self.viewRect.top += ychange
		if self.viewRect.top < 0:
			self.viewRect.top = 0
		elif self.viewRect.top >= self.height-self.viewRect.height:
			self.viewRect.top = self.height-self.viewRect.height
			
	def recenterView(self, position):
		self.viewRect.center = position
		
		if self.viewRect.left < 0:
			self.viewRect.left = 0		
		elif self.viewRect.left >= self.width-self.viewRect.width:
			self.viewRect.left = self.width-self.viewRect.width
			
		if self.viewRect.top < 0:
			self.viewRect.top = 0
		elif self.viewRect.top >= self.height-self.viewRect.height:
			self.viewRect.top = self.height-self.viewRect.height
			
	def getLocation(self):
		return self.viewRect.topleft
		
	def mapCoord(self, object):
		#this converts the mouse coord on the displaysurf into a coord on the map surface
		if (type(object) == pygame.Rect):
			rect = object.copy()
			rect.left += self.viewRect.left
			rect.top += self.viewRect.top
			return rect
		else:
			(x1, y1) = object
			x1 += self.viewRect.left
			y1 += self.viewRect.top
			return (x1, y1)
		
	def viewscreenCoord(self, object):
		#the inverse of mapCoord, this converts a coord or rect on the map
		#to the viewscreen(display)
		if (type(object) == pygame.Rect):
			rect = object.copy()
			rect.left -= self.viewRect.left
			rect.top -= self.viewRect.top
			return rect
		else:
			(x1, y1) = object
			x1 -= self.viewRect.left
			y1 -= self.viewRect.top
			return (x1, y1)
		
	def getBoxAtCoord(self, coord):
		(xcoord, ycoord) = self.mapCoord(coord)
		return (xcoord/self.boxsize, ycoord/self.boxsize)
		
	# def zoomCoordinate(coordinate, zoomLevel):
		# #function for determine the corresponding coordinate on a different zoomLevel
		# x,y = coordinate
		# return (x*zoomLevel/self.zoomLevel, y*zoomOutLevel/self.zoomLevel)
		
		
		
	#Map Sketching Tools	
	def addRect(self, color, rect, width=0):
		#rect = self.mapCoord(rect)
		if width == 0:
			self.mapSurface.fill(color, rect)
		
		else:
			surf = pygame.Surface(rect.size).convert()
			surf.set_colorkey(UGLY)
			surf.fill(color)
			surf.fill(UGLY, pygame.Rect(2*width,2*width, rect.width-4*width, rect.height-4*width))
			self.mapSurface.blit(surf, rect)
	
	
	def addCircle(self, color, center, radius, width=0):
		#center = self.mapCoord(center)
		if radius-2*width <= 0:
			width = 0
		
		if width == 0:
			pygame.draw.circle(self.mapSurface, color, center, radius)
			
		else:
			surf = pygame.Surface((radius*2, radius*2)).convert()
			surf.fill(UGLY)
			surf.set_colorkey(UGLY)
			pygame.draw.circle(surf, color, (radius, radius), radius)
			pygame.draw.circle(surf, UGLY, (radius, radius), radius-2*width)
			self.mapSurface.blit(surf, pygame.Rect(center[0]-radius, center[1]-radius, radius*2,
								 radius*2)
								 )


	def addLine(self, color, startpos, endpos, thickness = 1):
		pygame.draw.line(self.mapSurface, color, startpos, endpos, thickness*2)
		
	#if you intend to draw a line of thickness = 1 it is best to use aaline
	def addAALine(self, color, startpos, endpos, blend = 0):
		pygame.draw.aaline(self.mapSurface, color, startpos, endpos, 0)
		
		
	def addPolygon(self, color, vertexlist):
		#pygame.draw.polygon(self.mapSurface, color, map(self.mapCoord, vertexlist))
		pygame.draw.polygon(self.mapSurface, color, vertexlist)
		
		
	def addEllipse(self, color, rect, width=0):
		if rect.width-4*width <= 0 or rect.height-4*width <= 0:
			width = 0
		
		if width == 0:
			pygame.draw.ellipse(self.mapSurface, color, rect)
			
		else:
			surf = pygame.Surface(rect.size).convert()
			surf.set_colorkey(UGLY)
			surf.fill(UGLY)
			pygame.draw.ellipse(surf, color, pygame.Rect(0, 0, rect.width, rect.height))
			pygame.draw.ellipse(surf, UGLY, pygame.Rect(2*width,2*width, rect.width-4*width,
								rect.height-4*width)
								)
			self.mapSurface.blit(surf, rect)


	def addText(self, text, center, color, fontSize):
		Font = pygame.font.Font('freesansbold.ttf', fontSize)
		textBlock = Font.render(text, 1, color)
		textBlockRect = textBlock.get_rect()
		textBlockRect.center = center
		self.mapSurface.blit(textBlock, textBlockRect)
		