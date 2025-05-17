from . import user_input as inp

from src.item_class import Item

from utils import infrastructure as inf

from data import expense_categories as expCats
from data import time_vals as time
from data import vals as vals
from data import file_paths as paths

import os


most_recent_itm_path = ""

menu_message = ""


def get_new_exp() -> type[Item]:
    inf.flush_terminal()
    exp_name = inp.get_user_name()
    exp_amount = inp.get_user_amount()
    cat_num = inp.get_user_category()
    exp_month = inp.get_user_month()
    exp_day = inp.get_user_day(month=exp_month)
    exp_year = inp.get_user_year()
    exp_cd = inp.get_user_cd()

    new_exp = Item(name=exp_name, category=expCats.categories[cat_num], amount=exp_amount, month=exp_month,
                      day=exp_day, year=exp_year, cd=exp_cd)
    inf.flush_terminal()
    return new_exp

def save_exp(exp:Item) -> None:
    global most_recent_itm_path, menu_message

    exp_file_path = f"records/records{exp.year}.csv"
    most_recent_itm_path = f"records/records{exp.year}.csv"

    with open(exp_file_path, 'a') as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day},{exp.year},{exp.cd}\n")
        file.close()

    menu_message = f"Saved expense: [{exp.get_exp()}] to {exp_file_path}"

def get_all_exp() -> dict:
    exp_file_dir = f"records/"
    expenses_dict = {}

    for filepath in os.listdir(exp_file_dir):
        with open(f"records/{filepath}", 'r') as file:
            lines = file.readlines()

            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd = line.strip().split(',')
                expense =Item(name=exp_name, category=exp_cat, amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd)
                if expense.year in expenses_dict:
                        expenses_dict[expense.year][int(exp_month) - 1].append(expense)
                else:
                        expenses_dict[expense.year] = [[] for _ in range(12)]
                        expenses_dict[expense.year][int(exp_month) - 1].append(expense)

            file.close()

    return expenses_dict

def getCurExp() -> None:
    if not inf.fileExists(paths.curExpFile):
        return

    with open(paths.curExpFile, 'r') as expFile:
        lines = expFile.readlines()

        for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd = line.strip().split(',')

                vals.expenses.append(Item(name=exp_name, category=exp_cat, amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd))

        expFile.close()


def getAmountByCat() -> None:
    for expense in vals.expenses:
        key = expense.category
        if key in vals.amountByCat:
            vals.amountByCat[key] += expense.amount
        else:
            vals.amountByCat[key] = expense.amount

def sumExp() -> None:
    vals.totalExp, vals.gnrlExp, vals.grcryExp = 0, 0, 0

    for expense in vals.expenses:
        vals.totalExp += expense.amount

        if expense.category.lower() == "grocery":
            grcryExp += expense.amount
        else:
            gnrlExp += expense.amount

def get_daily_exp(expenses: list[Item]) -> list[str]:
    daily_expenses = [[] for _ in range(31)]

    for expense in expenses:
        daily_expenses[expense.day - 1].append(expense.get_expf())

    return daily_expenses


def undo_last_exp() -> None:
    global menu_message

    if len(most_recent_itm_path) <= 0:
        menu_message = "~~Nothing to undo!~~"
        return

    inf.flush_terminal()
    message = "~~WARNING~~\nAre you sure you wish to undo the most recent CSV write?\nThis cannot be undone! [y/n]: "
    con = None
    while True:
        inp = input(message).strip().lower()
        if inp == 'y':
            con = True
            break
        elif inp == 'n':
            con = False
            break

    if con:
        with open(most_recent_itm_path, 'r') as file:
            lines = file.readlines()
            file.close()

        if lines:
            last_line = lines[len(lines) - 1]
            lines = lines[:-1]

            itm_name, itm_cat, itm_amount, itm_month, itm_day, itm_year, itm_cd = last_line.strip().split(',')
            item =item(name=itm_name, category=itm_cat, amount=float(itm_amount), month=int(itm_month), day=int(itm_day), year=int(itm_year), cd=itm_cd)

            with open(most_recent_itm_path, 'w') as file:
                file.writelines(lines)
                file.close()

        menu_message = f"Removed {item.get_dep()} from {most_recent_itm_path}"
