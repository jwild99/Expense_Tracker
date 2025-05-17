from . import terminal as tUtils
from . import help as help
from data import messages as messages
from data import exceptions as exceptions

from src import expense_tracker as expApp
from src import views


def get_action() -> str:
    """ Gets user input for an action and then dispatches correct code for that action """

    global menu_message

    return input(f"\n\nx: quit | h: help\nWhat would you like to do:\n").strip().lower()

def is_valid(action: str) -> bool:
    if action not in action_dict.keys():
        messages.DEBUG_MESSAGE = f"~~Not a valid action~~\n{action_dict.keys()}"
        return False
    else:
        messages.DEBUG_MESSAGE = ""
        return True

def execute(action: str) -> None:
    action_dict[action]()

def go_back() -> None:
    raise exceptions.BreakLoop


action_dict = {
    "q": tUtils.close,
    "x": go_back,
    "h": help.help_message,
    "e": expApp.get_new_exp,
    "u": expApp.undo_last_exp,
    "s": views.display_verbose_menu,
    "s -a": views.display_alltime_summary
}

