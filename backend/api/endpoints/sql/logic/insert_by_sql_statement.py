import traceback

from injector import inject

from api.endpoints.sql.models.insert_sql_result import InsertSqlResult
from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class InsertBySqlStatement(ICommand[InsertSqlResult]):
    @inject
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, uuid: str) -> InsertSqlResult:
        try:
            _id: int = await self._db.create_by_sql(DbUser(payload.username, payload.password), uuid, payload.sql_statement)
            return InsertSqlResult(
                operation="insert",
                result=_id,
                errors=None
            )
        except Exception as e:
            return InsertSqlResult(
                operation="insert",
                result=None,
                errors=str(e)
            )
