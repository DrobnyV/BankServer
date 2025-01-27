import sqlite3


class Connection:
    @staticmethod
    def get_connection():
        return sqlite3.connect("bank.db")

