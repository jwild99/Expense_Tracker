from data import vals as vals
from utils import systemUtils as tUtils
from data import timeVals as time

def getCategory() -> int:
    while True:
        print("Select a category:")
        i = 1
        for catName in vals.budgets.keys():
            if str.lower(catName) == "total":
                continue
            print(f"    {i}. {catName}")
            i += 1

        valRange = f"[1 - {i - 1}]"

        try:
            catNum = int(input(f"Enter category number {valRange}: ")) - 1

            if catNum not in range(0, len(vals.budgets.keys())):
                raise Exception

            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print(f"\n\n~~ERROR~~\nInvalid category number entered. Please enter a value between 1 and {len(vals.budgets.keys())}.\n\n")

    return catNum

def getDay(month: int) -> int:
    while True:
        try:
            inp = input("Enter a day number [1-31]- leave blank for current day: ")

            if inp == '':
                day = time.day
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


            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print(f"\n\n~~ERROR~~\nInvalid date number entered. Please enter a value between 1 and 31 and make sure the value is valid for the month.\n\n")

    return day

def getMonth() -> int:
    while True:
        try:
            inp = input("Enter a month number [1-12]- leave blank for current month: ")

            if inp == '':
                month = time.month
            else:
                month = int(inp)

            if month not in range(1, 13):
                raise Exception

            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print(f"\n\n~~ERROR~~\nInvalid month number entered. Please enter a value between 1 and 12.\n\n")

    return month

def getYear() -> int:
    while True:
        try:
            inp = input("Enter a year number- leave blank for current year: ")

            if inp == '':
                year = time.year
            else:
                year = int(inp)

            if year < 1:
                raise Exception

            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print(f"\n\n~~ERROR~~\nInvalid year number entered. Please enter a value between 1 and 12.\n\n")

    return year

def getAmount() -> float:
    while True:
        try:
            amount = float(input("Enter amount: "))
            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print("\n\n~~ERROR~~\nInvalid expense amount entered! Please try again.\n\n")

    return amount

def getCd() -> str:
    while True:
        try:
            cd = input("Is this a credit or debit expense? [c/d]: ").strip().lower()

            if cd != 'c' and cd != 'd':
                raise Exception

            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print(f"\n\n~~ERROR~~\nInvalid credit/debit value entered. Please enter either 'c' or 'd'.\n\n")

    return cd

def getName() -> str:
    while True:
        try:
            name = input("Enter expense name: ").strip()

            if name.find(",") != -1:
                raise Exception

            tUtils.flushTerminal()
            break
        except Exception:
            tUtils.flushTerminal()
            print(f"\n\n~~ERROR~~\nInvalid name value entered. Make sure there are no commas!\n\n")

    return name
