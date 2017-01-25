import random, copy
from itertools import chain

import screen, game


class Tetromino:

    count = 0

    def __init__(self):
        self.bitmap = []
        self.id = chr(Tetromino.count + ord('A'))
        self.char = '#'
        Tetromino.count += 1
        self.pos = [0, 0]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str("T({}, {})".format(self.id, self.get_coverage()))

    def get_id(self):
        return self.id

    def get_char(self):
        return self.id

    def get_width(self):
        return len(self.bitmap[0])

    def get_height(self):
        return len(self.bitmap)

    def get_pos(self):
        return pos

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def set_pos(self, pos):
        self.pos = pos

    def apply_key(self, key):

        if key == game.KEY_MLEFT:
            self.move_left()

        elif key == game.KEY_MRIGHT:
            self.move_right()

        elif key == game.KEY_MDOWN:
            self.move_down()

        elif key == game.KEY_RLEFT:
            self.rotate_left()

        elif key == game.KEY_RRIGHT:
            self.rotate_right()

        else:
            raise Exception("Unhandled key: {}".format(key))

    def move_right(self):
        self.pos[0] += 1

    def move_left(self):
        self.pos[0] -= 1

    def move_down(self):
        self.pos[1] += 1

    def rotate_left(self):
        rangei = list(range(self.get_height()))
        rangej = list(reversed(range(self.get_width())))
        self.permute(rangei, rangej)

    def rotate_right(self):
        rangei = list(reversed(range(self.get_height())))
        rangej = list(range(self.get_width()))
        self.permute(rangei, rangej)

    def permute(self, rangei, rangej):

        self.bitmap = [[self.bitmap[i][j]
            for i in rangei]
            for j in rangej]

    def get_bitmap(self):
        return self.bitmap

    def get_charmap(self):
        return [[self.char if bit else ' '
            for bit in chain.from_iterable(zip(bitline, [0] * len(bitline)))]
            for bitline in self.bitmap]

    def get_coverage(self):
        return {(i + self.get_x(), j + self.get_y())
            for i in range(len(self.bitmap))
            for j in range(len(self.bitmap[0]))
            if self.bitmap[i][j]}

    def collide(self, others):
        
        screen.log("collide:: s: {}, o: {}".format(self,
            [o.get_id() for o in others]))
        s_coverage = self.get_coverage()

        for c in s_coverage:
            if (c[0] < 0 or c[0] >= 10
                or c[1] < 0 or c[1] >= 20):

                screen.log("collide:: border")
                return True

        for o in others:
            o_coverage = o.get_coverage()

            if len(s_coverage.intersection(o_coverage)) > 0:

                screen.log("collide:: collision: {}".format(o))
                return True

        return False


class I(Tetromino):

    def __init__(self):
        super().__init__()
        self.bitmap = [[True,  True,  True,  True]]
        self.char = 'I'

class J(Tetromino):

    def __init__(self):
        super().__init__()
        self.bitmap = [ [True,  True,  True],
                        [False, False, True]]
        self.char = 'J'

class L(Tetromino):

    def __init__(self):
        super().__init__()
        self.bitmap = [ [True,  True,  True],
                        [True,  False, False]]
        self.char = 'L'

class O(Tetromino):

    def __init__(self):
        super().__init__()
        self.bitmap = [ [True,  True] ,
                        [True,  True]]
        self.char = 'O'

class T(Tetromino):

    def __init__(self):
        super().__init__()
        self.bitmap = [ [True,  True,  True],
                        [False, True,  False]]
        self.char = 'T'

class S(Tetromino):

    def __init__(self):
        super().__init__()
        self.bitmap = [ [False, True,  True],
                        [True,  True,  False]]
        self.char = 'S'

class Z(Tetromino):
    def __init__(self):
        super().__init__()
        self.bitmap = [ [True,  True,  False],
                        [False, True,  True]]
        self.char = 'Z'


def get_random():
    return random.sample(TETROMINOS, 1)[0]()


TETROMINOS = (I, J, L, O, T, S, Z)
