import configparser
import socket
from logger import logger

config = configparser.ConfigParser()
config.read("conf.ini")

def find_open_port(ip):
    start_port = int(config["SERVER"]["PORT_TO_SCAN"])
    timeout = float(config["SERVER"]["TIMEOUT_PORT"])

    for port in range(start_port, start_port + 10):
        try:
            with socket.socket() as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                logger.info(f"Found open port: {port} on {ip}")
                return port
        except (socket.timeout, ConnectionRefusedError):
            logger.warning(f"Port {port} on {ip} is not available.")
            continue

    logger.error(f"No open ports found on {ip}.")
    return None

def proxy_request(ip, message):
    port = find_open_port(ip)
    if port is None:
        return "ER Proxy error: No available ports\r\n"

    try:
        with socket.socket() as s:
            timeout = float(config["SERVER"]["TIMEOUT_PORT"])
            s.settimeout(timeout)
            s.connect((ip, port))
            s.sendall(message.encode())

            response = s.recv(1024).decode()
            logger.info(f"Received response from {ip}:{port}: {response.strip()}")
        return response
    except Exception as e:
        logger.error(f"Proxy error: {e}")
        return f"ER Proxy error: {e}\r\n"
