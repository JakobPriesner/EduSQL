import ast
import importlib
import os
from typing import Generator, Type

from fastapi import FastAPI, Request
from injector import inject, Injector
from starlette.responses import RedirectResponse
from uvicorn import Config, Server

from api.middleware.database_error import DatabaseErrorMiddleware
from log.logger_interface import ILogger


class Api:
    @inject
    def __init__(self, logger: ILogger, injector: Injector):
        self._logger = logger
        self._injector = injector
        self._module_path = os.path.join(os.path.dirname(__file__), "endpoints")
        self._app = FastAPI(
            title="Jarvis API",
            description=""
        )
        self._api = FastAPI(title="Api")
        self._server = None
        self._setup_routes()

    def start(self):
        config = Config(self._app, host="127.0.0.1", port=8080, log_level="warning")
        self._server = Server(config=config)
        self._logger.info(f"Api is available on http://{config.host}:{config.port}")
        self._server.run()

    @staticmethod
    def _setup_middleware(app):
        app.add_middleware(DatabaseErrorMiddleware)

    def _setup_routes(self):
        @self._app.get("/app")
        def read_main(request: Request):
            return {
                "message": "Hello from speech assistant app",
                "root_path": request.scope.get("root_path"),
            }

        @self._app.get("/")
        def redirect_to_latest_docs(request: Request):
            return RedirectResponse(request.scope.get("path").lstrip("/") + "/api/docs")

        controllers = self._get_controller_classes(self._module_path)

        versions = list(set(getattr(controller, "version", "") for controller in controllers))
        for version in versions:
            version_controllers = [controller for controller in controllers if
                                   getattr(controller, 'version', '') == version]
            self.include_controllers(version, version_controllers)

    def include_controllers(self, version: str, controllers: list):
        v_app = FastAPI()
        self._setup_middleware(v_app)
        for controller in controllers:
            instance = self._injector.get(controller)
            instance.add_routes()
            router = instance.router
            prefix = f"/{version}" + (controller.base_path if hasattr(controller, 'base_path') else "")
            tags = controller.tags if hasattr(controller, 'tags') else []
            v_app.include_router(router, prefix=prefix, tags=tags)
        self._app.mount(app=v_app, path=f"/api/{version}", name=version)

    def _get_controller_classes(self, path: str) -> list[Type]:
        python_files = self._get_python_files(path)
        controller_classes = []
        for file_path in python_files:
            module = self._load_module(file_path)
            class_names = self._get_classes_from_file(file_path)
            for class_name in class_names:
                cls = getattr(module, class_name)
                if hasattr(cls, 'is_controller') and getattr(cls, 'is_controller'):
                    controller_classes.append(cls)
        return controller_classes

    @staticmethod
    def _get_python_files(path: str) -> Generator[str, None, None]:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    yield os.path.join(root, file)

    def _get_classes_from_file(self, file_path: str) -> Generator[str, None, None]:
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
            for node in tree.body:
                if isinstance(node, ast.ClassDef) and self._has_fastapi_controller_decorator(node):
                    yield node.name

    @staticmethod
    def _has_fastapi_controller_decorator(class_node: ast.ClassDef) -> bool:
        return any(
            isinstance(decorator, ast.Name) and decorator.id == 'fastapi_controller'
            for decorator in class_node.decorator_list
        )

    @staticmethod
    def _load_module(file_path: str):
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def stop(self):
        self._logger.info("Stopping api")
        if self._server:
            self._server.should_exit = True
        self._logger.info("Api stopped")


if __name__ == "__main__":
    api = Api()
    api.start()
