import os 
import platform
import datetime
import sys
import json 

from item import Item

exp_categories = [
    "Food",
    "Home",
    "Laundry"
    "Grocery",
    "Work",
    "Travel",
    "Fun",
    "Misc"
]

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
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

# First line formatting in csv:
# total budget, misc budget, grocery budget, total spending this month, month number, date number, year number, c/d, true expense?, item type

def flush_terminal() -> None:
    print("\n" * 500)
    if platform.system() == 'Windows':
        os.system('cls')  
    else:
        os.system('clear') 
    sys.stdout.flush()

def get_user_expense() -> type[Item]:
    global exp_categories, info_file_path, cur_month, cur_day, cur_year

    flush_terminal()

    exp_name = input("Enter expense name: ")
    flush_terminal()

    while True:
        try:
            exp_amount = float(input("Enter expense amount: "))
            flush_terminal()
            break
        except Exception:
            flush_terminal()
            print("\n\n~~ERROR~~\nInvalid expense amount entered! Please try again.\n\n")

    while True:
        print("Select a category:")
        for i, category_name in enumerate(exp_categories):
            print(f"    {i + 1}. {category_name}")
        
        val_range = f"[1 - {len(exp_categories)}]"

        try:
            cat_num = int(input(f"Enter category number {val_range}: ")) - 1

            if cat_num not in range(0, len(exp_categories)):
                raise Exception
            
            flush_terminal()
            break
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid category number entered. Please enter a value between 1 and {len(exp_categories)}.\n\n")

    while True:
        try:
            inp = input("Enter a month number [1-12]- leave blank for current month: ")

            if inp == '':
                exp_month = cur_month
            else:
                exp_month = int(inp)

            if exp_month not in range(1, 13):
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid month number entered. Please enter a value between 1 and 12.\n\n")

    while True:
        try:
            inp = input("Enter a day number [1-31]- leave blank for current day: ")

            if inp == '':
                exp_day = cur_day
            else:
                exp_day = int(inp)

            if exp_day not in range(1, 32):
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid date number entered. Please enter a value between 1 and 31.\n\n")

    while True:
        try:
            inp = input("Enter a year number- leave blank for current year: ")

            if inp == '':
                exp_year = cur_year
            else:
                exp_year = int(inp)

            if exp_year < 1:
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid year number entered. Please enter a value between 1 and 12.\n\n")

    while True:
        try:
            exp_cd = input("Is this a credit or debit expense? [c/d]: ")

            if exp_cd.strip().lower() != 'c' and exp_cd.strip().lower() != 'd':
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid credit/debit value entered. Please enter either 'c' or 'd'.\n\n")

    while True:
        try:
            tru_exp = input("Is this a 'true expense'? [y/n] (leave blank for 'y'): ").strip().lower()

            if tru_exp == '':
                tru_exp = 'y'

            if tru_exp.strip().lower() != 'y' and tru_exp.strip().lower() != 'n':
                raise Exception
            
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid 'true expense' value entered. Please enter either 'y' or 'n'.\n\n")

    new_exp = Item(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=exp_month, 
                      day=exp_day, year=exp_year, cd=exp_cd, tru_exp=tru_exp, itm_type="EXP")
    flush_terminal()
    return new_exp

def get_user_deposit() -> type[Item]:
    flush_terminal()

    dep_name = input("Enter expense name: ")
    flush_terminal()

    while True:
        try:
            dep_amount = float(input("Enter expense amount: "))
            flush_terminal()
            break
        except Exception:
            flush_terminal()
            print("\n\n~~ERROR~~\nInvalid expense amount entered! Please try again.\n\n")

    while True:
        try:
            inp = input("Enter a month number [1-12]- leave blank for current month: ")

            if inp == '':
                dep_month = cur_month
            else:
                dep_month = int(inp)

            if dep_month not in range(1, 13):
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid month number entered. Please enter a value between 1 and 12.\n\n")

    while True:
        try:
            inp = input("Enter a day number [1-31]- leave blank for current day: ")

            if inp == '':
                dep_day = cur_day
            else:
                dep_day = int(inp)

            if dep_day not in range(1, 32):
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid date number entered. Please enter a value between 1 and 31.\n\n")

    while True:
        try:
            inp = input("Enter a year number- leave blank for current year: ")

            if inp == '':
                dep_year = cur_year
            else:
                dep_year = int(inp)

            if dep_year < 1:
                raise Exception
            
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid year number entered. Please enter a value between 1 and 12.\n\n")
        
    new_exp = Item(name=dep_name, category="misc", amount=dep_amount, month=dep_month, 
                      day=dep_day, year=dep_year, cd='c', tru_exp="n", itm_type="DEP")
    flush_terminal()
    return new_exp

def save_expense(exp: Item) -> None:
    global most_recent_itm_path, menu_message

    exp_file_path = f"records/records{exp.year}.csv"
    most_recent_itm_path = f"records/records{exp.year}.csv"

    with open(exp_file_path, "a") as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day},{exp.year},{exp.cd},{exp.tru_exp},{exp.itm_type}\n")

        file.close()

    menu_message = f"Saved expense: [{exp.get_exp()}] to {exp_file_path}"

def save_deposit(dep: Item) -> None:
    global most_recent_itm_path, menu_message

    dep_file_path = f"records/records{dep.year}.csv"
    most_recent_itm_path = f"records/records{dep.year}.csv"

    with open(dep_file_path, "a") as file:
        file.write(f"{dep.name},{dep.category},{dep.amount},{dep.month},{dep.day},{dep.year},{dep.cd},{dep.tru_exp},{dep.itm_type}\n")

        file.close()

    menu_message = f"Saved deposit: [{dep.get_dep()}] to {dep_file_path}"

def get_all_expenses() -> dict:
    exp_file_dir = f"records/"
    expenses_dict = {}
    
    for filepath in os.listdir(exp_file_dir):
        with open(f"records/{filepath}", 'r') as file:
            lines = file.readlines()

            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd, tru_exp, itm_type = line.strip().split(',')

                if tru_exp.strip().lower() == 'y' and itm_type.strip().lower() == 'exp':
                    expense = Item(name=exp_name, category=exp_cat, 
                                amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd, tru_exp=tru_exp, itm_type=itm_type)

                    if expense.year in expenses_dict:
                        expenses_dict[expense.year][int(exp_month) - 1].append(expense)
                    else:
                        expenses_dict[expense.year] = [[] for _ in range(12)]
                        expenses_dict[expense.year][int(exp_month) - 1].append(expense)

            file.close() 

    return expenses_dict

def get_cur_expenses() -> list[Item]:
    expenses: list[Item] = []
    exp_file_path = f"records/records{cur_year}.csv"

    if not os.path.exists(exp_file_path):
        return []

    with open(exp_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd, tru_exp, itm_type = line.strip().split(',')

            if int(exp_month) == cur_month and int(exp_year) == cur_year and tru_exp.strip().lower() == 'y' and itm_type.strip().lower() == 'exp':
                expenses.append(Item(name=exp_name, category=exp_cat, amount=float(exp_amount), 
                                month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd, tru_exp=tru_exp, itm_type=itm_type))
                    
        file.close()
                    
    return expenses

def get_budgets() -> None:
    global info_file_path, total_budget, grcry_budget, gnrl_budget

    with open(info_file_path, 'r') as file:
        data = json.load(file)

        total_budget = float(data["total_budget"])
        gnrl_budget = float(data["general_budget"])
        grcry_budget = float(data["grocery_budget"])

        file.close()

def get_amount_by_cat(expenses: list[Item]) -> dict:
    amount_by_cat = {}

    for expense in expenses:
        key = expense.category
        if key in amount_by_cat:
            amount_by_cat[key] += expense.amount
        else:
            amount_by_cat[key] = expense.amount

    return amount_by_cat

def sum_expenses(expenses: list[Item]) -> None:
    global total_exp, gnrl_exp, grcry_exp

    total_exp, gnrl_exp, grcry_exp = 0, 0, 0

    for expense in expenses:
        total_exp += expense.amount

        if expense.category.lower() == "grocery":
            grcry_exp += expense.amount
        else:
            gnrl_exp += expense.amount

def get_daily_expenses(expenses: list[Item]) -> list[str]:
    daily_expenses = [[] for _ in range(31)]
    
    for expense in expenses:
        daily_expenses[expense.day - 1].append(expense.get_expf())

    return daily_expenses

def print_amount_by_cat(amount_by_cat: dict) -> None:
    print("Monthly expenses by category:")
    for key, amount in amount_by_cat.items():
        percentage = (amount / total_budget) * 100
        print(f"    {key}:   \t${amount:.2f}       {percentage:.2f}%")

def print_remaining_budget() -> None:
    global total_budget, total_exp, gnrl_budget, gnrl_exp, grcry_budget, grcry_exp

    print(f"\n${total_budget - total_exp} of total budget remaining   \t[${total_budget}]")
    print(f"${gnrl_budget - gnrl_exp} of general budget remaining \t[${gnrl_budget}]")
    print(f"${grcry_budget - grcry_exp} of grocery budget remaining \t[${grcry_budget}]")

def print_daily_expenses(daily_expenses: list[Item]) -> None:
    for i in range(len(daily_expenses)):
            for exp in daily_expenses[i]:
                print(exp)

def get_menu_summary() -> None:
    flush_terminal()

    expenses = get_cur_expenses()
    amount_by_cat = get_amount_by_cat(expenses)
    sum_expenses(expenses)

    print(f"Expense Tracker [{months[cur_month - 1]}, {cur_year}]")
    if len(menu_message) > 0:
        print(menu_message)
    print("-"*60)
    print()

    if len(expenses) > 0:
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show at this time.")

    print_remaining_budget() 

def get_full_summary() -> None:
    flush_terminal()

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
    while input("") != 'x':
        continue

def print_monthly_exp_summary(expenses: list[Item], months_index, year: int, reached_current: bool) -> None:
    global total_budget, total_exp, gnrl_budget, gnrl_exp, grcry_budget, grcry_exp, months

    amount_by_cat = get_amount_by_cat(expenses)
    daily_expenses = get_daily_expenses(expenses)
    sum_expenses(expenses)
    
    if reached_current:
        print(f"Summary for {months[months_index]}, {year} (current month)")
        print("-"*60)
    else:
        print(f"Summary for {months[months_index]}, {year}")
        print("-"*60)

    if len(expenses) > 0:
        print_daily_expenses(daily_expenses)
        print("\n")
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show for this month.")

    print(f"\n${total_exp} \tof ${total_budget} total   budget in {months[months_index]}, {year}")
    print(f"${gnrl_exp} \tof ${gnrl_budget} general budget in {months[months_index]}, {year}")
    print(f"${grcry_exp}     \tof ${grcry_budget} grocery budget in {months[months_index]}, {year}")
    
    if reached_current:
        print("\n")
    else:
        print("\n\n\n\n\n")

def get_alltime_summary() -> None:
    global cur_month, cur_year
    expenses = get_all_expenses()
    reached_current = False
    months_index = 0
    cur_month_index = cur_month - 1

    flush_terminal()
    
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
    while input("") != 'x':
        continue

    flush_terminal()

# Opens the help menu until the user enters 'x' to go back
def help() -> None:
    flush_terminal()

    print("Help Menu")
    print('-'*30)

    print("\nCommand List:")
    print("'x'    | quit or go back")
    print("'e'    | add a new expense")
    print("'d'    | add a new deposit")
    print("'u'    | undo most recently added expense or deposit")
    print("'s'    | full expense summary of current month")
    print("'s -a' | all-time monthly summary of expenses")
    print("'f'    | full report of all account activity in system")

    print("\n'x' to go back")
    while input("") != 'x':
        continue

    flush_terminal()

# Erases the most recent line written as an expense
def undo_last_expense() -> None:
    global most_recent_itm_path, menu_message

    if len(most_recent_itm_path) <= 0:
        menu_message = "~~Nothing to undo!~~"
        return

    with open(most_recent_itm_path, 'r') as file:
        lines = file.readlines()  

        file.close()

    if lines:  
        lines = lines[:-1]  

        with open(most_recent_itm_path, 'w') as file:
            file.writelines(lines) 

            file.close()

# Close the app (flush terminal and then exit)
def close() -> None:
    flush_terminal()
    exit()

# Initializes information necessary for using the app
def init() -> None:
    global cur_month, cur_day, cur_year

    cur_month = datetime.datetime.now().month
    cur_day = datetime.datetime.now().day
    cur_year = datetime.datetime.now().year

    with open(f"records/records{cur_year}.csv", 'a') as file:
        pass

    get_budgets()

# Menu loop where options can be selected from
def cli_loop() -> None:
    global menu_message

    while True:
        flush_terminal()

        get_menu_summary()

        action = input(f"\n\nx: quit | h: help\nWhat would you like to do:\n")

        if action.strip().lower() == 'x':
            close()
        elif action.strip().lower() == 'e':
            menu_message = ""
            exp = get_user_expense()
            save_expense(exp)
        elif action.strip().lower() == 'u':
            menu_message = ""
            undo_last_expense()
        elif action.lower() == "s":
            menu_message = ""
            get_full_summary()
        elif action == "s -a":
            menu_message = ""
            get_alltime_summary()
        elif action == 'f':
            menu_message = ""
            pass
            # full_report()
        elif action == 'd':
            menu_message = ""
            dep = get_user_deposit()
            save_deposit(dep)
            # get_deposit(), save_deposit
        elif action == 'h':
            menu_message = ""
            help()

# Runs the main program
def main() -> None:
    init()
    cli_loop()

if __name__ == "__main__":
    main()