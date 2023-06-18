import traceback

from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from api.endpoints.sql.models.sql_execution_result import SqlExecutionResult
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class DeleteBySqlStatement(ICommand[SqlExecutionResult]):
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, user_uuid: str) -> SqlExecutionResult:
        try:
            row_count: int = await self._db.delete_by_sql(DbUser(payload.user_name, payload.password), user_uuid, payload.sql_statement)
            return SqlExecutionResult(
                result_as_dict={"affectedRows": row_count},
                errors=None
            )
        except Exception as e:
            return SqlExecutionResult(
                result_as_dict={},
                errors=traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )
