import traceback

from injector import inject

from api.endpoints.sql.models.select_single_sql_result import SelectSingleSqlResult
from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from command_interface import ICommand
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LoadSingleBySqlStatement(ICommand[SelectSingleSqlResult]):
    @inject
    def __init__(self, db: IPostgresqlConnection):
        self._db: IPostgresqlConnection = db

    async def handle(self, payload: SqlExecutionPayload, uuid: str) -> SelectSingleSqlResult:
        try:
            result: dict = await self._db.load_single_by_sql(DbUser(payload.username, payload.password), uuid, payload.sql_statement)
            return SelectSingleSqlResult(
                operation="selectSingle",
                result=result,
                errors=None
            )
        except Exception as e:
            return SelectSingleSqlResult(
                operation="selectSingle",
                result_as_dict=None,
                errors=str(e)
            )
