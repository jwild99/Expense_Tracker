import utils.systemUtils as sUtils
import utils.setupManager as Setup
import utils.userAction as UsrActs
from utils import budgetManager as BudgetManager
import src.views as ViewManager
import data.exceptions as Exceptions

def main() -> None:
    Setup.init()
    loop()

def loop() -> None:
    while True:
        try:
            sUtils.flushTerminal()
            BudgetManager.getCurBudgets()
            ViewManager.displayMenu()
            action = UsrActs.getAction()
            if UsrActs.isValid(action):
                UsrActs.execute(action)
        except Exceptions.BreakLoop:
            pass
