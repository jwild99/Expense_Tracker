import sys
import os
import platform

def flushTerminal() -> None:
    """ Flushes print buffers and clears the terminal """

    print("\n" * 500)
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    sys.stdout.flush()

def close() -> None:
    """ Closes the app """

    flushTerminal()
    exit()

def spacing(lines) -> None:
    """ Prints spacing the given number of times """

    print("\n" * (lines - 1))

def lines(num) -> None:
        """ Prints a '-' character the given number of times """

        print("-"*num)

def fileExists(file_path: str) -> bool:
    return os.path.exists(file_path)
