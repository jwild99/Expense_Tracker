import os 
import platform
import datetime
import sys
import json 

from expense import Expense

exp_categories = [
    "Food",
    "Home",
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
most_recent_exp_path = ""

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
# total budget, misc budget, grocery budget, total spending this month, month number, date number, year number, true expense?

def flush_terminal():
    print("\n" * 500)
    if platform.system() == 'Windows':
        os.system('cls')  
    else:
        os.system('clear') 
    sys.stdout.flush()

def get_user_expense():
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
            inp = input("Enter a year number [1-12]- leave blank for current year: ")

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
            inp = input("Is this a 'true expense'? [y/n] (leave blank for 'y'): ").strip().lower()

            if inp == '':
                tru_exp = 'y'
            else:
                tru_exp = inp

            if tru_exp.strip().lower() != 'y' and tru_exp.strip().lower() != 'n':
                raise Exception
            
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid 'true expense' value entered. Please enter either 'y' or 'n'.\n\n")

    new_exp = Expense(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=exp_month, day=exp_day, year=exp_year, tru_exp=tru_exp)
    flush_terminal()
    return new_exp

def save_expense(exp: Expense):
    global most_recent_exp_path

    exp_file_path = f"expenses/expenses{exp.year}.csv"
    most_recent_exp_path = f"expenses/expenses{exp.year}.csv"

    with open(exp_file_path, "a") as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day},{exp.year},{exp.tru_exp}\n")

        file.close()

    print(f"Saved expense: [{exp.get_exp()}] to {exp_file_path}")

def get_all_expenses() -> dict:
    exp_file_dir = f"expenses/"
    expenses_dict = {}
    
    for filepath in os.listdir(exp_file_dir):
        with open(f"expenses/{filepath}", 'r') as file:
            lines = file.readlines()

            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, tru_exp = line.strip().split(',')

                if tru_exp.strip().lower() == 'y':
                    expense = Expense(name=exp_name, category=exp_cat, 
                                amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), tru_exp=tru_exp)

                    if expense.year in expenses_dict:
                        expenses_dict[expense.year][int(exp_month) - 1].append(expense)
                    else:
                        expenses_dict[expense.year] = [[] for _ in range(12)]
                        expenses_dict[expense.year][int(exp_month) - 1].append(expense)

            file.close() 

    return expenses_dict

def get_cur_expenses() -> list[Expense]:
    expenses: list[Expense] = []
    exp_file_path = f"expenses/expenses{cur_year}.csv"

    if not os.path.exists(exp_file_path):
        return []

    with open(exp_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, tru_exp = line.strip().split(',')

            if int(exp_month) == cur_month and int(exp_year) == cur_year and tru_exp.strip().lower() == 'y':
                expenses.append(Expense(name=exp_name, category=exp_cat, amount=float(exp_amount), 
                                month=int(exp_month), day=int(exp_day), year=int(exp_year), tru_exp=tru_exp))
                    
        file.close()
                    
    return expenses

def get_budgets():
    global info_file_path, total_budget, grcry_budget, gnrl_budget

    with open(info_file_path, 'r') as file:
        data = json.load(file)

        total_budget = float(data["total_budget"])
        gnrl_budget = float(data["general_budget"])
        grcry_budget = float(data["grocery_budget"])

        file.close()

def get_amount_by_cat(expenses: list[Expense]):
    amount_by_cat = {}

    for expense in expenses:
        key = expense.category
        if key in amount_by_cat:
            amount_by_cat[key] += expense.amount
        else:
            amount_by_cat[key] = expense.amount

    return amount_by_cat

def sum_expenses(expenses: list[Expense]):
    global total_exp, gnrl_exp, grcry_exp

    total_exp, gnrl_exp, grcry_exp = 0, 0, 0

    for expense in expenses:
        total_exp += expense.amount

        if expense.category.lower() == "grocery":
            grcry_exp += expense.amount
        else:
            gnrl_exp += expense.amount

def get_daily_expenses(expenses: list[Expense]):
    daily_expenses = [[] for _ in range(31)]
    
    for expense in expenses:
        daily_expenses[expense.day - 1].append(expense.get_expf())

    return daily_expenses

def print_amount_by_cat(amount_by_cat: dict):
    print("Monthly expenses by category:")
    for key, amount in amount_by_cat.items():
        percentage = (amount / total_budget) * 100
        print(f"    {key}:   \t${amount:.2f}    {percentage:.2f}%")

def print_remaining_budget():
    global total_budget, total_exp, gnrl_budget, gnrl_exp, grcry_budget, grcry_exp

    print(f"\n${total_budget - total_exp} of ${total_budget} total budget remaining")
    print(f"    ${gnrl_budget - gnrl_exp} of ${gnrl_budget} general budget remaining")
    print(f"    ${grcry_budget - grcry_exp} of ${grcry_budget} grocery budget remaining")

def print_daily_expenses(daily_expenses: list[Expense]):
    for i in range(len(daily_expenses)):
            for exp in daily_expenses[i]:
                print(exp)

def get_menu_summary():
    flush_terminal()

    expenses = get_cur_expenses()
    amount_by_cat = get_amount_by_cat(expenses)
    sum_expenses(expenses)

    print(f"Expense Tracker- Month of {months[cur_month - 1]}\n--------------------------------------\n")

    if len(expenses) > 0:
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show at this time.")

    print_remaining_budget() 

def get_month_summary():
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

def print_monthly_exp_summary(expenses: list[Expense], months_index, year: int, reached_current: bool):
    global total_budget, total_exp, gnrl_budget, gnrl_exp, grcry_budget, grcry_exp, months

    amount_by_cat = get_amount_by_cat(expenses)
    daily_expenses = get_daily_expenses(expenses)
    sum_expenses(expenses)

    print(f"Summary for {months[months_index]}, {year}")
    print(f"--------------------------------")

    if len(expenses) > 0:
        print_daily_expenses(daily_expenses)
        print("\n")
        print_amount_by_cat(amount_by_cat)
    else:
        print("No expenses to show for this month.")

    print(f"\nYou spent ${total_exp} of ${total_budget} total budget in {months[months_index]}, {year}")
    print(f"    You spent ${gnrl_exp} of ${gnrl_budget} general budget in {months[months_index]}, {year}")
    print(f"    You spent ${grcry_exp} of ${grcry_budget} grocery budget in {months[months_index]}, {year}")

    if not reached_current:
        print("\n\n\n\n\n")

def get_alltime_summary():
    global cur_month, cur_year
    expenses = get_all_expenses()
    reached_current = False
    months_index = 0
    cur_month_index = cur_month - 1

    flush_terminal()
    
    if len(expenses) > 0:
        for year_key in expenses.keys():
            months_index = 0
            for month_list in expenses[year_key]:
                if (int(year_key) == cur_year and months_index == cur_month_index):
                    reached_current = True
                    break

                print_monthly_exp_summary(month_list, months_index, year=int(year_key), reached_current=reached_current)
                months_index += 1

            if reached_current:
                print_monthly_exp_summary(month_list=month_list, months_index=months_index, year=int(year_key), reached_current=reached_current)
                sum_expenses(month_list)
                break

    else:
        print("No expenses to show at this time.")

    print("\n'x' to go back")
    while input("") != 'x':
        continue

    flush_terminal()

def undo_last_expense():
    global most_recent_exp_path

    with open(most_recent_exp_path, 'r') as file:
        lines = file.readlines()  

        file.close()

    if lines:  
        lines = lines[:-1]  

        with open(most_recent_exp_path, 'w') as file:
            file.writelines(lines) 

            file.close()

def close():
    flush_terminal()
    exit()

def init():
    global cur_month, cur_day, cur_year

    cur_month = datetime.datetime.now().month
    cur_day = datetime.datetime.now().day
    cur_year = datetime.datetime.now().year

    with open(f"expenses/expenses{cur_year}.csv", 'a') as file:
        pass

    get_budgets()

def cli_loop():
    while True:
        flush_terminal()

        get_menu_summary()

        action = input(f"\n\nx: quit | e: new expense | u: undo most recent expense | s: expanded month summary | s -a: all-time summary\nWhat would you like to do:\n")

        if action.strip().lower() == 'x':
            close()
        elif action.strip().lower() == 'e':
            exp = get_user_expense()
            save_expense(exp)
        elif action.strip().lower() == 'u':
            undo_last_expense()
        elif action.lower() == "s":
            get_month_summary()
        elif action == "s -a":
            get_alltime_summary()

def main():
    init()
    cli_loop()

if __name__ == "__main__":
    main()