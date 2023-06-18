def base_url(path):
    def decorator(cls):
        cls.base_path = path
        return cls
    return decorator
