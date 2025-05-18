from . import itemClass
from . import expenseApp as expApp

from data import timeVals as time
from data import vals as vals

def printAmountByCat() -> None:
    print("Monthly expenses by category:")
    for key, amount in vals.amountByCat.items():
        percentage = (amount / vals.totalBudget) * 100
        if key.strip().lower() == "grocery":
            print(f"    {key}:   \t${amount:.2f}    \t{percentage:.2f}% \t -want-> 20%")
        else:
            print(f"    {key}:   \t${amount:.2f}    \t{percentage:.2f}%")


def printRemainingBudget() -> None:
    print(f"\n${vals.totalBudget - vals.totalExp:.2f}    \tof total budget remaining   \t[${vals.totalBudget:.2f}]")
    print(f"${vals.gnrlBudget - vals.gnrlExp:.2f}    \tof general budget remaining \t[${vals.gnrlBudget:.2f}]")
    print(f"${vals.grocBudget - vals.grocExp:.2f}    \tof grocery budget remaining \t[${vals.grocBudget:.2f}]")


def print_daily_expenses(daily_expenses: list[itemClass.Item]) -> None:
    """ Displays a day-by-day summary of expenses """

    print("Date \t\t\tCategory \tAmount \t\tCard Type \tName\n")
    for i in range(len(daily_expenses)):
        for exp in daily_expenses[i]:
            print(exp)


def print_monthly_exp_summary(expenses: list[itemClass.Item], months_index: int, year: int, reached_current: bool) -> None:
    """ Displays a summary of the given month to the console """

    if len(expenses) <= 0:
        return

    amount_by_cat = expApp.get_amount_by_cat(expenses)
    daily_expenses = expApp.get_daily_exp(expenses)
    expApp.sum_exp(expenses)

    if reached_current:
        print(f"Summary for {time.months[months_index]}, {year} (current month)")
        print("-"*60)
    else:
        print(f"Summary for {time.months[months_index]}, {year}")
        print("-"*60)

    if len(expenses) > 0:
        print_daily_expenses(daily_expenses)
        print("\n")
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show for this month.")

    if total_exp < total_budget:
        total_diff = f"+{total_budget - total_exp:.2f}"
    elif total_exp > total_budget:
        total_diff = f"{total_budget - total_exp:.2f}"
    else:
        total_diff = "0"

    if gnrl_exp < gnrl_budget:
        gnrl_diff = f"+{gnrl_budget - gnrl_exp:.2f}"
    elif gnrl_exp > gnrl_budget:
        gnrl_diff = f"{gnrl_budget - gnrl_exp:.2f}"
    else:
        gnrl_diff = "0"

    if grcry_exp < grcry_budget:
        grcy_diff = f"+{grcry_budget - grcry_exp:.2f}"
    elif grcry_exp > grcry_budget:
        grcy_diff = f"{grcry_budget - grcry_exp:.2f}"
    else:
        grcy_diff = "0"


    print(f"\n\n${total_exp:.2f}  \tof ${total_budget:.2f} total   budget in {time.months[months_index]}, {year} \t[{total_diff}]")
    print(f"${gnrl_exp:.2f}  \tof ${gnrl_budget:.2f} general budget in {time.months[months_index]}, {year} \t[{gnrl_diff}]")
    print(f"${grcry_exp:.2f}  \tof ${grcry_budget:.2f} grocery budget in {time.months[months_index]}, {year} \t[{grcy_diff}]")

    if reached_current:
        print("\n")
    else:
        print("\n\n\n\n\n")
