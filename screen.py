import os, shutil, curses
import screen


log = None
interface = None

class Window:
    
    def __init__(self, x, y, w, h, scr, name):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.scr = scr
        self.name = name
        self.border = True
        self.text_center = False

        self.wipe()

    def set_border(self, value):
        self.border = value

    def set_text_center(self, value):
        self.text_center = value

    def set_box_center(self):
        x = (screen.interface.get_width() - self.get_width()) // 2
        y = (screen.interface.get_height() - self.get_height()) // 2
        self.move(x, y)

    def refresh(self):
        self.scr.refresh()

    def clear(self):
        self.scr.clear()

    def wipe(self):
        self.scr.clear()
        self.decorate()

    def move(self, x, y):
        self.scr.mvwin(y, x)

    def decorate(self):
        if self.border:
            self.scr.border()
            self.scr.addstr(0, 1, " " + self.name + " ")

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def write(self, x, y, string):

        margin = 0

        if self.border:
            margin = 1

        if self.text_center:
            padding = (self.get_width() - len(string) - 2 * margin) // 2
            string = " " * padding + string
            
        self.scr.addnstr(x + margin, y + margin,
            string, self.get_width() - 2 * margin)


class Log(Window):

    def __init__(self):
        x, y, w, h = 0, curses.LINES - 10,  curses.COLS, 10
        scr = curses.newwin(h, w, y, x)
        super().__init__(x, y, w, h, scr, "Log")
        self.history = []
        self("Bite")

    def __call__(self, smt):
        self.to_file(smt)
        self.to_scr(smt)

    def to_scr(self, smt):

        h = self.history
        h += [smt]

        if len(h) > self.get_height() - 2:
            h = h[len(h) - (self.get_height() - 2):]

        self.wipe()
        [self.write(i, 0, h[i]) for i in range(len(h))]
        self.scr.refresh()

    def to_file(self, smt):
        with open('screen.log', 'a') as f:
            f.write(smt + "\n")


class Title(Window):

    def __init__(self):
        pass


class Interface(Window):

    def __init__(self):
        scr = curses.initscr()
        x, y = 0, 0
        w, h = curses.COLS, curses.LINES

        super().__init__(x, y, w, h, scr, "Interface")
        self.set_border(False)
        self.clear()
        self.refresh()

        self.scr.keypad(True)
        self.scr.nodelay(True)


    def end(self):
        self.scr.keypad(False)
        self.scr.nodelay(False)

    def get_key(self):

        try:
            key = self.scr.getkey()
            curses.flushinp()
            log("Key: {}".format(key))

        except:
            key = None

        return key


def init():
    global interface, log

    interface = Interface()
    log = Log()

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

def end():
    interface.end()

    curses.echo()
    curses.nocbreak()
    curses.curs_set(2)
    curses.endwin()
