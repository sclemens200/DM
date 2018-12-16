import pygame
from pygame.locals import *
from colors import *
from misc import quitCheck, toDisplayCoordinates


pygame.init()

TEXT_LENGTH_LIMIT = 30 #Sorta arbitrary, 30 works well to keep it from flying off the viewscreen

pygame.key.set_repeat(120) #the number of milliseconds chosen here was done based on feel

class TextInput:
	def __init__(self, name, parentSurface, parentSurfaceTopLeft, displaySurface, rect,
				 fontSize=28, revealed = True):
		self.name = name
		self.parentSurface = parentSurface
		self.parentSurfaceTopLeft = parentSurfaceTopLeft
		self.displaySurface = displaySurface
		self.rect = rect
		self.displayLengthLimit = self.rect.width
		self.text = ''
		self.font = pygame.font.Font('freesansbold.ttf', fontSize)
		self.revealed = revealed
		pygame.draw.rect(self.parentSurface, BLACK, rect.inflate(4,4))
		
	def getInput(self):
		while True:
			for event in pygame.event.get():
				quitCheck(event)
				
				if event.type == KEYDOWN:
					#escaping
					if event.key == K_ESCAPE or event.key == K_RETURN:
						return None
					
					#deleting
					elif event.key == K_BACKSPACE:
						if len(self.text) == 1:
							self.text = ''
						elif len(self.text) > 1:
							self.text = self.text[:len(self.text)-1]
						self.draw()
					
					#getting text imput
					else:
						if len(self.text) < TEXT_LENGTH_LIMIT:
							self.text = self.text + event.unicode
							self.draw()
				

				#we want the user to be able to still use the mouse to interact with the outside
				#game if they do they will return to higher level menu and need to reclick
				#into text box to continue typing
				if event.type == MOUSEBUTTONDOWN:
					return event

					
	def draw(self):
		pygame.draw.rect(self.parentSurface, WHITE, self.rect)

		
		if len(self.text) > 0:
			renderedText = self.text
			TextDisplay = self.font.render(renderedText, 1, BLACK)
			TextDisplayRect = TextDisplay.get_rect()
			#need to contain the displayed text to the width of the field
			if TextDisplayRect.width > self.displayLengthLimit:
				TextDisplayRect.left = TextDisplayRect.width - self.displayLengthLimit
			
			self.parentSurface.blit(TextDisplay, self.rect, TextDisplayRect)
			
		pygame.display.update(self.displaySurface.blit(
							  self.parentSurface, toDisplayCoordinates(
							  self.parentSurfaceTopLeft,self.rect), self.rect))	


	def reset(self):
		self.text = ''
		pygame.draw.rect(self.parentSurface, WHITE, self.rect)
