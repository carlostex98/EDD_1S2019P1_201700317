import os
import curses
import time
from curses import textpad
import random
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
        self.tipo = tipo
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
        self.tam += 1

    def truncar(self):
        self.primero = None
        self.ultimo = None
        self.tam = 0

    def reporte(self):
        if self.tam > 0:
            actual = self.primero
            f = open("Grafix2.dot", "w")
            f.write("digraph G {\n node [shape=plaintext]\n")
            f.write(
                "some_node [ \n label=< \n <table border=\"0\" cellborder=\"1\" cellspacing=\"0\"> \n")
            f.write(" <tr><td> </td></tr> \n")
            while not actual is None:
                f.write(" <tr><td> (" + str(actual.x) + " , " +
                        str(actual.y) + ") " + str(actual.tipo) + " </td></tr> \n")
                actual = actual.sig

            f.write("</table>> \n ];")
            f.write("}")
            f.close()
            os.system("dot -Tjpg Grafix2.dot -o imagen2.jpg")

            os.system("xdg-open imagen2.jpg")


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

    def reporte(self):
        if self.tam > 0:
            f = open("Grafix4.dot", "w")
            f.write("digraph G {\n")
            f.write("node [shape = square];\n")
            f.write("rankdir=LR;\n")

            actual = self.primero
            x = 0
            while x != self.tam:
                f.write("s" + str(actual.nombre) +
                        " [label=\"" + str(actual.nombre) + "\"]; \n")
                x += 1
                actual = actual.sig

            actual = self.primero
            x = 0
            while x != self.tam:
                f.write("s" + str(actual.nombre) + "->s" +
                        str(actual.sig.nombre) + ";\n")
                f.write("s" + str(actual.nombre) + "->s" +
                        str(actual.ant.nombre) + ";\n")
                x += 1
                actual = actual.sig
            f.write("}")
            f.close()
            os.system("dot -Tjpg Grafix4.dot -o imagen4.jpg")
            os.system("xdg-open imagen4.jpg")


class puntoss():
    def __init__(self, nombre, puntos):
        self.sig = None
        self.nombre = nombre
        self.puntos = puntos


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

    def reporte(self):
        actual = self.primero
        f = open("Grafix3.dot", "w")
        f.write("digraph G {\n rankdir=LR\n ")
        f.write("node [shape = square];\n")
        while not actual is None:
            f.write("s" + str(actual.nombre) +
                    " [label=\"(" + str(actual.nombre) + " , " + str(actual.puntos) + ")\"]; \n")
            actual = actual.sig

        actual = self.primero
        while not actual is None:
            if not actual.sig is None:
                f.write("s" + str(actual.nombre) + " -> s" +
                        str(actual.sig.nombre) + "; \n")
            actual = actual.sig
        actual = self.ultimo
        f.write("s" + str(actual.nombre) + " -> NULL; \n")
        f.write("}")
        f.close()
        os.system("dot -Tjpg Grafix3.dot -o imagen3.jpg")

        os.system("xdg-open imagen3.jpg")

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
        self.tam = 0

    def mas_culebra(self, x, y):
        nuevo = numeral(x, y)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.sig = nuevo
            nuevo.ant = self.ultimo
            self.ultimo = nuevo
        self.tam += 1

    def quitar_culebra(self):
        self.ultimo = None
        self.primero = None
        self.tam = 0

    def reporte(self):
        if self.tam > 0:
            actual = self.primero
            f = open("Grafix1.dot", "w")
            f.write("digraph G {\n")
            f.write("node [shape = square];\n")
            f.write("rankdir=LR;\n")
            while not actual is None:
                f.write("s" + str(actual.x) + str(actual.y) +
                        " [label=\"(" + str(actual.x) + " , " + str(actual.y) + ")\"]; \n")
                actual = actual.sig
            actual = self.primero

            while not actual is None:
                if actual == self.primero:
                    if not actual.sig is None:
                        f.write("s" + str(actual.x) + str(actual.y) +
                                " -> s" + str(actual.sig.x) + str(actual.sig.y) + ";\n")
                else:
                    f.write("s" + str(actual.x) + str(actual.y) +
                            " -> s" + str(actual.ant.x) + str(actual.ant.y) + ";\n")
                    if not actual.sig is None:
                        f.write("s" + str(actual.x) + str(actual.y) +
                                " -> s" + str(actual.sig.x) + str(actual.sig.y) + ";\n")
                actual = actual.sig
            actual = self.primero
            f.write("s" + str(actual.x) + str(actual.y) + " ->NULL_i ;\n")

            actual = self.ultimo
            f.write("s" + str(actual.x) + str(actual.y) + " -> NULL_f ;\n")

            f.write("}")
            f.close()
            os.system("dot -Tjpg Grafix1.dot -o imagen1.jpg")

            os.system("xdg-open imagen1.jpg")


# fin culebra
# fin de estructuras
sc = cc_punto()
scu = cc_usuario()
pila = cc_pila()
masacuata = cc_numeral()

menu = ['1. Play', '2. Scoreboard', '3. User Selection',
        '4. Reports', '5. Bulk loading', '6. Exit']

menu2 = ['1. snake report', '2. score report', '3. scoreboard report',
         '4. user report', '5. regresar']


def create_food(snake, box):
    food = None
    while food is None:
        food = [random.randint(box[0][0] + 1, box[1][0] - 1),
                random.randint(box[0][1] + 1, box[1][1] - 1)]
        if food in snake:
            food = None
    return food


def create_nofood(snake, box):
    nfood = None
    while nfood is None:
        nfood = [random.randint(box[0][0] + 1, box[1][0] - 1),
                 random.randint(box[0][1] + 1, box[1][1] - 1)]
        if nfood in snake:
            nfood = None
    return nfood


def culebra2(stdscr):
    # nivel dos compa
    masacuata.quitar_culebra()
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(70)

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh // 2, sw // 2 + 1],
             [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
    direction = curses.KEY_RIGHT

    for y, x in snake:
        stdscr.addstr(y, x, '#')

    # comida/enemigo
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '+')

    # mostramos el punteo
    score = 0
    score_text = "Punteo: " + str(score * 10)
    stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text, curses.A_BOLD)

    while 1:
        key = stdscr.getch()

        if key in [curses.KEY_RIGHT,
                   curses.KEY_LEFT,
                   curses.KEY_DOWN,
                   curses.KEY_UP]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]

        # lo manejamos como una pila
        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        if snake[0] == food:
            # si cabeza esta en comida
            score += 1
            score_text = "Score: " + str(score * 10)
            stdscr.addstr(1, sw // 2 - len(score_text) //
                          2, score_text, curses.A_BOLD)
            pila.agregar(food[1], food[0], "Comida (*)")
            # nueva comida/nocomida
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '+')

        else:
            # cambio cola culebra
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # para que acabe el juego
        if (snake[0][0] in [box[0][0], box[1][0]] or
                snake[0][1] in [box[0][1], box[1][1]]):
            msg = "<------Fin, has perdido------>"
            sc.modificar(usx.getx(), score * 10)
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            x = 0
            while True:
                if x == len(snake):
                    break
                else:
                    ss = snake[x]
                    masacuata.mas_culebra(ss[1], ss[0])
                    x += 1

            break

        if score == 4:
            msg = "<------Fin has ganado, presiona enter------>"
            sc.modificar(usx.getx(), score * 10)
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            x = 0
            while True:
                if x == len(snake):
                    break
                else:
                    ss = snake[x]
                    masacuata.mas_culebra(ss[1], ss[0])
                    x += 1

            break


def culebra(stdscr):

    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    masacuata.quitar_culebra()

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh // 2, sw // 2 + 1],
             [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
    direction = curses.KEY_RIGHT

    for y, x in snake:
        stdscr.addstr(y, x, '#')

    # comida/enemigo
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '+')

    # mostramos el punteo
    score = 0
    score_text = "Punteo: " + str(score * 10)
    stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text, curses.A_BOLD)

    while 1:
        key = stdscr.getch()

        if key in [curses.KEY_RIGHT,
                   curses.KEY_LEFT,
                   curses.KEY_DOWN,
                   curses.KEY_UP]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]

        # lo manejamos como una pila
        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        if snake[0] == food:
            # si cabeza esta en comida
            score += 1
            score_text = "Punteo: " + str(score * 10)
            stdscr.addstr(1, sw // 2 - len(score_text) //
                          2, score_text, curses.A_BOLD)
            pila.agregar(food[1], food[0], "Comida (*)")
            # nueva comida/nocomida
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '+')

        else:
            # cambio cola culebra
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # para que acabe el juego
        if (snake[0][0] in [box[0][0], box[1][0]] or
                snake[0][1] in [box[0][1], box[1][1]]):
            msg = "<------Fin, has perdido------>"
            sc.modificar(usx.getx(), score * 10)
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            x = 0
            while True:
                if x == len(snake):
                    break
                else:
                    ss = snake[x]
                    masacuata.mas_culebra(ss[1], ss[0])
                    x += 1
            break

        if score == 3:
            msg = "<------Fin, has ganado, presiona enter para el nivel 2------>"
            sc.modificar(usx.getx(), score * 10)
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            x = 0
            while True:
                if x == len(snake):
                    break
                else:
                    ss = snake[x]
                    masacuata.mas_culebra(ss[1], ss[0])
                    x += 1

            culebra2(stdscr)
            break


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


def print_menu2(stdscr, selected_row_idx):
    stdscr.clear()
    stdscr.addstr(0, 5, "Usurio seleccionado: " + usx.getx())
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu2):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu2) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def new_user(stdscr):
    stdscr.clear()
    actual = ""
    while True:
        stdscr.addstr(
            2, 2, "Escribe para registrar un usuario, luego pulsa enter")
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            print_center(stdscr, "Nombre ingresado: " + actual +
                         "        -> Presiona enter para continuar")
            sc.agregar(actual)
            scu.agregar(actual)
            usx.setx(actual)
            break
        else:
            actual += str(chr(key))
            print_center(stdscr, actual)


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(text) // 2
    y = h // 2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def s_menu(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    current_row = 0

    print_menu2(stdscr, current_row)

    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1

        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                masacuata.reporte()
            if current_row == 1:
                pila.reporte()
            if current_row == 2:
                sc.reporte()
            if current_row == 3:
                scu.reporte()

            stdscr.getch()
            if current_row == len(menu2) - 1:
                break

        print_menu2(stdscr, current_row)


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
                pila.truncar()
                if usx.getx() == "":
                    new_user(stdscr)
                    culebra(stdscr)
                else:
                    culebra(stdscr)

            if current_row == 1:
                sc.scoreboard(stdscr)
            if current_row == 2:
                usr_select(stdscr)
            if current_row == 3:
                s_menu(stdscr)
            if current_row == 4:
                print_center(stdscr,":(")
            if current_row == 5:
                print_center(stdscr, "#LoveYou3000")

            stdscr.getch()
            if current_row == len(menu) - 1:
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)

