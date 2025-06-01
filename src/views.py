from . import printers as printers
from . import expenseApp as expApp

from utils import systemUtils as inf
from utils import budgetManager as Budgets

from data import timeVals as time
from data import vals as vals

def displayVerboseMenu() -> None:
    inf.flushTerminal()

    expApp.getCurExp()
    expApp.getAmountByCat()
    expApp.getDailyExp()
    expApp.sumExp()

    if len(vals.expenses) > 0:
        printers.printDailyExp()
        print("\n\n")
        printers.printAmountByCat()
    else:
        print("No expenses to show at this time.")

    printers.printRemainingBudget()

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

def displayAlltimeSummary() -> None:
    expenses = expApp.getAllExp()
    reachedCurrent = False
    monthsIndex = 0
    curMonthIndex = time.month - 1
    inf.flushTerminal()
    if len(expenses) > 0:
        for yearKey in sorted(expenses.keys()):
            monthsIndex = 0
            for monthList in expenses[yearKey]:
                if int(yearKey) == time.year and monthsIndex == curMonthIndex:
                    reachedCurrent = True
                    break
                Budgets.getMonthlyBudgets(month=monthsIndex, year=int(yearKey))
                printers.printMonthlyExpSummary(expenses=monthList, months_index=monthsIndex, year=int(yearKey), reached_current=reachedCurrent)
                monthsIndex += 1

            if reachedCurrent:
                printers.printMonthlyExpSummary(expenses=monthList, months_index=monthsIndex, year=int(yearKey), reached_current=reachedCurrent)
                expApp.sumExp()
                break
    else:
        print("No expenses to show at this time.")

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

    inf.flushTerminal()

def displayMenu() -> None:
    inf.flushTerminal()
    expApp.getCurExp()
    expApp.getAmountByCat()
    expApp.sumExp()
    printers.printTitle()
    print("\n")
    if len(vals.expenses) > 0:
        printers.printAmountByCat()
    else:
        print("No expenses to show at this time.")
    print("\n")
    printers.printRemainingBudget()
    print("\n")
    printers.printActionPrompt()
