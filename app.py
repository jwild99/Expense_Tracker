import utils.infrastructure as inf
import utils.setup as setup
import utils.user_action as usrActns

import src.views as views

import data.exceptions as exceptions

def main() -> None:
    setup.init()
    cliLoop()

def cliLoop() -> None:
    while True:
        try:
            inf.flushTerminal()
            views.displayMenu()

            action = usrActns.getAction()
            if usrActns.isValid(action):
                usrActns.execute(action)

        except exceptions.BreakLoop:
            pass
