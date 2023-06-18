def api_version(version):
    def decorator(cls):
        cls.version = version
        return cls
    return decorator
