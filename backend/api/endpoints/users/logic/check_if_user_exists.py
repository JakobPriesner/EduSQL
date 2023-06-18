import uuid

from injector import inject

from api.endpoints.users.models.get_user_response import GetUserResponse
from command_interface import ICommand
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection
from mediator.mediator_interface import IMediator


class CheckIfUserExists(ICommand[GetUserResponse]):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler, mediator: IMediator):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")
        self._mediator: IMediator = mediator

    async def handle(self, db: str) -> GetUserResponse:
        try:
            await self._db.load_single_by_sql(self._admin_user, db, "SELECT COUNT(*) FROM person;")
            return GetUserResponse(exists=True)
        except Exception as e:
            return GetUserResponse(exists=False)

