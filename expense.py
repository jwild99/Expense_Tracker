class Expense:

    def __init__(self, name: str, category: str, amount: float, month: int) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.month = month

    
    def get_exp(self):
        return f"'{self.name}' | {self.category} | {self.amount}"