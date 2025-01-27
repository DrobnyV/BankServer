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
    def create_account(bank_code,account_number, balance = 0):
        if account_number in range(10000,99999):
            conn = Connection().get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO accounts (account_number,bank_id,balance) VALUES (?)", (account_number,bank_code,balance))
            conn.commit()
            conn.close()
            return Account(account_number,bank_code,balance)
        else:
            print("Account number must be between 10000 and 99999")



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


    def add_account(self,account_number,balance = 0):
        Account.create_account(account_number,self.bank_code,balance)

    def get_clients(self):
        return None

    def get_total_balance(self):
        total_balance = 0
        return total_balance

