class Item:

    def __init__(self, name: str, category: str, amount: float, month: int, day: int, year: int, cd: str, tru_exp: str, itm_type: str, b_after: float) -> None:
        self.name = name                    # Name of Item
        self.category = category            # Category of Item- somtimes won't matter for things like credit card payments and deposits
        self.amount = amount                # Item Amount
        self.month = month                  # Month the Item occurred
        self.day = day                      # Day the Item occurred
        self.year = year                    # Year the Item occurred
        self.cd = cd                        # Is the Item a Credit Card expense or Debit Card Expense
        self.tru_exp = tru_exp              # Is the Item a 'True Expense' meaning that I carry the expense and I'm not being reimbursed for the expense
        self.itm_type = itm_type            # Type of Item- 'DEP' = Deposit, 'EXP' = Expense
        self.b_after = b_after              # Account Balance after the addition of the Item to the ledger

    
    def get_exp(self):
        return f"'{self.name}' | {self.category} | {self.amount:.2f} | {self.month}/{self.day}/{self.year} | {self.tru_exp} | {self.itm_type}"
    
    def get_dep(self):
        return f"'{self.name}' | {self.amount:.2f} | {self.month}/{self.day}/{self.year} | {self.itm_type}"

    def get_expf(self):
        if self.cd == 'c':
            return f"{self.month}/{self.day}/{self.year}       \t{self.category}       \t${self.amount:.2f}       \tCredit       \t${self.b_after:.2f}    \t'{self.name}'"
        if self.cd == 'd':
            return f"{self.month}/{self.day}/{self.year}       \t{self.category}       \t${self.amount:.2f}       \tDebit       \t${self.b_after:.2f}    \t'{self.name}'"