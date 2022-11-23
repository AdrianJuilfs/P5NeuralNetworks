import pygame as py,sys
from pygame.locals import *
import time

breite = 500
hoehe = 500
XO = "x"
gewonnen = None
hintergrund = (255, 255, 255)
linienFarbe = (10,10,10)

TicTacToe = [[None] * 3, [None] * 3, [None] * 3]

py.init()
fps = 30
CLOCK = py.time.Clock()
display = py.display.set_mode((breite, hoehe + 100), 0, 32)

intro = py.image.load('intro.png')
bildX = py.image.load('x.png')
bildO = py.image.load('o.png')

intro = py.transform.scale(intro, (breite, hoehe + 100))
bildX = py.transform.scale(bildX, (80, 80))
bildO = py.transform.scale(bildO, (80, 80))

def game_opening():
    display.blit(intro,(0,0))
    py.display.update()
    CLOCK.sleep(1)
    display.fill(hintergrund)

    py.draw.line(display,linienFarbe,(breite/3,0),(breite/3, hoehe),7)
    py.draw.line(display,linienFarbe,(breite/3*2,0),(breite/3*2, hoehe),7)

    py.draw.line(display,linienFarbe,(0,hoehe/3),(breite, hoehe/3),7)
    py.draw.line(display,linienFarbe,(0,hoehe/3*2),(breite, hoehe/3*2),7)
    draw_status()

def draw_status():
    global draw
    if gewonnen is None:
        message = XO.upper() + "'s Turn"
    else:
        message = gewonnen.upper() + " won!"
    if draw:
        message = 'Game Draw!'
    font = py.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    display.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(breite/2, 500-50))
    display.blit(text, text_rect)
    py.display.update()

def check_win():
    global TTT, winner,draw
    # check for winning rows
    for row in range (0,3):
        if ((TTT [row][0] == TTT[row][1] == TTT[row][2]) and(TTT [row][0] is not None)):
            # this row won
            winner = TTT[row][0]
            py.draw.line(display, (250,0,0), (0, (row + 1)*hoehe/3 -hoehe/6),
                         (breite, (row + 1)*hoehe/3 - hoehe/6 ), 4)
            break
    # check for winning columns
    for col in range (0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            gewonnen = TTT[0][col]
            #draw winning line
            py.draw.line (display, (250,0,0),((col + 1)* breite/3 - breite/6, 0),
                          ((col + 1)* breite/3 - breite/6, hoehe), 4)
            break
    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        gewonnen = TTT[0][0]
        py.draw.line (display, (250,70,70), (50, 50), (350, 350), 4)
    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        gewonnen = TTT[0][2]
        py.draw.line (display, (250,70,70), (350, 50), (50, 350), 4)
    if(all([all(row) for row in TTT]) and gewonnen is None ):
        draw = True
    draw_status()


def drawXO(row,col):
    global TTT,XO
    if row==1:
        posx = 30
    if row==2:
        posx = breite/3 + 30
    if row==3:
        posx = breite/3*2 + 30

    if col==1:
        posy = 30
    if col==2:
        posy = hoehe/3 + 30
    if col==3:
        posy = hoehe/3*2 + 30
    TTT[row-1][col-1] = XO
    if(XO == 'x'):
        display.blit(bildX,(posy,posx))
        XO= 'o'
    else:
        display.blit(bildO,(posy,posx))
        XO= 'x'
    py.display.update()
    #print(posx,posy)
    print(TTT)


def userClick():
    # get coordinates of mouse click
    x, y = py.mouse.get_pos()
    # get column of mouse click (1-3)
    if (x < breite / 3):
        col = 1
    elif (x < breite / 3 * 2):
        col = 2
    elif (x < breite):
        col = 3
    else:
        col = None
    # get row of mouse click (1-3)
    if (y < hoehe / 3):
        row = 1
    elif (y < hoehe / 3 * 2):
        row = 2
    elif (y < hoehe):
        row = 3
    else:
        row = None
    # print(row,col)
    if (row and col and TTT[row - 1][col - 1] is None):
        global XO
        # draw the x or o on screen
        drawXO(row, col)
        check_win()

def reset_game():
    global TTT, gewonnen, XO, draw
    CLOCK.sleep(3)
    XO = 'x'
    draw = False
    game_opening()
    gewonnen = None
    TTT = [[None] * 3, [None] * 3, [None] * 3]


game_opening()
# run the game loop forever
while(True):
    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            userClick()
            if(gewonnen or draw):
                reset_game()
    py.display.update()
    CLOCK.tick(fps)