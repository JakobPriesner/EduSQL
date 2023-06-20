import logging
from typing import Annotated

from fastapi import APIRouter, status, Header
from injector import inject
from api.annotations import fastapi_controller
from api.annotations.base_url import base_url
from api.annotations.api_tags import api_tags
from api.annotations.http_methods.post import post
from api.endpoints.sql.logic.delete_by_sql_statement import DeleteBySqlStatement
from api.endpoints.sql.logic.insert_by_sql_statement import InsertBySqlStatement
from api.endpoints.sql.logic.load_all_by_sql_statement import LoadAllBySqlStatement
from api.endpoints.sql.logic.load_single_by_sql_statement import LoadSingleBySqlStatement
from api.endpoints.sql.logic.update_by_sql_statement import UpdateBySqlStatement
from api.endpoints.sql.models.delete_sql_result import DeleteSqlResult
from api.endpoints.sql.models.insert_sql_result import InsertSqlResult
from api.endpoints.sql.models.select_all_sql_result import SelectAllSqlResult
from api.endpoints.sql.models.select_single_sql_result import SelectSingleSqlResult
from api.endpoints.sql.models.sql_execution_payload import SqlExecutionPayload
from api.endpoints.sql.models.sql_execution_result import SqlExecutionResult
from api.endpoints.sql.models.update_sql_result import UpdateSqlResult
from mediator.mediator_interface import IMediator

logger = logging.getLogger(__name__)


@fastapi_controller
@base_url("sqls")
@api_tags(["Sqls"])
class AlarmController:
    @inject
    def __init__(self, mediator: IMediator):
        self._mediator: IMediator = mediator

    @post("/load-all", response_model=SqlExecutionResult, status_code=status.HTTP_200_OK)
    async def load_all_by_sql_statement(self, payload: SqlExecutionPayload, user_uuid: Annotated[str | None, Header()] = None) -> SelectAllSqlResult:
        return await self._mediator.execute_async(LoadAllBySqlStatement, payload=payload, user_uuid=user_uuid)

    @post("/load-single", response_model=SqlExecutionResult, status_code=status.HTTP_200_OK)
    async def load_single_by_sql(self, payload: SqlExecutionPayload, user_uuid: Annotated[str | None, Header()] = None) -> SelectSingleSqlResult:
        return await self._mediator.execute_async(LoadSingleBySqlStatement, payload=payload, user_uuid=user_uuid)

    @post("/insert", response_model=SqlExecutionResult, status_code=status.HTTP_200_OK)
    async def insert_by_sql(self, payload: SqlExecutionPayload, user_uuid: Annotated[str | None, Header()] = None) -> InsertSqlResult:
        return await self._mediator.execute_async(InsertBySqlStatement, payload=payload, user_uuid=user_uuid)

    @post("/update", response_model=SqlExecutionResult, status_code=status.HTTP_200_OK)
    async def update_by_sql(self, payload: SqlExecutionPayload, user_uuid: Annotated[str | None, Header()] = None) -> UpdateSqlResult:
        return await self._mediator.execute_async(UpdateBySqlStatement, payload=payload, user_uuid=user_uuid)

    @post("/delete", response_model=SqlExecutionResult, status_code=status.HTTP_201_CREATED)
    async def delete_by_sql(self, payload: SqlExecutionPayload, user_uuid: Annotated[str | None, Header()] = None) -> DeleteSqlResult:
        return await self._mediator.execute_async(DeleteBySqlStatement, payload=payload, user_uuid=user_uuid)
