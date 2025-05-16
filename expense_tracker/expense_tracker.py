import json
from expense_tracker.item_class import Item
from utils import terminal_utils as tUtils
import os
from const import time_const as time

exp_categories = [
    "Food",
    "Home",
    "Clothes",
    "Laundry",
    "Grocery",
    "Work",
    "Travel",
    "Fun",
    "Misc"
]


info_file_path = "info.json"
most_recent_itm_path = ""

menu_message = ""

cur_month = 0
cur_day = 0
cur_year = 0



total_budget = 0
gnrl_budget = 0
grcry_budget = 0

total_exp = 0
gnrl_exp = 0
grcry_exp = 0

acc_blnce = 0

recent_acc_blnce = 0
recent_cc_blnce = 0

# TERMINAL UTILS
################################################################################################################################



# USER INPUT UTILS
################################################################################################################################

def get_user_category() -> int:
    """ Gets user input for the category of an item """

    while True:
        print("Select a category:")
        for i, category_name in enumerate(exp_categories):
            print(f"    {i + 1}. {category_name}")

        val_range = f"[1 - {len(exp_categories)}]"

        try:
            cat_num = int(input(f"Enter category number {val_range}: ")) - 1

            if cat_num not in range(0, len(exp_categories)):
                raise Exception

            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid category number entered. Please enter a value between 1 and {len(exp_categories)}.\n\n")

    return cat_num

def get_user_day(month: int) -> int:
    """ Gets user input for day the item occurred """

    while True:
        try:
            inp = input("Enter a day number [1-31]- leave blank for current day: ")

            if inp == '':
                day = cur_day
            else:
                day = int(inp)

            if day not in range(1, 32):
                raise Exception

            # February cannot have more than 29 days
            if month == 2 and day > 29:
                raise Exception
            # April, June, September, and November have 30 days
            if month in {4, 6, 9, 11} and month > 30:
                raise Exception


            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid date number entered. Please enter a value between 1 and 31 and make sure the value is valid for the month.\n\n")

    return day

def get_user_month() -> int:
    """ Gets user input for the month an item occurred """

    while True:
        try:
            inp = input("Enter a month number [1-12]- leave blank for current month: ")

            if inp == '':
                month = cur_month
            else:
                month = int(inp)

            if month not in range(1, 13):
                raise Exception

            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid month number entered. Please enter a value between 1 and 12.\n\n")

    return month

def get_user_year() -> int:
    """ Gets uer input for the year an item occurred """

    while True:
        try:
            inp = input("Enter a year number- leave blank for current year: ")

            if inp == '':
                year = cur_year
            else:
                year = int(inp)

            if year < 1:
                raise Exception

            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid year number entered. Please enter a value between 1 and 12.\n\n")

    return year

def get_user_amount() -> float:
    """ Gets user input for the amount of the item """

    while True:
        try:
            amount = float(input("Enter amount: "))
            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print("\n\n~~ERROR~~\nInvalid expense amount entered! Please try again.\n\n")

    return amount

def get_user_cd() -> str:
    """ Gets user input for whether or not the expense is a debit or credit card expense """

    while True:
        try:
            cd = input("Is this a credit or debit expense? [c/d]: ").strip().lower()

            if cd != 'c' and cd != 'd':
                raise Exception

            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid credit/debit value entered. Please enter either 'c' or 'd'.\n\n")

    return cd

def get_user_name() -> str:
    """ Gets a new item name from the user and ensures it is valid with no commas """

    while True:
        try:
            name = input("Enter expense name: ").strip()

            if name.find(",") != -1:
                raise Exception

            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid name value entered. Make sure there are no commas!\n\n")

    return name

# GETTING ITEMS FROM USER
################################################################################################################################

def get_user_expense() -> type[Item]:
    """ Collects from the user the necessary info to create a new expense and creates one """

    tUtils.flush_terminal()
    exp_name = get_user_name()
    exp_amount = get_user_amount()
    cat_num = get_user_category()
    exp_month = get_user_month()
    exp_day = get_user_day(month=exp_month)
    exp_year = get_user_year()
    exp_cd = get_user_cd()

    new_exp =Item(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=exp_month,
                      day=exp_day, year=exp_year, cd=exp_cd)
    tUtils.flush_terminal()
    return new_exp

# WRITING TO CSV
################################################################################################################################

def save_expense(exp:Item) -> None:
    """ Saves a new expense to the correct CSV. Also stores the most recent file path """

    global most_recent_itm_path, menu_message

    exp_file_path = f"records/records{exp.year}.csv"
    most_recent_itm_path = f"records/records{exp.year}.csv"

    with open(exp_file_path, 'a') as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day},{exp.year},{exp.cd}\n")
        file.close()

    menu_message = f"Saved expense: [{exp.get_exp()}] to {exp_file_path}"

# WRITING TO OR READING FROM INFO.JSON
################################################################################################################################

def get_budgets() -> None:
    """ Reads in the budget values from info.json and stores them as global variables """

    global info_file_path, total_budget, grcry_budget, gnrl_budget

    with open(info_file_path, 'r') as file:
        data = json.load(file)

        total_budget = float(data["total_budget"])
        gnrl_budget = float(data["general_budget"])
        grcry_budget = float(data["grocery_budget"])

        file.close()

# READING ITEMS FROM CSVs
################################################################################################################################

def get_all_expenses() -> dict:
    """ Iterates through the directory containing the CSVs and gets a dictionary of all expenses
    for each year. Each dictionary entry contains its own list of size 12 for
    each month. Any given expense will be sorted into the proepr
    dictionary bucket based on year, and then places
    into the correct list within that bucket
    based on month of occurance """

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

def get_cur_expenses() -> list[Item]:
    """ Gets a list of the expenses from the current month """

    expenses: list[Item] = []
    exp_file_path = f"records/records{cur_year}.csv"

    if not os.path.exists(exp_file_path):
        return []

    with open(exp_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd = line.strip().split(',')

                expenses.append(Item(name=exp_name, category=exp_cat, amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd))

        file.close()

    return expenses

# PROCESSING ITEMS FROM CSVs
################################################################################################################################

def get_amount_by_cat(expenses: list[Item]) -> dict:
    """ Gets a dictionary of expenses by category """

    amount_by_cat = {}

    for expense in expenses:
        key = expense.category
        if key in amount_by_cat:
            amount_by_cat[key] += expense.amount
        else:
            amount_by_cat[key] = expense.amount

    return amount_by_cat

def sum_expenses(expenses: list[Item]) -> None:
    """ Sums the expenses of each type: total, grocery, and general """

    global total_exp, gnrl_exp, grcry_exp

    total_exp, gnrl_exp, grcry_exp = 0, 0, 0

    for expense in expenses:
        if expense.name != "[CREDIT CARD PAYMENT]":
            total_exp += expense.amount

            if expense.category.lower() == "grocery":
                grcry_exp += expense.amount
            else:
                gnrl_exp += expense.amount

def get_daily_expenses(expenses: list[Item]) -> list[str]:
    """ Gets a list of daily expenses in a formatted string """

    daily_expenses = [[] for _ in range(31)]

    for expense in expenses:
        daily_expenses[expense.day - 1].append(expense.get_expf())

    return daily_expenses

# ITEM PRINT UTILS
################################################################################################################################

def print_amount_by_cat(amount_by_cat: dict) -> None:
    """ Displays the amount spent per category as well as the percentage of the total budget being spent there """

    print("Monthly expenses by category:")
    for key, amount in amount_by_cat.items():
        percentage = (amount / total_budget) * 100
        if key.strip().lower() == "grocery":
            print(f"    {key}:   \t${amount:.2f}    \t{percentage:.2f}% \t -want-> 20%")
        else:
            print(f"    {key}:   \t${amount:.2f}    \t{percentage:.2f}%")

def print_remaining_budget() -> None:
    """ Displays the remaining amount of each budget type"""

    print(f"\n${total_budget - total_exp:.2f}    \tof total budget remaining   \t[${total_budget:.2f}]")
    print(f"${gnrl_budget - gnrl_exp:.2f}    \tof general budget remaining \t[${gnrl_budget:.2f}]")
    print(f"${grcry_budget - grcry_exp:.2f}    \tof grocery budget remaining \t[${grcry_budget:.2f}]")

def print_daily_expenses(daily_expenses: list[Item]) -> None:
    """ Displays a day-by-day summary of expenses """

    print("Date \t\t\tCategory \tAmount \t\tCard Type \tName\n")
    for i in range(len(daily_expenses)):
        for exp in daily_expenses[i]:
            print(exp)

def print_monthly_exp_summary(expenses: list[Item], months_index: int, year: int, reached_current: bool) -> None:
    """ Displays a summary of the given month to the console """

    if len(expenses) <= 0:
        return

    amount_by_cat = get_amount_by_cat(expenses)
    daily_expenses = get_daily_expenses(expenses)
    sum_expenses(expenses)

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

# EXPENSE REPORT ACTIONS
################################################################################################################################

def get_full_summary() -> None:
    """ Gets a more verbose summary of the current months expenses than the one from the main menu """

    tUtils.flush_terminal()

    expenses = get_cur_expenses()
    amount_by_cat = get_amount_by_cat(expenses)
    daily_expenses = get_daily_expenses(expenses)
    sum_expenses(expenses)

    if len(expenses) > 0:
        print_daily_expenses(daily_expenses)
        print("\n\n")
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show at this time.")

    print_remaining_budget()

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

def get_alltime_summary() -> None:
    """ Gets an all-time version of the full month summary """

    expenses = get_all_expenses()
    reached_current = False
    months_index = 0
    cur_month_index = cur_month - 1

    tUtils.flush_terminal()

    if len(expenses) > 0:
        for year_key in sorted(expenses.keys()):
            months_index = 0
            for month_list in expenses[year_key]:
                if (int(year_key) == cur_year and months_index == cur_month_index):
                    reached_current = True
                    break

                print_monthly_exp_summary(expenses=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                months_index += 1

            if reached_current:
                print_monthly_exp_summary(expenses=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                sum_expenses(month_list)
                break
    else:
        print("No expenses to show at this time.")

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

    tUtils.flush_terminal()

# MISC USER ACTIONS
################################################################################################################################

def help() -> None:
    """ Prints out a list of commands for the app. May expand later to other help stuff """

    tUtils.flush_terminal()

    print("Help Menu")
    print('-'*30)

    print("\nCommand List:")
    print("'x'     | quit or go back")
    print("'e'     | add a new expense")
    print("'u'     | undo most recently added expense or deposit")
    print("'s'     | full expense summary of current month")
    print("'s -a'  | all-time monthly summary of expenses")

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

    tUtils.flush_terminal()

# DANGER ZONE USER ACTIONS
################################################################################################################################

def undo_last_expense() -> None:
    """ Un-does the most recent CSV write. This can be an expense, deposit, or CC payment. The function just
    erases the bottom line of the most recent file written to. If the user just opened the app, there will be
    no 'most_recent_itm' at that point so nothing will be undone. In cases like this, edit the CSV directly """

    global menu_message

    if len(most_recent_itm_path) <= 0:
        menu_message = "~~Nothing to undo!~~"
        return

    tUtils.flush_terminal()
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

# CLI UTILS AND MAIN MENU LOOP
################################################################################################################################

def init() -> None:
    """ Initializes current data and makes sure there is a csv file created for the current year.
    Also gets the current budgets from info.json """

    global cur_month, cur_day, cur_year
    cur_month = time.cur_month
    cur_day = time.cur_day
    cur_year = time.cur_year

    with open(f"expense_tracker\\records\\records{cur_year}.csv", 'a') as file:
        pass

    init_json()

    get_budgets()

def init_json() -> None:
    file_name = 'info.json'

    if not os.path.exists(file_name):
        tUtils.flush_terminal()
        print("info.json file not found. Creating a new one")

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

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"{file_name} created successfully with new data.")

def get_menu_summary() -> None:
    """ Gets and displays the main menu summary which includes expenses
    by category, account balances, and remaining budget """

    tUtils.flush_terminal()
    expenses = get_cur_expenses()
    amount_by_cat = get_amount_by_cat(expenses)
    sum_expenses(expenses)

    print(f"Expense Tracker [{time.months[cur_month - 1]}, {cur_year}]")
    if len(menu_message) > 0:
        print(menu_message)
    tUtils.lines(60)
    tUtils.spacing(1)

    if len(expenses) > 0:
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show at this time.")

    print_remaining_budget()

def get_user_action() -> None:
    """ Gets user input for an action and then dispatches correct code for that action """

    global menu_message

    action = input(f"\n\nx: quit | h: help\nWhat would you like to do:\n").strip().lower()
    if action == 'x':
        tUtils.close()
    elif action == 'e':
        menu_message = ""
        exp = get_user_expense()
        save_expense(exp)
    elif action == 'u':
        menu_message = ""
        undo_last_expense()
    elif action == "s":
        menu_message = ""
        get_full_summary()
    elif action == "s -a":
        menu_message = ""
        get_alltime_summary()
    elif action == 'h':
        menu_message = ""
        help()

def cli_loop() -> None:
    """ Loop that runs until user quits- displays main menu and gets user actions """

    while True:
        tUtils.flush_terminal()
        get_menu_summary()
        get_user_action()

# EXECUTION
################################################################################################################################

def main() -> None:
    """ Main Function that begins app execution """

    init()
    cli_loop()

