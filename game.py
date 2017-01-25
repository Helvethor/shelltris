import time, copy
import screen, tetromino


KEY_MLEFT   = 'a'
KEY_MRIGHT  = 'd'
KEY_MDOWN   = 's'
KEY_RLEFT   = 'q'
KEY_RRIGHT  = 'e'
KEY_MBOTTOM = ' '
GAME_KEYS   = set([KEY_MLEFT, KEY_MRIGHT, KEY_MDOWN, KEY_RLEFT, KEY_RRIGHT])


def start():

    scene = screen.Scene(0, 0, 10, 20)
    play(scene)
    game_over()


def play(scene):

    au_delay = 1
    last_au = time.time()

    cur_tetromino = tetromino.get_random()
    tetrominos = set()

    while True:

        key = screen.interface.get_key()

        if key in GAME_KEYS:
            legal_move(key, cur_tetromino, tetrominos)
        elif key == KEY_MBOTTOM:
            while legal_move(KEY_MDOWN, cur_tetromino, tetrominos):
                pass

        if time.time() - last_au > au_delay:

            last_au = time.time()
            
            if not legal_move(KEY_MDOWN, cur_tetromino, tetrominos):
                tetrominos.add(cur_tetromino)
                cur_tetromino = tetromino.get_random()

            if cur_tetromino.collide(tetrominos):
                break

        scene.clear()
        [scene.draw_tetromino(t) for t in tetrominos]
        scene.draw_tetromino(cur_tetromino)
        scene.refresh()


def game_over():

    screen.log("game_over:: Ha!")    
    while not screen.interface.get_key():
        pass



def legal_move(key, t, tetrominos):

    new_t = copy.deepcopy(t)
    new_t.apply_key(key)

    if not new_t.collide(tetrominos):
        t.apply_key(key)
        screen.log('legal_move:: {}'.format(key))
        return True

    return False
