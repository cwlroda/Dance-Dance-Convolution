import pygame
import time
import datetime
from random import randint
import numpy as np

pygame.init()

width = 1200
height = 800

black = (0,0,0)
white = (255,255,255)

num = np.fromfile("a.cpp", int, 1)
print(num)

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("DDC")
gameDisplay.fill(black)
pygame.display.flip()

start = time.clock()

def symbolv():
    gameDisplay.fill(black)
    pygame.draw.polygon(gameDisplay, white, ((50,150),(110,90),(600,450),(1110,90),(1150,150),(600,650)))
    pygame.display.flip()

def symbolt():
    gameDisplay.fill(black)
    pygame.draw.rect(gameDisplay, white, (50,550,1100,100))
    pygame.display.flip()

def symboli():
    gameDisplay.fill(black)
    pygame.draw.rect(gameDisplay, white, (550,50,100,700))
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    while (time.clock() - start) < 5:
        num = randint(0,2)

    print(num)

    if num == 0:
        symbolt()
    elif num == 1:
        symbolv()
    elif num == 2:
        symboli()

    start = time.clock()