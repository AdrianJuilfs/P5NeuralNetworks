import pygame
import random
import os
import time
import neat
import pickle
pygame.font.init() #initialisierung der Schriftarten von pygame

FENSTER_BREITE = 600
FENSTER_HOEHE = 800
BODEN = 730
STAT_FONT = pygame.font.SysFont("arial", 50)
END_FONT = pygame.font.SysFont("arial", 70)
LINIEN_ZEICHNEN = False

WIN = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE))
pygame.display.set_caption("Flappy Bird")

roehren_bild = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/roehre.png")).convert_alpha())
hintergrund_bild = pygame.transform.scale(pygame.image.load(os.path.join("imgs/hintergrund.png")).convert_alpha(), (600, 900))
vogel_bilder = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/vogel" + str(x) + ".png"))) for x in range(1, 4)]
boden_bild = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs/boden.png")).convert_alpha())

gen = 0

class Vogel:

    animationsrotation = 25
    bilder = vogel_bilder
    rotationsgeschwindigkeit = 20
    animationszeit = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.ausrichtung = 0
        self.tick_zaehler = 0
        self.geschwindigkeit = 0
        self.hoehe = self.y
        self.bild_zaehler = 0
        self.bild = self.bilder[0]

    def springen(self):

        self.geschwindigkeit = -10.5
        self.tick_zaehler = 0
        self.hoehe = self.y

    def bewegen(self):

        self.tick_zaehler += 1

        # gravitation
        verschiebung = self.geschwindigkeit * self.tick_zaehler + 0.5 * 3 * self.tick_zaehler ** 2

        # geschwindigkeit
        if verschiebung >= 16:
            verschiebung = (verschiebung/abs(verschiebung)) * 16

        if verschiebung < 0:
            verschiebung -= 2

        self.y = self.y + verschiebung

        if verschiebung < 0 or self.y < self.hoehe + 50:
            if self.ausrichtung < self.animationsrotation:
                self.ausrichtung = self.animationsrotation
        else: 
            if self.ausrichtung > -90:
                self.ausrichtung -= self.rotationsgeschwindigkeit

    def zeichnen(self, win):

        self.bild_zaehler += 1

        # Animation des Vogels
        if self.bild_zaehler <= self.animationszeit:
            self.bild = self.bilder[0]
        elif self.bild_zaehler <= self.animationszeit*2:
            self.bild = self.bilder[1]
        elif self.bild_zaehler <= self.animationszeit*3:
            self.bild = self.bilder[2]
        elif self.bild_zaehler <= self.animationszeit*4:
            self.bild = self.bilder[1]
        elif self.bild_zaehler == self.animationszeit*4 + 1:
            self.bild = self.bilder[0]
            self.bild_zaehler = 0

        if self.ausrichtung <= -80:
            self.bild = self.bilder[1]
            self.bild_zaehler = self.animationszeit * 2


        gedrehtesBild(win, self.bild, (self.x, self.y), self.ausrichtung)

    def get_mask(self):

        return pygame.mask.from_surface(self.bild)


class Roehre():

    platz = 200
    geschwindigkeit = 5

    def __init__(self, x):

        self.x = x
        self.hoehe = 0

        self.oben = 0
        self.unten = 0

        self.ROHERE_OBEN = pygame.transform.flip(roehren_bild, False, True)
        self.ROEHRE_UNTEN = roehren_bild

        self.geschafft = False

        self.hoehe_setzen()

    def hoehe_setzen(self):

        self.hoehe = random.randrange(50, 450)
        self.oben = self.hoehe - self.ROHERE_OBEN.get_height()
        self.unten = self.hoehe + self.platz

    def bewegen(self):

        self.x -= self.geschwindigkeit

    def zeichnen(self, win):

        # obere Röhre wird gezeichnet
        win.blit(self.ROHERE_OBEN, (self.x, self.oben))
        # untere Röhre wird gezeichnet
        win.blit(self.ROEHRE_UNTEN, (self.x, self.unten))


    def kollision(self, bird, win):

        vogel_maske = bird.get_mask()
        obere_maske = pygame.mask.from_surface(self.ROHERE_OBEN)
        untere_maske = pygame.mask.from_surface(self.ROEHRE_UNTEN)
        oben_versetzt = (self.x - bird.x, self.oben - round(bird.y))
        unten_versetzt = (self.x - bird.x, self.unten - round(bird.y))

        unterer_punkt = vogel_maske.overlap(untere_maske, unten_versetzt)
        oberer_Punkt = vogel_maske.overlap(obere_maske,oben_versetzt)

        if unterer_punkt or oberer_Punkt:
            return True

        return False

class Boden:
    GESCHWINDIGKEIT = 5
    BREITE = boden_bild.get_width()
    BILD = boden_bild

    def __init__(self, y):
 
        self.y = y
        self.x1 = 0
        self.x2 = self.BREITE

    def bewegen(self):

        self.x1 -= self.GESCHWINDIGKEIT
        self.x2 -= self.GESCHWINDIGKEIT
        if self.x1 + self.BREITE < 0:
            self.x1 = self.x2 + self.BREITE

        if self.x2 + self.BREITE < 0:
            self.x2 = self.x1 + self.BREITE

    def zeichnen(self, win):

        win.blit(self.BILD, (self.x1, self.y))
        win.blit(self.BILD, (self.x2, self.y))


def gedrehtesBild(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def fenster_zeichnen(gewonnen, voegel, roehren, boden, punktzahl, gen, pipe_ind):

    if gen == 0:
        gen = 1
    gewonnen.blit(hintergrund_bild, (0, 0))

    for pipe in roehren:
        pipe.zeichnen(gewonnen)

    boden.zeichnen(gewonnen)
    for bird in voegel:
        # zeichnet Linien vom vogel zur Röhre
        if LINIEN_ZEICHNEN:
            try:
                pygame.draw.line(gewonnen, (255, 0, 0), (bird.x + bird.bild.get_width() / 2, bird.y + bird.bild.get_height() / 2),
                                 (roehren[pipe_ind].x + roehren[pipe_ind].ROHERE_OBEN.get_width() / 2, roehren[pipe_ind].hoehe), 5)
                pygame.draw.line(gewonnen, (255, 0, 0), (bird.x + bird.bild.get_width() / 2, bird.y + bird.bild.get_height() / 2),
                                 (roehren[pipe_ind].x + roehren[pipe_ind].ROEHRE_UNTEN.get_width() / 2, roehren[pipe_ind].unten), 5)
            except:
                pass
        # vogel zeichnen
        bird.zeichnen(gewonnen)

    # Punktzahl anzeigen
    score_label = STAT_FONT.render("Score: " + str(punktzahl), 1, (255, 255, 255))
    gewonnen.blit(score_label, (FENSTER_BREITE - score_label.get_width() - 15, 10))

    # Generationen
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    gewonnen.blit(score_label, (10, 10))

    # Anzahl der lebenden Vögel anzeigen
    score_label = STAT_FONT.render("Alive: " + str(len(voegel)), 1, (255, 255, 255))
    gewonnen.blit(score_label, (10, 50))

    pygame.display.update()


def gene_auswerten(genomes, config):

    global WIN, gen
    win = WIN
    gen += 1

    # Zuerst werden Listen erstellt, welche die Gene enthalten, dann diese im Zusammenhang mit dem neuronalen Netzwerk
    # und am Ende wird noch das Vogelobjekt erstellt, mit welchem die KI am Ende spielt
    nets = []
    voegel = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # Zu beginn ist das fitness level 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        voegel.append(Vogel(230, 350))
        ge.append(genome)

    base = Boden(BODEN)
    roehren = [Roehre(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(voegel) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(voegel) > 0:
            if len(roehren) > 1 and voegel[0].x > roehren[0].x + roehren[0].ROHERE_OBEN.get_width():  # guckt, ob die erste oder die zweite Röhre
                pipe_ind = 1                                                                            #verwendet werden soll, wenn mehrere auf dem Bildschirm sind

        for x, vogel in enumerate(voegel):  # pro sekunde wo ein Vogel lebt, wird das fitness level um 0,1 hochgesetzt
            ge[x].fitness += 0.1
            vogel.bewegen()

            # sendet dem neuron die Vogelposition, die Röhrenpositionen and und lässt die KI entscheiden, ob der Vogel springen soll, oder nicht
            output = nets[voegel.index(vogel)].activate((vogel.y, abs(vogel.y - roehren[pipe_ind].hoehe), abs(vogel.y - roehren[pipe_ind].unten)))

            if output[0] > 0.5:  # benutzt wird eine tanh Aktivierungsfunktion, welche ein Ergebniuss zwischen -1 und 1 hält. Wenn über 0.5 soll der Vogel springen
                vogel.springen()

        base.bewegen()

        rem = []
        add_pipe = False
        for pipe in roehren:
            pipe.bewegen()
            # checking for collision
            for vogel in voegel:
                if pipe.kollision(vogel, win):
                    ge[voegel.index(vogel)].fitness -= 1
                    nets.pop(voegel.index(vogel))
                    ge.pop(voegel.index(vogel))
                    voegel.pop(voegel.index(vogel))

            if pipe.x + pipe.ROHERE_OBEN.get_width() < 0:
                rem.append(pipe)

            if not pipe.geschafft and pipe.x < vogel.x:
                pipe.geschafft = True
                add_pipe = True

        if add_pipe:
            score += 1
            # hier wird der fitnesswert jedes Mal, wenn er eine Röhre durchquert, hochgesetzt
            for genome in ge:
                genome.fitness += 5
            roehren.append(Roehre(FENSTER_BREITE))

        for r in rem:
            roehren.remove(r)

        for vogel in voegel:
            if vogel.y + vogel.bild.get_height() - 10 >= BODEN or vogel.y < -50:
                nets.pop(voegel.index(vogel))
                ge.pop(voegel.index(vogel))
                voegel.pop(voegel.index(vogel))

        fenster_zeichnen(WIN, voegel, roehren, base, score, gen, pipe_ind)




def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Population wird erstellt
    p = neat.Population(config)

    # ein reporter wird erstellt, um den Fortschritt der KI in der Konsole auszugeben
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Maximum 50 Generationen werden erstellt
    winner = p.run(gene_auswerten, 50)

    # nach 50 Generationen wird das finale Ergebnis abgezeigt
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'CONFIG.txt')
    run(config_path)