from src.db import Connection


class Account:
    def __init__(self, account_number,bank_code,balance =0):
        self.balance = balance
        self.account_number = account_number
        self.bank_code = bank_code

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self.balance += amount
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_number = ? AND bank_code = ?
            """,
            (self.balance, self.account_number, self.bank_code)
        )
        conn.commit()
        conn.close()

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """  
            UPDATE accounts  
            SET balance = ?  
            WHERE account_number = ? AND bank_code = ?  
            """,
            (self.balance, self.account_number, self.bank_code)
        )
        conn.commit()
        conn.close()

    def get_balance(self):
        return self.balance

    @staticmethod
    def create_account(bank_code):
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT IFNULL(MAX(account_number), 9999) FROM accounts")
        max_account_number = cursor.fetchone()[0]
        next_account_number = max_account_number + 1
        if next_account_number < 10000:
            next_account_number = 10000
        elif next_account_number > 99999:
            conn.close()
            raise ValueError("Cannot create account: account_number exceeds 99999.")
        cursor.execute(
            "INSERT INTO accounts (bank_code, account_number) VALUES (?, ?)",
            (bank_code, next_account_number)
        )
        conn.commit()
        conn.close()

        return next_account_number

    @staticmethod
    def get_account(account_number, bank_code):
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT account_number, bank_code, balance
            FROM accounts
            WHERE account_number = ? AND bank_code = ?
            """,
            (account_number, bank_code)
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            raise ValueError(f"Account {account_number}/{bank_code} not found.")
        return Account(account_number=row[0], bank_code=row[1], balance=row[2])

    def remove(self):
        conn = Connection().get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """  
            DELETE FROM accounts  
            WHERE account_number = ? AND bank_code = ?  
            """,
            (self.account_number, self.bank_code)
        )
        conn.commit()
        conn.close()


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

    def get_bank_info(self):
        conn = Connection().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(account_number), COALESCE(SUM(balance), 0)
            FROM accounts
            WHERE bank_code = ?
        """, (self.bank_code,))

        num_clients, total_balance = cursor.fetchone()

        conn.close()
        return num_clients, total_balance



