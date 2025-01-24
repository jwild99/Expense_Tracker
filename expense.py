class Expense:

    def __init__(self, name: str, category: str, amount: float, month: int, day: int, year: int) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.month = month
        self.day = day
        self.year = year

    
    def get_exp(self):
        return f"'{self.name}' | {self.category} | {self.amount} | {self.month}/{self.day}/{self.year}"
    
    def get_expf(self):
        return f"{self.month}/{self.day}/{self.year} \t{self.category}       \t{self.amount} \t\t'{self.name}'"