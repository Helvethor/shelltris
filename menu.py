import curses
import screen, game, keyboard

def start():

    menu = MainMenu()
    menu.start()


class Item:

    def __init__(self, name, function, args = []):
        self.function = function
        self.args = args
        self.name = name
        self.clean_please = True

    def set_clean_please(self, value):
        self.clean_please = value

    def get_clean_please(self):
        return self.clean_please

    def start(self):
        f = self.function
        screen.log(str(self.args))
        f(*self.args)

    def get_name(self):
        return self.name


class Menu(screen.Window):

    def __init__(self, x, y, w, items, name = "Menu"):
        h = len(items) * 2 + 3
        scr = curses.newwin(h, w, y, x)
        super().__init__(x, y, w, h, scr, name)
        self.set_text_center(True)

        self.items = list(items)
        self.index = 0
        self.running = False
        self.set_box_center()


    def is_selected(self, item):
        return item == self.items[self.index]

    def previous_item(self):
        self.index = (self.index - 1) % len(self.items)

    def next_item(self):
        self.index = (self.index + 1) % len(self.items)

    def get_item(self):
        return self.items[self.index]

    def handle_key(self):

        key = screen.interface.get_key()

        if key not in keyboard.menu():
            return

        if key == keyboard.UP:
            self.previous_item()

        elif key == keyboard.DOWN:
            self.next_item()

        elif key == keyboard.SELECT:
            if self.get_item().get_clean_please():
                self.clear()
                self.refresh()
            self.get_item().start()

        elif key == keyboard.BACK:
            self.end()

    def start(self):

        self.running = True
        while self.running:

            self.wipe() 
            self.draw()
            self.refresh()

            self.handle_key()

    def end(self):
        self.clear()
        self.refresh()
        self.running = False

    def draw(self):

        for index, item in enumerate(self.items):

            string = item.get_name()

            if self.is_selected(item):
                string = "[ " + string + " ]"

            self.write(1 + 2 * index, 0, string)


class MainMenu(Menu):

    def __init__(self): 
        items = [   Item("Play", game.start),
                    Item("Score", game.start),
                    Item("Keyboard", self.keyboard),
                    Item("Quit", self.end)]

        super().__init__(0, 0, 30, items)

    def keyboard(self):

        keyboard = Keyboard()
        keyboard.start()


class Keyboard(Menu):

    def __init__(self):

        items = [Item("{}: '{}'".format(keyboard.to_str(k), k), self.edit, [k])
            for k in keyboard.all()]
        [item.set_clean_please(False) for item in items]

        super().__init__(0, 0, 30, items, "Keyboard")

    def edit(self, key):

        scr = curses.newwin(5, 20, 0, 0)
        box = screen.Window(0, 0, 20, 5, scr, "Edit {}".format(keyboard.to_str(key)))
        box.set_box_center()
        box.set_text_center(True)
        box.wipe()
        box.write(0, 1, "Press a key")
        box.refresh()

        while True:
            if key:
                break
