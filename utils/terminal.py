import sys
import os
import platform

def flush_terminal() -> None:
    """ Flushes print buffers and clears the terminal """

    print("\n" * 500)
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    sys.stdout.flush()

def close() -> None:
    """ Closes the app """

    flush_terminal()
    exit()

def spacing(lines) -> None:
    """ Prints spacing the given number of times """

    print("\n" * (lines - 1))

def lines(num) -> None:
        """ Prints a '-' character the given number of times """

        print("-"*num)
