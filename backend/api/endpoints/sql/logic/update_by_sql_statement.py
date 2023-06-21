import traceback

from injector import inject

from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from api.endpoints.sql.models.update_sql_result import UpdateSqlResult
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class UpdateBySqlStatement(ICommand[UpdateSqlResult]):
    @inject
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, uuid: str) -> UpdateSqlResult:
        try:
            row_count: int = await self._db.update_by_sql(DbUser(payload.username, payload.password), uuid, payload.sql_statement)
            return UpdateSqlResult(
                operation="update",
                result={"affectedRows": row_count},
                errors=""
            )
        except Exception as e:
            return UpdateSqlResult(
                operation="update",
                result=None,
                errors=str(e)
            )
