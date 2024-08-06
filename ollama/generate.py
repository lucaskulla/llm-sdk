import json
import time

import requests
from requests import RequestException


import json
import requests
from requests.exceptions import RequestException

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
        RequestException: If an error occurs during the API request.
        JSONDecodeError: If the response contains invalid JSON.
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
    except RequestException as e:
        print(f"An error occurred: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None, None



import time
from requests.exceptions import RequestException


def generate_single_response(user_prompt, system_prompt, messages, model, options=None, context=None,
                             answer_format=None, base_url="localhost", base_url_port=11434, max_retries=10):
    """
    Send a single request to the API and return the response and context.
    If an error occurs, the same request is sent again (up to 10 times, each time 5 seconds sleep).

    Args:
        user_prompt (str): The user prompt for generating the response.
        system_prompt (str): The system prompt for generating the response.
        messages (list): List of messages to include in the conversation.
        model (str): The name of the model to use for generating the response.
        options (dict): Additional options for generating the response.
        context (str, optional): The context for generating the response. Defaults to None.
        answer_format (str, optional): The format of the generated answer. Defaults to None.
        base_url (str, optional): The base URL of the API. Defaults to "localhost".
        base_url_port (int, optional): The port of the API. Defaults to 11434.
        max_retries (int, optional): The maximum number of retries. Defaults to 10.

    Returns:
        tuple: A tuple containing the generated response and the final context.
    """
    retries = 0
    context_old = context
    response = None

    while retries < max_retries:
        try:
            if retries == max_retries - 1:  # One last chance to get a response
                context = None

            response, context = generate(
                base_url=f"http://{base_url}:{base_url_port}",
                model=model,
                user_prompt=user_prompt,
                system_prompt=system_prompt,
                options=options,
                messages=messages,
                context=context,
                answer_format=answer_format
            )

            if response is None:
                raise RequestException("Response is None")

            # If no exception occurs, break the loop
            break

        except RequestException as e:
            print(f"RequestException: {e}")
            context = context_old  # Reuse the old context
            retries += 1
            time.sleep(5)

    return response, context
