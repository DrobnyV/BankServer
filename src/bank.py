from src.db import Connection


class Account:
    def __init__(self, account_number,bank_code,balance =0):
        self.balance = balance
        self.account_number = account_number
        self.bank_code = bank_code

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def get_balance(self):
        return self.balance

    @staticmethod
    def create_account(bank_code):
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT IFNULL(MAX(account_number), 9999) FROM accounts WHERE bank_code = ?",
            (bank_code,)
        )
        max_account_number = cursor.fetchone()[0]
        next_account_number = max_account_number + 1
        if next_account_number > 99999:
            conn.close()
            raise ValueError(f"Cannot create account: account_number exceeds 99999 for bank_code {bank_code}.")
        cursor.execute(
            "INSERT INTO accounts (bank_code, account_number) VALUES (?, ?)",
            (bank_code, next_account_number)
        )
        conn.commit()
        conn.close()
        return next_account_number




class Bank:
    def __init__(self, bank_code):
        self.bank_code = bank_code

    @staticmethod
    def create_bank(bank_code):
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO banks (bank_code) VALUES (?)", (bank_code,))
        conn.commit()
        conn.close()
        return Bank(bank_code)

    @staticmethod
    def get_bank(bank_code):
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT bank_code FROM banks WHERE bank_code = ?", (bank_code,))
        row = cursor.fetchone()
        if row:
            bank = Bank(row[0])
        else:
            bank = Bank.create_bank(bank_code)

        conn.close()
        return bank

    def get_bank_code(self):
        return self.bank_code


    def add_account(self):
        return Account.create_account(self.bank_code)

    def get_clients(self):
        return None

    def get_total_balance(self):
        total_balance = 0
        return total_balance

