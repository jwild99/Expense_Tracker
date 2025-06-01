from . import budgetManager as Budget
from . import systemUtils as sUtils
from data import timeVals as Time
from data import filePaths as Paths
import datetime as DateTime

def init() -> None:
    sUtils.ensurePip()
    sUtils.installRequirements()

    Time.month = DateTime.datetime.now().month
    Time.day = DateTime.datetime.now().day
    Time.year = DateTime.datetime.now().year

    if not sUtils.fileExists(Paths.curBudgetFile):
        Budget.initBudgets()

    with open(f"records/expenses/expenses-{Time.year}.csv", 'a') as file:
        pass
    file.close()

    Paths.curExpFile = f"records/expenses/expenses-{Time.year}.csv"
    Paths.curBudgetRecord = f"records/budgets/budgets-{Time.month}-{Time.year}.json"

    if not sUtils.fileExists(Paths.curBudgetRecord):
        Budget.initBudgetsRecord()









