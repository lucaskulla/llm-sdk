import socket
from contextlib import closing

import requests
import json


def generate(base_url, model, user_prompt, stream=True, system_prompt=None, messages=None, answer_format=None,
             context=None, options=None):
    """
    Generate a response using the specified model and prompts.

    Args:
        base_url (str): The base URL of the API.
        model (str): The name of the model to use for generating the response.
        user_prompt (str): The user prompt for generating the response.
        stream (bool, optional): Whether to stream the response or not. Defaults to True.
        system_prompt (str, optional): The system prompt for generating the response. Defaults to None.
        messages (list, optional): List of messages to include in the conversation. Defaults to None.
        answer_format (str, optional): The format of the generated answer. Defaults to None.
        context (str, optional): The context for generating the response. Defaults to None.
        options (dict, optional): Additional options for generating the response. Defaults to None.

    Returns:
        tuple: A tuple containing the generated response and the final context.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
        json.decoder.JSONDecodeError: If the response contains invalid JSON.
    """
    url = f"{base_url}/api/generate"

    payload = {
        "model": model,
        "prompt": user_prompt,
        "system": system_prompt,
        "format": answer_format,
        "messages": messages,
        "context": context,
        "options": options
    }

    # Remove keys with None values
    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        with requests.post(url, json=payload, stream=stream) as response:
            response.raise_for_status()

            final_context = None
            full_response = []

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                    except json.JSONDecodeError:
                        print("Invalid JSON received")
                        return None, None

                    response_piece = chunk.get("response", "")
                    full_response.append(response_piece)

                    if chunk.get("done"):
                        final_context = chunk.get("context")
                        break

            return ''.join(full_response), final_context
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None, None


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
