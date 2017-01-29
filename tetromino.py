import random, copy
import screen, game, keyboard


class Tetromino:

    count = 0

    def __init__(self, block_map, char = '#', pos = [0, 0]):

        self.char = char
        self.block_map = block_map
        self.pos = list(pos)

        self.id = chr(__class__.count + ord('A'))
        __class__.count += 1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str("T({}, {})".format(self.id, self.get_coverage()))

    def get_id(self):
        return self.id

    def get_char(self):
        return self.char

    def get_blockmap(self):
        return self.block_map

    def get_coverage(self):
        return {(b[0] + self.get_x(), b[1] + self.get_y())
            for b in self.block_map}

    def get_char_coverage(self):
        return {(b[0] + self.get_x(), b[1] + self.get_y(), self.get_char())
            for b in self.block_map}

    def get_span(self, dim):

        M = max(self.get_coverage(), key = lambda c: c[dim])[dim]
        m = min(self.get_coverage(), key = lambda c: c[dim])[dim]

        return M - m + 1

    def get_width(self):
        return self.get_span(0)

    def get_height(self):
        return self.get_span(1)

    def get_size(self):
        return max(self.get_width(), self.get_height())

    def get_pos(self):
        return pos

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def set_pos(self, pos):
        self.pos = list(pos)

    def move_right(self):
        self.pos[0] += 1

    def move_left(self):
        self.pos[0] -= 1

    def move_down(self):
        self.pos[1] += 1

    def move_up(self):
        self.pos[1] -= 1

    def rotate_left(self):
        c = self.get_size() - 1
        self.block_map = {(p[1], c - p[0]) for p in self.block_map}

    def rotate_right(self):
        c = self.get_size() - 1
        self.block_map = {(c -p[1], p[0]) for p in self.block_map}

    def apply_key(self, key):

        if key == keyboard.LEFT:
            self.move_left()

        elif key == keyboard.RIGHT:
            self.move_right()

        elif key == keyboard.DOWN:
            self.move_down()

        elif key == keyboard.UP:
            self.move_up()

        elif key == keyboard.ROT_L:
            self.rotate_left()

        elif key == keyboard.ROT_R:
            self.rotate_right()

        else:
            return False

        return True

    def collide(self, groupomino, scene_size):
        
        s_coverage = self.get_coverage()

        for c in s_coverage:
            if (c[0] < 0 or c[0] >= scene_size[0]
                or c[1] < 0 or c[1] >= scene_size[1]):
                return True

        g_coverage = groupomino.get_coverage()  
        if len(s_coverage.intersection(g_coverage)) > 0:
            return True

        return False


class Groupomino:

    def __init__(self):
        self.char_coverage = set()

    def get_coverage(self):
        return {(b[0], b[1]) for b in self.char_coverage}

    def get_char_coverage(self):
        return self.char_coverage

    def add(self, tetromino):
        self.char_coverage = self.char_coverage.union(
            tetromino.get_char_coverage())

    def chop(self, scene_width):

        lines = self.find_choppable(scene_width)

        for line in lines:
            self.char_coverage = {b if b[1] > line else (b[0], b[1] + 1, b[2])
                for b in self.char_coverage 
                if b[1] != line}

        return len(lines)

    def find_choppable(self, scene_width):

        mH = min(self.get_coverage(), key = lambda c: c[1])[1]
        MH = max(self.get_coverage(), key = lambda c: c[1])[1]

        lines = set()

        for line in range(mH, MH + 1):
            coverage = {c[0] for c in self.get_coverage() if c[1] == line}

            if len(coverage) == scene_width:
                lines.add(line)
                screen.log("find_choppable:: line: {}".format(line))

        return lines

class I(Tetromino):

    char = 'I'

    def __init__(self):
        block_map = {(0, 1), (1, 1), (2, 1), (3, 1)}
        super().__init__(block_map, __class__.char)

class T(Tetromino):

    char = 'T'

    def __init__(self):
        block_map = {(0, 1), (1, 1), (1, 0), (2, 1)}
        super().__init__(block_map, __class__.char)

class J(Tetromino):

    char = 'J'

    def __init__(self):
        block_map = {(0, 1), (1, 1), (2, 1), (2, 2)}
        super().__init__(block_map, __class__.char)

class L(Tetromino):

    char = 'L'

    def __init__(self):
        block_map = {(0, 2), (0, 1), (1, 1), (2, 1)}
        super().__init__(block_map, __class__.char)

class S(Tetromino):

    char = 'S'

    def __init__(self):
        block_map = {(0, 2), (1, 2), (1, 1), (2, 1)}
        super().__init__(block_map, __class__.char)

class Z(Tetromino):

    char = 'Z'

    def __init__(self):
        block_map = {(0, 1), (1, 1), (1, 2), (2, 2)}
        super().__init__(block_map, __class__.char)

class O(Tetromino):

    char = 'O'

    def __init__(self):
        block_map = {(0, 0), (0, 1), (1, 0), (1, 1)}
        super().__init__(block_map, __class__.char)


def get_random():
    return random.sample(TETROMINOS, 1)[0]()


TETROMINOS = (I, J, L, O, T, S, Z)
