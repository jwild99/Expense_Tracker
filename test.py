from expense import Expense
import os

def get_all_expenses() -> list[Expense]:
    exp_file_dir = f"expenses/"
    file_count = sum(1 for filename in os.listdir(exp_file_dir) if os.path.isfile(os.path.join(exp_file_dir, filename)))

    # expenses: list[Expense] = []
    expenses_dict = {}

    for filepath in os.listdir(exp_file_dir):
        with open(f"expenses/{filepath}", 'r') as file:
            lines = file.readlines()

            for line in lines:
                exp_name, exp_cat, exp_amount, exp_month, exp_day, exp_year = line.strip().split(',')

                key = exp_year
                if key in expenses_dict:
                    expenses_dict[key].append(Expense(name=exp_name, category=exp_cat, 
                            amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year)))
                else:
                    expenses_dict[key] = []
                    expenses_dict[key].append(Expense(name=exp_name, category=exp_cat, 
                            amount=float(exp_amount), month=int(exp_month), day=int(exp_day), year=int(exp_year)))
            
            file.close()            
    
    return expenses_dict

test = get_all_expenses()
for year in test:
    for expense in year:
        print(expense.get_expf())