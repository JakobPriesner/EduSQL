
from injector import inject
from starlette import status

from api.annotations import fastapi_controller
from api.annotations.base_url import base_url
from api.annotations.api_tags import api_tags
from api.annotations.http_methods.get import get
from api.annotations.http_methods.post import post

from api.endpoints.levels.logic.validation.validate_task import ValidateTask
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from mediator.mediator_interface import IMediator


@fastapi_controller
@base_url("levels")
@api_tags(["Level Validation"])
class UsersController:
    @inject
    def __init__(self, mediator: IMediator):
        self._mediator: IMediator = mediator

    @post("/{level_number}/tasks/{task_number}/validate", response_model=LevelValidationResult, status_code=status.HTTP_200_OK)
    async def validate_level_with_payload(self, level_number: int, task_number: int, payload: dict, uuid: str) -> LevelValidationResult:
        result = await self._mediator.execute_async(ValidateTask, level_number=level_number, task_number=task_number, db=uuid, payload=payload)
        return result

    @get("/{level_number}/tasks/{task_number}/validate", response_model=LevelValidationResult,
         status_code=status.HTTP_200_OK)
    async def validate_level_without_payload(self, level_number: int, task_number: int, uuid: str) -> LevelValidationResult:
        return await self._mediator.execute_async(ValidateTask, level_number=level_number, task_number=task_number,
                                                  db=uuid)
