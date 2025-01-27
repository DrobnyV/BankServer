import socket
import threading

from src.bank import Bank

server_inet_address = ("127.0.0.1", 65430)
CLIENT_TIMEOUT = 60

def handle_client(connection, client_inet_address):
    connection.settimeout(CLIENT_TIMEOUT)
    print(f"Client connected from {client_inet_address[0]}:{client_inet_address[1]}")

    try:
        connection.send("AHOJ\n".encode())
        bank = Bank.get_bank(server_inet_address[0])
        while True:
            try:
                client_message = connection.recv(100).decode("utf-8").strip().lower()

                print(f"Received from {client_inet_address}: {client_message}")
                match client_message:
                    case "bc":
                        print("BC " + bank.get_bank_code())
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