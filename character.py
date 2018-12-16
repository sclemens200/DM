import pygame

from colors import *
from constants import BOXSIZE, VIEWWIDTH
from misc import pow2, zoomCoordinate

MAX_NUMBER_OF_CHARACTERS = 20

pygame.init()


def characterImage(initial, color, dimension):
	#set the underlying surface, it will be transparent
	image = pygame.Surface((dimension,dimension))
	image.fill(UGLY) # UGLY is the "ugliest known color"
	image.set_colorkey(UGLY)
	
	#add circle to surface
	pygame.draw.circle(image, color, ((dimension)/2,(dimension)/2), (dimension)/2)
	if color == WHITE: #Draw a blank outline of the circle
		pygame.draw.circle(image, BLACK, ((dimension)/2,(dimension)/2), (dimension)/2, 2)
	
	#add initial to surface of character image is big enough (at least BOXSIZE)
	if dimension >= BOXSIZE:
		Font = pygame.font.Font('freesansbold.ttf', int(24*(dimension/float(BOXSIZE))))
		
		if color in (BLACK, CHARCOAL, DARKTURQUOISE, NAVY, PRUSSIANBLUE, TYRIANPURPLE, WEBINDIGO):
		#colors where black text is less readable
			text = Font.render(initial, 1, WHITE)
		else:
			text = Font.render(initial, 1, BLACK)
		textRect = text.get_rect()
		textRect.center = (dimension/2,dimension/2)
		image.blit(text, textRect)
	
	return image


class Character:
	def __init__(self, name, displaySurface, location, color = RED, size = 1):
		self.name = name
		self.initial = name[0]
		self.displaySurface = displaySurface
		self.boxsize = BOXSIZE
		self.color = color
		self.size = size
		self.dimension = self.boxsize*size
		self.onField = False
		#need three images and three rects, one for each zoomlevel
		self.rects = {}
		for i in range(3):
			self.rects[pow2(i)] = pygame.Rect(location, (self.dimension/pow2(i),
											  self.dimension/pow2(i)))
		self.images = {}
		for i in range(3):
			self.images[pow2(i)] = characterImage(self.initial, self.color,
												  self.dimension/pow2(i))
	
	#rather than using the topleft corner to determine where a character lands we use the
	#center as it is more intuitive
	def relocate(self, coordinate):
		x,y = pygame.Rect(coordinate, (self.boxsize, self.boxsize)).center 													
		self.rects[1].topleft = (x - x%self.boxsize, y - y%self.boxsize)
		self.rects[2].topleft = zoomCoordinate(self.rects[1].topleft, 2, 1)
		self.rects[4].topleft = zoomCoordinate(self.rects[1].topleft, 4, 1)

	#we need map independent character drawing for when the player is moving the character,
	#since this will only be done at zoom = 1 we needn't account for zoomLevel		
	def draw(self, loaction):
		self.displaySurface.blit(self.image[0], location)
	
	#translates a rect or coordinate as though the character topleft is (0,0)
	def characterRelativeRect(self, object, zoomLevel):
		if (type(object) == pygame.Rect):
			rect = object.copy()
			rect.left -= self.rects[zoomLevel].left
			rect.top -= self.rects[zoomLevel].top
			return rect
		else:
			(x1, y1) = object
			x1 -= self.rects[zoomLevel].left
			y1 -= self.rects[zoomLevel].top
			return (x1, y1)
	
	#when the mouse hovers over a character, draw character name onscreen
	def mouseHover(self, characterSpace, zoomLevel):
		Font = pygame.font.Font('freesansbold.ttf', 24)
		hoverName = Font.render(self.name, 1, BLACK)
		hoverNameRect = hoverName.get_rect()
		hoverNameRect.bottomleft = characterSpace.viewscreenCoord(self.rects[zoomLevel].center)
		
		#some adjustments to keep the name on the viewscreen
		if hoverNameRect.bottom < self.boxsize:
			hoverNameRect.top = characterSpace.viewscreenCoord((0,
									self.rects[zoomLevel].centery))[1]
			#the mouse tends to cover part of it which annoys me, this helps
			if hoverNameRect.left > hoverNameRect.width:
				hoverNameRect.right = characterSpace.viewscreenCoord((
										self.rects[zoomLevel].centerx, 0))[0]
		elif hoverNameRect.left > VIEWWIDTH - hoverNameRect.width:
			hoverNameRect.right = characterSpace.viewscreenCoord((
										self.rects[zoomLevel].centerx, 0))[0]
		
		if hoverNameRect.left < 0: #for those stupidly long names
				hoverNameRect.centerx = VIEWWIDTH/2
		
		pygame.draw.rect(self.displaySurface, WHITE, hoverNameRect)
		pygame.display.update(self.displaySurface.blit(hoverName, hoverNameRect)) 
		
#///////////////////////////////////////////////CHARACTER SPACE///////////////////////////////////		

class CharacterSpace:
	'''
	The characterSpace is the overal container for character related objects
	'''
	def __init__(self, dimensions, boxsize = BOXSIZE):
		self.viewRect = pygame.Rect((0,0), dimensions)
		self.boxsize = boxsize
		self.maxLength = MAX_NUMBER_OF_CHARACTERS
		self.list = {}
		
	def move(self, newPosition):
		self.viewRect.topleft = newPosition

	#this converts the mouse coord on the displaysurf into a coord on the map		
	def mapCoord(self, object):
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
	
	#the inverse of mapCoord, this converts a coord on the map to the displaysurf	
	def viewscreenCoord(self, object):
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
	
	
	#functions for adding/removing characters to the CharacterSpace		
	def addToSpace(self, character):
		if len(self.list) < MAX_NUMBER_OF_CHARACTERS:
			self.list[character.name] = character
			return True
		else:
			return False
		
	def clearFromSpace(self, characterName):
		self.list.pop(characterName)
		
	
	#functions for adding/removing characters to the Map	
	def addToField(self, characterName):
		self.list[characterName].onField = True
		
	def clearFromField(self, characterName):
		self.list[characterName].onField = False
	
	
	#for use when moving a character, to make sure the destination is unoccupied
	def occupied(self, characterRect, zoomLevel = 1):
		#As characters can be size > 1 we need a way of handling that situation, otherwise 
		#checking if the center collided would be sufficient.  Thus we create an internal 
		#rectangle that is BOXSIZE less than the original on each side but shares
		#the same center as the character
		rect = pygame.Rect(0, 0, characterRect.width-self.boxsize,
						   characterRect.height-self.boxsize)
		rect.center = characterRect.center
		
		for key in self.list.keys():
			if self.list[key].rects[zoomLevel].colliderect(rect) and self.list[key].onField:
				return True
		return False
	
	#to determine what character the mouse is on
	def getCharacterCollision(self, pos, zoomLevel = 1):
		for key in self.list.keys():
			if (self.list[key].rects[zoomLevel].collidepoint(self.mapCoord(pos)) and 
				self.list[key].onField):
				return self.list[key].name
		return None
	
	#to ensure each Character has a unique name
	def nameIsNotTaken(self, name):
		for key in self.list.keys():
			if name == key:
				return False
		return True
	
	#drawing Characters
	def drawCharacters(self, displaySurf, zoomLevel):
		for key in self.list.keys():
			if (self.list[key].rects[zoomLevel].colliderect(self.viewRect) and 
				self.list[key].onField):
				viewableRect = self.viewRect.clip(self.list[key].rects[zoomLevel])
				viewscreenViewableRect = self.viewscreenCoord(viewableRect)
				visiblePortionOfCharacter = self.list[key].characterRelativeRect(
											viewableRect, zoomLevel)
				displaySurf.blit(self.list[key].images[zoomLevel], viewscreenViewableRect,
								 visiblePortionOfCharacter)
		