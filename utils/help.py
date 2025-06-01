from . import systemUtils as Inf

HELP_MESSAGE = """
x       | go back
q       | quit
h       | go to help page
ex      | create a new expense
u       | undo last expense
sm      | verbose summary of current month's expenses
sm -a   | verbose summary of all-time expenses
b       | edit budgets
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



