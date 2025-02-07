from src.bank import Account
from src.command_interface import Command


class BCCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("BC " + bank.get_bank_code())

class ACCommand(Command):
    def execute(self, connection, bank, client_message):
        account_number = bank.add_account()
        connection.send(("AC " + str(account_number) + "/" + bank.get_bank_code()).encode())

class ADCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 3:
                connection.send("Invalid AD command format.\n".encode())
                return
            account_and_ip, amount = parts[1], parts[2]
            account_code, ip = account_and_ip.split("/")
            amount = float(amount)
            if amount <= 0:
                connection.send("Deposit amount must be greater than 0.\n".encode())
                return
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)
            account.deposit(amount)
            connection.send(f"Balance after deposit: {account.get_balance()}\n".encode())
        except ValueError:
            connection.send("Invalid account or amount.\n".encode())
        except Exception as e:
            connection.send(f"Error processing deposit: {e}\n".encode())

class AWCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 3:
                connection.send("Invalid AW command format.\n".encode())
                return
            account_and_ip, amount = parts[1], parts[2]
            account_code, ip = account_and_ip.split("/")
            amount = float(amount)
            if amount <= 0:
                connection.send("Withdrawal amount must be greater than 0.\n".encode())
                return
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)
            if account.get_balance() < amount:
                connection.send("Insufficient funds.\n".encode())
                return
            account.withdraw(amount)
            connection.send(f"Balance after withdrawal: {account.get_balance()}".encode())
        except ValueError:
            connection.send("Invalid account or amount.\n".encode())
        except Exception as e:
            connection.send(f"Error processing withdrawal: {e}\n".encode())

class ABCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 2:
                connection.send("Invalid AB command format.\n".encode())
                return
            account_and_ip = parts[1]
            account_code, ip = account_and_ip.split("/")
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)
            connection.send(f"Current balance: {account.get_balance()}".encode())
        except ValueError:
            connection.send("Invalid account.\n".encode())
        except Exception as e:
            connection.send(f"Error retrieving balance: {e}\n".encode())


class ARCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 2:
                connection.send("Invalid AR command format.\n".encode())
                return
            account_and_ip = parts[1]
            account_code, ip = account_and_ip.split("/")
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)

            if account is None:
                connection.send("Account not found.\n".encode())
                return

            account.remove()
            connection.send("Account successfully removed.\n".encode())

        except ValueError:
            connection.send("Invalid account.\n".encode())
        except Exception as e:
            connection.send(f"Error removing account: {e}\n".encode())


class ExitCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("Closing connection.".encode())

class HelpCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("Available commands: exit, help, BC, AC, AD, AW, AB, AR, BA, BN".encode())

class UnknownCommand(Command):
    def execute(self, connection, bank, client_message):
        connection.send("Unknown command".encode())

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
            "exit": ExitCommand(),
            "help": HelpCommand()
        }
        return commands.get(command_type, UnknownCommand())