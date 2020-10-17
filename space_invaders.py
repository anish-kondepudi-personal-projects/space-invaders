import pygame
from random import randint, choice
from math import sqrt

######################################
"""          WINDOW SETUP          """
######################################

# Intilizaes 'Mixer' - lowers sound latency
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Initializes Pygame
pygame.init()

# Creates screen (window)
screen = pygame.display.set_mode((800,600))

# Sets title of window
pygame.display.set_caption("Space Invaders")

# Sets icon for window
icon = pygame.image.load('./metadata/spaceship_icon.png')
pygame.display.set_icon(icon)

# Plays Background Music
pygame.mixer.music.load('./metadata/background_music.mp3')
pygame.mixer.music.play(-1) # -1 loops music || 'music' is for long files while 'sound' is for short files
pygame.mixer.music.set_volume(0.15) # Sets volume to 5%

######################################
"""  Initialize Variables & Images """
######################################

# Speed of the Player and the Enemies
velocity = 4.5 # In future add randomized speed for enemies and constant speed for player || Increase as game goes on

# Creates background image of window
background = pygame.image.load('./metadata/background.png')

# Creating image and coordinates of player spaceship
playerImg = pygame.image.load('./metadata/spaceship.png')
playerX = 400-32 # 64x64 PNG (32 pixel shift will center image)
playerY = 475
playerX_change = 0

# Creating image and coordinates for all alien enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
down = []
current_Y = []
respawn_cooldown = []
num_enemies = 5

for i in range(num_enemies):
	enemyImg.append(pygame.image.load('./metadata/alien.png'))
	enemyX.append(randint(1,800-65))	# 1 Pixel Shift to Avoid Edge Cases
	enemyY.append(randint(50,175))
	enemyX_change.append(choice((1,-1)) * velocity)
	down.append(False) # Used for Enemy Snake Down Logic
	current_Y.append(0)
	respawn_cooldown.append(0)

# Creating image and coordinates of player bullet
bulletImg = pygame.image.load("./metadata/bullet.png")
bulletX = 0
bulletY = 0
bullet_visibility = False

# Create Score
score_value = 0
score_font = pygame.font.Font('./metadata/response.ttf', 32)
textX = 10
testY = 10

# Create Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

######################################
""" Function to Update Coordinates """
######################################

# This function will print player spaceship onto window
def player_update(X,Y):
	screen.blit(playerImg,(int(X),int(Y)))

# This function will print enemy alien onto window
def enemy_update(X,Y,i):
	screen.blit(enemyImg[i],(int(X),int(Y)))

# This function will print bullet onto window
def bullet_update(X,Y):
	screen.blit(bulletImg,(int(X),int(Y)))

# Checks to see if there is a collision
def isCollision(bulletX,bulletY,enemyX,enemyY):
	# Circluar Collisions Circles (Code Below)
	distance = sqrt(pow((bulletX+16)-(enemyX+32),2)+pow((bulletY+16)-(enemyY+32),2))
	if distance <= 48:
		return True
	return False
	# Square Collision Boxes (Code Below)
	# if (enemyX - bulletX <= 32) and (bulletX - enemyX <= 64):
	# 	if (bulletY - enemyY <= 64) and (enemyY - bulletY <= 32):
	# 		return True
	# return False

# Displays Score
def show_score(X, Y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (X, Y))

# Display Game Over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

######################################
"""            GAME LOOP           """
######################################

# Game Loop
running = True
while running:

	# Sets screen background to RGB value
	screen.fill((51, 153, 255))

	# Sets background to 'space' image file
	screen.blit(background,(0,0))

	for event in pygame.event.get():

		# If 'X' is pressed, then window is closed
		if event.type == pygame.QUIT:
			running = False

		# If specified key is pressed, 'playerX_change' is set accordingly
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change -= velocity
			if event.key == pygame.K_RIGHT:
				playerX_change += velocity
			# Deal with bullet logic with keystokes
			if event.key == pygame.K_SPACE:
				if bullet_visibility == False:
					bullet_sound = pygame.mixer.Sound('./metadata/laser.wav')
					bullet_sound.play()
					bullet_visibility = True
					bulletX = playerX + 16
					bulletY = playerY + velocity

		# If specified key is pressed, 'playerX_change' is reset to 0
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				playerX_change += velocity
			if event.key == pygame.K_RIGHT:
				playerX_change -= velocity

	# Updates Bullet's Coordinates, Checks for Boundaries, and Updates Display
	if bullet_visibility:
		bulletY -= 3 * velocity
		bullet_update(bulletX,bulletY)
		if bulletY < -32:
			bullet_visibility = False

	# Updates Player's Coordinates based on Keystrokes, Checks for Boundaries, and Updates Display
	playerX += playerX_change

	if playerX > 800-64: # 64x64 PNG (64 pixel shift will acount for image size)
		playerX = 800-64
	elif playerX < 0:
		playerX = 0

	player_update(playerX,playerY)

	# Logic for Enemies to Snake down to Player, Deal with Collisions, and Game Over
	for i in range(num_enemies):
		if enemyY[i] > 420:
			for j in range(num_enemies):
				enemyY[j] = 600
			game_over_text()
			break
		if respawn_cooldown[i] == 0:
			if not down[i]:
				enemyX[i] += enemyX_change[i]
				if enemyX[i] >= 800-64:
					enemyX_change[i] = -1 * velocity
					current_Y[i] = enemyY[i]
					down[i] = True
				elif enemyX[i] <= 0:
					enemyX_change[i] = velocity
					current_Y[i] = enemyY[i]
					down[i] = True
			else:
				if enemyY[i] < current_Y[i]+32:
					enemyY[i] += velocity
				else:
					down[i] = False
			collision = isCollision(bulletX,bulletY,enemyX[i],enemyY[i])
			if collision:
				explode_sound = pygame.mixer.Sound('./metadata/explosion.wav')
				explode_sound.play()
				bullet_visibility = False
				bulletY = -32
				score_value += 1
				enemyY[i] = -10000
				respawn_cooldown[i] = 200
		elif respawn_cooldown[i] == 1:
				respawn_sound = pygame.mixer.Sound('./metadata/respawn.wav')
				respawn_sound.play()
				enemyX[i] = randint(1,800-65)	# 1 Pixel Shift to Avoid Edge Cases
				enemyY[i] = randint(50,175)
				respawn_cooldown[i] -= 1
		else:
			respawn_cooldown[i] -= 1

		enemy_update(enemyX[i],enemyY[i], i)

	# Update Player Score
	show_score(textX, testY)

	# Updates display
	pygame.display.update()