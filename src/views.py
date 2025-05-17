from utils import terminal as tUtils
from . import prints as prints
from . import expense_tracker as expApp

from data import time_const as time

def display_verbose_menu() -> None:
    tUtils.flush_terminal()

    expenses = expApp.get_cur_exp()
    amount_by_cat = expApp.get_amount_by_cat(expenses)
    daily_expenses = expApp.get_daily_exp(expenses)
    expApp.sum_exp(expenses)

    if len(expenses) > 0:
        prints.print_daily_expenses(daily_expenses)
        print("\n\n")
        prints.print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show at this time.")

    prints.print_remaining_budget()

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

def display_alltime_summary() -> None:
    expenses = expApp.get_all_exp()
    reached_current = False
    months_index = 0
    cur_month_index = time.cur_month - 1

    tUtils.flush_terminal()

    if len(expenses) > 0:
        for year_key in sorted(expenses.keys()):
            months_index = 0
            for month_list in expenses[year_key]:
                if (int(year_key) == time.cur_year and months_index == cur_month_index):
                    reached_current = True
                    break

                prints.print_monthly_exp_summary(expenses=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                months_index += 1

            if reached_current:
                prints.print_monthly_exp_summary(expenses=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                expApp.sum_exp(month_list)
                break
    else:
        print("No expenses to show at this time.")

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

    tUtils.flush_terminal()

def display_menu() -> None:
    tUtils.flush_terminal()
    expenses = expApp.get_cur_exp()
    amount_by_cat = expApp.get_amount_by_cat(expenses)
    expApp.sum_exp(expenses)

    print(f"Expense Tracker [{time.months[time.cur_month - 1]}, {time.cur_year}]")

    tUtils.lines(60)
    tUtils.spacing(1)

    if len(expenses) > 0:
        prints.print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show at this time.")

    prints.print_remaining_budget()
