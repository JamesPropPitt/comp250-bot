#! / usr / bin / env python
# -*-coding:utf-8-*-
import pygame, sys
import win32api, win32console, win32gui, codecs
import time, random
from pygame.sprite import Sprite

pygame.init()

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

# Display settings
display_width = 1440
display_height = 900
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Ice Spy")

# Imagery
icon = pygame.image.load("ice.png")
pygame.display.set_icon(icon)
img = pygame.image.load("snakehead.png")
img2 = pygame.image.load("snaketail.png")
ice = pygame.image.load("ice.png")
clock = pygame.time.Clock()
iceThickness = 100
block_size = 40
FPS = 30000

smallfont = pygame.font.SysFont("Oswald", 25)
medfont = pygame.font.SysFont("Oswald", 50)
largefont = pygame.font.SysFont("Oswald", 80)


def pause():
    paused = True

    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press C to continue or Q to quit", black, 25)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def score(score):
    text = smallfont.render("Score: " + str(score), True, red)
    gameDisplay.blit(text, [0, 0])


def randice():
    randicex = round(random.randrange(0, display_width - iceThickness))
    randicey = round(random.randrange(0, display_height - iceThickness))
    return randicex, randicey


def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
        tail = pygame.transform.rotate(img2, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
        tail = pygame.transform.rotate(img2, 90)
    if direction == "up":
        head = img
        tail = img2
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
        tail = pygame.transform.rotate(img2, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    #  gameDisplay.blit(tail, (snakeList[20][20], snakeList[20],[20]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, (XnY[0], XnY[1], block_size, block_size))


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_change=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_change
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    global direction

    direction = "right"
    running = True
    gameOver = False

    len_x = display_width / 2
    len_y = display_height / 2

    len_x_change = 0
    len_y_change = 0

    snakeList = []
    snakeLength = 3
    Snaketail_x = len_x - len(snakeList)
    Snaketail_y = len_y - len(snakeList)
    randicex, randicey = randice()

    while running:
        if gameOver == True:
            message_to_screen("Game over", red, -50, size="large")
            message_to_screen("Press C to play again or Q to quit", white, 50, size="medium")
            pygame.display.update()

        if len_x != randicex and len_x > randicex and len_x >= (display_width - display_width + 1):
            len_x -= 1
            head = pygame.transform.rotate(img, 180)

        elif len_x != randicex and len_x < randicex and len_x <= (display_width - 1):
            len_x += 1
            head = img
        elif len_y != randicey and len_y > randicey and len_y >= (display_height - display_height + 1):
            len_y -= 1
            head = pygame.transform.rotate(img, 270)
        elif len_y != randicey and len_y < randicey and len_y <= (display_height - 1):
            len_y += 1
            head = pygame.transform.rotate(img, 90)

        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        if len_x >= display_width or len_x < 0 or len_y < 0 or len_y >= display_height:
            gameOver = True

        len_x += len_x_change
        len_y += len_y_change
        gameDisplay.fill(black)

        gameDisplay.blit(ice, (randicex, randicey))
        snakeTail = []
        snakeTail.append(Snaketail_x)
        snakeTail.append(Snaketail_y)
        snakeHead = []
        snakeHead.append(len_x)
        snakeHead.append(len_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        # if moving right
        #   next_x = len_x + 60
        #   next_y = len_y
        # elif moving up
        # next_x = len_x
        # next_y = len_y + 60
        # elif ....

        # next_position = [next_x, next_y]

        # for eachSegment in snakeList[:-1]:
        #    if eachSegment == next_position:
        # Blocked -- need to choose a different direction

        snake(block_size, snakeList)

        score(snakeLength - 1)

        if len_x > randicex and len_x < randicex + iceThickness or len_x + block_size > randicex and len_x + block_size < randicex + iceThickness:
            if len_y > randicey and len_y < randicey + iceThickness:
                randicex, randicey = randice()
                snakeLength += 10
            elif len_y + block_size > randicey and len_y + block_size < randicey + iceThickness:
                randicex, randicey = randice()
                snakeLength += 10
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


gameLoop()