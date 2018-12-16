import pygame
from constants import WINDOWWIDTH

FPS = 60
ANIMATION_RATE = 10


def animateMenuForward(displaySurf, animatingMenus):
	'''
	Function for animating the submenus forward
	'''

	#animation_rate = 20
	fpsClock = pygame.time.Clock()
	
	
	#////////////////start-of-subfunction////////////////
	def forwardAnimation(animatingMenu):
		displaySurf.blit(animatingMenu.surface,
						(WINDOWWIDTH - (i+1) * animatingMenu.rect.width / ANIMATION_RATE,
						animatingMenu.rect.top)
						)
	#////////////////end-of-subfunction////////////////
	
	if type(animatingMenus) is not list:
		animatingMenus = [animatingMenus]
	
	for i in range(ANIMATION_RATE):
		for animatingMenu in animatingMenus:
			forwardAnimation(animatingMenu)
		pygame.display.update()
		fpsClock.tick(FPS)

		
		
			
def animateMenuBackward(displaySurf, beneathMenu, animatingMenus):
	'''
	Function for animating the submenus backward
	'''
	
	#animation_rate = 20
	fpsClock = pygame.time.Clock()
	
	
	#////////////////start-of-subfunction////////////////
	def backwardAnimation(animatingMenu):
		displaySurf.blit(beneathMenu.surface,
						(WINDOWWIDTH - animatingMenu.rect.width , animatingMenu.rect.top), 
						(0, animatingMenu.rect.top, (i+1)*beneathMenu.width/ANIMATION_RATE,
						animatingMenu.rect.height)
						)
		displaySurf.blit(animatingMenu.surface,
						(WINDOWWIDTH - (ANIMATION_RATE-1-i) * animatingMenu.rect.width
						/ ANIMATION_RATE, animatingMenu.rect.top)
						)
	#////////////////end-of-subfunction////////////////	
	
	if type(animatingMenus) is not list:
		animatingMenus = [animatingMenus]
	
	for i in range(ANIMATION_RATE):
		for animatingMenu in animatingMenus:
			backwardAnimation(animatingMenu)
		pygame.display.update()
		fpsClock.tick(FPS)