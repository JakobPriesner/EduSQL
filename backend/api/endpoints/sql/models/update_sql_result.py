from typing import Optional

from api.camel_model import CamelModel


class UpdateSqlResult(CamelModel):
    operation: str = "update"
    result: Optional[int]
    errors: str = ""
