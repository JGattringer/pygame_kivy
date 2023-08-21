# importing our modules here
import math
import random
import pygame
from pygame import mixer #import this module to be able to add sounds and music

# initializa pygame to have access to all tools
pygame.init()

# creating our screen
screen = pygame.display.set_mode((800, 600))  # here we define the size of our window

# Background
background = pygame.image.load('imgs/background.png')  # load and created a background var

# Background Sound
mixer.music.load('sounds/background.wav')
mixer.music.play(-1) # we add -1 inside for the musica play on loop

# size of screen must be a tuple
# changing Tittle and Icon of the game
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('imgs/ovni.png')
pygame.display.set_icon(icon)

# Player IMG and starting coordinates (x,y)
playerImg = pygame.image.load('imgs/nave-espacial.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy IMG and starting coordinates (x,y)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy): # loop for create the num of enemies and append to the list
    enemyImg.append(pygame.image.load('imgs/alien.png'))
    enemyX.append(random.randint(0, 735))  # use a random gen to create the obj in any part of X and Y that we passas
    enemyY.append(random.randint(10, 10))
    enemyX_change.append(2)
    enemyY_change.append(0.3)

# Ready - missil is armed but you cant see it
# Fire - missil is current moving

# Missil IMG and starting coordinates (x,y)
missilImg = pygame.image.load('imgs/missil.png')
missilX = 0
missilY = 480  # TENTAR MUDAR PARA ATIRAR DA POSICAO ATUAL DA NAVA
missilX_change = 0
missilY_change = 20
missil_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# creat a func to show the point on the screen, use typecasting to transform the int in str, true to be displayed and the RGB collor
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fire_missil(x, y):
    global missil_state  # Update missilY when firing the missile
    missil_state = "fire"
    screen.blit(missilImg, (x + 16, y + 10))  # adjust the missil to be released from midle of ship


def isCollision(enemyX, enemyY, missilX, missilY): # distance between 2 points and midlepoint formula
    distance = math.sqrt((math.pow(enemyX - missilX, 2)) + (math.pow(enemyY - missilY, 2)))
    if distance < 27:
        return True
    else:
        return False


# create a var for be able to close the loop
running = True

# here we create our main game loop for the game
while running:  # all the permanent remanning code should come inside of the loop

    screen.fill((0, 0, 0))  # define the screen RGB filling, screen come first and rest on top of it

    # call the backgroun image on the screen
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # get all events that can happen
        if event.type == pygame.QUIT:  # event to end loop
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change += 7  # speed of pixel moving
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
            #if event.key == pygame.K_UP:
            #    playerY_change -= 0.5
            #if event.key == pygame.K_DOWN:
            #    playerY_change += 0.5
            if event.key == pygame.K_TAB:
                if missil_state == "ready":  # condition to only made possible shot 1 bullet at time otherwise once
                    missil_sound = mixer.Sound('sounds/laser.wav')
                    missil_sound.play()
                    missilX = playerX  # pressed again the bullet would take the actual coordinates of the ship
                    fire_missil(missilX, missilY)

        if event.type == pygame.KEYUP:  # make the space ship stop moving
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # checking boundaries of spaceship, and we define the bounderies of our screen
    playerX += playerX_change  # update our player position
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    playerY += playerY_change
    if playerY <= 330:
        playerY = 330
    elif playerY >= 536:  # the limit of the screen is the size - size of ship
        playerY = 536

    # Movement of invader and checking boundaries of invader
    for i in range(num_of_enemy):  # loop for program know witch invader he need to move

        # Game Over
        if enemyY[i] > 440:                # game over loop
            for j in range(num_of_enemy):  # once reach this pixel all invaders will be moved out of screen and game end
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2  # movement of invader side ways
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2

        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 0
            enemyY[i] += enemyY_change[i]
        elif enemyY[i] >= 536:
            enemyY[i] = 536

        # Collision check
        collision = isCollision(enemyX[i], enemyY[i], missilX, missilY)
        if collision:
            collision_sound = mixer.Sound('sounds/explosion.wav')
            collision_sound.play()
            missilY = 480  # if a collision happen the bullet will be reload and score is up
            missil_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)  # reload our invader once collision happens
            enemyY[i] = random.randint(10, 10)

        enemy(enemyX[i], enemyY[i], i)

    # Missil movement
    if missilY <= 0:  # missil reload once go off screen
        missilY = 480
        missil_state = "ready"

    if missil_state == "fire":
        fire_missil(missilX, missilY)
        missilY -= missilY_change

    show_score(textX,textY)
    player(playerX, playerY)  # call our player to the screen in the coordinates
    pygame.display.update()  # this line makes all our code changes be shown
