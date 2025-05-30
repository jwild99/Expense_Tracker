import utils.infrastructure as inf
import utils.setup as setup
import utils.userAction as usrActns
from utils import budgets as budget

import src.views as views

import data.exceptions as exceptions

def main() -> None:
    setup.init()
    cliLoop()

def cliLoop() -> None:
    while True:
        try:
            inf.flushTerminal()
            budget.getBudgets()
            views.displayMenu()

            action = usrActns.getAction()
            if usrActns.isValid(action):
                usrActns.execute(action)

        except exceptions.BreakLoop:
            pass
