import asyncio
import uuid
from pathlib import Path

import aiofiles
from injector import inject

from api.endpoints.users.models.register_user_payload import RegisterUserPayload
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

    async def handle(self, payload: RegisterUserPayload) -> RegisterUserResponse:
        user_uuid: str = uuid.uuid4().hex
        print("created user with uuid: " + user_uuid)
        await self._create_database(user_uuid)
        return RegisterUserResponse(user_uuid=user_uuid)

    async def _create_database(self, user_uuid: str) -> None:
        await self._db.create_database(self._admin_user, "postgres", user_uuid)
        await self._create_roles(user_uuid)
        await self._create_users(user_uuid)

    async def _create_roles(self, user_uuid: str) -> None:
        await asyncio.gather(*[
            self._db.execute_without_response(self._admin_user, user_uuid, statement)
            for statement in await self._load_sql_statements("create_roles_for_new_schema.sql")
            if not statement.startswith("--") and statement != ""
        ])

    async def _create_users(self, user_uuid: str) -> None:
        await asyncio.gather(*[
            self._db.execute_without_response(self._admin_user, user_uuid, statement)
            for statement in await self._load_sql_statements("create_users_for_new_schema.sql")
            if not statement.startswith("--") and statement != ""
        ])

    async def _load_sql_statements(self, file_name: str) -> list[str]:
        file_path: Path = Path(__file__).parent.parent / "sqls" / file_name
        async with aiofiles.open(file_path, "r") as file:
            file_content: str = await file.read()
            return file_content.split("\n")
