import configparser
import socket
import threading
from traceback import print_tb

from src.bank import Bank

config = configparser.ConfigParser()
config.read("conf.ini")
CLIENT_TIMEOUT = int(config["SERVER"]["TIMEOUT"])

def handle_client(connection, client_inet_address):
    connection.settimeout(CLIENT_TIMEOUT)
    print(f"Client connected from {client_inet_address[0]}:{client_inet_address[1]}")
    try:
        connection.send("AHOJ\n".encode())
        bank = Bank.get_bank(client_inet_address[0])
        while True:
            try:
                client_message = connection.recv(100).decode("utf-8").strip().lower()

                print(f"Received from {client_inet_address}: {client_message}")
                if client_message == "":
                    connection.send(f"You have to write something\n".encode())
                else:

                    match client_message.split()[0]:
                        case "bc":
                            print("BC " + bank.get_bank_code())
                        case "ac":
                            account_number = bank.add_account()
                            print("AC " + str(account_number) + "/" + bank.get_bank_code())
                        case "ad":
                            try:
                                parts = client_message.split()
                                if len(parts) != 3:
                                    connection.send("Invalid AD command format.\n".encode())
                                    continue
                                account_and_ip, amount = parts[1], parts[2]
                                account_code, ip = account_and_ip.split("/")
                                amount = float(amount)
                                if amount <= 0:
                                    connection.send("Deposit amount must be greater than 0.\n".encode())
                                    continue
                                account_code = int(account_code)
                                account = bank.get_account(account_code,ip)
                                account.deposit(500)
                                print(f"Balance after deposit: {account.get_balance()}")
                            except ValueError:
                                connection.send("Invalid account or amount.\n".encode())
                            except Exception as e:
                                connection.send(f"Error processing deposit: {e}\n".encode())
                        case "exit":
                            connection.send("Closing connection.".encode())
                            break
                        case "help":
                            connection.send("Available commands: exit, help, BC, AC, AD, AW, AB, AR, BA, BN".encode())
                        case _:
                            connection.send("Unknown command".encode())
            except socket.timeout:
                connection.send("Disconnected due to inactivity.".encode())
                break
    except Exception as e:
        print(f"Error handling client {client_inet_address}: {e}")
    finally:
        connection.close()
        print(f"Connection with {client_inet_address[0]}:{client_inet_address[1]} closed.")


def accept_clients(server_socket):
    while True:
        try:
            connection, client_inet_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(connection, client_inet_address), daemon=True
            )
            client_thread.start()
        except Exception as e:
            print(f"Error accepting clients: {e}")
            break