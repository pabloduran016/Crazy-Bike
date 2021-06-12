from Functions.functions import *
from math import *
# from PIL import Image
vec = pg.math.Vector2


class Text:
    def __init__(self, fontname=None, fontsize=70):
        pg.font.init()
        self.font = pg.font.Font(fontname, fontsize)
        self.size = fontsize

    def render(self, surface, text, c, pos):
        x, y = pos
        surface.blit(self.font.render(text, True, c), (x, y))
        y += self.size


class Canvas(Map, pg.sprite.Sprite):
    def __init__(self, game):
        Map.__init__(self)
        pg.sprite.Sprite.__init__(self)
        self.lapizy = 0
        self.game = game
        self.lapizx = WIDTH - 2
        self.fondo = vec(0, 0)
        self.chunkimages = CANVAS_IMAGES
        self.totaly = 100
        self.totalx = WIDTH - 2
        self.totalmap = {}
        self.surfaces = {}
        self.stop = 0
        self.text = Text()
        self.loadfirstchunk()

    def loadfirstchunk(self):
        # Este método crea el primer chunk
        self.surfaces[(0, 0)] = pg.sky_image.load(self.chunkimages['chunk1'])
        self.text.render(surface=self.surfaces[(0, 0)], text=f'(0, 0)', c=REDISH, pos=(0, 0))
        # print(f'Se crean un nuevo chunk (0, 0)')

    def loademergencychunk(self, posx, posy):
        # Este método crea un nuevo chunk en la misma posición, en caso de que no haya
        if (posx, posy) not in self.surfaces:
            self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk'])
            # print(f'EMERGENCIA Se crean un nuevo chunk ({posx}, {posy})')

    def posiciondelchunky(self):
        # Este método retorna la posicion en y del chunk en el que se encuentra en lápiz
        return floor((- self.totaly + HEIGHT) / HEIGHT)

    def posiciondelchunkx(self):
        # Este método retorna la posicion en x del chunk en que se encuentra el lápiz
        return floor(self.totalx / WIDTH)

    def surfaceofchunk(self, pos=0):
        # Este método retornara la imagen del chunk
        """for (POSx, POSy) in self.surfaces:
                    if (POSx, POSy) == (self.posiciondelchunkx(), self.posiciondelchunky() + pos):
                        return self.surfaces[POSx, POSy]

                px = self.posiciondelchunkx()
                py = self.posiciondelchunky()+pos
                print(px, py)

                if (px, py) not in self.surfaces:
                    self.loademergencychunk(pos)
                    print('EMERGENCY', '!'*100)
                    return self.surfaces[px, py]"""
        try:
            return self.surfaces[self.posiciondelchunkx(), self.posiciondelchunky() + pos]
        except KeyError:
            self.loademergencychunk(self.posiciondelchunkx(), self.posiciondelchunky() + pos)
            print('EMERGENCY', '!' * 100)
            print(self.posiciondelchunkx(), self.posiciondelchunky() + pos)
            return self.surfaces[self.posiciondelchunkx(), self.posiciondelchunky() + pos]

    def eliminarchunks(self):
        # Este método borra lo chunks que se hayan quedado atrás
        p = self.game.player
        lista = []
        for i in self.surfaces:
            if i[0] < (self.posiciondelchunkx() - 10) and i[0] < (p.posiciondelchunkx() - 10):
                lista.append(i)
            elif i[1] < (self.posiciondelchunky() - 5) and i[1] < (p.posiciondelchunky() - 10):
                lista.append(i)
            elif i[1] > (self.posiciondelchunky() + 10) and i[1] > (p.posiciondelchunky() + 20):
                lista.append(i)

        for i in lista:
            self.surfaces.pop(i)
            # print(f'ELIMINADO EL CHUNK {i}')

    def eliminardelmapa(self):
        # Este método borra los datos del mapa que se van quedando atrás
        lista = []
        for i in self.totalmap:
            if i < self.totalx - 10 * WIDTH:
                lista.append(i)

        for i in lista:
            self.totalmap.pop(i)

    def move(self):
        player = self.game.player
        velx = round(player.vel.x * 50)
        # vely = round(sinelen.vy * 50)
        if velx < 0:
            s = -1
        elif velx > 0:
            s = 1
        else:
            s = 0

        for n in range(abs(velx)):
            if s == 1 or s == 0:
                if self.totalx == self.stop:
                    self.stop = 0
                if self.stop == 0:  # Si se está creando mapa nuevo ...
                    # ----1) Definir la posicion total de la y-------------------------------------------------------- #
                    self.totaly = round(self.get_y())

                    # ----2) Meter en un diccionario la coordenada x con su coordenada y------------------------------ #
                    if self.totalx not in self.totalmap:
                        self.totalmap[self.totalx] = self.totaly

                    # ----3) Segun eso, definir su posicion en el self---------------------------------------------- #
                    self.lapizx = self.totalx - WIDTH * self.posiciondelchunkx()
                    self.lapizy = - self.totaly + HEIGHT - HEIGHT * (self.posiciondelchunky())

                    # ----4) Cargar los chunks de arriba, abajo y derecha si no existen ya---------------------------- #
                    loadchunks(self)
                    # self.loadchunksp(sinelen) CREA LENTITUD REVISAR !!!!!!

                    # ----5) Pintar en el lienzo que toca con las coordenadas de lapiz x y lapiz y-------------------- #
                    rr = 20
                    pg.draw.rect(self.surfaceofchunk(), BLACK, [self.lapizx, self.lapizy, 1, int(20 * rr)])
                    pic = self.surfaceofchunk(pos=-1)
                    altura = self.lapizy - 700
                    pg.draw.rect(pic, BLACK, [self.lapizx, altura, 1, int(20 * rr)])

                # ----6) Cambiar la posición del lienzo o del personaje dependiendo de si ha saltado o no------------- #
                '''if self.totalx >= WIDTH:
                    if (self.totalx - (WIDTH - player.backwheel)) in self.totalmap:
                        self.fondo.y = -self.totalmap[self.totalx-(WIDTH-player.backwheel)]+(1/7)*HEIGHT
                    else:
                        self.fondo.y = 0
                    self.fondo.x -= 1'''

                # ----7) Aumentar en 1 la posicion total de la x------------------------------------------------------ #
                self.totalx += 1

            '''else:
                self.loadchunks()
                if self.stop == 0:
                    self.stop = self.totalx
                if (self.totalx - (WIDTH - player.backwheel)) in self.totalmap:
                    self.fondo.y = -self.totalmap[self.totalx-(WIDTH - player.backwheel)]+(1 / 7)*HEIGHT
                self.totalx -= 1
                self.fondo.x += 1'''

    def draw(self, p=0):
        player = self.game.player
        if player.frontwheel.body.velocity.x < 0:
            s = -1
        elif player.frontwheel.body.velocity.x > 0:
            s = 1
        else:
            s = 0
        for n in range(round(player.frontwheel.body.velocity.x) + p):
            if s == 1 or s == 0:
                if self.totalx == self.stop:
                    self.stop = 0
                if self.stop == 0:  # Si se está creando mapa nuevo ...
                    # ----1) Definir la posicion total de la y-------------------------------------------------------- #
                    self.totaly = round(self.get_y())
                    # ----2) Meter en un diccionario la coordenada x con su coordenada y------------------------------ #
                    if self.totalx not in self.totalmap:
                        self.totalmap[self.totalx] = self.totaly
                    # ----3) Segun eso, definir su posicion en el self---------------------------------------------- #
                    self.lapizx = self.totalx - WIDTH * self.posiciondelchunkx()
                    self.lapizy = - self.totaly + HEIGHT - HEIGHT * (self.posiciondelchunky())
                    # ----4) Cargar los chunks de arriba, abajo y derecha si no existen ya---------------------------- #
                    loadchunks(self)
                    # ----5) Pintar en el lienzo que toca con las coordenadas de lapiz x y lapiz y-------------------- #
                    rr = 20
                    pg.draw.rect(self.surfaceofchunk(), BLACK, [self.lapizx, self.lapizy, 1, int(20 * rr)])
                    pic = self.surfaceofchunk(pos=1)
                    altura = self.lapizy - 700
                    pg.draw.rect(pic, BLACK, [self.lapizx, altura, 1, int(20 * rr)])
                # ----6) Aumentar en 1 la posicion total de la x------------------------------------------------------ #
                self.totalx += 1
            else:
                loadchunks(self)
                if self.stop == 0:
                    self.stop = self.totalx
                self.totalx -= 1
    '''def loadchunks(self):
            up, down, right_down, right, right_up, left_up, left, left_down = \
             (0, -1), (0, 1), (1, 1), (1, 0), (1, -1), (-1, -1), (-1, 0), (-1, 1)
            for x, y in [up, right_up, right, right_down, left_up]:
                posx = self.posiciondelchunkx() + x
                posy = self.posiciondelchunky() + y
                if not (posx, posy) in self.surfaces:
                    self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk'])
                    self.text.render(surface=self.surfaces[posx, posy], text=f'({posx}, {posy})', lineslope=REDISH, pos=(0, 0))
                    # print(f'Se crean un nuevo chunk ({posx}, {posy})')

            posx = self.posiciondelchunkx()

            if posx < 4:
                x, y = left
                posx = self.posiciondelchunkx() + x
                posy = self.posiciondelchunky() + y
                if (posx, posy) not in self.surfaces:
                    if (posx, posy) == left:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk-1'])
                    else:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk'])
                    # print(f'Se crean un nuevo chunk ({posx}, {posy})')

                x, y = down
                posx = self.posiciondelchunkx() + x
                posy = self.posiciondelchunky() + y
                if (posx, posy) not in self.surfaces:
                    if (posx, posy) == left_down:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk-2'])
                    elif (posx, posy) == down:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk-3'])
                    else:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk'])
                    # print(f'Se crean un nuevo chunk ({posx}, {posy})')

                x, y = left_down
                posx = self.posiciondelchunkx() + x
                posy = self.posiciondelchunky() + y
                if (posx, posy) not in self.surfaces:
                    if (posx, posy) == down:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk-2'])
                    elif (posx, posy) == left_down:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk-3'])
                    else:
                        self.surfaces[(posx, posy)] = pg.sky_image.load(self.chunkimages['chunk'])
                    # print(f'Se crean un nuevo chunk ({posx}, {posy})')'''