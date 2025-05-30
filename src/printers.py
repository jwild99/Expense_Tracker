from . import itemClass
from . import expenseApp as expApp

from data import timeVals as time
from data import vals as vals

def printAmountByCat() -> None:
    print("Monthly expenses by category:")
    print(f"    Category:        \tAmount    \tPercentage Total    \tPercentage Local")
    for key, amount in vals.amountByCat.items():
        percentage = (amount / vals.budgets["total"]) * 100
        localPercentage = (amount / vals.budgets[key]) * 100
        print(f"    {key}:        \t${amount:.2f}    \t{percentage:.2f}%    \t\t{localPercentage:.2f}%")


def printRemainingBudget() -> None:
    print(f"\n${vals.budgets["total"] - vals.sumExp["total"]:.2f}    \tof total budget remaining          \t[${vals.budgets["total"]:.2f}]")

    for key in vals.budgets.keys():
        if str.lower(key) == "total":
            continue
        print(f"${vals.budgets[key] - vals.sumExp[key]:.2f}    \tof {key} budget remaining          \t[${vals.budgets[key]:.2f}]")


def printDailyExp() -> None:
    """ Displays a day-by-day summary of expenses """

    print("Date \t\t\tCategory \tAmount \t\tCard Type \tName\n")
    for i in range(len(vals.dailyExp)):
        for exp in vals.dailyExp[i]:
            print(exp)


def printMonthlyExpSummary(expenses: list[itemClass.Item], months_index: int, year: int, reached_current: bool) -> None:
    """ Displays a summary of the given month to the console """

    if len(expenses) <= 0:
        return

    amountByCat = expApp.getAmountByCat()
    dailyExpenses = expApp.getDailyExp()
    expApp.sumExp()

    if reached_current:
        print(f"Summary for {time.months[months_index]}, {year} (current month)")
        print("-"*60)
    else:
        print(f"Summary for {time.months[months_index]}, {year}")
        print("-"*60)

    if len(expenses) > 0:
        printDailyExp()
        print("\n")
        printAmountByCat()
    else:
        print("No expenses to show for this month.")

    print("\n")
    for key in vals.budgets.keys():
        exp = vals.sumExp[key]
        budget = vals.budgets[key]

        diff = f"{budget - exp:.2f}"
        print(f"${exp:.2f}  \tof [${budget:.2f}] {key} \tbudget spent | {diff} remaing")

    if reached_current:
        print("\n")
    else:
        print("\n\n\n\n\n")
