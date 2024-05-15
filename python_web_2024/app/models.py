class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Account:
    def __init__(self, id, user_id, balance):
        self.id = id
        self.user_id = user_id
        self.balance = balance

class Transaction:
    def __init__(self, id, account_from, account_to, amount):
        self.id = id
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount
