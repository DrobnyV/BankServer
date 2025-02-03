from src.bank import Account
from src.command_interface import Command


class BCCommand(Command):
    def execute(self, connection, bank, client_message):
        print("BC " + bank.get_bank_code())

class ACCommand(Command):
    def execute(self, connection, bank, client_message):
        account_number = bank.add_account()
        print("AC " + str(account_number) + "/" + bank.get_bank_code())

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
            print(f"Balance after deposit: {account.get_balance()}")
        except ValueError:
            connection.send("Invalid account or amount.\n".encode())
        except Exception as e:
            connection.send(f"Error processing deposit: {e}\n".encode())

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
            "exit": ExitCommand(),
            "help": HelpCommand()
        }
        return commands.get(command_type, UnknownCommand())