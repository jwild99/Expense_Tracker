from . import infrastructure as Inf

from data import filePaths as Paths
from data import vals as Vals

import json as Json

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

    with open(Paths.BUDGETS, 'r') as budgets:
        data = Json.load(budgets)

        inp = ''
        while str.lower(inp) != 'x':
            print("Current Budgets:")
            for i, key in enumerate(data.keys()):
                print(f"{i} | {key}: \t${data[key]}")

            budgetNum = int(input("Enter the number of the budget you would like to enter (enter 'a' to add a new budget): "))

            inp = input("\nx to go back")



        # data = {
        #     "total": 0.0,
        # }
        # data["total"] = float(input("Enter total budget: "))

        # cat = ""
        # while True:
        #      Inf.flushTerminal()
        #      cat = input("Enter new category (enter 'x' to continue): ")
        #      if str.lower(cat)== 'x':
        #           break
        #      budget = float(input(f"Enter amount for category {cat}: "))
        #      data[cat] = budget

        with open(Paths.BUDGETS, 'w') as budgets:
            Json.dump(data, budgets, indent=4)

        print(f"budgets.json file created successfully with new data.")
