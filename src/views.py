from . import printers as printers
from . import expenseApp as expApp

from utils import infrastructure as inf

from data import messages as messages
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
    expenses = expApp.get_all_exp()
    reached_current = False
    months_index = 0
    cur_month_index = time.cur_month - 1

    inf.flush_terminal()

    if len(expenses) > 0:
        for year_key in sorted(expenses.keys()):
            months_index = 0
            for month_list in expenses[year_key]:
                if (int(year_key) == time.year and months_index == cur_month_index):
                    reached_current = True
                    break

                printers.print_monthly_exp_summary(expenses=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                months_index += 1

            if reached_current:
                printers.print_monthly_exp_summary(expenses=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                expApp.sum_exp(month_list)
                break
    else:
        print("No expenses to show at this time.")

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

    inf.flush_terminal()

def displayMenu() -> None:
    inf.flushTerminal()
    print(messages.debug)

    expApp.getCurExp()
    expApp.getAmountByCat()
    expApp.sumExp()

    print(f"Expense Tracker [{time.months[time.month - 1]}, {time.year}]")

    inf.lines(60)
    inf.spacing(1)

    if len(vals.expenses) > 0:
        printers.printAmountByCat()
    else:
        print("No expenses to show at this time.")

    printers.printRemainingBudget()
