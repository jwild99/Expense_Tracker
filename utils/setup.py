from . import budgets as budget
from . import infrastructure as inf

from data import timeVals as time
from data import filePaths as paths

import datetime


def init() -> None:
    time.month = datetime.datetime.now().month
    time.day = datetime.datetime.now().day
    time.year = datetime.datetime.now().year

    if not inf.fileExists(paths.curBudgetFile):
        budget.initBudgets()

    with open(f"records/expenses/expenses-{time.year}.csv", 'a') as file:
        pass

    paths.curExpFile = f"records/expenses/expenses-{time.year}.csv"
    paths.curBudgetRecord = f"records/budgets/budgets-{time.month}-{time.year}.json"

    if not inf.fileExists(paths.curBudgetRecord):
        budget.initBudgetsRecord()









