class Expense_Summary:

    def __init__(self):
        self.total_budget = 0
        self.gnrl_budget = 0
        self.grcry_budget = 0
        self.amount_by_cat = {}
        self.daily_expenses = []

    def set_total_budget(self, val: float):
        self.total_budget = val

    def set_gnrl_budget(self, val: float):
        self.gnrl_budget = val 

    def set_grcry_budget(self, val: int):
        self.grcry_budget = val 

    def set_amnt_by_cat(self, val):
        self.amount_by_cat = val

    def set_daily_expenses(self, val):
        self.daily_expenses = val