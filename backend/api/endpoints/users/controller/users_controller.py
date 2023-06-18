from injector import inject
from starlette import status

from api.annotations import fastapi_controller
from api.annotations.base_url import base_url
from api.annotations.api_tags import api_tags
from api.annotations.http_methods.get import get
from api.annotations.http_methods.post import post
from api.endpoints.users.logic.check_if_user_exists import CheckIfUserExists
from api.endpoints.users.logic.register_user import RegisterUser
from api.endpoints.users.logic.verify_if_db_user_exists import VerifyIfDbUserExists
from api.endpoints.users.models.get_user_response import GetUserResponse
from api.endpoints.users.models.register_user_response import RegisterUserResponse
from database.models.db_user import DbUser
from mediator.mediator_interface import IMediator


@fastapi_controller
@base_url("users")
@api_tags(["Users"])
class UsersController:
    @inject
    def __init__(self, mediator: IMediator):
        self._mediator: IMediator = mediator
        # self.router.add_api_route("/register", self.register_user, response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED, methods=["POST"])

    @get("/me", response_model=GetUserResponse, status_code=status.HTTP_200_OK)
    async def get_user(self, uuid: str) -> GetUserResponse:
        return await self._mediator.execute_async(CheckIfUserExists, db=uuid)

    @post("/db-user", response_model=GetUserResponse, status_code=status.HTTP_200_OK)
    async def verify_db_user(self, payload: DbUser, uuid: str) -> GetUserResponse:
        return await self._mediator.execute_async(VerifyIfDbUserExists, payload=payload, db=uuid)

    @post("/register", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
    async def register_user(self) -> RegisterUserResponse:
        return await self._mediator.execute_async(RegisterUser)
