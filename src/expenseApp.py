from . import expInput as expInp

from src.itemClass import Item

from utils import systemUtils as inf

from data import timeVals as time
from data import vals as vals
from data import filePaths as paths
from data import messages as messages

import os


def createNewExp():
    inf.flushTerminal()
    expName = expInp.getName()
    expAmount = expInp.getAmount()
    catNum = expInp.getCategory() + 1
    expMonth = expInp.getMonth()
    expDay = expInp.getDay(month=expMonth)
    expYear = expInp.getYear()
    expCd = expInp.getCd()
    newExp = Item(name=expName, category=list(vals.budgets.keys())[catNum], amount=expAmount, month=expMonth,
                      day=expDay, year=expYear, cd=expCd)
    inf.flushTerminal()
    saveExp(newExp)

def saveExp(exp:Item) -> None:
    expFilePath = f"records\\expenses\\expenses-{exp.year}.csv"
    paths.curExpFile = expFilePath

    with open(expFilePath, 'a') as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day},{exp.year},{exp.cd}\n")
        file.close()

    messages.menu = f"Saved expense: [{exp.get_exp()}] to {expFilePath}"

def getAllExp() -> dict:
    exp_file_dir = f"records/expenses"
    expenses_dict = {}

    for filepath in os.listdir(exp_file_dir):
        with open(f"records/expenses/{filepath}", 'r') as file:
            lines = file.readlines()

            for line in lines:
                print(line)
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
        vals.expenses.clear()
        for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd = line.strip().split(',')

                vals.expenses.append(Item(name=exp_name, category=exp_cat, amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd))

        expFile.close()


def getAmountByCat() -> None:
    for key in vals.amountByCat.keys():
        vals.amountByCat[key] = 0

    for expense in vals.expenses:
        key = expense.category
        if key in vals.amountByCat:
            vals.amountByCat[key] += expense.amount
        else:
            vals.amountByCat[key] = expense.amount

def sumExp() -> None:
    for key in vals.sumExp.keys():
        vals.sumExp[key] = 0

    for key in vals.budgets.keys():
        if key not in vals.sumExp.keys():
            vals.sumExp[key] = 0

    for expense in vals.expenses:
        vals.sumExp["total"] += expense.amount
        vals.sumExp[expense.category] += expense.amount

def getDailyExp() -> None:
    dailyExpenses = [[] for _ in range(31)]

    for expense in vals.expenses:
        dailyExpenses[expense.day - 1].append(expense.get_expf())

    vals.dailyExp = dailyExpenses


def undoLastExp() -> None:
    lastExpFilePath = paths.curExpFile

    if len(lastExpFilePath) <= 0:
        menu_message = "~~Nothing to undo!~~"
        return

    inf.flushTerminal()
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
        with open(lastExpFilePath, 'r') as file:
            lines = file.readlines()
            file.close()

        if lines:
            last_line = lines[len(lines) - 1]
            lines = lines[:-1]

            itm_name, itm_cat, itm_amount, itm_month, itm_day, itm_year, itm_cd = last_line.strip().split(',')
            item = Item(name=itm_name, category=itm_cat, amount=float(itm_amount), month=int(itm_month), day=int(itm_day), year=int(itm_year), cd=itm_cd)

            with open(lastExpFilePath, 'w') as file:
                file.writelines(lines)
                file.close()

        messages.menu = f"Removed {item.get_dep()} from {lastExpFilePath}"
