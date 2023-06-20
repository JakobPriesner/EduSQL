import traceback

from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from api.endpoints.sql.models.sql_execution_result import SqlExecutionResult
from api.endpoints.sql.models.update_sql_result import UpdateSqlResult
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class UpdateBySqlStatement(ICommand[SqlExecutionResult]):
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, user_uuid: str) -> UpdateSqlResult:
        try:
            row_count: int = await self._db.update_by_sql(DbUser(payload.user_name, payload.password), user_uuid, payload.sql_statement)
            return UpdateSqlResult(
                operation="update",
                result={"affectedRows": row_count},
                errors=None
            )
        except Exception as e:
            return UpdateSqlResult(
                operation="update",
                result=None,
                errors=traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )
