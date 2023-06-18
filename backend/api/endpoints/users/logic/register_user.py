import uuid

from injector import inject

from api.endpoints.users.models.register_user_response import RegisterUserResponse
from command_interface import ICommand
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection
from mediator.mediator_interface import IMediator


class RegisterUser(ICommand[RegisterUserResponse]):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler, mediator: IMediator):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")
        self._mediator: IMediator = mediator

    async def handle(self) -> RegisterUserResponse:
        user_uuid: str = uuid.uuid4().hex
        print("created user with uuid: " + user_uuid)
        await self.create_database(user_uuid)
        # await self._mediator.execute_async(CreateAllTablesForSchema, user_uuid=user_uuid)
        return RegisterUserResponse(user_uuid=user_uuid)

    async def create_database(self, user_uuid: str) -> None:
        await self._db.create_database(self._admin_user, "postgres", user_uuid)


