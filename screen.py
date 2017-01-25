import os, shutil, curses


log = None
interface = None


class Window:
    
    def __init__(self, x, y, w, h, scr):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.scr = scr

    def refresh(self):
        self.scr.refresh()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def clear(self):
        self.scr.clear()


class Log(Window):

    def __init__(self, x, y, w, h):
        scr = curses.newwin(h, w, y, x)
        super().__init__(x, y, w, h, scr)
        self.history = []

    def __call__(self, smt):
        self.to_file(smt)
        self.to_scr(smt)

    def to_scr(self, smt):
        h = self.history

        h += [smt]
        if len(h) > self.get_height() - 2:
            h = h[len(h) - self.get_height():]

        [self.scr.addnstr(i + 1, 1,
            h[i] + " " * (self.get_width() - len(smt) - 2), self.get_width() - 2)
            for i in range(len(h))]

        self.scr.refresh()

    def to_file(self, smt):
        with open('screen.log', 'a') as f:
            f.write(smt + "\n")


class Interface(Window):

    def __init__(self):
        scr = curses.initscr()
        x, y = 0, 0
        w, h = curses.COLS, curses.LINES

        super().__init__(x, y, w, h, scr)

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


class Scene(Window):

    def __init__(self, x, y, w, h):
        w, h = 2 * w + 1, h + 2
        scr = curses.newwin(h, w, y, x)
        super().__init__(x, y, w, h, scr)
        self.clear()
        self.refresh()

    def draw_tetromino(self, t):
        for c in t.get_coverage():
            self.scr.addstr(c[1] + 1, 2 * c[0] + 1, t.get_char())
            
    def clear(self):
        super().clear()
        self.scr.border()


def init():
    global interface, scene, log

    interface = Interface()
    print(interface)
    log = Log(0, curses.LINES - 10,  curses.COLS, 10)

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)


def end():
    print(interface)
    interface.end()

    curses.echo()
    curses.nocbreak()
    curses.curs_set(2)
    curses.endwin()
