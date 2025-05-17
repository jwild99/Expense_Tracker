import json
from . import terminal as tUtils
from data import file_paths as paths
from . import file as fUtils
from data import expVsBud as eb

def init_budgets() -> None:
        tUtils.flush_terminal()
        print("budgets.json file not found. Creating a new one...")

        data = {
            "total_budget": 0.0,
            "general_budget": 0.0,
            "grocery_budget": 0.0,
        }

        data['total_budget'] = float(input("Enter total budget: "))
        tUtils.flush_terminal()
        data['general_budget'] = float(input("Enter general budget: "))
        tUtils.flush_terminal()
        data['grocery_budget'] = float(input("Enter grocery budget: "))
        tUtils.flush_terminal()

        new_file = open(paths.BUDGETS, 'w')
        json.dump(data, new_file, indent=4)

        print(f"budgets.json file created successfully with new data.")

def get_budgets() -> None:
    """ Reads in the budget values from info.json and stores them as global variables """

    file = fUtils.open_json(paths.BUDGETS,'r')
    data = json.load(file)

    eb.total_budget = float(data["total_budget"])
    eb.gnrl_budget = float(data["general_budget"])
    eb.groc_budget = float(data["grocery_budget"])

    file.close()
