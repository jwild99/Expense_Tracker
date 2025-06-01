import sys as Sys
import os as OS
import platform as Platform
import subprocess as Subprocess

from data import exceptions as Exceptions

def flushTerminal() -> None:
    """ Flushes print buffers and clears the terminal """
    print("\n" * 500)
    if Platform.system() == 'Windows':
        OS.system('cls')
    else:
        OS.system('clear')
    Sys.stdout.flush()

def close() -> None:
    """ Closes the app """
    flushTerminal()
    exit()

def spacing(n) -> None:
    """ Prints spacing the given number of times """
    print("\n" * (n - 1))

def lines(n) -> None:
        """ Prints a '-' character the given number of times """
        print("-"*n)

def fileExists(file_path: str) -> bool:
    return OS.path.exists(file_path)

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def goBack() -> None:
    raise Exceptions.BreakLoop

def ensurePip():
    """Ensure pip is installed."""
    try:
        import pip
    except ImportError:
        print("pip not found. Attempting to install it...")
        Subprocess.check_call([Sys.executable, "-m", "ensurepip", "--upgrade"])

def installRequirements():
    """Install dependencies from requirements.txt"""
    if not OS.path.isfile("requirements.txt"):
        print("requirements.txt not found.")
        return
    try:
        Subprocess.check_call([Sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except Subprocess.CalledProcessError:
        print("Failed to install requirements.")
        Sys.exit(1)
