#menu initialization
import math
import pygame

from colors import *
from constants import *
from menuClass import *
from textInput import TextInput

FONTSIZE = 28

Font = pygame.font.Font('freesansbold.ttf', FONTSIZE)
TitleFont = pygame.font.Font('freesansbold.ttf', 48)
SubFont = pygame.font.Font('freesansbold.ttf', 16)

#///////////////////////////////////////////MAIN INIT/////////////////////////////////////////////
def initMainMenu(displaySurface):
	'''Main Menu Initialization'''
	main = MenuClass("mainMenu", displaySurface, MAINMENU_RECT)
	main.buttonList['Draw'] = TextButton("Draw", "Draw", main.surface, (main.width/20, 0))
	main.buttonList['Distance'] = TextButton("Distance", "Dist", main.surface, 
											(main.width/20, 40)
											)
	main.buttonList['CharacterCreator'] = TextButton("CharacterCreator", "Chars", main.surface,
													(main.width/20, 80)
													)
	main.buttonList['Save'] = TextButton("Save", "Save", main.surface, (6*main.width/10, 0))
	main.buttonList['Load'] = TextButton("Load", "Load", main.surface, (6*main.width/10, 40))
	main.buttonList['Undo'] = TextButton("Undo", "Undo", main.surface, (6*main.width/10, 80))
	main.buttonList['About'] = TextButton("About", "About", main.surface, (2*main.width/3,
										  MAINMENU_RECT.height-30), revealed = False)
	main.blitButtons()
	return main

	
#///////////////////////////////////////////COLORMENU INIT////////////////////////////////////////
def initColorMenu(displaySurface):
	'''Color Menu Initialization'''
	colorMenu = MenuClass("colorMenu", displaySurface, COLORMENU_RECT)
	menuFile = open('colorPickerMenu.txt', 'r')
	colors = menuFile.read().split('\n')
	(i,j) = (0,0)
	for color in colors:
			colorMenu.buttonList[color] = Button(color, colorMenu.surface,
												(i * colorMenu.width/7, j * colorMenu.height/7),
												(BOXSIZE, BOXSIZE), COLORDICTIONARY[color])
			j += 1
			if j >= 7:
				j = 0
				i += 1
	
	colorMenu.blitButtons()
	return colorMenu

	
#///////////////////////////////////////////SHAPE INIT////////////////////////////////////////////
def initShapeMenu(displaySurface):
	'''Shape Menu Initialization'''
	shapeMenu = MenuClass("shapeMenu", displaySurface, SHAPEMENU_RECT)
	shapeMenu.buttonList['Rect'] = TextButton("Rect", "Rect", shapeMenu.surface,
											 (shapeMenu.width/20, 0)
											 )
	addIncreaseDecrease(shapeMenu, 'Rect', (0,9), (shapeMenu.width/20, 31))
	
	shapeMenu.buttonList['Circle'] = TextButton("Circle", "Circle", shapeMenu.surface,
											   (6*shapeMenu.width/10, 0)
											   )
	addIncreaseDecrease(shapeMenu, 'Circle', (0,9), (6*shapeMenu.width/10, 31))
	
	shapeMenu.buttonList['Polygon'] = TextButton("Polygon", "Polygon", shapeMenu.surface,
												(shapeMenu.width/20, 62)
												)
	
	shapeMenu.buttonList['Line'] = TextButton("Line", "Line", shapeMenu.surface,
											 (6*shapeMenu.width/10, 62)
											 )
	addIncreaseDecrease(shapeMenu, 'Line', (1,9), (6*shapeMenu.width/10, 93))
	
	shapeMenu.buttonList['Ellipse'] = TextButton("Ellipse", "Ellipse", shapeMenu.surface,
												(6*shapeMenu.width/10, 124)
												)
	addIncreaseDecrease(shapeMenu, 'Ellipse', (0,9), (6*shapeMenu.width/10, 155))
	
	shapeMenu.buttonList['Undo'] = TextButton("Undo", "Undo", shapeMenu.surface,
											 (6*shapeMenu.width/10, 4*shapeMenu.height/5+5)
											 )
	shapeMenu.imageList['ColorImage'] = ColorDisplay("ColorImage", RED, shapeMenu,
													(shapeMenu.width/10, 4*shapeMenu.height/5+5),
													(BOXSIZE, BOXSIZE)
													)
	shapeMenu.blitButtons()
	shapeMenu.blitImages()
	return shapeMenu
	


#///////////////////////////////////////////CHARACTER INIT////////////////////////////////////////

def initCharacterCreator(displaySurface):
	'''Character Menu Initialization'''
	characterCreator = MenuClass("characterCreator", displaySurface, CHARACTERCREATOR_RECT)
	
	#name
	nameTextImage = Font.render('Name:', 1, BLACK)
	addStaticImage("Name", characterCreator, nameTextImage, (characterCreator.width/20, 5)) 
	characterCreator.buttonList['CharacterName'] = TextInput("CharacterName",
															 characterCreator.surface, 
															 characterCreator.topleft, 
															 displaySurface,
															 pygame.Rect(
															 (2*characterCreator.width/5+2, 5,
															 characterCreator.width/2,
															 FONTSIZE+1))
															 )
	
	
	#this adds the decrease/increase buttons for the character size
	sizeTextImage = Font.render('Size:', 1, BLACK)
	addStaticImage("Size", characterCreator, sizeTextImage, (characterCreator.width/20,
				   characterCreator.height/5)
				   ) 
	addIncreaseDecrease(characterCreator, '', (1,4),
					   (2*characterCreator.width/5,characterCreator.height/5)
					   )
	
	characterCreator.buttonList['NewCharacter'] = TextButton("NewCharacter", "New",
															 characterCreator.surface,
															 (characterCreator.width/20,
															 characterCreator.height/2)
															 )
	
	#here we create a blank area where the created characters will appear
	blankIcon = pygame.Surface((BOXSIZE,BOXSIZE))
	blankIcon.fill(characterCreator.color)
	characterCreator.buttonList['CharacterIcon'] = ImageButton("CharacterIcon", blankIcon,
															   characterCreator.surface,
															   (4*characterCreator.width/10,
															   characterCreator.height/2)
															   )

	#display the currently selected color
	characterCreator.imageList['ColorImage'] = ColorDisplay("ColorImage", RED,
															characterCreator,
															(characterCreator.width/10,
															4*characterCreator.height/5),
															(BOXSIZE, BOXSIZE)
															)
	
	characterCreator.blitButtons()
	characterCreator.blitImages()
	return characterCreator


	
#///////////////////////////////////////////SAVEGAME INIT/////////////////////////////////////////
def initSaveMenu(displaySurface):
	'''Save Menu Initialization'''
	saveMenu = MenuClass("SaveMenu", displaySurface, SAVEMENU_RECT, YELLOW, BLACK)
	saveMenu.buttonList['Save'] = TextButton("Save", "Save", saveMenu.surface,
											(saveMenu.width/4, 4*saveMenu.height/5),
											centered = True)
	saveMenu.buttonList['Cancel'] = TextButton("Cancel", "Cancel", saveMenu.surface,
											  (3*saveMenu.width/4, 4*saveMenu.height/5),
											  centered = True)
	#the text box
	addStaticImage("Filename", saveMenu, Font.render("Name:", 1, BLACK), (saveMenu.width/20,
													 2*saveMenu.height/5)
													 )
	saveMenu.buttonList['SaveName'] = TextInput("SaveName", saveMenu.surface, saveMenu.topleft,
												displaySurface, pygame.Rect(
												(saveMenu.width/4, 2*saveMenu.height/5,
												2*saveMenu.width/3, FONTSIZE+1))
												)
												
	saveMenu.blitButtons()											
	return saveMenu

												
												
#///////////////////////////////////////////LOADGAME INIT/////////////////////////////////////////
SAVEDGAMEBUTTONS_TOPLEFT = (LOADMENU_RECT.width/6, LOADMENU_RECT.height/5)


def initLoadMenuSuper(displaySurface):
	'''Load Menu Initialization'''
	loadMenuSuper = MenuClass("LoadMenuSuper", displaySurface, LOADMENU_RECT, YELLOW, BLACK)
	loadMenuSuper.buttonList['SavedGames'] = ImageButton("SavedGames",
														 pygame.Surface(
														 (2*loadMenuSuper.width/3,
														 (FONTSIZE+1)*4 + 4)), 
														 loadMenuSuper.surface,
														 SAVEDGAMEBUTTONS_TOPLEFT)
	loadMenuSuper.buttonList['Load'] = TextButton("Load", "Load", loadMenuSuper.surface,
												 (loadMenuSuper.width/8,
												 4*loadMenuSuper.height/5)
												 )
	loadMenuSuper.buttonList['Delete'] = TextButton("Delete", "Delete", loadMenuSuper.surface,
												   (2*loadMenuSuper.width/5,
												   4*loadMenuSuper.height/5)
												   )
	loadMenuSuper.buttonList['Cancel'] = TextButton("Cancel", "Cancel", loadMenuSuper.surface,
												   (9*loadMenuSuper.width/12,
													4*loadMenuSuper.height/5)
													)
	addUpDown(loadMenuSuper, (SAVEDGAMEBUTTONS_TOPLEFT[0] +
							  loadMenuSuper.buttonList['SavedGames'].rect.width,
							  SAVEDGAMEBUTTONS_TOPLEFT[1]), (FONTSIZE+1)*3)
	loadMenuSuper.blitButtons()
	return loadMenuSuper
	
	
def initLoadMenuSub(displaySurface):
	#the topleft of the rect is used in button click collisions so we need to be precise
	loadMenuSub = MenuClass("LoadMenuSub", displaySurface,
							pygame.Rect(LOADMENU_RECT.left+SAVEDGAMEBUTTONS_TOPLEFT[0],
							LOADMENU_RECT.top+SAVEDGAMEBUTTONS_TOPLEFT[1],
							2*LOADMENU_RECT.width/3,0), YELLOW, BLACK)
	return loadMenuSub
	
#///////////////////////////////////////////ABOUT INIT////////////////////////////////////////////
def initAbout(displaySurface):
	about = MenuClass("About", displaySurface, ABOUT_RECT, BLUE)
	dungeonMaster = TitleFont.render("DUNGEON MASTER", 1, BLACK)
	bySeanClemens = Font.render("by Sean Clemens", 1, BLACK)
	madeWithPythonPygame  = SubFont.render("Made with: Python and pygame",1, BLACK)
	addStaticImage("dungeonMaster", about, dungeonMaster, (ABOUT_RECT.width/40,0))
	addStaticImage("bySeanClemens", about, bySeanClemens,
				  (ABOUT_RECT.width/4,ABOUT_RECT.height/6)
				  )
	addStaticImage("madeWithPythonPygame", about, madeWithPythonPygame,
				  (ABOUT_RECT.width/4,ABOUT_RECT.height/3)
				  )
	about.buttonList['OK'] = TextButton("OK", "OK", about.surface,
									   (ABOUT_RECT.width/2,5*ABOUT_RECT.height/6),
									   textColor = GREEN, centered = True)
	about.blitButtons()
	return about

#//////////////////////////////////////////Additional Functions///////////////////////////////////

#a function to add two buttons for increase and decrease with a range of values
def addIncreaseDecrease(menu, name, sizeRange, location):	
	sizeDecrease = pygame.Surface((BOXSIZE, BOXSIZE)).convert()
	sizeDecrease.fill(UGLY)
	sizeDecrease.set_colorkey(UGLY)
	pygame.draw.polygon(sizeDecrease, GREEN, [(25, 5), (25, 25), (5, 15)])
	left, top = location
	
	#decrease button
	menu.buttonList[name+'SizeDecrease'] = ImageButton(name+"SizeDecrease",
													   sizeDecrease, menu.surface, (left, top)
													   )
	#size images
	numberImageList = {}
	for i in range(sizeRange[0], sizeRange[1]+1):
		numberImageList[i] = Font.render(str(i), 1, BLACK)
	menu.imageList[name+'Size']=PresetDisplay(name+"Size", numberImageList, menu, (left+30,top))
	#increase button
	sizeIncrease = pygame.transform.flip(sizeDecrease, True, False)
	menu.buttonList[name+'SizeIncrease'] = ImageButton(name+"SizeIncrease",
													   sizeIncrease, menu.surface, (left+45,top)
													   )
	
	
def addUpDown(menu, location, distanceApart):	
	upButton = pygame.Surface((BOXSIZE, BOXSIZE)).convert()
	upButton.fill(UGLY)
	upButton.set_colorkey(UGLY)
	pygame.draw.polygon(upButton, GREEN, [(15, 5), (25, 25), (5, 25)])
	left, top = location
	
	#up button
	menu.buttonList['UpButton'] = ImageButton("UpButton", upButton, menu.surface, (left, top))

	#down button
	downButton = pygame.transform.flip(upButton, False, True)
	menu.buttonList['DownButton'] = ImageButton("DownButton", downButton, menu.surface,
											   (left,top+distanceApart)
											   )
	
	
#a function that adds an unchanging image to the surface of a menu	
def addStaticImage(name, parentMenu, image, location):
		menuSurface = parentMenu.surface
		imageRect = image.get_rect(topleft = location)
		menuSurface.blit(image, imageRect)