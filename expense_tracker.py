import os 
import platform
import datetime

from expense import Expense

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

# First line formatting in csv:
# total budget, misc budget, grocery budget, total spending this month, month number


def main():
    global exp_file_path, info_file_path, cur_month

    cur_month = datetime.datetime.now().month

    while True:
        clear_terminal()

        print(f"Expense Tracker- Month of {months[cur_month - 1]}\n--------------------------------------\n")

        summarize_expenses('.')

        action = input(f"\n\nx: quit | e: new expense | u: undo most recent expense | s: full summary | s -a: all-time summary\nWhat would you like to do:\n")

        if action.lower() == 'x':
            clear_terminal()
            exit()
        elif action.lower() == "e":
            exp = get_user_expense()

            print(f"Saving expense: [{exp.get_exp()}] to {exp_file_path}")
            save_expense(exp)
        elif action.lower() == "s":
            summarize_expenses('s')
        elif action == "s -a":
            summarize_expenses('sa')
        elif action == "u":
            pass


def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')  
    else:
        os.system('clear') 


def get_user_expense():
    global exp_categories, info_file_path, cur_month

    clear_terminal()

    exp_name = input("Enter expense name: ")
    clear_terminal()

    while True:
        try:
            exp_amount = float(input("Enter expense amount: "))
            clear_terminal()
            break
        except Exception:
            clear_terminal()
            print("\n\n~~ERROR~~\nInvalid expense amount entered! Please try again.\n\n")

    while True:
        print("Select a category:")
        for i, category_name in enumerate(exp_categories):
            print(f"    {i + 1}. {category_name}")
        
        val_range = f"[1 - {len(exp_categories)}]"

        try:
            cat_num = int(input(f"Enter category number {val_range}: ")) - 1

            if cat_num not in range(1, len(exp_categories) + 1):
                raise Exception
            
            clear_terminal()
            break
        except Exception:
            clear_terminal()
            print(f"\n\n~~ERROR~~\nInvalid category number entered. Please enter a value between 1 and {len(exp_categories)}.\n\n")

    while True:
        try:
            inp = input("Enter a month number [1-12]- leave blank for current month: ")

            if inp == '':
                exp_month = cur_month
            else:
                exp_month - int(inp)

            if exp_month not in range(1, 13):
                raise Exception
            
            break 
        except Exception:
            clear_terminal()
            print(f"\n\n~~ERROR~~\nInvalid month number entered. Please enter a value between 1 and 12.\n\n")

    new_exp = Expense(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=exp_month)
    clear_terminal()
    return new_exp


def save_expense(exp: Expense):
    global exp_file_path

    with open(exp_file_path, "a") as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month}\n")


def summarize_expenses(type: str):
    global exp_file_path

    amount_by_cat = {}
    expenses: list[Expense] = []

    with open(exp_file_path, 'r') as file:
        lines = file.readlines()

        if len(lines) > 0:
            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month = line.strip().split(',')

                expenses.append(Expense(name=exp_name, category=exp_cat, amount=float(exp_amount), month=int(exp_month)))

    with open(info_file_path, 'r') as file:
        lines = file.readlines()

        total_budget = float(lines[0])
        misc_budget = float(lines[1])
        grocery_budget = float(lines[2])

    total_exp = 0
    grocery_exp = 0
    misc_exp = 0

    for expense in expenses:
        key = expense.category
        if key in amount_by_cat:
            amount_by_cat[key] += expense.amount
        else:
            amount_by_cat[key] = expense.amount

        total_exp += expense.amount

        if expense.category.lower() == "grocery":
            grocery_exp += expense.amount
        else:
            misc_exp += expense.amount

    if type.lower() == 's':
        clear_terminal()

        if len(expenses) > 0:
            print("Monthly expenses:")
            for expense in expenses:
                print(f"    {expense.name} \t\t\t{expense.category} \t\t{expense.amount}")
        else:
            print("No expenses to show at this time.")

    elif type.lower() == 'sa':
        pass

    else:
        if len(expenses) > 0:
            print("Monthly expenses by category:")
            for key, amount in amount_by_cat.items():
                print(f"    {key}: ${amount:.2f}")
        else:
            print("No expenses to show at this time.")

        print(f"\n${total_budget - total_exp} of ${total_budget} total budget remaining")
        print(f"    ${misc_budget - misc_exp} of ${misc_budget} general budget remaining")
        print(f"    ${grocery_budget - grocery_exp} of ${grocery_budget} grocery budget remaining")


    

if __name__ == "__main__":
    main()