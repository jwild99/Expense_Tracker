import os 
import platform
import datetime
import sys
import json 

from item import Item

exp_categories = [
    "Food",
    "Home",
    "Laundry",
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

acc_blnce = 0

recent_acc_blnce = 0
recent_cc_blnce = 0

# TERMINAL UTILS
################################################################################################################################

def flush_terminal() -> None:
    """ Flushes print buffers and clears the terminal """

    print("\n" * 500)
    if platform.system() == 'Windows':
        os.system('cls')  
    else:
        os.system('clear') 
    sys.stdout.flush()

def close() -> None:
    """ Closes the app """

    flush_terminal()
    exit()

def spacing(lines) -> None:
    """ Prints spacing the given number of times """

    print("\n" * (lines - 1))

def lines(num) -> None:
        """ Prints a '-' character the given number of times """

        print("-"*num)

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
            
            flush_terminal()
            break
        except Exception:
            flush_terminal()
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

            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
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
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
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
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid year number entered. Please enter a value between 1 and 12.\n\n") 

    return year

def get_user_amount() -> float:
    """ Gets user input for the amount of the item """

    while True:
        try:
            amount = float(input("Enter amount: "))
            flush_terminal()
            break
        except Exception:
            flush_terminal()
            print("\n\n~~ERROR~~\nInvalid expense amount entered! Please try again.\n\n")

    return amount

def get_user_cd() -> str:
    """ Gets user input for whether or not the expense is a debit or credit card expense """

    while True:
        try:
            cd = input("Is this a credit or debit expense? [c/d]: ").strip().lower()

            if cd != 'c' and cd != 'd':
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid credit/debit value entered. Please enter either 'c' or 'd'.\n\n")

    return cd

def get_user_true_exp() -> str:
    """ Gets user input for whether or not the expense is a 'true expense' meaning 
    that the user will not be reimbursed for it """

    while True:
        try:
            tru_exp = input("Is this a 'true expense'? [y/n] (leave blank for 'y'): ").strip().lower()

            if tru_exp == '':
                tru_exp = 'y'

            if tru_exp != 'y' and tru_exp != 'n':
                raise Exception
            
            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid 'true expense' value entered. Please enter either 'y' or 'n'.\n\n")

    return tru_exp

def get_user_name() -> str:
    """ Gets a new item name from the user and ensures it is valid with no commas """

    while True:
        try:
            name = input("Enter expense name: ").strip()

            if name.find(",") != -1:
                raise Exception

            flush_terminal()
            break 
        except Exception:
            flush_terminal()
            print(f"\n\n~~ERROR~~\nInvalid name value entered. Make sure there are no commas!\n\n")

    return name

# GETTING ITEMS FROM USER
################################################################################################################################

def get_user_expense() -> type[Item]:
    """ Collects from the user the necessary info to create a new expense and creates one """

    flush_terminal()
    exp_name = get_user_name()
    exp_amount = get_user_amount()
    cat_num = get_user_category()
    exp_month = get_user_month()
    exp_day = get_user_day(month=exp_month)
    exp_year = get_user_year()
    exp_cd = get_user_cd()
    tru_exp = get_user_true_exp()

    if exp_cd.strip().lower() == 'd':
        exp_b_after = acc_blnce - exp_amount
    else:
        exp_b_after = acc_blnce

    new_exp = Item(name=exp_name, category=exp_categories[cat_num], amount=exp_amount, month=exp_month, 
                      day=exp_day, year=exp_year, cd=exp_cd, tru_exp=tru_exp, itm_type="EXP", b_after=exp_b_after)
    flush_terminal()
    return new_exp

def get_user_deposit() -> type[Item]:
    """ Collects from user the necessary info to create a new deposit and creates one """

    flush_terminal()
    dep_name = get_user_name()
    dep_amount = get_user_amount()
    dep_month = get_user_month()
    dep_day = get_user_day(month=dep_month)
    dep_year = get_user_year()
    dep_b_after = acc_blnce + dep_amount
        
    new_dep = Item(name=dep_name, category="Misc", amount=dep_amount, month=dep_month, 
                      day=dep_day, year=dep_year, cd='d', tru_exp="n", itm_type="DEP", b_after=dep_b_after)
    flush_terminal()
    return new_dep

def get_user_cc_payment() -> type[Item]:
    """ Collects info needed to create a new Payment type expense from the user and creates one """

    flush_terminal()
    pay_amount = get_user_amount()
    pay_month = get_user_month()
    pay_day = get_user_day(month=pay_month)
    pay_year = get_user_year()
    pay_b_after = acc_blnce - pay_amount
    new_pay = Item(name=f"[CREDIT CARD PAYMENT]", category="Misc", amount=pay_amount, month=pay_month, 
                      day=pay_day, year=pay_year, cd='d', tru_exp="y", itm_type="EXP", b_after=pay_b_after)
    flush_terminal()
    return new_pay

# WRITING TO CSV
################################################################################################################################

def save_expense(exp: Item) -> None:
    """ Saves a new expense to the correct CSV. Also stores the most recent file path """

    global most_recent_itm_path, menu_message

    exp_file_path = f"records/records{exp.year}.csv"
    most_recent_itm_path = f"records/records{exp.year}.csv"

    with open(exp_file_path, 'a') as file:
        file.write(f"{exp.name},{exp.category},{exp.amount},{exp.month},{exp.day},{exp.year},{exp.cd},{exp.tru_exp},{exp.itm_type},{exp.b_after}\n")

        file.close()

    update_balances(exp)

    menu_message = f"Saved expense: [{exp.get_exp()}] to {exp_file_path}"

def save_deposit(dep: Item) -> None:
    """ Saves a new deposit to the correct CSV. Also stored the most recent file path """

    global most_recent_itm_path, menu_message

    dep_file_path = f"records/records{dep.year}.csv"
    most_recent_itm_path = f"records/records{dep.year}.csv"

    with open(dep_file_path, "a") as file:
        file.write(f"{dep.name},{dep.category},{dep.amount},{dep.month},{dep.day},{dep.year},{dep.cd},{dep.tru_exp},{dep.itm_type},{dep.b_after}\n")

        file.close()

    update_balances(dep)

    menu_message = f"Saved deposit: [{dep.get_dep()}] to {dep_file_path}"

# WRITING TO OR READING FROM INFO.JSON
################################################################################################################################

def update_balances(itm: Item) -> None:
    """ Updates the account and credit card balances as expenses, deposits, and CC payments are entered """

    global recent_acc_blnce, recent_cc_blnce

    with open(info_file_path, 'r') as file:
        data = json.load(file)
        file.close

    # item is an expense to debit card/checking account
    if itm.itm_type.strip().lower() == "exp" and itm.cd.strip().lower() == 'd' and itm.name != "[CREDIT CARD PAYMENT]":
        recent_acc_blnce = data["checking_balance"]
        data["checking_balance"] -= itm.amount

    # item is a deposit to debit card/checking account
    elif itm.itm_type.strip().lower() == "dep" and itm.cd.strip().lower() == 'd' and itm.name != "[CREDIT CARD PAYMENT]":
        recent_acc_blnce = data["checking_balance"]
        data["checking_balance"] += itm.amount

    # item is an expense to credit card/credit card balance
    elif itm.itm_type.strip().lower() == "exp" and itm.cd.strip().lower() == 'c' and itm.name != "[CREDIT CARD PAYMENT]":
        recent_cc_blnce = data["cc_balance"]
        data["cc_balance"] += itm.amount

    # item is an expense to checking account specifically a credit card payment
    elif itm.itm_type.strip().lower() == "exp" and itm.cd.strip().lower() == 'd' and itm.name == "[CREDIT CARD PAYMENT]":
        recent_cc_blnce = data["cc_balance"]
        recent_acc_blnce = data["checking_balance"]
        data["cc_balance"] -= itm.amount
        data["checking_balance"] -= itm.amount

    with open(info_file_path, "w") as file:
        json.dump(data, file, indent=4)
        file.close()

def get_budgets() -> None:
    """ Reads in the budget values from info.json and stores them as global variables """

    global info_file_path, total_budget, grcry_budget, gnrl_budget

    with open(info_file_path, 'r') as file:
        data = json.load(file)

        total_budget = float(data["total_budget"])
        gnrl_budget = float(data["general_budget"])
        grcry_budget = float(data["grocery_budget"])

        file.close()

def set_acc_blnce() -> None:
    """ Sets a global variable to whatever the currently stored account balance value is- for processing purposes """

    global acc_blnce

    with open(info_file_path, 'r') as file:
        data = json.load(file)
        acc_blnce = data["checking_balance"]
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
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd, tru_exp, itm_type, b_after = line.strip().split(',')

                if tru_exp.strip().lower() == 'y' and itm_type.strip().lower() == 'exp' and exp_name != "[CREDIT CARD PAYMENT]":
                    expense = Item(name=exp_name, category=exp_cat, 
                                amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd, tru_exp=tru_exp, itm_type=itm_type, b_after=float(b_after))

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
            exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year, exp_cd, tru_exp, itm_type, b_after = line.strip().split(',')

            if int(exp_month) == cur_month and int(exp_year) == cur_year and tru_exp.strip().lower() == 'y' and itm_type.strip().lower() == 'exp' and exp_name != "[CREDIT CARD PAYMENT]":
                expenses.append(Item(name=exp_name, category=exp_cat, amount=float(exp_amount), 
                                month=int(exp_month), day=int(exp_day), year=int(exp_year), cd=exp_cd, tru_exp=tru_exp, itm_type=itm_type, b_after=float(b_after)))
                    
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

    print(f"\n${total_budget - total_exp:.2f} \tof total budget remaining   \t[${total_budget:.2f}]")
    print(f"${gnrl_budget - gnrl_exp:.2f} \tof general budget remaining \t[${gnrl_budget:.2f}]")
    print(f"${grcry_budget - grcry_exp:.2f} \tof grocery budget remaining \t[${grcry_budget:.2f}]")

def print_daily_expenses(daily_expenses: list[Item]) -> None:
    """ Displays a day-by-day summary of expenses """

    print("Date \t\t\tCategory \tAmount \t\tCard Type \tBalance After   Name\n")
    for i in range(len(daily_expenses)):
        for exp in daily_expenses[i]:
            print(exp)

def print_balances() -> None:
    """ Reads in the current account and credit card balances and displays them """

    with open(info_file_path, 'r') as file:
        data = json.load(file)
        print(f"Checking Account Balance: {data['checking_balance']}")
        print(f"Credit Card Balance: {data['cc_balance']}")

        file.close()

def print_monthly_exp_summary(expenses: list[Item], months_index: int, year: int, reached_current: bool) -> None:
    """ Displays a summary of the given month to the console """

    if len(expenses) <= 0:
        return

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


    print(f"\n\n${total_exp:.2f}  \tof ${total_budget:.2f} total   budget in {months[months_index]}, {year} \t[{total_diff}]")
    print(f"${gnrl_exp:.2f}  \tof ${gnrl_budget:.2f} general budget in {months[months_index]}, {year} \t[{gnrl_diff}]")
    print(f"${grcry_exp:.2f}  \tof ${grcry_budget:.2f} grocery budget in {months[months_index]}, {year} \t[{grcy_diff}]")
    
    if reached_current:
        print("\n")
    else:
        print("\n\n\n\n\n")

# EXPENSE REPORT ACTIONS
################################################################################################################################

def get_full_summary() -> None:
    """ Gets a more verbose summary of the current months expenses than the one from the main menu """

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
    while input("").strip().lower() != 'x':
        continue

def get_alltime_summary() -> None:
    """ Gets an all-time version of the full month summary """

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
    while input("").strip().lower() != 'x':
        continue

    flush_terminal()

# MISC USER ACTIONS
################################################################################################################################

def help() -> None:
    """ Prints out a list of commands for the app. May expand later to other help stuff """

    flush_terminal()

    print("Help Menu")
    print('-'*30)

    print("\nCommand List:")
    print("'x'     | quit or go back")
    print("'e'     | add a new expense")
    print("'d'     | add a new deposit")
    print("'c'     | add a new credit card payment")
    print("'u'     | undo most recently added expense or deposit")
    print("'o -ab' | overwrite currently stored account balance")
    print("'o -cb' | overwrite currently stored credit card balance")
    print("'s'     | full expense summary of current month")
    print("'s -a'  | all-time monthly summary of expenses")

    print("\n'x' to go back")
    while input("").strip().lower() != 'x':
        continue

    flush_terminal()

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
    
    flush_terminal()
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

            itm_name, itm_cat, itm_amount, itm_month, itm_day, itm_year, itm_cd, itm_tru_exp, itm_type, b_after = last_line.strip().split(',')
            item = Item(name=itm_name, category=itm_cat, amount=float(itm_amount), month=int(itm_month), day=int(itm_day), 
                        year=int(itm_year), cd=itm_cd, tru_exp=itm_tru_exp, itm_type=itm_type, b_after=float(b_after))

            with open(most_recent_itm_path, 'w') as file:
                file.writelines(lines) 
                file.close()
        
        # Make updates to balances to reflect undo
        with open(info_file_path, 'r') as file:
            data = json.load(file)
            if itm_cd.strip().lower() == 'd':
                data["checking_balance"] = recent_acc_blnce
            elif itm_cd.strip().lower() == 'c':
                data["cc_balance"] = recent_cc_blnce
            file.close

        with open(info_file_path, "w") as file:
            json.dump(data, file, indent=4)

        menu_message = f"Removed {item.get_dep()} from {most_recent_itm_path}"

        

def overwrite_acc_balance() -> None:
    """ Overwrites the stored account balance. Checks for confirmation first as 
    this is an irreversible action. Writes a new, blank expense to the CSV to 
    indicate that the balance was updated- for all-time summary purposes """

    global menu_message

    flush_terminal()
    message = "~~WARNING~~\nAre you sure you wish to overwrite the stored account balance?\nThis cannot be undone! [y/n]: "
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
        with open(info_file_path, 'r') as file:
            data = json.load(file)
            old_bal = data["checking_balance"]
            file.close

        while True:
            try:
                new_bal = float(input(f"The current balance is {data['checking_balance']}. What would you like to change it to: "))
                if new_bal < 0:
                    raise Exception
                break
            except Exception:
                flush_terminal()
                print("Invalid balance amount entered! Please try again.")

        data["checking_balance"] = new_bal
        fix_exp = Item(name=f"FIXED ACC BALANCE (NOT REAL EXPENSE)", category="Misc", amount=0, month=cur_month, 
                      day=cur_day, year=cur_year, cd='d', tru_exp="y", itm_type="EXP", b_after=new_bal)
        save_expense(fix_exp)

        with open(info_file_path, "w") as file:
            json.dump(data, file, indent=4)
        menu_message = f"Changed account balance from {old_bal} to {new_bal}."
        
def overwrite_cc_balance() -> None:
    """ Allows the user to overwrite the stored credit card balance. Checks for confirmation 
    before doing so since this is an irreversible action"""

    global menu_message

    flush_terminal()
    message = "~~WARNING~~\nAre you sure you wish to overwrite the stored credit card balance?\nThis cannot be undone! [y/n]: "
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
        with open(info_file_path, 'r') as file:
            data = json.load(file)
            old_bal = data["cc_balance"]
            file.close

        while True:
            try:
                new_bal = float(input(f"The current balance is {data['cc_balance']}. What would you like to change it to: "))
                if new_bal < 0:
                    raise Exception
                break
            except Exception:
                flush_terminal()
                print("Invalid balance amount entered! Please try again.")

        data["cc_balance"] = new_bal
        with open(info_file_path, "w") as file:
            json.dump(data, file, indent=4)
        menu_message = f"Changed credit card balance from {old_bal} to {new_bal}."

# CLI UTILS AND MAIN MENU LOOP
################################################################################################################################

def init() -> None:
    """ Initializes current data and makes sure there is a csv file created for the current year. 
    Also gets the current budgets from info.json """

    global cur_month, cur_day, cur_year

    cur_month = datetime.datetime.now().month
    cur_day = datetime.datetime.now().day
    cur_year = datetime.datetime.now().year

    with open(f"records/records{cur_year}.csv", 'a') as file:
        pass

    get_budgets()

def get_menu_summary() -> None:
    """ Gets and displays the main menu summary which includes expenses 
    by category, account balances, and remaining budget """

    flush_terminal()
    expenses = get_cur_expenses()
    amount_by_cat = get_amount_by_cat(expenses)
    sum_expenses(expenses)

    print(f"Expense Tracker [{months[cur_month - 1]}, {cur_year}]")
    if len(menu_message) > 0:
        print(menu_message)
    lines(60)

    print_balances()
    spacing(1)

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
        close()
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
    elif action == 'd':
        menu_message = ""
        dep = get_user_deposit()
        save_deposit(dep)
    elif action == 'h':
        menu_message = ""
        help()
    elif action == 'c':
        menu_message = ""
        pay = get_user_cc_payment()
        save_expense(pay)
    elif action == "o -ab":
        menu_message = ""
        overwrite_acc_balance()
    elif action == "o -cb":
        menu_message = ""
        overwrite_cc_balance()

def cli_loop() -> None:
    """ Loop that runs until user quits- displays main menu and gets user actions """

    while True:
        flush_terminal()
        set_acc_blnce()
        get_menu_summary()
        get_user_action()   

# EXECUTION
################################################################################################################################

def main() -> None:
    """ Main Function that begins app execution """

    init()
    cli_loop()

if __name__ == "__main__":
    main()