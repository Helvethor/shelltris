#!/usr/bin/python3 


import sys
import menu, screen


def main():

    exception = None

    try:
        screen.init()
        menu.start()

    except Exception as e:
        print(e)
        exception = e

    finally:
        screen.end()

    if exception:
        raise exception


if __name__ == '__main__':
    main()
