import traceback

from injector import inject

from api.endpoints.sql.models.delete_sql_result import DeleteSqlResult
from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class DeleteBySqlStatement(ICommand[DeleteSqlResult]):
    @inject
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, uuid: str) -> DeleteSqlResult:
        try:
            row_count: int = await self._db.delete_by_sql(DbUser(payload.username, payload.password), uuid, payload.sql_statement)
            return DeleteSqlResult(
                operation="delete",
                result={"affectedRows": row_count},
                errors=None
            )
        except Exception as e:
            return DeleteSqlResult(
                operation="delete",
                result={},
                errors=str(e)
            )
