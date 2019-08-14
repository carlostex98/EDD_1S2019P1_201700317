import os
import curses
import time
from curses import textpad
# glo vars


class vr_us_actual():
    def __init__(self):
        self.valor = ""

    def setx(self, nomb):
        self.valor = nomb

    def getx(self):
        return self.valor


usx = vr_us_actual()


class npunto():
    def __init__(self, x, y, tipo):
        self.sig = None
        self.x = x
        self.y = y


class cc_pila():
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tam = 0

    def agregar(self, x, y, tipo):
        nuevo = npunto(x, y, tipo)
        if self.primero is None:
            self.primero = self.ultimo = nuevo
        else:
            nuevo.sig = self.primero
            self.primero = nuevo

    def truncar(self):
        self.primero = None
        self.ultimo = None


# inicio usuarios
class usuario():
    def __init__(self, nombre):
        self.sig = None
        self.ant = None
        self.nombre = nombre


class cc_usuario():
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tam = 0

    def agregar(self, name):
        nuevo = usuario(name)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
            self.primero.sig = self.ultimo
            self.ultimo.ant = self.primero
            self.tam += 1

        else:
            nuevo.ant = self.ultimo
            nuevo.sig = self.primero
            self.ultimo.sig = nuevo
            self.primero.ant = nuevo
            self.ultimo = nuevo
            self.tam += 1

    def get_at_idx(self, index):
        x = 0
        actual = self.primero
        while x != self.tam:
            tmp = actual.nombre
            if x == index:
                return tmp
            else:
                actual = actual.sig
            x += 1

    def get_tam(self):
        return self.tam

# fin usuarios


# inicio scoreboard, la que debe tener max de 10
class puntoss():
    def __init__(self, nombre, puntos):
        self.sig = None
        self.nombre = nombre
        self.puntos = puntos
        self.tam = 0


class cc_punto():
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tam = 0

    def unqueue(self):
        aux = self.primero
        aux1 = self.primero.sig
        aux.sig = None
        self.primero = aux1
        self.tam -= 1

    def agregar(self, nombre):
        # solo un parametro, porque inicializamos el usuario con 0 puntos

        nuevo = puntoss(nombre, 0)
        if self.tam == 10:
            aux = self.primero
            aux1 = self.primero.sig
            aux.sig = None
            self.primero = aux1
            self.tam -= 1

        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.sig = nuevo
            self.ultimo = nuevo
        self.tam += 1

    def modificar(self, nombre, puntos):
        actual = self.primero
        enc = None
        while not enc:
            if actual.nombre == nombre:
                enc = True
            else:
                actual = actual.sig
        actual.puntos = puntos

    def scoreboard(self, stdscr):
        stdscr.clear()
        curses.beep()
        stdscr.addstr(0, 1, "SCOREBOARD", curses.A_BOLD)
        h, w = stdscr.getmaxyx()
        x = w // 2 - 20
        xx = x + 25
        stdscr.addstr(2, x, "Nombre", curses.A_UNDERLINE)
        stdscr.addstr(2, xx, "Punteo", curses.A_UNDERLINE)
        actual = self.primero
        y = 3
        while actual != None:
            stdscr.addstr(y, x, actual.nombre)
            stdscr.addstr(y, xx, str(actual.puntos))
            actual = actual.sig
            y += 1
        stdscr.refresh()


# fin scoreboard

# inicio culebra
class numeral():
    def __init__(self, x, y):
        self.sig = None
        self.ant = None
        self.x = x
        self.y = y


class cc_numeral():
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def mas_culebra(self, x, y):
        nuevo = numeral(x, y)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.sig = nuevo
            nuevo.ant = self.ultimo
            self.ultimo = nuevo

    def quitar_culebra(self):
        aux = self.ultimo
        aux1 = self.ultimo.ant
        aux1.sig = None
        aux.ant = None
        self.ultimo = aux1


# fin culebra
# fin de estructuras
sc = cc_punto()
scu = cc_usuario()

menu = ['1. Play', '2. Scoreboard', '3. User Selection',
        '4. Reports', '5. Bulk loading', '6. Exit']


def usr_select(stdscr):
    index = -1
    tecla = None
    while 1:
        if index == -1:
            index = 0
        else:
            tecla = stdscr.getch()

        if tecla == curses.KEY_RIGHT:
            index = index + 1
        elif tecla == curses.KEY_LEFT:
            index = index - 1
        elif tecla == curses.KEY_ENTER or tecla in [10, 13]:
            break

        if(index < 0):
            index = scu.get_tam() - 1

        if(index >= scu.get_tam()):
            index = 0
        vlx = scu.get_at_idx(index)
        usx.setx(str(vlx))
        print_center(stdscr, "<--" + vlx + "-->")


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    stdscr.addstr(0, 5, "Usurio seleccionado: " + usx.getx())
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(text) // 2
    y = h // 2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def main(stdscr):

    sc.agregar("michael")
    sc.agregar("juan")
    sc.agregar("pedro")
    sc.modificar("michael", 10)

    scu.agregar("michael")
    scu.agregar("juan")
    scu.agregar("pedro")

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    current_row = 0

    print_menu(stdscr, current_row)

    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                print_center(stdscr, "0")
            if current_row == 1:
                sc.scoreboard(stdscr)
            if current_row == 2:
                usr_select(stdscr)
            if current_row == 3:
                print_center(stdscr, "3")
            if current_row == 4:
                print_center(stdscr, "4")
            if current_row == 5:
                print_center(stdscr, "5")

            stdscr.getch()
            if current_row == len(menu) - 1:
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)
