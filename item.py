class Item:

    def __init__(self, name: str, category: str, amount: float, month: int, day: int, year: int, cd: str, tru_exp: str, itm_type: str) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.month = month
        self.day = day
        self.year = year
        self.cd = cd
        self.tru_exp = tru_exp
        self.itm_type = itm_type

    
    def get_exp(self):
        return f"'{self.name}' | {self.category} | {self.amount} | {self.month}/{self.day}/{self.year} | {self.tru_exp} | {self.type}"
    
    def get_dep(self):
        return f"'{self.name}' | {self.amount} | {self.month}/{self.day}/{self.year} | {self.type}"

    def get_expf(self):
        return f"{self.month}/{self.day}/{self.year}       \t{self.category}       \t${self.amount}       \t{self.cd}       \t'{self.name}'"