from functools import wraps

from starlette import status


def put(path, response_model=None, status_code=status.HTTP_200_OK):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        # Add route metadata to the function
        wrapper.route_info = {
            "path": path,
            "response_model": response_model,
            "status_code": status_code,
            "methods": ["PUT"],
        }
        return wrapper
    return decorator
