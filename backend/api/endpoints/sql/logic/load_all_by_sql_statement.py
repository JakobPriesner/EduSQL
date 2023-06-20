import traceback

from api.endpoints.sql.models.select_all_sql_result import SelectAllSqlResult
from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from api.endpoints.sql.models.sql_execution_result import SqlExecutionResult
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LoadAllBySqlStatement(ICommand[SqlExecutionResult]):
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, user_uuid: str) -> SelectAllSqlResult:
        try:
            result: list[dict] = await self._db.load_all_by_sql(DbUser(payload.user_name, payload.password), user_uuid, payload.sql_statement)
            return SelectAllSqlResult(
                operation="selectAll",
                result=result,
                errors=None
            )
        except Exception as e:
            return SelectAllSqlResult(
                operation="selectAll",
                result={},
                errors=traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            )
