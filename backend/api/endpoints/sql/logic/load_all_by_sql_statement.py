from injector import inject

from api.endpoints.sql.models.select_all_sql_result import SelectAllSqlResult
from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LoadAllBySqlStatement(ICommand[SelectAllSqlResult]):
    @inject
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, uuid: str) -> SelectAllSqlResult:
        try:
            result: list[dict] = await self._db.load_all_by_sql(DbUser(payload.username, payload.password), uuid, payload.sql_statement)
            return SelectAllSqlResult(
                operation="selectAll",
                result=result,
                errors=None
            )
        except Exception as e:
            return SelectAllSqlResult(
                operation="selectAll",
                result=[],
                errors=str(e)
            )
