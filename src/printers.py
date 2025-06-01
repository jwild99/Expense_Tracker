from rich.text import Text

from . import itemClass
from . import expenseApp as expApp

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from data import messages as Messages

from data import timeVals as Time
from data import vals as Vals

def printAmountByCat() -> None:
    table = Table(title="Expenses by Category", border_style="bold bold dark_blue")
    table.add_column("Category", justify="right", style="cyan", no_wrap=True)
    table.add_column("Amount", justify="right", style="magenta")
    table.add_column("Percentage of Total", justify="right", style="green")
    table.add_column("Percentage of Budget", justify="right", style="green")

    for key, amount in Vals.amountByCat.items():
        percentage = (amount / Vals.budgets["total"]) * 100
        localPercentage = (amount / Vals.budgets[key]) * 100
        # print(f"    {key}:        \t${amount:.2f}    \t{percentage:.2f}%    \t\t{localPercentage:.2f}%")
        table.add_row(f"{key}", f"${round(amount, 2)}", f"{round(percentage, 2)}%", f"{round(localPercentage, 2)}%")

    console = Console()
    console.print(table)

def printRemainingBudget() -> None:
    table = Table(title="Budget Report", border_style="bold bold dark_blue")
    table.add_column("Budget", justify="right", style="cyan", no_wrap=True)
    table.add_column("Budget Total", justify="right", style="green")
    table.add_column("Amount Spent", justify="right", style="green")
    table.add_column("Difference", justify="right", style="green")
    table.add_column("Remaining Amount", justify="right", style="magenta")



    # print(f"\n${Vals.budgets["total"] - Vals.sumExp["total"]:.2f}    \tof total budget remaining          \t[${Vals.budgets["total"]:.2f}]")

    for key in Vals.budgets.keys():
        if str.lower(key) == "total":
            continue
        diff = round(Vals.budgets[key] - Vals.sumExp[key], 2)
        table.add_row(f"{key}", f"${round(Vals.budgets[key], 2)}", f"{round(Vals.sumExp[key])}", f"${diff}", f"${0 if diff < 0 else diff}")

    diff = round(Vals.budgets["total"] - Vals.sumExp["total"], 2)
    note = Panel.fit(
        f"[bold white] ${diff} of total budget remaining [${Vals.budgets["total"]}] | {round((diff / Vals.budgets["total"]) * 100, 2)}% spent",
        border_style="bold bold dark_blue",
    )

    console = Console()
    console.print(table)
    console.print(note)

def printDailyExp() -> None:
    """ Displays a day-by-day summary of expenses """

    print("Date \t\t\tCategory \tAmount \t\tCard Type \tName\n")
    for i in range(len(Vals.dailyExp)):
        for exp in Vals.dailyExp[i]:
            print(exp)


def printMonthlyExpSummary(expenses: list[itemClass.Item], months_index: int, year: int, reached_current: bool) -> None:
    """ Displays a summary of the given month to the console """

    if len(expenses) <= 0:
        return

    expApp.getAmountByCat()
    expApp.getDailyExp()
    expApp.sumExp()

    if reached_current:
        print(f"Summary for {Time.months[months_index]}, {year} (current month)")
        print("-"*60)
    else:
        print(f"Summary for {Time.months[months_index]}, {year}")
        print("-"*60)

    if len(expenses) > 0:
        printDailyExp()
        print("\n")
        printAmountByCat()
    else:
        print("No expenses to show for this month.")

    print("\n")
    for key in Vals.monthlyBudgets.keys():
        exp = Vals.sumExp[key]
        budget = Vals.monthlyBudgets[key]

        diff = f"{budget - exp:.2f}"
        print(f"${exp:.2f}  \tof [${budget:.2f}] {key} \tbudget spent | {diff} remaing")

    if reached_current:
        print("\n")
    else:
        print("\n\n\n\n\n")

def printTitle():
    console = Console()
    title = Panel.fit(f"[bold white] Expense Tracker: {Time.months[Time.month - 1]}, {Time.year}[/]", title="", subtitle="", border_style="bold dark_blue")
    console.print(title)

    text = Text(Messages.debug)
    text.stylize("bold red", 0, 45)
    console.print(text)

def printActionPrompt():
    note = Panel.fit(
        "[bold white]    q: quit | h: help\nWhat would you like to do?",
        border_style="bold bold dark_blue"
    )
    console = Console()
    console.print(note)
