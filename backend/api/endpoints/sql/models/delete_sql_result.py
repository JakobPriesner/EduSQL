from typing import Optional

from api.camel_model import CamelModel


class DeleteSqlResult(CamelModel):
    operation: str = "delete"
    result: Optional[int]
    errors: str = ""
