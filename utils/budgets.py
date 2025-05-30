from . import infrastructure as Inf

from data import filePaths as Paths
from data import vals as Vals
from data import exceptions

import json as Json
import sys

def initBudgets() -> None:
        Inf.flushTerminal()
        print("budgets.json file not found. Creating a new one...")

        data = {
            "total": 0.0,
        }
        data["total"] = float(input("Enter total budget: "))

        cat = ""
        while True:
             Inf.flushTerminal()
             cat = input("Enter new category (enter 'x' to continue): ")
             if str.lower(cat)== 'x':
                  break
             budget = float(input(f"Enter amount for category {cat}: "))
             data[cat] = budget

        with open(Paths.BUDGETS, 'w') as budgets:
            Json.dump(data, budgets, indent=4)

        print(f"budgets.json file created successfully with new data.")

def getBudgets() -> None:
    """ Reads in the budget values from info.json and stores them as global variables """

    with open(Paths.BUDGETS,'r') as budgets:
        Vals.budgets = Json.load(budgets)

    budgets.close()


def editBudgets() -> None:
    Inf.flushTerminal()

    data  = {}
    with open(Paths.BUDGETS, 'r') as budgets:
        data = Json.load(budgets)

        while True:
            print("Current Budgets:")
            for i, key in enumerate(data.keys()):
                print(f"{i} | {key}: \t${data[key]}")

            budgetNum = input("Enter the number of the budget you would like to enter (enter 'a' to add a new budget): ")
            if isInt(budgetNum):
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
                 raise exceptions.BreakLoop
            elif str.lower(budgetNum) == 'q':
                Inf.flushTerminal()
                sys.exit()

            with open(Paths.BUDGETS, 'w') as budgets:
                Json.dump(data, budgets, indent=4)

    print(f"budgets.json file created successfully with new data.")


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
