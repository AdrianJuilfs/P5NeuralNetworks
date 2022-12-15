import sys

import pygame as py
from pygame.locals import *
import time

# deklaration des Feldes und des startenden zeichens
breite = 400
hoehe = 400
XO = "x"
# Deklaration des zeichnens und des Gewinn booleans
zeichnen = False
gewonnen = None
# Hintergrundfarbe und Farbe der Linie
hintergrund = (255, 255, 255)
linienFarbe = (10, 10, 10)

# Das TicTacToe-Feld als Array
TicTacToe = [[None] * 3, [None] * 3, [None] * 3]

# Initialisierung
py.init()
fps = 30
CLOCK = py.time.Clock()
display = py.display.set_mode((breite, hoehe + 100), 0, 32)

# Implementierung des Intros und der X'e und O's
intro = py.image.load('intro.png')
bildX = py.image.load('x.png')
bildO = py.image.load('o.png')

# Skalierung der Bilder auf die richtige Größe
intro = py.transform.scale(intro, (breite, hoehe + 100))
bildX = py.transform.scale(bildX, (80, 80))
bildO = py.transform.scale(bildO, (80, 80))


# Definition des Spielstarts:
def spiel_starten():
    display.blit(intro, (0, 0))
    py.display.update()
    time.sleep(1)
    display.fill(hintergrund)
# Spielfeld aufbauen:
    py.draw.line(display, linienFarbe, (breite / 3, 0), (breite / 3, hoehe), 7)
    py.draw.line(display, linienFarbe, (breite / 3 * 2, 0), (breite / 3 * 2, hoehe), 7)
# Waagerechte Linien
    py.draw.line(display, linienFarbe, (0, hoehe / 3), (breite, hoehe / 3), 7)
    py.draw.line(display, linienFarbe, (0, hoehe / 3 * 2), (breite, hoehe / 3 * 2), 7)
# Senkrechte Linien
    zeichen_status()


# Überprüfung was gezeichnet wurde
def zeichen_status():
    global zeichnen

    if gewonnen is None:
        message = XO.upper() + "'s ist am Zug"
    else:
        message = gewonnen.upper() + " hat Gewonnen!"
    if zeichnen:
        message = 'Unentschieden!'
    font = py.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    display.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(breite / 2, 500 - 50))
    display.blit(text, text_rect)
    py.display.update()


# Gewinnüberprüfung
def gewonnen_pruefen():
    global TicTacToe, gewonnen, zeichnen
    # überprüfung von gewonnen Reihen
    for row in range(0, 3):
        if (TicTacToe[row][0] == TicTacToe[row][1] == TicTacToe[row][2]) and (TicTacToe[row][0] is not None):
            # Gewonnen
            gewonnen = TicTacToe[row][0]
            # Gewinnerlinie zeichnen
            py.draw.line(display, (250, 0, 0), (0, (row + 1) * hoehe / 3 - hoehe / 6),
                         (breite, (row + 1) * hoehe / 3 - hoehe / 6), 4)
            break
    # überprüfung von gewonnen Reihen
    for col in range(0, 3):
        if (TicTacToe[0][col] == TicTacToe[1][col] == TicTacToe[2][col]) and (TicTacToe[0][col] is not None):
            # gewonnen
            gewonnen = TicTacToe[0][col]
            # Gewinner-Linie zeichnen
            py.draw.line(display, (250, 0, 0), ((col + 1) * breite / 3 - breite / 6, 0),
                         ((col + 1) * breite / 3 - breite / 6, hoehe), 4)
            break
    # überprüfung diagonaler Gewinner
    if (TicTacToe[0][0] == TicTacToe[1][1] == TicTacToe[2][2]) and (TicTacToe[0][0] is not None):
        # Diagonaler Sieg von links nach rechts
        gewonnen = TicTacToe[0][0]
        py.draw.line(display, (250, 70, 70), (50, 50), (350, 350), 4)
    if (TicTacToe[0][2] == TicTacToe[1][1] == TicTacToe[2][0]) and (TicTacToe[0][2] is not None):
        # Diagonaler Sieg von rechts nach Links
        gewonnen = TicTacToe[0][2]
        py.draw.line(display, (250, 70, 70), (350, 50), (50, 350), 4)
        # Überpreüfung ob alle Felder Leer sind
    if all([all(row) for row in TicTacToe]) and gewonnen is None:
        zeichnen = True
    zeichen_status()


# Zeichnet die X'e und O's
def zeichnen_von_xo(row, col):
    global TicTacToe, XO, posx, posy
    if row == 1:
        posx = 30
    if row == 2:
        posx = breite / 3 + 30
    if row == 3:
        posx = breite / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = hoehe / 3 + 30
    if col == 3:
        posy = hoehe / 3 * 2 + 30
    TicTacToe[row - 1][col - 1] = XO
    if XO == 'x':
        display.blit(bildX, (posy, posx))
        XO = 'o'
    else:
        display.blit(bildO, (posy, posx))
        XO = 'x'
    py.display.update()
    # gibt das akzuelle Spielfeld in die Konsole aus
    print(TicTacToe)


def user_click():
    # bekommte die Koordinaten des geklickten Feldes
    x, y = py.mouse.get_pos()
    # bekommt die Zeile des geklickten Feldes
    if x < breite / 3:
        col = 1
    elif x < breite / 3 * 2:
        col = 2
    elif x < breite:
        col = 3
    else:
        col = None
    # bekommt die Spalte des geklickten Feldes
    if y < hoehe / 3:
        row = 1
    elif y < hoehe / 3 * 2:
        row = 2
    elif y < hoehe:
        row = 3
    else:
        row = None
    if row and col and TicTacToe[row - 1][col - 1] is None:
        global XO
        # zeichnet das X oder O auf das Feld
        zeichnen_von_xo(row, col)
        gewonnen_pruefen()


def spiel_reseten():
    global TicTacToe, gewonnen, XO, zeichnen
    time.sleep(3)
    zeichnen = False
    XO = 'x'
    spiel_starten()
    gewonnen = None
    TicTacToe = [[None] * 3, [None] * 3, [None] * 3]


spiel_starten()
# Endlosschleife des Spiels, damit es immer wieder gespielt werden kann
while True:
    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # Click-Event Erkennung
            user_click()
            if gewonnen or zeichnen:
                spiel_reseten()
    py.display.update()
    CLOCK.tick(fps)
