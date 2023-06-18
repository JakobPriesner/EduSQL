from fastapi import APIRouter

from api.middleware.database_error import DatabaseErrorMiddleware


def fastapi_controller(cls):
    cls.is_controller = True

    def add_routes(self):
        self.router = APIRouter()
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "route_info"):
                self.router.add_api_route(**attr.route_info, endpoint=attr)

    cls.add_routes = add_routes

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.add_routes()

    # cls.__init__ = new_init todo: fix injection
    return cls
