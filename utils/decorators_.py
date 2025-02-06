import time
import requests
from functools import wraps


def retry_request(max_retries=3, initial_delay=2):
    """
    Retry decorator to retry a function in case of failure (non-200 HTTP status code).

    Parameters:
    - max_retries: The maximum number of retries (default is 3).
    - initial_delay: The delay between retries in seconds (default is 2).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            status = ""
            while retries < max_retries:
                response = func(*args, **kwargs)
                if response.status_code == 200:
                    return response, response.status_code
                else:
                    retries += 1
                    print(
                        f"Attempt {retries}/{max_retries} failed with status code {response.status_code}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff: delay doubles after each attempt
                    status = response.status_code
            print(f"All {max_retries} attempts failed. Giving up.")
            return None, status

        return wrapper

    return decorator
