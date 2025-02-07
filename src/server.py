import configparser
import socket
import threading

from src.bank import Bank
from src.commands import GetCommands
from logger import logger

config = configparser.ConfigParser()
config.read("conf.ini")
CLIENT_TIMEOUT = int(config["SERVER"]["TIMEOUT"])
server_inet_address = (config["SERVER"]["HOST"], int(config["SERVER"]["PORT"]))


def handle_client(connection, client_inet_address):
    connection.settimeout(CLIENT_TIMEOUT)
    logger.info(f"Client connected from {client_inet_address[0]}:{client_inet_address[1]}")

    try:
        bank = Bank.get_bank(server_inet_address[0])
        while True:
            try:
                client_message = connection.recv(1024).decode().strip()
                if not client_message:
                    command = GetCommands.get_command("unknown")
                else:
                    parts = client_message.split()
                    if parts:
                        command_type = parts[0].lower()
                        command = GetCommands.get_command(command_type)
                    else:
                        command = GetCommands.get_command("unknown")

                logger.info(f"Received command: {client_message} from {client_inet_address}")
                command.execute(connection, bank, client_message)
            except socket.timeout:
                logger.warning(f"Client {client_inet_address} disconnected due to inactivity.")
                connection.send("Disconnected due to inactivity.".encode())
                break
    except Exception as e:
        logger.error(f"Error handling client {client_inet_address}: {e}")
    finally:
        connection.close()
        logger.info(f"Connection with {client_inet_address[0]}:{client_inet_address[1]} closed.")


def accept_clients(server_socket):
    while True:
        try:
            connection, client_inet_address = server_socket.accept()
            logger.info(f"New connection from {client_inet_address[0]}:{client_inet_address[1]}")
            client_thread = threading.Thread(
                target=handle_client, args=(connection, client_inet_address), daemon=True
            )
            client_thread.start()
        except Exception as e:
            logger.error(f"Error accepting clients: {e}")
            break
