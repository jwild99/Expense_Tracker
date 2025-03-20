class Item:

    def __init__(self, name: str, category: str, amount: float, month: int, day: int, year: int, cd: str) -> None:
        self.name = name                    # Name of Item
        self.category = category            # Category of Item
        self.amount = amount                # Item Amount
        self.month = month                  # Month the Item occurred
        self.day = day                      # Day the Item occurred
        self.year = year                    # Year the Item occurred
        self.cd = cd                        # Is the Item a Credit Card expense or Debit Card Expense

    def get_exp(self):
        return f"'{self.name}' | {self.category} | {self.amount:.2f} | {self.month}/{self.day}/{self.year}"

    def get_dep(self):
        return f"'{self.name}' | {self.amount:.2f} | {self.month}/{self.day}/{self.year}"

    def get_expf(self):
        if self.cd == 'c':
            return f"{self.month}/{self.day}/{self.year}        \t{self.category}       \t${self.amount:.2f}       \tCredit    \t'{self.name}'"
        if self.cd == 'd':
            return f"{self.month}/{self.day}/{self.year}        \t{self.category}       \t${self.amount:.2f}       \tDebit    \t'{self.name}'"
