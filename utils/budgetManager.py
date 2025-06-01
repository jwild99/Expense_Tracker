from . import systemUtils as Inf

from data import filePaths as Paths
from data import vals as Vals
from data import timeVals as Time

import json as Json
import sys

def initBudgetsRecord():
    with open(Paths.curBudgetFile, "r") as curBudgets:
        print(curBudgets)
        data = Json.load(curBudgets)

        with open(Paths.curBudgetRecord, "w") as curRecord:
            Json.dump(data, curRecord, indent=4)


def initBudgets() -> None:
        Inf.flushTerminal()
        print("budgets.json file not found. Creating a new one...")

        data = {}
        total = 0
        category = ""
        while True:
             Inf.flushTerminal()
             category = input("Enter new category (enter 'x' to continue): ")
             if str.lower(category)== 'x':
                  break
             budget = float(input(f"Enter amount for category {category}: "))
             data[category] = budget
             total += budget
        data["total"] = total

        with open(Paths.curBudgetFile, 'w') as budgets:
            Json.dump(data, budgets, indent=4)
        with open(Paths.curBudgetRecord, 'w') as budgetsRecord:
            Json.dump(data, budgetsRecord, indent=4)

        print(f"budgets.json file created successfully with new data.")

def getCurBudgets() -> None:
    """ Reads in the budget values from info.json and stores them as global variables """
    with open(Paths.curBudgetFile,'r') as budgets:
        Vals.budgets = Json.load(budgets)
    budgets.close()

def getMonthlyBudgets(month: int, year: int) -> None:
    """ Reads in the budget values from info.json and stores them as global variables """

    with open(f"records/budgets/budgets-{Time.month}-{Time.year}.json",'r') as budgets:
        Vals.monthlyBudgets = Json.load(budgets)

    budgets.close()

def editBudgets() -> None:
    Inf.flushTerminal()

    data  = {}
    with open(Paths.curBudgetFile, 'r') as budgets:
        data = Json.load(budgets)

        while True:
            print("Current Budgets:")
            for i, key in enumerate(data.keys()):
                print(f"{i} | {key}: \t${data[key]}")

            budgetNum = input("Enter the number of the budget you would like to enter (enter 'a' to add a new budget): ")
            if Inf.isInt(budgetNum):
                 budgetNum = int(budgetNum)
                 if budgetNum not in range(0, len(data.keys())):
                      print("invalid category number!")
                      continue
                 else:
                    category = list(data.keys())[budgetNum]
                    Inf.flushTerminal()
                    budget = float(input(f"Enter amount for category {category}: "))
                    data[category] = budget
            elif str.lower(budgetNum) == 'a':
                Inf.flushTerminal()
                cat = input("Enter new category: ")
                budget = float(input(f"Enter amount for category {cat}: "))
                data[cat] = budget
            elif str.lower(budgetNum) == 'x':
                 Inf.goBack()
            elif str.lower(budgetNum) == 'q':
                Inf.close()

            with open(Paths.curBudgetFile, 'w') as budgets:
                Json.dump(data, budgets, indent=4)

            with open(Paths.curBudgetRecord, 'w') as budgetsRecord:
                Json.dump(data, budgetsRecord, indent=4)

    print(f"budgets.json file created successfully with new data.")


