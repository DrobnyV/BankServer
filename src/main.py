import socket
import threading

from src.server import accept_clients


def main():
    server_inet_address = ("127.0.0.1", 65430)
    server_socket = socket.socket()
    server_socket.bind(server_inet_address)
    server_socket.listen()
    print("Server started on " + str(server_inet_address[0]) + ":" + str(server_inet_address[1]))

    try:
        accept_thread = threading.Thread(target=accept_clients, args=(server_socket,), daemon=True)
        accept_thread.start()
        print("Listening for incoming connections...")
        accept_thread.join()
    except KeyboardInterrupt:
        print("Server shutting down.")
    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        server_socket.close()
        print("Server shutdown.")

if __name__ == '__main__':
    main()