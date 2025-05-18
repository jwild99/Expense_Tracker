from . import infrastructure as Inf
from . import user_action as UsrActns

HELP_MESSAGE = """
x    | go back
q    | quit
h    | go to help page
e    | create a new expense
s    | verbose summary of current month's expenses
s -a | verbose summary of all-time expenses
"""

def helpMessage() -> None:
    Inf.flushTerminal()
    print(HELP_MESSAGE)
    while True:
        usr_input = input().strip().lower()

        if usr_input == "x" or usr_input == "q":
            UsrActns.action_dict[usr_input]()


