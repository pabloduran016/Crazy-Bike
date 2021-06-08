# from matplotlib import pyplot as plt  # Se importan las librerías
from math import *
import random


class MapCreator:
    # constants
    rquadratic = 1
    rlinear = 2
    rsine = 3
    rgrowing = 1
    rdecreasing = 2
    rparabolaup = 3
    rparaboladown = 4
    r2 = 1
    r5 = random.randint(0, 100)

    def __init__(self, initial):
        self.parablen = 0  # Length of the parable
        self.parab_a = 1  # ax2 + bx (parable)
        self.parab_b = 0  # ax2 + bx (parable)
        self.linelen = 0  # Length of the stright line
        self.lineslope = 1  # cx (recta)
        self.sinelen = 0  # Length of the wave
        self.sine_d = 100  # sine_d(sin(ex)) (wave)
        self.sine_e = 1 / 4  # sine_d(sin(ex)) (wave)
        self.map = []  # Where map values are stored
        self.finalmap = []  # Completed map storage whe using createmap
        self.totaldistance = 0  # Value of max(x) in the map
        self.type = None  # String with type of map being created
        self.lastdot = initial  # Ultimo valor de la y para enlazar con la siguiente parte

    def __str__(self):
        # Cuando se llama al objeto este devuelve una value de sus atributos
        data = [self.parablen, self.linelen, self.sinelen, self.parab_a, self.parab_b, self.lineslope, self.sine_d,
                self.sine_e, self.map, self.totaldistance, self.type, self.lastdot]
        return str(data)

    def typelength(self):
        # Este método se usa para seleccionar que tipo de mapa se va acrear y cual va parab_a ser su longitud
        r1 = random.randint(1, 3)
        # r1 = 10
        r4 = random.randint(500, 800)
        if r1 == self.rquadratic:
            self.parablen = r4 * 2
            r5 = random.randint(1500, 3000)
            self.r2 = random.randint(1, 4)
            if self.r2 == self.rgrowing:
                self.parab_a = 1 / r5
                self.type = 'quadratic growing'
            elif self.r2 == self.rdecreasing:
                self.parab_a = -1 / r5
                self.type = 'quadratic decreasing'
            elif self.r2 == self.rparabolaup:
                r3 = random.randint(0, 100)
                self.parab_a = 1 / r5
                self.parab_b = self.parablen * (r3 / 100) / 2
                self.type = 'parabola up'
            elif self.r2 == self.rparaboladown:
                r3 = random.randint(0, 100)
                self.parab_a = -1 / r5
                self.parab_b = self.parablen * (r3 / 100) / 2
                self.type = 'parabola up'
            self.quadratic()

        elif r1 == self.rlinear:
            self.linelen = r4 * 2
            self.r5 = random.randint(-100, 100)
            self.lineslope = 1.7 * self.r5 / 100
            self.type = 'linear'
            self.linear()

        elif r1 == self.rsine:
            r2 = random.randint(50, 80)
            r3 = random.randint(1, 10)
            self.sinelen = int(r4 * 5 / r3)
            self.sine_d = r3 / 10
            self.sine_e = r2
            self.type = 'sine'
            self.sine()

    def straightline(self, n):
        for x in range(n):
            self.map.append(self.lastdot)
        self.totaldistance = self.totaldistance + n
        self.lastdot = self.lastdot

    def quadratic(self):
        for x in range(self.parablen):
            self.map.append(self.parab_a * (x - self.parab_b) ** 2 + self.lastdot -
                            (self.parab_b * self.parab_a * (self.parab_b - (2 * x))))
        self.totaldistance = self.totaldistance + self.parablen
        self.lastdot = self.parab_a * (self.parablen - self.parab_b) ** 2 + self.lastdot - \
                       (self.parab_b * self.parab_a * (self.parab_b - (2 * self.parablen)))

    def linear(self):
        for x in range(self.linelen):
            self.map.append(self.lineslope * x + self.lastdot)
        self.totaldistance = self.totaldistance + self.linelen
        self.lastdot = self.lineslope * self.linelen + self.lastdot

    def sine(self):
        for x in range(self.sinelen):
            self.map.append(self.sine_d * self.sine_e * sin(x / self.sine_e) + self.lastdot)
        self.totaldistance = self.totaldistance + self.sinelen
        self.lastdot = self.sine_d * self.sine_e * sin(self.sinelen / self.sine_e) + self.lastdot

    def updatemap(self):
        # Este método se usa para crear más mapa si el que ya estaba credo se ha acabado
        self.straightline(500)
        self.typelength()
        return self.totaldistance

    def get_y(self):
        # Este método se usa para recorrer los valores y del mapa y crear mapa infinito
        if self.map:
            y = self.map[0]
            self.map.pop(0)
            return y
        else:
            self.updatemap()
            y = self.map[0]
            self.map.pop(0)
            return y

    def createmap(self, n):
        # Este métdo se usa para crear un gráfico del mapa
        for k in range(n):
            self.straightline(500)
            for i in self.map:
                self.finalmap.append(i)
            self.map = []
            self.typelength()
            for i in self.map:
                self.finalmap.append(i)
            self.map = []

        # plt.plot(range(self.totaldistance), self.finalmap, 'k-')

        # ----Descomentar para enseñar un grafico y guradarlo---- #
        # plt.axis([0, 700, -350, 3500])
        # plt.savefig('f3')
        # plt.show()


def createmap(n):
    # Función para crear un mapa
    finalmap = []
    newmap = MapCreator(100)

    while newmap.totaldistance < n:

        newmap.straightline(500)

        for i in newmap.map:
            finalmap.append(i)

        newmap.map = []

        newmap.typelength()

        for i in newmap.map:
            finalmap.append(i)

        newmap.map = []

    # plt.plot(range(newmap.totaldistance), finalmap, 'k-')

    # ----Descomentar para enseñar un grafico y guradarlo---- #
    # plt.axis([0, 700, -350, 3500])
    # plt.savefig('f3')
    # plt.show()
