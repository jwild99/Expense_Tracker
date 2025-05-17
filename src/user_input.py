from data import expense_categories as expCat
from utils import infrastructure as tUtils
from data import time_vals as time

def get_user_category() -> int:
    """ Gets user input for the category of an item """

    while True:
        print("Select a category:")
        for i, category_name in enumerate(expCat.categories):
            print(f"    {i + 1}. {category_name}")

        val_range = f"[1 - {len(expCat.categories)}]"

        try:
            cat_num = int(input(f"Enter category number {val_range}: ")) - 1

            if cat_num not in range(0, len(expCat.categories)):
                raise Exception

            tUtils.flush_terminal()
            break
        except Exception:
            tUtils.flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid category number entered. Please enter a value between 1 and {len(expCat.categories)}.\n\n")

    return cat_num

def get_user_day(month: int) -> int:
    """ Gets user input for day the item occurred """

    while True:
        try:
            inp = input("Enter a day number [1-31]- leave blank for current day: ")

            if inp == '':
                day = time.cur_day
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
                month = time.cur_month
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
    while True:
        try:
            inp = input("Enter a year number- leave blank for current year: ")

            if inp == '':
                year = time.cur_year
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
