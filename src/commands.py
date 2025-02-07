from src.bank import Account
from src.command_interface import Command
from src.proxy import proxy_request
from logger import logger


class BCCommand(Command):
    def execute(self, connection, bank, client_message):
        logger.info("Executing BCCommand")
        connection.send(f"BC {bank.get_bank_code()}\r\n".encode())


class ACCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            account_number = bank.add_account()
            logger.info(f"New account created: {account_number}/{bank.get_bank_code()}")
            connection.send(f"AC {account_number}/{bank.get_bank_code()}\r\n".encode())
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            connection.send(f"ER {e}\r\n".encode())


class ADCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 3:
                connection.send("ER Invalid AD command format.\r\n".encode())
                return

            account_and_ip, amount = parts[1], parts[2]
            account_code, ip = account_and_ip.split("/")
            amount = float(amount)

            if amount <= 0:
                connection.send("ER Deposit amount must be greater than 0.\r\n".encode())
                return

            account_code = int(account_code)

            if ip != bank.get_bank_code():
                response = proxy_request(ip, client_message)
                logger.info(f"Proxying AD command to {ip}")
                connection.send(response.encode())
                return

            account = Account.get_account(account_code, ip)
            account.deposit(amount)
            logger.info(f"Deposited {amount} to account {account_code}")
            connection.send("AD\r\n".encode())

        except ValueError:
            logger.warning("Invalid AD command format")
            connection.send("ER Invalid account or amount.\r\n".encode())
        except Exception as e:
            logger.error(f"Error in AD command: {e}")
            connection.send(f"ER {e}\r\n".encode())


class AWCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 3:
                connection.send("ER Invalid AW command format.\r\n".encode())
                return

            account_and_ip, amount = parts[1], parts[2]
            account_code, ip = account_and_ip.split("/")
            amount = float(amount)

            if amount <= 0:
                connection.send("ER Withdrawal amount must be greater than 0.\r\n".encode())
                return

            account_code = int(account_code)

            if ip != bank.get_bank_code():
                response = proxy_request(ip, client_message)
                logger.info(f"Proxying AW command to {ip}")
                connection.send(response.encode())
                return

            account = Account.get_account(account_code, ip)

            if account.get_balance() < amount:
                logger.warning(f"Insufficient funds for account {account_code}")
                connection.send("ER Insufficient funds.\r\n".encode())
                return

            account.withdraw(amount)
            logger.info(f"Withdrew {amount} from account {account_code}")
            connection.send("AW\r\n".encode())

        except ValueError:
            logger.warning("Invalid AW command format")
            connection.send("ER Invalid account or amount.\r\n".encode())
        except Exception as e:
            logger.error(f"Error in AW command: {e}")
            connection.send(f"ER {e}\r\n".encode())


class ABCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 2:
                connection.send("ER Invalid AB command format.\r\n".encode())
                return

            account_and_ip = parts[1]
            account_code, ip = account_and_ip.split("/")
            account_code = int(account_code)

            if ip != bank.get_bank_code():
                response = proxy_request(ip, client_message)
                logger.info(f"Proxying AB command to {ip}")
                connection.send(response.encode())
                return

            account = Account.get_account(account_code, ip)
            balance = account.get_balance()
            logger.info(f"Balance for account {account_code}: {balance}")
            connection.send(f"AB {balance}\r\n".encode())

        except ValueError:
            logger.warning("Invalid AB command format")
            connection.send("ER Invalid account.\r\n".encode())
        except Exception as e:
            logger.error(f"Error in AB command: {e}")
            connection.send(f"ER {e}\r\n".encode())


class ARCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            parts = client_message.split()
            if len(parts) != 2:
                connection.send("ER Invalid AR command format.\r\n".encode())
                return

            account_and_ip = parts[1]
            account_code, ip = account_and_ip.split("/")
            account_code = int(account_code)
            account = Account.get_account(account_code, ip)

            if account is None:
                logger.warning(f"Account {account_code} not found")
                connection.send("ER Account not found.\r\n".encode())
                return

            account.remove()
            logger.info(f"Removed account {account_code}")
            connection.send("AR\r\n".encode())

        except ValueError:
            logger.warning("Invalid AR command format")
            connection.send("ER Invalid account.\r\n".encode())
        except Exception as e:
            logger.error(f"Error in AR command: {e}")
            connection.send(f"ER {e}\r\n".encode())


class BACommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            bank_amount = bank.get_bank_info()[1]
            logger.info(f"Bank amount requested: {bank_amount}")
            connection.send(f"BA {bank_amount}\r\n".encode())
        except Exception as e:
            logger.error(f"Error in BA command: {e}")
            connection.send(f"ER {e}\r\n".encode())


class BNCommand(Command):
    def execute(self, connection, bank, client_message):
        try:
            bank_count = bank.get_bank_info()[0]
            logger.info(f"Bank count requested: {bank_count}")
            connection.send(f"BN {bank_count}\r\n".encode())
        except Exception as e:
            logger.error(f"Error in BN command: {e}")
            connection.send(f"ER {e}\r\n".encode())


class ExitCommand(Command):
    def execute(self, connection, bank, client_message):
        logger.info("Closing connection.")
        connection.send("Closing connection.\r\n".encode())


class HelpCommand(Command):
    def execute(self, connection, bank, client_message):
        logger.info("Help command executed")
        connection.send("Available commands: exit, help, BC, AC, AD, AW, AB, AR, BA, BN\r\n".encode())


class UnknownCommand(Command):
    def execute(self, connection, bank, client_message):
        logger.warning(f"Unknown command received: {client_message}")
        connection.send("ER Unknown command\r\n".encode())


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
