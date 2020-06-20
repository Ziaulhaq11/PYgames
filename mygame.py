import math
import random
import pygame
from pygame import mixer

pygame.init()

#screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.png')

#player
playerimg = pygame.image.load('players.png')
playerX = 370
playerY = 520
playerX_change = 0

#enemy
enemy_img = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
	enemy_img.append(pygame.image.load('enemy.png'))
	enemyx.append(random.randint(0,800))
	enemyy.append(random.randint(0,200))
	enemyx_change.append(2)
	enemyy_change.append(10)

#bullet
bullet_img = pygame.image.load('bullet.png')
bulletx = 0
bullety = 520
bulletx_change = 0
bullety_change = 10
bullet_state = 'ready'

def player(x,y):
	screen.blit(playerimg,(x,y))

def enemy(x,y):
	screen.blit(enemy_img[i], (x,y))
	enemyx[i] += enemyx_change[i]

def bullet(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bullet_img,(x + 16,y + 10))

running = True
while running:
	screen.fill((255,255,0))
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change += -5
			if event.key == pygame.K_RIGHT:
				playerX_change += 5
			if event.key == pygame.K_SPACE:
				if bullet_state == 'ready':
					bulletx = playerX
					bullet(bulletx,bullety)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				playerX_change = 0
			if event.key == pygame.K_RIGHT:
				playerX_change = 0
	

	#Boundaries

	if playerX <= 0:
		playerX =0
	elif playerX >=740:
		playerX = 740

	#Enemies

	for i in range(no_of_enemies):
		enemy(enemyx[i],enemyy[i])
		for j in range(i):
			if enemyx[j]>=740:
				enemyx[j] -= enemyx_change[j]
				enemyy[j] += enemyy_change[j]


	# Bullet
	if bullety <=0:
		bullety = 480
		bullet_state = 'ready'

	if bullet_state == 'fire':
		bullet(bulletx,bullety)
		bullety -= bullety_change

	playerX += playerX_change
	player(playerX,playerY)

	pygame.display.update()
