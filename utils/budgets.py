from . import infrastructure as Inf

from data import file_paths as Paths
from data import vals as Vals

import json as Json

def initBudgets() -> None:
        Inf.flush_terminal()
        print("budgets.json file not found. Creating a new one...")

        data = {
            "total_budget": 0.0,
            "general_budget": 0.0,
            "grocery_budget": 0.0,
        }

        data['total_budget'] = float(input("Enter total budget: "))
        Inf.flush_terminal()
        data['general_budget'] = float(input("Enter general budget: "))
        Inf.flush_terminal()
        data['grocery_budget'] = float(input("Enter grocery budget: "))
        Inf.flush_terminal()

        with open(Paths.BUDGETS, 'w') as budgets:
            Json.dump(data, budgets, indent=4)

        print(f"budgets.json file created successfully with new data.")

def getBudgets() -> None:
    """ Reads in the budget values from info.json and stores them as global variables """

    with open(Paths.BUDGETS,'r') as budgets:
        data = Json.load(budgets)

    Vals.totalBudget = float(data["total_budget"])
    Vals.gnrlBudget = float(data["general_budget"])
    Vals.grocBudget = float(data["grocery_budget"])

    budgets.close()
