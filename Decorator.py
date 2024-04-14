import functools
from datetime import datetime

def log_func_execution_time(log_file_path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with open(log_file_path, 'a') as log_file:
                func_name = func.__qualname__
                # log_file.write("Function: {}\n".format(func_name))
                execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write("Execution time: {} - {}\n".format(execution_time, func_name))
            return func(*args, **kwargs)
        return wrapper
    return decorator