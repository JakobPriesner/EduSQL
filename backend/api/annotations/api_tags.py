def api_tags(tags: list[str]):
    def decorator(cls):
        cls.tags = tags
        return cls
    return decorator
