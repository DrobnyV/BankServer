from src.bank import Account
from src.command_interface import Command


class BCCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send(f"BC {bank.get_bank_code()}\n\r".encode())


class ACCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            account_number = bank.add_account()
            connection.send(f"AC {account_number}/{bank.get_bank_code()}\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class ADCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 3:
                connection.send("ER Invalid AD command format.\n\r".encode())
                return

            account_and_ip, amount = parts[1], parts[2]
            account_code, ip = account_and_ip.split("/")
            amount = float(amount)

            if amount <= 0:
                connection.send("ER Deposit amount must be greater than 0.\n\r".encode())
                return

            account_code = int(account_code)
            account = Account.get_account(account_code, ip)
            account.deposit(amount)

            connection.send("AD\n\r".encode())

        except ValueError:
            connection.send("ER Invalid account or amount.\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class AWCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 3:
                connection.send("ER Invalid AW command format.\n\r".encode())
                return

            account_and_ip, amount = parts[1], parts[2]
            account_code, ip = account_and_ip.split("/")
            amount = float(amount)

            if amount <= 0:
                connection.send("ER Withdrawal amount must be greater than 0.\n\r".encode())
                return

            account_code = int(account_code)
            account = Account.get_account(account_code, ip)

            if account.get_balance() < amount:
                connection.send("ER Insufficient funds.\n\r".encode())
                return

            account.withdraw(amount)
            connection.send("AW\n\r".encode())

        except ValueError:
            connection.send("ER Invalid account or amount.\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class ABCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 2:
                connection.send("ER Invalid AB command format.\n\r".encode())
                return

            account_and_ip = parts[1]
            account_code, ip = account_and_ip.split("/")
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)

            connection.send(f"AB {account.get_balance()}\n\r".encode())

        except ValueError:
            connection.send("ER Invalid account.\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class ARCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 2:
                connection.send("ER Invalid AR command format.\n\r".encode())
                return

            account_and_ip = parts[1]
            account_code, ip = account_and_ip.split("/")
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)

            if account is None:
                connection.send("ER Account not found.\n\r".encode())
                return

            account.remove()
            connection.send("AR\n\r".encode())

        except ValueError:
            connection.send("ER Invalid account.\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class BACommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            bank_amount = bank.get_bank_info()[1]
            connection.send(f"BA {bank_amount}\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class BNCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            bank_count = bank.get_bank_info()[0]
            connection.send(f"BN {bank_count}\n\r".encode())
        except Exception as e:
            connection.send(f"ER {e}\n\r".encode())


class ExitCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("Closing connection.\n\r".encode())


class HelpCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("Available commands: exit, help, BC, AC, AD, AW, AB, AR, BA, BN\n\r".encode())


class UnknownCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("ER Unknown command\n\r".encode())


class GetCommands:
    @staticmethod
    def get_command(command_type):
        commands = {
            "bc": BCCommand(),
            "ac": ACCommand(),
            "ad": ADCommand(),
            "aw": AWCommand(),
            "ab": ABCommand(),
            "ar": ARCommand(),
            "ba": BACommand(),
            "bn": BNCommand(),
            "exit": ExitCommand(),
            "help": HelpCommand()
        }
        return commands.get(command_type, UnknownCommand())
