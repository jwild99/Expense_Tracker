from . import terminal_utils as tUtils
from . import help as help
from const import messages as messages
from const import exceptions as exceptions

from expense_tracker import expense_tracker as expApp


def get_action() -> str:
    """ Gets user input for an action and then dispatches correct code for that action """

    global menu_message

    return input(f"\n\nx: quit | h: help\nWhat would you like to do:\n").strip().lower()

def validate_action(action: str) -> None:
    if action not in action_dict.keys():
        messages.DEBUG_MESSAGE = f"~~Not a valid action~~\n{action_dict.keys()}"
    else:
        messages.DEBUG_MESSAGE = ""

def execute_action(action: str) -> None:
    action_dict[action]()

def go_back() -> None:
    raise exceptions.BreakLoop


action_dict = {
    "q": tUtils.close,
    "x": go_back,
    "help": help.help_message,
    "exp": expApp.main
}

