import os 
import platform
import datetime
import sys

from expense import Expense
from expense_summary import Expense_Summary

exp_categories = [
    "Food",
    "Home",
    "Grocery",
    "Work",
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
    "september",
    "October",
    "November",
    "December"
]

exp_file_path = "expenses.csv"
info_file_path = "info.txt"
cur_month = None
cur_day = None

total_budget = None
gnrl_budget = None
grcry_budget = None

total_exp = None
gnrl_exp = None 
grcry_exp = None

# First line formatting in csv:
# total budget, misc budget, grocery budget, total spending this month, month number


def flush_terminal():
    if platform.system() == 'Windows':
        os.system('cls')  
    else:
        os.system('clear') 

    sys.stdout.flush()

def get_user_expense():
    global exp_categories, info_file_path, cur_month, cur_day

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
            
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid date number entered. Please enter a value between 1 and 31.\n\n")

    new_exp = Expense(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=exp_month, day=exp_day)
    flush_terminal()
    return new_exp

def save_expense(exp: Expense):
    global exp_file_path

    with open(exp_file_path, "a") as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day}\n")

def get_amount_by_cat():
    pass

def get_all_expenses() -> list[Expense]:
    expenses: list[Expense] = []

    with open(exp_file_path, 'r') as file:
        lines = file.readlines()

        if len(lines) > 0:
            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day = line.strip().split(',')

                expenses.append(Expense(name=exp_name, category=exp_cat, 
                            amount=float(exp_amount), month=int(exp_month), day=int(exp_day)))
                
    return expenses

def get_cur_expenses() -> list[Expense]:
    expenses: list[Expense] = []

    with open(exp_file_path, 'r') as file:
        lines = file.readlines()

        if len(lines) > 0:
            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day = line.strip().split(',')

                if int(exp_month) == cur_month:
                    expenses.append(Expense(name=exp_name, category=exp_cat, 
                                amount=float(exp_amount), month=int(exp_month), day=int(exp_day)))
                    
    return expenses

def get_budgets(sum: Expense_Summary):
    global info_file_path, total_budget, grcry_budget, gnrl_budget

    with open(info_file_path, 'r') as file:
        lines = file.readlines()

        sum.set_total_budget(float(lines[0]))
        sum.set_gnrl_budget(float(lines[1]))
        sum.set_grcry_budget(float(lines[2]))

def sort_expenses(expenses: list[Expense]):
    global total_exp, gnrl_exp, grcry_exp

    amount_by_cat = {}

    for expense in expenses:
        key = expense.category
        if key in amount_by_cat:
            amount_by_cat[key] += expense.amount
        else:
            amount_by_cat[key] = expense.amount

        total_exp += expense.amount

        if expense.category.lower() == "grocery":
            grcry_exp_exp += expense.amount
        else:
            gnrl_exp_exp += expense.amount
            
    return amount_by_cat

def summary():

    if len(expenses) > 0:
        print("Monthly expenses by category:")
        for key, amount in amount_by_cat.items():
            percentage = (amount / total_budget) * 100
            print(f"    {key}:   \t${amount:.2f}    {percentage:.2f}%")
    else:
        print("No expenses to show at this time.")

    print(f"\n${total_budget - total_exp} of ${total_budget} total budget remaining")
    print(f"    ${misc_budget - misc_exp} of ${misc_budget} general budget remaining")
    print(f"    ${grocery_budget - grocery_exp} of ${grocery_budget} grocery budget remaining")

def verbose_summary():
    global exp_file_path, cur_month, months

    amount_by_cat = {}
    daily_expenses = [[] for _ in range(31)]

    flush_terminal()

    total_exp = 0
    grocery_exp = 0
    misc_exp = 0

    daily_expenses[expense.day - 1].append(expense.get_exp_sum())

    flush_terminal()

    if len(expenses) > 0:
        for i in range(len(daily_expenses)):
            for exp in daily_expenses[i]:
                print(exp)

        print(f"\n\nExpenses by category for {months[cur_month - 1]}:")
        for key, amount in amount_by_cat.items():
            percentage = (amount / total_budget) * 100
            print(f"    {key}:   \t${amount:.2f}     {percentage:.2f}%")
        
    else:
        print("No expenses to show at this time.")

    print(f"\n${total_budget - total_exp} of ${total_budget} total budget remaining")
    print(f"    ${misc_budget - misc_exp} of ${misc_budget} general budget remaining")
    print(f"    ${grocery_budget - grocery_exp} of ${grocery_budget} grocery budget remaining")

    print("\n'x' to go back")

    while input("") != 'x':
        continue

def summary_handler(sum_type: str):
    flush_terminal()
    if sum_type == 's':
        verbose_summary()
    elif sum_type == 's -a':
        pass
    else:
        summary()

def init():
    global exp_file_path, info_file_path, cur_month, cur_day, months

    cur_month = datetime.datetime.now().month
    cur_day = datetime.datetime.now().day

    get_budgets()

def cli_loop():
    while True:
        flush_terminal()

        print(f"Expense Tracker- Month of {months[cur_month - 1]}\n--------------------------------------\n")

        summary_handler('.')

        action = input(f"\n\nx: quit | e: new expense | u: undo most recent expense | s: full summary | s -a: all-time summary\nWhat would you like to do:\n")

        if action.lower() == 'x':
            flush_terminal()
            exit()
        elif action.lower() == "e":
            exp = get_user_expense()
            print(f"Saving expense: [{exp.get_exp()}] to {exp_file_path}")
            save_expense(exp)
        elif action.lower() == "s":
            summary_handler('s')
        elif action == "s -a":
            summary_handler('sa')
        elif action == "u":
            pass

def main():
    global exp_file_path, info_file_path, cur_month, cur_day, months

    init()
    cli_loop()

if __name__ == "__main__":
    main()