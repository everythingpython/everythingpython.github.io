import time
from functools import wraps


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (float(end_time) - float(start_time))*(10**12)
        print(f"Function '{func.__name__}' executed in {elapsed_time} seconds.")
        return result

    return wrapper
