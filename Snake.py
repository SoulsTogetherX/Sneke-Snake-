	# Imports modulus
import numpy as np
import random as rd
import pygame as pg

	# Base variables
		# Default Screen/Board/Pixel size
scale, boardW, boardH, delay = 8, 30, 30, 8
		# Game Event Booleans
menu, run, mainGame, gameOver, changeKey = True, False, True, False, False
		# Score
score, highScore = 0, 0
		# Font
pg.font.init()
font = pg.font.SysFont("Comic Sans MS", 36)
		# Menu values
size_M = (600, 600)
V_pad, menu_type, idx = 60, 0, 0
options = []
			# Other
key_change = 0
select_color = (0, 0, 0)

	# Constants
		# Color Constants
WHITE		=	( 255, 255, 255)
BLACK		=	(   0,   0,   0)
GRAY		=	( 127, 127, 127)
GREEN		=	(   0, 255,   0)
DARK_GREEN	=	(   0, 200,   0)
RED			=	( 255,   0,   0)
KHAKI		=	( 240, 230, 140)
			# Keys
K_inputs = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_SPACE]
			# Limits
MIN_SCALE = 4
MAX_SCALE = 50
MIN_BOARD_W = 4
MAX_BOARD_W = 50
MIN_BOARD_H = 4
MAX_BOARD_H = 50
MIN_DELAY = 4
MAX_DELAY = 25
			# Other
saveFileName = ".snakeSaveFile"


	# Class defintions
		# Base Class for all Entities
class Tile:
	def __init__(self, cords):
		self.cords = cords

	def __repr__(self):
		return "E"

	def color(self):
		return BLACK

	def update(self):
		pass

		# SnakeTail
class SnakeT(Tile):
	count = 0

	def __repr__(self):
		return "ST"

	def color(self):
		return GREEN

	def update(self):
		if self.count >= maxTail:
			board[self.cords] = Empty(self.cords)
		else:
			self.count += 1

		# SnakeHead
class SnakeH(Tile):
	dir = 0

	def __repr__(self):
		return "SH"

	def color(self):
		return DARK_GREEN

		# Apple
class Apple(Tile):
	def __repr__(self):
		return "F"

	def color(self):
		return RED

		# Wall
class Wall(Tile):
	def __repr__(self):
		return "W"

	def color(self):
		return GRAY

		# Wall
class Empty(Tile):
	def __repr__(self):
		return " "

	def color(self):
		return BLACK

	# Attempts to access saved options in the option file. Creates a new one, with default settings, if error occurs
try:
	with open(saveFileName, "r") as opFile:
		scale, boardW, boardH, delay, highScore, K_inputs[0], K_inputs[1], K_inputs[2], K_inputs[3], K_inputs[4] = map(int, opFile.readlines())
except:
	print("\nError in accessing 'options.o' file!\nCreating new one with default options...")
	opFile = open(saveFileName, "w")
	opFile.write("\n".join(map(str, (scale, boardW, boardH, delay, highScore, K_inputs[0], K_inputs[1], K_inputs[2], K_inputs[3], K_inputs[4]))))
	opFile.close()
	print("Done.\n")

	# Updating Options menu
options =	[(4, ("Play", "Controls", "Settings", "Quit")),
			(6, ("Left: " + pg.key.name(K_inputs[0]), "Right: " + pg.key.name(K_inputs[1]), "Up: " + pg.key.name(K_inputs[2]), "Down: " + pg.key.name(K_inputs[3]), "Enter: " + pg.key.name(K_inputs[4]),"Back")),
			(5, ("Resolution: " + str(scale), "Board Width: " + str(boardW), "Board Height: " + str(boardH), "Snake Delay: " + str(delay), "Back"))]

	# Starts pygame
pg.init()

	# The screen caption
pg.display.set_caption("Sneck")

	# Clock to track game FPS
clock = pg.time.Clock()

while mainGame:
	# The menu screen
	screen = pg.display.set_mode(size_M)

		# Main game loop
	while menu:
		select_color = KHAKI
		screen.fill(BLACK)

			# Checks for game events
		for event in pg.event.get():
				# Ends the game if quit
			if event.type == pg.QUIT:
				mainGame, menu = False, False

				# Checks if a key has been pressed
			elif event.type == pg.KEYDOWN:
					# Checks if the user is attempting to change the controls
				if changeKey:
					if event.key in K_inputs:
						if event.key != K_inputs[key_change]:
							select_color = RED
					else:
						K_inputs[key_change] = event.key
						options[1] = (6, ("Left: " + pg.key.name(K_inputs[0]), "Right: " + pg.key.name(K_inputs[1]), "Up: " + pg.key.name(K_inputs[2]), "Down: " + pg.key.name(K_inputs[3]), "Enter: " + pg.key.name(K_inputs[4]),"Back"))
						
					changeKey = False
				else:
					if event.key == K_inputs[4]:
						if menu_type == 0:
							if idx == 0:
								menu, run = False, True
							elif idx == 3:
								mainGame, menu = False, False
							else:
								menu_type, idx = idx, 0
						elif menu_type == 1:
							if idx == 5:
								menu_type, idx = 0, 1
							else:
								key_change = idx
								changeKey = True
						elif menu_type == 2:
							if idx == 4:
								menu_type, idx = 0, 2
						
					elif event.key == K_inputs[3]:
						idx = (idx + 1) % options[menu_type][0]
					elif event.key == K_inputs[2]:
						idx = (idx - 1) % options[menu_type][0]
					elif menu_type == 2:
						if event.key == K_inputs[0]:
							if idx == 0:
								if scale - 1 < MIN_SCALE:
									select_color = RED
								else:
									scale -= 1
							elif idx == 1:
								if boardW - 1 < MIN_BOARD_W:
									select_color = RED
								else:
									boardW -= 1
							elif idx == 2:
								if boardH - 1 < MIN_BOARD_H:
									select_color = RED
								else:
									boardH -= 1
							elif idx == 3:
								if delay - 1 < MIN_DELAY:
									select_color = RED
								else:
									delay -= 1

						elif event.key == K_inputs[1]:
							if idx == 0:
								if scale + 1 > MAX_SCALE:
									select_color = RED
								else:
									scale += 1
							elif idx == 1:
								if boardW + 1 > MAX_BOARD_W:
									select_color = RED
								else:
									boardW += 1
							elif idx == 2:
								if boardH + 1 > MAX_BOARD_H:
									select_color = RED
								else:
									boardH += 1
							elif idx == 3:
								if delay + 1 > MAX_DELAY:
									select_color = RED
								else:
									delay += 1

						options[2] = (5, ("Resolution: " + str(scale), "Board Width: " + str(boardW), "Board Height: " + str(boardH), "Snake Delay: " + str(delay), "Back"))



			# Displays all options in the menu, from order
				# Highlight the current selected option
		for num, op in enumerate(options[menu_type][1]):
			if num == idx:
					# Highlightws
				text = font.render(op, True, select_color)
			else:
					# Normal
				text = font.render(op, True, WHITE)
				# Displays text
			screen.blit(text, ((screen.get_width() - text.get_width()) // 2, (screen.get_height() + (num - (options[menu_type][0] / 2))*(text.get_height() + V_pad)) // 2))

			# Display
		pg.display.flip()

			# FPS
		clock.tick(60)

		# TailSize
	maxTail = 1
		# Add Food True
	food = True
		# Resets Score
	score = 0

		# Initializes the gameBoard
	board = np.empty((boardW+2, boardH+2), dtype=Tile)
		# Sets the Walls, Empty, and Player tiles in the board
			# Walls and empty
	for c in range(boardW + 2):
		for r in range(boardH + 2):
			if c == 0 or c == boardW + 1 or r == 0 or r == boardH + 1:
				board[c, r] = Wall((c, r))
			else:
				board[c, r] = Empty((c, r))

			# Player
	player = SnakeH(((boardW+1)//2, (boardH+1)//2))
	board[boardW//2, boardH//2] = player

		# The screen size
	size_G = (max((boardW+2)*scale, font.render("________" + str(highScore), True, KHAKI).get_width()), (boardH+2)*scale + 100)

		# Game Screen
	screen = pg.display.set_mode(size_G)

		# Sets up a repeating event to update the tiles
	STEP_EVENT = pg.USEREVENT + 0
	pg.time.set_timer(STEP_EVENT, delay*10)

		# Where the player will move to next
	newDir = player.dir

		# Main game loop
	while run:
			# Checks for game events
		for event in pg.event.get():
				# Ends the game if quit
			if event.type == pg.QUIT:
				mainGame, run = False, False
				# Updates all tiles when step event occurs
			elif event.type == STEP_EVENT:
					# Increases the count of all snake tail tiles
				for _, item in np.ndenumerate(board):
					item.update()

					# Creates new snake tail tile
				board[player.cords] = SnakeT(player.cords)

					# Sets the new direction and placement for the snake head
				player.dir = newDir
				player.cords = (player.cords[0] + (newDir == 1) - (newDir == 3), player.cords[1] + (newDir == 2) - (newDir == 0))

					# If the snake is moving into a wall or its tail, game over
				if isinstance(board[player.cords], Wall) or isinstance(board[player.cords], SnakeT):
						# Stops main loop and starts game-over waiting loop
					run, menu = False, True
						# Stops the Step timer
					pg.time.set_timer(STEP_EVENT, 0)
						# Pauses the game in the event of a game_over
					gameOver = True

				else:
					# If the snake is moving into an apple, increase tail length
					if isinstance(board[player.cords], Apple):
							# Increases tail length
						maxTail += 1
							# Large boost in score
						score += 100
							# Updates HighScore
						highScore = max(highScore, score)
							# Tells game to add new apple onto board
						food = True


						# Places snake head at new coordinates
					board[player.cords] = player

						# Checks if new apple needs to be put on the board
					if food and not gameOver:
							# Finds all Empty tiles on the board
						empties = [idx for idx, item in np.ndenumerate(board) if isinstance(item, Empty)]
							# Checks if any Empty tiles were found
						if len(empties):
								# If Empty tiles, then randomly chooses one of them on the board to place an Apple at
							pos = rd.choice(empties)
						else:
								# If no Empty tiles, then game is over
							gameOver = True
								# Very large boost in score
							score += 1000
								# Updates HighScore
							highScore = max(highScore, score)

							# Places the apple at the randomly chosen tile
						board[pos] = Apple(pos)
							# No longer needs a new apple
						food = False


			# Updates the direction the player will move to next dependant on key presses and current direction
		if pg.key.get_pressed()[K_inputs[0]]:
			if player.dir != 1:
				newDir = 3
		elif pg.key.get_pressed()[K_inputs[1]]:
			if player.dir != 3:
				newDir = 1
		elif pg.key.get_pressed()[K_inputs[2]]:
			if player.dir != 2:
				newDir = 0
		elif pg.key.get_pressed()[K_inputs[3]]:
			if player.dir != 0:
				newDir = 2

			# Draw Background, Tiles, and Score Text
				# Background
		screen.fill(BLACK)
				# Tiles
		for index, item in np.ndenumerate(board):
			pg.draw.rect(screen, item.color(), pg.Rect(scale*index[0], scale*index[1], scale, scale))
				# Draw Score Text
		screen.blit(font.render("Score: " + str(score), True, KHAKI), (10, (boardH+2)*scale + 5))
		screen.blit(font.render("High:  " + str(highScore), True, KHAKI), (10, (boardH+2)*scale + 45))

			# Display
		pg.display.flip()

			# FPS
		clock.tick(60)

	while gameOver:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				mainGame, gameOver = False, False
			elif event.type == pg.KEYDOWN and event.key == K_inputs[4]:
				gameOver = False

	# Saves settings
print("Saving...")
opFile = open(saveFileName, "w")
opFile.write("\n".join(map(str, (scale, boardW, boardH, delay, highScore, K_inputs[0], K_inputs[1], K_inputs[2], K_inputs[3], K_inputs[4]))))
opFile.close()
print("Done!")

print("Thanks for playing!")