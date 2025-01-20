import os 
import platform
import datetime

from expense import Expense

exp_categories = [
    "Food",
    "Home",
    "Work",
    "Fun",
    "Misc"
]

amount_by_cat = {}
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

        print(f"Expense Tracker\n------------------------\n")

        summarize_expenses()

        action = input(f"\n\nx: quit | e: new expense | s: full summary | s -a: all-time summary\nWhat would you like to do:\n")

        if action == 'x':
            clear_terminal()
            exit()
        elif action == "e":
            exp = get_user_expense()

            print(f"Saving expense: [{exp.get_exp()}] to {exp_file_path}")
            save_expense(exp)
        elif action == "s":
            pass
        elif action == "s -a":
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

            if cat_num in range(1, len(exp_categories) + 1):
                new_exp = Expense(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=cur_month)
                clear_terminal()
                return new_exp
            else:
                raise Exception
        except Exception:
            clear_terminal()
            print(f"\n\n~~ERROR~~\nInvalid category number entered. Please enter a value between 1 and {len(exp_categories)}.\n\n")



def save_expense(exp: Expense):
    global exp_file_path

    with open(exp_file_path, "a") as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month}\n")


def summarize_expenses():
    global amount_by_cat, exp_file_path

    expenses: list[Expense] = []

    with open(exp_file_path, "r") as file:
        lines = file.readlines()

        if len(lines) > 0:
            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month = line.strip().split(',')

                if exp_month == cur_month:
                    expenses.append(Expense(name=exp_name, category=exp_cat, amount=float(exp_amount), month=exp_month))

    if len(expenses) > 0:
        for expense in expenses:
            key = expense.category
            
            if key in amount_by_cat:
                amount_by_cat[key] += expense.amount
            else:
                amount_by_cat[key] = expense.amount

        total_exp = sum([x.amount for x in expenses])

        print("Expenses by category:")
        for key, amount in amount_by_cat.items():
            print(f"    {key}: ${amount:.2f}")
    else:
        print("No expenses to show at this time.")

if __name__ == "__main__":
    main()