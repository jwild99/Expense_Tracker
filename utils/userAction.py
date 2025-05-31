from . import infrastructure as inf
from . import help as help

from data import messages as messages
from data import exceptions as exceptions

from src import expenseApp as expApp
from src import views

from utils import budgets as budgets


def getAction() -> str:
    return input(f"\n\nq: quit | h: help\nWhat would you like to do:\n").strip().lower()

def isValid(action: str) -> bool:
    if action not in action_dict.keys():
        messages.debug = f"~~Not a valid action~~"
        return False
    else:
        messages.debug = ""
        return True

def execute(action: str) -> None:
    action_dict[action]()


action_dict = {
    "q": inf.close,
    "x": inf.goBack,
    "h": help.helpMessage,
    "e": expApp.createNewExp,
    "u": expApp.undoLastExp,
    "s": views.displayVerboseMenu,
    "s -a": views.displayAlltimeSummary,
    "b": budgets.editBudgets
}

