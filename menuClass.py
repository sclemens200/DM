import pygame

import globals
from colors import *
from textInput import TextInput
from misc import toDisplayCoordinates

pygame.init()
Font = pygame.font.Font('freesansbold.ttf', 28)

#at the moment clicking a button will switch its background color
CLICKED_COLOR = CYAN

class MenuClass:
	def __init__(self, name, displaySurface, menuRect, color = GRAY, borderColor = None):
		self.name = name
		self.rect = menuRect
		self.topleft = menuRect.topleft
		self.width = menuRect.width
		self.height = menuRect.height
		self.color = color
		self.surface = pygame.Surface((self.width, self.height)).convert()
		self.surface.fill(color)
		if borderColor != None:
			pygame.draw.rect(self.surface, borderColor,
							 pygame.Rect(0,0,self.width, self.height), 5)
		self.displaySurface = displaySurface
		self.buttonList = {}
		self.imageList = {}
		
	def addButton(self, name, location, dimensions, color = None, borderColor = None,
				  revealed = True):
		if color == None:
			color = WHITE
		if borderColor == None:
			borderColor = BLACK
			
		self.buttonList[name] = Button(name, self.surface, location, dimensions, color,
									   borderColor)
		#self.buttonList[name].draw()
		
	def addTextButton(self, name, text, location, dimensions = None, color = None,
					  borderColor = None, textColor = BLACK, revealed = True):
		if dimensions == None:
			dimensions = (1,1)
		if color == None:
			color = WHITE
		if borderColor == None:
			borderColor = BLACK
			
		self.buttonList[name] = TextButton(name, text, self.surface, location,
										   dimensions, color, borderColor)
		#self.buttonList[name].draw()
	
	def toMenuCoordinates(self, object):
		#this converts a coord on the menu into a coord on the display surface
		#This will be important to get accurate collision detection with pygame's collidepoint
		if (type(object) == pygame.Rect):
			rect = object.copy()
			rect.left -= self.rect.left
			rect.top -= self.rect.top
			return rect
		else:
			(x,y) = object
			x -= self.rect.left
			y -= self.rect.top
			return (x, y)	
		
	def toDisplayCoordinates(self, object):
		#this converts a coord on the menu into a coord on the display surface
		if (type(object) == pygame.Rect):
			rect = object.copy()
			rect.left += self.rect.left
			rect.top += self.rect.top
			return rect
		else:
			(x, y) = object
			x += self.rect.left
			y += self.rect.top
			return (x, y)	
		
		
	def getButtonCollision(self, pos):
		for key in self.buttonList.keys():
			if (self.buttonList[key].rect.collidepoint(self.toMenuCoordinates(pos))
				and (self.buttonList[key].revealed or globals.secretButtonPressed)
				):
				return self.buttonList[key].name
		return None
		
	def blitButtons(self):
		for key in self.buttonList.keys():
			if self.buttonList[key].revealed or globals.secretButtonPressed:
				self.buttonList[key].draw()
			
	def blitImages(self):
		for key in self.imageList.keys():
			if self.imageList[key].revealed or globals.secretButtonPressed:
				self.imageList[key].draw()
		
	def draw(self):
		self.surface.fill(self.color)
		self.blitButtons()
		pygame.display.update(self.displaySurface.blit(self.surface, self.topleft))
		
	def redraw(self):
		pygame.display.update(self.displaySurface.blit(self.surface, self.topleft))
		
	def reblit(self):
		self.blitButtons()
		
	def buttonClicked(self, buttonName, color = CLICKED_COLOR):
		self.buttonList[buttonName].clicked = True
		self.buttonList[buttonName].color = color
		self.buttonList[buttonName].draw()
		pygame.display.update(self.displaySurface.blit(
							  self.surface, self.toDisplayCoordinates(
							  self.buttonList[buttonName].rect), self.buttonList[buttonName].rect)
							  )
		
	def buttonUnclicked(self, buttonName, color = WHITE, redraw = True):
		self.buttonList[buttonName].clicked = False
		self.buttonList[buttonName].color = color
		self.buttonList[buttonName].draw()
		if redraw:
			pygame.display.update(self.displaySurface.blit(
								  self.surface, self.toDisplayCoordinates(
								  self.buttonList[buttonName].rect),
								  self.buttonList[buttonName].rect)
								  )
															
															
	def move(self, change):
		(leftChange, topChange) = change
		self.rect.left += leftChange
		self.rect.top += topChange
		self.topleft = self.rect.topleft

		
		
#//////////////////////////////BUTTONS/////////////////////////////////

class Button:
	def __init__(self, name, menuSurface, location, dimensions, color = WHITE,
				 borderColor = BLACK, revealed = True):
		self.name = name
		self.rect = pygame.Rect(location, dimensions)
		self.menuSurface = menuSurface
		self.color = color
		self.borderColor = borderColor
		self.clicked = False
		self.revealed = revealed
			
	def relocate(self, topleft):
		self.rect.topleft = topleft
		
	def draw(self):
		pygame.draw.rect(self.menuSurface, self.color, self.rect)
		pygame.draw.rect(self.menuSurface, self.borderColor, self.rect, 2)

		
class ImageButton(Button):
	def __init__(self, name, image, menuSurface, location, revealed = True):
		Button.__init__(self, name, menuSurface, location, (0,0), WHITE, BLACK, revealed)
		self.image = image
		self.rect = image.get_rect(topleft = location)
		
	def update(self, image):
		self.image = image
		self.rect = image.get_rect(topleft = self.rect.topleft)
		self.menuSurface.blit(self.image, self.rect)
		#Because of how we set up our menus we don't really want button sizes changing once set
		#hence this function should only be used to switch to an image of the same size
		
	def draw(self):
		self.menuSurface.blit(self.image, self.rect)
				
	
class TextButton(Button):
	def __init__(self, name, text, menuSurface, location, dimensions = (0,0), color = WHITE,
				 borderColor = BLACK, textColor = BLACK, centered = False, revealed = True):
		Button.__init__(self, name, menuSurface, location, dimensions, color, borderColor, 
						revealed)
		self.image = Font.render(text, 1, textColor)
		self.rect = self.image.get_rect(topleft = location)
		if centered:
			self.rect.center = location
		
	def draw(self):
		pygame.draw.rect(self.menuSurface, self.color, self.rect)
		pygame.draw.rect(self.menuSurface, self.borderColor, self.rect.inflate(2,2), 2)
		self.menuSurface.blit(self.image, self.rect)


#/////////////////////////////DISPLAY///////////////////////////////////////
'''
If we don't want a button but rather to display an Image we can use this class
'''

class Display: #base class for the following classes
	def __init__(self, name, parentMenu, location, revealed = True):
		self.name = name
		self.rect = pygame.Rect(location, (0,0)) #rect size will be adjusted later
		self.menuSurface = parentMenu.surface
		self.menuColor = parentMenu.color
		self.menuTopLeft = parentMenu.topleft
		self.displaySurface = parentMenu.displaySurface
		self.revealed = revealed

		
class PresetDisplay(Display):
	'''
	A display that can change between a finite number predefined images
	'''	
	def __init__(self, name, imageList, parentMenu, location, revealed = True):
		Display.__init__(self, name, parentMenu, location, revealed)
		self.imageNumber = min(imageList.keys())
		self.imageList = imageList
		
		#find rect that is large enough for any image in the display
		for image in imageList.values():
			imageRect = image.get_rect()
			if imageRect.width > self.rect.width:
				self.rect.width = imageRect.width
			if imageRect.height > self.rect.height:
				self.rect.height= imageRect.height
		
	def update(self, imageNumber, draw = False):
		self.imageNumber = imageNumber
		pygame.draw.rect(self.menuSurface, self.menuColor, self.rect)
		self.menuSurface.blit(self.imageList[self.imageNumber], self.rect)
		if draw:
			pygame.display.update(self.displaySurface.blit(
								  self.menuSurface, toDisplayCoordinates(
								  self.menuTopLeft, self.rect),self.rect))
		
	def draw(self):
		self.menuSurface.blit(self.imageList[self.imageNumber], self.rect)

	
# class MutableDisplay(Display):
	# '''
	# Display that can be changed to any image on the fly
	# '''
	# def __init__(self, name, image, parentMenu, location):
		# Display.__init__(self, name, parentMenu, location)
		# self.imageList = image
		
	# def update(self, image, draw = False):
		# self.image = image
		# pygame.draw.rect(self.menuSurface, self.menuColor, self.rect)
		# self.menuSurface.blit(self.image, self.rect)
		# if draw:
			# pygame.display.update(self.displaySurface.blit(
								   #self.menuSurface, toDisplayCoordinates(
								   #self.menuTopLeft, self.rect), self.rect))
		
	# def draw(self):
		# self.menuSurface.blit(self.image, self.rect)
		
		
class ColorDisplay(Display):
	'''
	For displaying the currently selected color, just a solid colored box
	'''
	def __init__(self, name, color, parentMenu, location, dimensions, revealed = True):
		Display.__init__(self, name, parentMenu, location, revealed)
		self.color = color
		self.rect = pygame.Rect(location, dimensions)
		self.revealed = revealed
		
	def draw(self):
		pygame.draw.rect(self.menuSurface, self.color, self.rect)
		
	def update(self, color, draw = False):
		self.color = color
		pygame.draw.rect(self.menuSurface, self.color, self.rect)
		if draw:
			pygame.display.update(self.displaySurface.blit(
								  self.menuSurface, toDisplayCoordinates(
								  self.menuTopLeft, self.rect), self.rect))
		



#////////////////////////////SCROLL BAR//////////////////////////////////////

#class ScrollBar:
	#def __init__(self, name, color, menuSurface, menuTopLeft, location, dimensions, orientation):
		#self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})


	
	
