import configparser
import socket

config = configparser.ConfigParser()
config.read("conf.ini")

def find_open_port(ip):
    start_port = int(config["SERVER"]["PORT_TO_SCAN"])
    timeout = int(config["SERVER"]["TIMEOUT_PORT"])

    for port in range(start_port, start_port + 10):
        try:
            with socket.socket() as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                return port
        except (socket.timeout, ConnectionRefusedError):
            continue
    return None

def proxy_request(ip, message):
    port = find_open_port(ip)
    if port is None:
        return "ER Proxy error: No available ports\r\n"

    try:
        with socket.socket() as s:
            s.settimeout(config["SERVER"]["TIMEOUT_PORT"])
            s.connect((ip, port))
            s.sendall(message.encode())
            response = s.recv(1024).decode()
        return response
    except Exception as e:
        return f"ER Proxy error: {e}\r\n"
