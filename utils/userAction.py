from . import systemUtils as sUtils
from . import help as Help
from data import messages as Messages
from src import expenseApp as ExpApp
from src import views as Views
from utils import budgetManager as Budgets
from rich.prompt import Prompt

def getAction() -> str:
    actionInput = Prompt.ask(f"", default="")
    return actionInput.strip().lower()

def isValid(action: str) -> bool:
    if action not in action_dict.keys():
        Messages.debug = f"~~Not a valid action~~"
        return False
    else:
        Messages.debug = ""
        return True

def execute(action: str) -> None:
    action_dict[action]()

action_dict = {
    "q": sUtils.close,
    "x": sUtils.goBack,
    "h": Help.helpMessage,
    "ex": ExpApp.createNewExp,
    "u": ExpApp.undoLastExp,
    "sm": Views.displayVerboseMenu,
    "sm -a": Views.displayAlltimeSummary,
    "b": Budgets.editBudgets
}

