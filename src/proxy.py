import configparser
import socket
config = configparser.ConfigParser()
config.read("conf.ini")

def find_open_port(ip):
    for port in range(config["SERVER"]["PORT_TO_SCAN"], config["SERVER"]["PORT_TO_SCAN"] + 10):
        try:
            with socket.socket() as s:
                s.settimeout(config["SERVER"]["TIMEOUT_PORT"])
                s.connect((ip, port))
                return port
        except (socket.timeout, ConnectionRefusedError):
            continue
    return None



def proxy_request(ip, message):
    port = find_open_port(ip)
    if port is None:
        return "ER Proxy error: No available ports\n\r"

    try:
        with socket.socket() as s:
            s.connect((ip, port))
            s.sendall(message.encode())
            response = s.recv(1024).decode()
        return response
    except Exception as e:
        return f"ER Proxy error: {e}\n\r"