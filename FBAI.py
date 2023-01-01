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

        self.PIPE_TOP = pygame.transform.flip(roehren_bild, False, True)
        self.PIPE_BOTTOM = roehren_bild

        self.passed = False

        self.hoehe_setzen()

    def hoehe_setzen(self):

        self.hoehe = random.randrange(50, 450)
        self.oben = self.hoehe - self.PIPE_TOP.get_height()
        self.unten = self.hoehe + self.platz

    def bewegen(self):

        self.x -= self.geschwindigkeit

    def zeichnen(self, win):

        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.oben))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.unten))


    def kollision(self, bird, win):

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.oben - round(bird.y))
        bottom_offset = (self.x - bird.x, self.unten - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

class Boden:
    VEL = 5
    WIDTH = boden_bild.get_width()
    IMG = boden_bild

    def __init__(self, y):
 
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def bewegen(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def zeichnen(self, win):

        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def gedrehtesBild(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def fenster_zeichnen(win, birds, pipes, base, score, gen, pipe_ind):

    if gen == 0:
        gen = 1
    win.blit(hintergrund_bild, (0, 0))

    for pipe in pipes:
        pipe.zeichnen(win)

    base.zeichnen(win)
    for bird in birds:
        # drawing lines from bird to pipe
        if LINIEN_ZEICHNEN:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x + bird.bild.get_width() / 2, bird.y + bird.bild.get_height() / 2),
                                 (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].hoehe), 5)
                pygame.draw.line(win, (255,0,0), (bird.x + bird.bild.get_width() / 2, bird.y + bird.bild.get_height() / 2),
                                 (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].unten), 5)
            except:
                pass
        # draw bird
        bird.zeichnen(win)

    # reflecting the score
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (FENSTER_BREITE - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def eval_genomes(genomes, config):

    global WIN, gen
    win = WIN
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Vogel(230, 350))
        ge.append(genome)

    base = Boden(BODEN)
    pipes = [Roehre(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1                                                                 # pipe on the screen for neural network input

        for x, bird in enumerate(birds):  # giving each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.bewegen()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].hoehe), abs(bird.y - pipes[pipe_ind].unten)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over, then 0.5 jump
                bird.springen()

        base.bewegen()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.bewegen()
            # checking for collision
            for bird in birds:
                if pipe.kollision(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Roehre(FENSTER_BREITE))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.bild.get_height() - 10 >= BODEN or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        fenster_zeichnen(WIN, birds, pipes, base, score, gen, pipe_ind)




def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'CONFIG.txt')
    run(config_path)