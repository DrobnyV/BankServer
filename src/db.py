import sqlite3


class Connection:
    @staticmethod
    def get_connection():
        return sqlite3.connect("bank.db")

    @staticmethod
    def initialize_db():
        with Connection().get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS banks (
                    bank_code TEXT PRIMARY KEY
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number INTEGER,
                    bank_code TEXT,
                    balance REAL DEFAULT 0,
                    PRIMARY KEY (account_number),
                    FOREIGN KEY (bank_code) REFERENCES banks(bank_code)
                )
                """
            )
            conn.commit()

