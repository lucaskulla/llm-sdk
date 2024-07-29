import socket
from contextlib import closing


def check_host(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Checks if a port on a given host is open.

    Args:
        host (str): Hostname or IP address of the server to check.
        port (int): Port number to check.
        timeout (float): Timeout in seconds. Default is 1.0 second.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    if not isinstance(host, str) or not host:
        raise TypeError("Host must be a non-empty string.")

    if not isinstance(port, int) or not (0 <= port <= 65535):
        raise ValueError("Port must be an integer between 0 and 65535.")

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        except (socket.timeout, socket.error):
            return False
