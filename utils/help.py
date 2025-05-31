from . import infrastructure as Inf

HELP_MESSAGE = """
x    | go back
q    | quit
h    | go to help page
e    | create a new expense
s    | verbose summary of current month's expenses
s -a | verbose summary of all-time expenses
b    | edit budgets
"""

def helpMessage() -> None:
    Inf.flushTerminal()
    print(HELP_MESSAGE)
    while True:
        usr_input = input().strip().lower()

        if usr_input == "x":
            Inf.goBack()
        elif usr_input == "q":
            Inf.close()



