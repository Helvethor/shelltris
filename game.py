import time, copy, curses
import screen, tetromino, keyboard


def start():
    game = Game()
    game.start()

class Game:

    def __init__(self):

        self.running = False
        self.start_time = None
        self.last_au = None
        self.au_delay = 1

        board_size = (10, 20)
        self.scene = Scene(0, 0, *board_size)
        self.stats = Stats(0, 0, 20, board_size[1])

        self.groupomino = tetromino.Groupomino()
        self.tetromino = None
        self.n_tetromino = tetromino.get_random()
        self.new_tetromino()

        frame_w = self.scene.get_width() + self.stats.get_width()
        frame_h = self.scene.get_height()

        x = (screen.interface.get_width() - frame_w) // 2
        y = (screen.interface.get_height() - frame_h) // 2

        self.scene.move(x, y)
        x += self.scene.get_width()
        self.stats.move(x, y)

    def start(self):

        self.start_time = time.time()
        self.last_au = self.start_time

        self.running = True
        while self.running:

            time.sleep(1 / 20)

            self.update()
            self.draw()
            self.handle_key()

    def end(self):

        self.running = False

        screen.log("game_over:: Ha!")    
        while not screen.interface.get_key():
            pass

        self.stats.clear()
        self.stats.refresh()
        self.scene.clear()
        self.scene.refresh()

        return self.stats.get_score()

    def draw(self):

        self.scene.wipe()
        self.scene.draw(self.groupomino)
        self.scene.draw(self.tetromino)
        self.scene.refresh()

        self.stats.wipe()
        self.stats.draw()
        self.stats.refresh()

    def update(self, force = False):

        if time.time() - self.last_au > self.au_delay or force:

            self.last_au = time.time()
            self.au_delay = (2 ** ((self.start_time - self.last_au)/ 120) * 3 / 4
                + 1 / 4)
            screen.log("update:: au_delay: {}".format(self.au_delay))
            
            if self.legal_move(keyboard.DOWN):
                self.stats.add_score(1)

            else:
                self.new_tetromino()
                lines = self.groupomino.chop(self.scene.get_board_size()[0])
                self.stats.add_score(
                    4 ** lines * self.scene.get_board_size()[0])


            if self.tetromino.collide(
                self.groupomino, self.scene.get_board_size()):
                self.end()


    def handle_key(self):

        key = screen.interface.get_key()

        if key in keyboard.game():

            if key == keyboard.BOTTOM:
                while self.legal_move(keyboard.DOWN):
                    self.stats.add_score(3)
                self.update(True)

            elif key == keyboard.BACK:
                self.end()

            else:
                self.legal_move(key)
                if key == keyboard.DOWN:
                    self.stats.add_score(2)

    def new_tetromino(self):
        
        if self.tetromino != None:
            self.groupomino.add(self.tetromino)
            self.stats.count_tetromino(self.tetromino)

        self.tetromino = self.n_tetromino
        self.n_tetromino = tetromino.get_random()

        self.tetromino.set_pos(((self.scene.get_board_size()[0]
            - self.tetromino.get_width()) // 2, 0))

        while self.legal_move(keyboard.UP):
            pass

    def legal_move(self, key):

        new_t = copy.deepcopy(self.tetromino)
        new_t.apply_key(key)

        if not new_t.collide(self.groupomino, self.scene.get_board_size()):
            self.tetromino.apply_key(key)
            screen.log('legal_move:: {}'.format(key))
            return True

        return False


class Scene(screen.Window):

    def __init__(self, x, y, w, h):
        self.board_size = (w, h)
        w, h = 2 * w + 1, h + 2
        scr = curses.newwin(h, w, y, x)
        super().__init__(x, y, w, h, scr, "Game")

    def draw(self, mino):
        for c in mino.get_char_coverage():
            self.write(c[1], 2 * c[0], c[2])

    def get_board_size(self):
        return self.board_size


class Stats(screen.Window):

    def __init__(self, x, y, w, h):
        w, h = w + 2, h + 2
        scr = curses.newwin(h, w, y, x)
        super().__init__(x, y, w, h, scr, "Stats")

        self.score = 0
        self.start_time = time.time()
        self.tetro_stats = {T.char: 0 for T in tetromino.TETROMINOS}

    def count_tetromino(self, t):
        self.tetro_stats[t.get_char()] += 1

    def get_score(self):
        return self.score

    def get_duration_str(self):
        duration = time.time() - self.start_time
        s = int(duration % 60)
        m = int(duration // 60)
        return "{:02d}:{:02d}".format(m, s)

    def add_score(self, n):
        self.score += n

    def draw(self):

        self.write(1, 1, "Time: {}".format(self.get_duration_str()))

        self.write(3, 1, "Score: {}".format(self.score))

        i = 0
        for t, s in self.tetro_stats.items():
            self.write(5 + 2 * i, 1, "{}: {}".format(t, s))
            i += 1

