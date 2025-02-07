import configparser
import socket
import threading

from src.db import Connection
from src.server import accept_clients
from logger import logger

def main():
    logger.info("Initializing database...")
    Connection.initialize_db()

    config = configparser.ConfigParser()
    config.read("conf.ini")
    server_inet_address = (config["SERVER"]["HOST"], int(config["SERVER"]["PORT"]))

    server_socket = socket.socket()
    server_socket.bind(server_inet_address)
    server_socket.listen()

    logger.info(f"Server started on {server_inet_address[0]}:{server_inet_address[1]}")

    try:
        accept_thread = threading.Thread(target=accept_clients, args=(server_socket,), daemon=True)
        accept_thread.start()
        logger.info("Listening for incoming connections...")
        accept_thread.join()
    except KeyboardInterrupt:
        logger.warning("Server shutting down due to keyboard interrupt.")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
    finally:
        server_socket.close()
        logger.info("Server shutdown.")

if __name__ == '__main__':
    main()
