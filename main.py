import pygame
import math
import random
from pygame import mixer   #for sounds and music

#Initialize the pygame
pygame.init()

#flaticon.com
#freepik.com
#dafont.com is used to download font  of  .ttf format and put in project and use it
#ctrl+alt+l for indentation in pycharm
#2 problems of bullet only one is firing and bullet is moving with player
#1:45:00 previously enemy x is 800 but after collision func we need to change it to the 736 as function because when enemy respawning at above 740 it goes down


#create the  screen
screen=pygame.display.set_mode((800,600))  #width, height


'''while True:
	pass'''

#event anything happened like pressing buttons up,down,exit

#Title and Icon
pygame.display.set_caption('Space invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Background
background_img = pygame.image.load('background.png')

#Background music
mixer.music.load('background.wav')   #we use music because it has to play continuously but for bullet we have to use sound
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('players.png')
playerX = 370
playerY = 520
playerX_change = 0
playerY_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
	enemyImg.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(0,740))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(2)
	enemyY_change.append(40)


#Bullet
#Ready state means you cant seen bullet on screen
#Fire state means the bullet is currently moving
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 520
bulletX_change = 0
bulletY_change = 10 #not 40 speed
bullet_state = 'ready'

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',30)
textX = 10
textY = 10

#Game over font
game_over_font = pygame.font.Font('freesansbold.ttf',50)
game_over_x = 200
game_over_y = 150

def player(x,y):
	#screen.blit(playerImg,(playerX,playerY))   #to draw
	screen.blit(playerImg, (x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bullet,(x+16, y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
	if distance < 27:	
		return True

def show_score(x,y):
	score = font.render('Score:'+str(score_value),True,(255,255,255))
	screen.blit(score, (x,y))

def game_over(x,y):
	game_over_text = game_over_font.render('Game Over',True,(255,255,255))
	final_score = game_over_font.render('Final Score : '+ str(score_value),True,(255,255,255))
	screen.blit(game_over_text, (x,y))
	screen.blit(final_score, (x,y+100))

 #Game Loop
running = True
while running:
	#RGB - Red, green, blue
	screen.fill((100, 130, 100))  #first screen
	#playerX+=0.2
	#Background image
	screen.blit(background_img,(0,0))

	for event in pygame.event.get():  #anything happened in the window and keystrokes are also events.
		#we can say all inputs will be stored in event loop variable
		if event.type == pygame.QUIT:
			running = False


		#if keystroke is pressed check whether its right or left
		if event.type == pygame.KEYDOWN: #it means pressing key
			if event.key == pygame.K_LEFT:
				playerX_change = -5
			if event.key == pygame.K_RIGHT:
				playerX_change = 5   #Before it was 0.3 due to image the iteration gets slow
			if event.key == pygame.K_SPACE:
				if bullet_state is 'ready':
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletX = playerX    #before it was playerx only but bullet is following along
					fire_bullet(bulletX,bulletY)  #if you put x+20 you can see bullet


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or pygame.K_LEFT:
				playerX_change = 0
				playerY_change = 0


	playerX += playerX_change
	# Checking for boundaries
	if playerX <= 0:
		playerX =0
	elif playerX >= 740:
		playerX = 740


	# Enemy Movement
	for i in range(no_of_enemies):
		#Game over
		if enemyY[i] > 440:
			for j in range(no_of_enemies):
				enemyY[j]=2000
			game_over(game_over_x,game_over_y)
			break

		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 2
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 740:
			enemyX_change[i] = -2
			enemyY[i] += enemyY_change[i]

		#Collision
		collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			collision_sound = mixer.Sound('explosion.wav')
			collision_sound.play()
			bulletY = 480
			bullet_state = 'ready'
			score_value += 1
			enemyX[i]= random.randint(0,740)
			enemyY[i]= random.randint(50,150)

		enemy(enemyX[i],enemyY[i],i)

	#Bullet Movement
	if bulletY <= 0:
		bulletY = 480
		bullet_state = 'ready'   #solving single bullet problem

	if bullet_state == 'fire':  #or if bullet_state is 'fire'
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change

	show_score(textX,textY)
	player(playerX,playerY)   #image displays which ever is up
	pygame.display.update()  #must line
