import pygame as py,sys
from pygame.locals import *
import time

breite = 500
hoehe = 500
hintergrund = (255,255,255)

TicTacToe = [[None] * 3, [None] * 3, [None] * 3]

py.init()
fps = 30
zeit = py.time.Clock()
bild = py.display.set_mode((breite,hoehe+100),0,32)

intro = py.image.load('intro.png')
bildX = py.image.load('x.png')
bildO = py.image.load('o.png')
