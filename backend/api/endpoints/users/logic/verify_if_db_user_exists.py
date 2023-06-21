import traceback

import psycopg2
from injector import inject

from api.endpoints.users.models.get_user_response import GetUserResponse
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class VerifyIfDbUserExists(ICommand[GetUserResponse]):
    @inject
    def __init__(self, db: IPostgresqlConnection):
        self._db = db

    async def handle(self, payload: DbUser, db: str) -> GetUserResponse:
        statement: str = "SELECT COUNT(*) FROM Address;"
        try:
            await self._db.load_single_by_sql(payload, db, statement)
            return GetUserResponse(exists=True)
        except Exception as e:
            if "permission denied for table address" in str(e):
                return GetUserResponse(exists=True)
            return GetUserResponse(exists=False)

