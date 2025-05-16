from . import terminal_utils as tUtils
from . import user_action_utils as usrActUtils

HELP_MESSAGE = """
x - go back
q - quit
help - go to help page
exp - go to expense tracker
"""

def help_message() -> None:
    tUtils.flush_terminal()
    print(HELP_MESSAGE)
    while True:
        usr_input = input().strip().lower()

        if usr_input == "x" or usr_input == "q":
            usrActUtils.action_dict[usr_input]()


