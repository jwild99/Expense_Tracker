class Expense:

    def __init__(self, name: str, category: str, amount: float, month: int, day: int) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.month = month
        self.day = day

    
    def get_exp(self):
        return f"'{self.name}' | {self.category} | {self.amount} | {self.month}/{self.day}"
    
    def get_exp_sum(self):
        return f"{self.month}/{self.day} \t{self.category}       \t{self.amount} \t\t'{self.name}'"